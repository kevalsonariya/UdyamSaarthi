from typing import Dict, Any
from app.schemas.schemas import BusinessInputRequest, FullAnalysisResponse
from app.engines.financial_engine import (
    calculate_financial_structure,
    route_scheme,
    calculate_emi,
    calculate_working_capital_plan,
    DISCLAIMER_TEXT,
)
from app.engines.business_analysis_engine import (
    analyze_business_profile,
    validate_business_inputs,
    BusinessAnalysisValidationError,
)


def perform_complete_analysis(request: BusinessInputRequest) -> FullAnalysisResponse:
    """
    Executes the deterministic financial structuring and dynamic business advisory pipeline.
    Validates location, business category, and available capital strictly.
    """
    validated = validate_business_inputs(
        location=request.location,
        business_category=request.business_category,
        available_capital=request.available_capital,
    )

    clean_loc = validated["location"]
    clean_cat = validated["business_category"]
    clean_cap = validated["available_capital"]

    # 1. Deterministic financial structuring
    fin = calculate_financial_structure(clean_cap)
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    emi, schedule = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    wc = calculate_working_capital_plan(fin.project_cost, emi.monthly_emi)

    # 2. Dynamic business analysis
    adv = analyze_business_profile(
        location=clean_loc,
        business_category=clean_cat,
        available_capital=clean_cap,
    )

    # 3. Assemble complete structured payload matching Phase B3 specifications
    data_payload = {
        "business": adv["business"],
        "market": adv["market"],
        "opportunities": adv["opportunities"],
        "swot": adv["swot"],
        "risks": adv["risks"],
        "competitors": adv["competitors"],
        "pricing": adv["pricing"],
        "recommendation": adv["recommendation"],
        "financial": fin,
        "scheme": sch,
        "emi": emi,
        "repayment": schedule,
        "working_capital": wc,
        "location": clean_loc,
        "business_category": clean_cat,
        "available_capital": clean_cap,
    }

    return FullAnalysisResponse(
        success=True,
        data=data_payload,
        metadata=adv["metadata"],
        business=adv["business"],
        location=clean_loc,
        business_category=clean_cat,
        available_capital=clean_cap,
        financial=fin,
        scheme=sch,
        emi=emi,
        repayment=schedule,
        working_capital=wc,
        market=adv["market"],
        opportunities=adv["opportunities"],
        swot=adv["swot"],
        risks=adv["risks"],
        competitors=adv["competitors"],
        pricing=adv["pricing"],
        recommendation=adv["recommendation"],
        disclaimer=DISCLAIMER_TEXT,
    )
