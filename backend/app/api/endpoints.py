from fastapi import APIRouter, Response, HTTPException
from app.schemas.schemas import (
    BusinessInputRequest,
    FullAnalysisResponse,
    FinancialStructuring,
    SchemeRecommendation,
    EMIBreakdown,
    WorkingCapitalPlan,
)
from app.engines.financial_engine import (
    calculate_financial_structure,
    route_scheme,
    calculate_emi,
    calculate_working_capital_plan,
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

@router.post("/financial/calculate", response_model=FinancialStructuring)
async def calculate_finance(request: BusinessInputRequest):
    """
    Deterministic financial structuring: Project Cost = Margin / 10%, Max Loan = 90%.
    """
    return calculate_financial_structure(request.available_capital)

@router.post("/scheme/recommend", response_model=SchemeRecommendation)
async def recommend_scheme(request: BusinessInputRequest):
    """
    Automatic scheme routing based on Project Cost threshold (₹1.40L).
    """
    fin = calculate_financial_structure(request.available_capital)
    return route_scheme(fin.project_cost, fin.max_loan_amount)

@router.post("/emi/calculate", response_model=EMIBreakdown)
async def calculate_loan_emi(request: BusinessInputRequest):
    """
    Computes exact post-moratorium monthly EMI and moratorium interest.
    """
    fin = calculate_financial_structure(request.available_capital)
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    emi, _ = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    return emi

@router.post("/repayment/calculate", response_model=list)
async def calculate_loan_repayment(request: BusinessInputRequest):
    """
    Computes full amortized month-by-month repayment schedule.
    """
    fin = calculate_financial_structure(request.available_capital)
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    _, schedule = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    return schedule

@router.post("/working-capital/calculate", response_model=WorkingCapitalPlan)
async def calculate_wc(request: BusinessInputRequest):
    """
    Generates operational cash flow and 3-month reserve requirements.
    """
    fin = calculate_financial_structure(request.available_capital)
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    emi, _ = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    return calculate_working_capital_plan(fin.project_cost, emi.monthly_emi)

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
