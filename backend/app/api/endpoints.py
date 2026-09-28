from typing import Any, Dict
from fastapi import APIRouter, Response, HTTPException
from app.schemas.schemas import (
    BusinessInputRequest,
    FullAnalysisResponse,
    FinancialCalculateRequest,
    SchemeRecommendRequest,
    EMICalculateRequest,
    RepaymentCalculateRequest,
    WorkingCapitalCalculateRequest,
)
from app.engines.financial_engine import (
    calculate_project_cost,
    calculate_maximum_loan,
    select_scheme,
    calculate_emi,
    generate_repayment_schedule,
    aggregate_quarterly_repayment,
    calculate_working_capital,
    FinancialValidationError,
    DISCLAIMER_TEXT,
)
from app.services.advisory_service import perform_complete_analysis
from app.utils.pdf_generator import generate_pdf_report

router = APIRouter()


@router.post("/business/analyze", response_model=FullAnalysisResponse)
async def analyze_business(request: BusinessInputRequest):
    """
    Complete end-to-end hyper-local business advisory and financial structuring.
    """
    return perform_complete_analysis(request)


@router.post("/financial/calculate")
async def calculate_finance(request: FinancialCalculateRequest):
    """
    Phase B2: Deterministic financial structuring endpoint.
    Project Cost = Available Margin / 10%
    Maximum Loan = 90% of Project Cost
    """
    margin = request.available_margin if request.available_margin is not None else request.available_capital
    if margin is None:
        raise FinancialValidationError(
            "Missing parameter: 'available_margin' or 'available_capital' must be provided.",
            field="available_margin",
            code="MISSING_PARAMETER",
        )

    project_cost = calculate_project_cost(margin)
    max_loan = calculate_maximum_loan(project_cost)
    scheme = select_scheme(project_cost)

    return {
        "success": True,
        "data": {
            "project_cost": project_cost,
            "maximum_loan": max_loan,
            "scheme": scheme.scheme_name,
            "scheme_name": scheme.scheme_name,
            "scheme_code": scheme.scheme_code,
            "interest_rate": scheme.interest_rate_percent,
            "tenure_years": scheme.tenure_years,
            "tenure_months": scheme.tenure_months,
            "moratorium_months": scheme.moratorium_months,
            "available_margin": margin,
            "promoter_contribution": margin,
            "margin_percentage": 10.0,
            "maximum_agency_funding": scheme.max_agency_funding,
            "eligible_funding": scheme.eligible_funding,
            "subsidy_estimate": round(project_cost * 0.15, 2),
            "disclaimer": DISCLAIMER_TEXT,
        },
    }


@router.post("/scheme/recommend")
async def recommend_scheme(request: SchemeRecommendRequest):
    """
    Phase B2: Deterministic scheme routing based on Project Cost threshold (₹1.40L).
    Micro Finance Scheme: Project Cost <= ₹1.40 Lakh
    Term Loan Scheme: Project Cost > ₹1.40 Lakh and <= ₹50 Lakh
    """
    if request.project_cost is not None:
        project_cost = request.project_cost
    else:
        margin = request.available_margin if request.available_margin is not None else request.available_capital
        if margin is None:
            raise FinancialValidationError(
                "Either 'project_cost' or 'available_margin' must be provided.",
                field="project_cost",
                code="MISSING_PARAMETER",
            )
        project_cost = calculate_project_cost(margin)

    scheme = select_scheme(project_cost, loan_amount=request.requested_loan_amount)

    return {
        "success": True,
        "data": {
            "project_cost": project_cost,
            "scheme": scheme.scheme_name,
            "scheme_name": scheme.scheme_name,
            "scheme_code": scheme.scheme_code,
            "interest_rate": scheme.interest_rate_percent,
            "interest_rate_percent": scheme.interest_rate_percent,
            "tenure_years": scheme.tenure_years,
            "tenure_months": scheme.tenure_months,
            "moratorium_months": scheme.moratorium_months,
            "maximum_agency_funding": scheme.max_agency_funding,
            "eligible_funding": scheme.eligible_funding,
            "governing_body": scheme.governing_body,
            "eligibility_criteria": scheme.eligibility_criteria,
            "key_benefits": scheme.key_benefits,
            "notes": scheme.notes,
        },
    }


@router.post("/emi/calculate")
async def calculate_loan_emi(request: EMICalculateRequest):
    """
    Phase B2: Deterministic EMI calculation using standard banking formula.
    """
    if request.principal is not None:
        principal = request.principal
        rate = request.annual_interest_rate if request.annual_interest_rate is not None else request.annual_interest_rate_percent
        if rate is None:
            raise FinancialValidationError(
                "Missing required parameter: 'annual_interest_rate' must be provided.",
                field="annual_interest_rate",
                code="MISSING_PARAMETER",
            )
        tenure = request.tenure_years
        if tenure is None:
            raise FinancialValidationError(
                "Missing required parameter: 'tenure_years' must be provided.",
                field="tenure_years",
                code="MISSING_PARAMETER",
            )
        moratorium = request.moratorium_months or 0
    else:
        margin = request.available_margin if request.available_margin is not None else request.available_capital
        if margin is None:
            raise FinancialValidationError(
                "Either 'principal' with interest parameters or 'available_margin' must be provided.",
                field="principal",
                code="MISSING_PARAMETER",
            )
        project_cost = calculate_project_cost(margin)
        scheme = select_scheme(project_cost)
        principal = scheme.eligible_funding
        rate = scheme.interest_rate_percent
        tenure = scheme.tenure_years
        moratorium = scheme.moratorium_months

    emi = calculate_emi(
        principal=principal,
        annual_interest_rate_percent=rate,
        tenure_years=tenure,
        moratorium_months=moratorium,
    )

    return {
        "success": True,
        "data": {
            "principal": emi.principal_amount,
            "annual_interest_rate": emi.annual_interest_rate_percent,
            "tenure_years": tenure,
            "tenure_months": emi.tenure_months,
            "moratorium_months": emi.moratorium_months,
            "post_moratorium_tenure_months": emi.post_moratorium_tenure_months,
            "monthly_emi": emi.monthly_emi,
            "moratorium_monthly_interest": emi.moratorium_monthly_interest,
            "total_interest_payable": emi.total_interest_payable,
            "total_repayment_amount": emi.total_repayment_amount,
        },
    }


@router.post("/repayment/calculate")
async def calculate_repayment(request: RepaymentCalculateRequest):
    """
    Phase B2: Month-by-month repayment schedule generation respecting scheme moratorium.
    """
    if request.principal is not None:
        principal = request.principal
        rate = request.annual_interest_rate if request.annual_interest_rate is not None else request.annual_interest_rate_percent
        if rate is None:
            raise FinancialValidationError(
                "Missing required parameter: 'annual_interest_rate' must be provided.",
                field="annual_interest_rate",
                code="MISSING_PARAMETER",
            )
        tenure = request.tenure_years
        if tenure is None:
            raise FinancialValidationError(
                "Missing required parameter: 'tenure_years' must be provided.",
                field="tenure_years",
                code="MISSING_PARAMETER",
            )
        moratorium = request.moratorium_months or 0
    else:
        margin = request.available_margin if request.available_margin is not None else request.available_capital
        if margin is None:
            raise FinancialValidationError(
                "Either 'principal' with interest parameters or 'available_margin' must be provided.",
                field="principal",
                code="MISSING_PARAMETER",
            )
        project_cost = calculate_project_cost(margin)
        scheme = select_scheme(project_cost)
        principal = scheme.eligible_funding
        rate = scheme.interest_rate_percent
        tenure = scheme.tenure_years
        moratorium = scheme.moratorium_months

    schedule = generate_repayment_schedule(
        principal=principal,
        annual_interest_rate_percent=rate,
        tenure_years=tenure,
        moratorium_months=moratorium,
    )
    quarterly_schedule = aggregate_quarterly_repayment(schedule)

    return {
        "success": True,
        "data": {
            "principal": principal,
            "annual_interest_rate": rate,
            "tenure_years": tenure,
            "tenure_months": tenure * 12,
            "moratorium_months": moratorium,
            "repayment_frequency": "Monthly (Quarterly roll-up available)",
            "total_installments": len(schedule),
            "total_quarters": len(quarterly_schedule),
            "schedule": [item.model_dump() for item in schedule],
            "quarterly_schedule": [item.model_dump() for item in quarterly_schedule],
            "financial_disclaimer": DISCLAIMER_TEXT,
            "indicative_notice": "Indicative repayment calculation. Verify applicable scheme terms before making financial decisions.",
        },
    }


@router.post("/working-capital/calculate")
async def calculate_wc(request: WorkingCapitalCalculateRequest):
    """
    Phase B2: Deterministic operational cash flow and 3-month reserve requirements.
    """
    if request.project_cost is not None:
        cost = request.project_cost
        emi_val = request.monthly_emi if request.monthly_emi is not None else 0.0
    else:
        margin = request.available_margin if request.available_margin is not None else request.available_capital
        if margin is None:
            raise FinancialValidationError(
                "Either 'project_cost' or 'available_margin' must be provided.",
                field="project_cost",
                code="MISSING_PARAMETER",
            )
        cost = calculate_project_cost(margin)
        scheme = select_scheme(cost)
        emi_res = calculate_emi(
            principal=scheme.eligible_funding,
            annual_interest_rate_percent=scheme.interest_rate_percent,
            tenure_years=scheme.tenure_years,
            moratorium_months=scheme.moratorium_months,
        )
        emi_val = emi_res.monthly_emi

    wc = calculate_working_capital(project_cost=cost, monthly_emi=emi_val)

    return {
        "success": True,
        "data": wc.model_dump(),
    }


@router.post("/report/generate")
async def generate_report_pdf(request: BusinessInputRequest):
    """
    Renders and streams downloadable ReportLab PDF dossier.
    """
    try:
        full_data = perform_complete_analysis(request)
        pdf_bytes = generate_pdf_report(full_data.dict())
        filename = f"BizSahayak_Plan_{request.business_category.replace(' ', '_')}_{int(request.available_capital)}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")


@router.post("/ai/explain")
async def generate_ai_advisory(request: BusinessInputRequest):
    """
    Phase B4: AI Advisory / Explanation Layer.
    Enhances already-calculated business profile and deterministic financial values.
    AI NEVER recalculates or overrides financial numbers.
    """
    try:
        from app.services.ai_advisory_service import ai_advisory_service
        full_analysis = perform_complete_analysis(request)
        ai_data = full_analysis.ai_explanation or ai_advisory_service.generate_advisory_explanation(full_analysis.model_dump())
        return {
            "success": True,
            "data": ai_data.model_dump() if hasattr(ai_data, "model_dump") else ai_data,
            "financial_invariants": {
                "project_cost": full_analysis.financial.project_cost,
                "eligible_funding": full_analysis.scheme.eligible_funding,
                "scheme_name": full_analysis.scheme.scheme_name,
                "monthly_emi": full_analysis.emi.monthly_emi,
            },
            "disclaimer": "AI-Assisted Business Insight & Planning Guidance. Indicative only.",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI advisory generation error: {str(e)}")

