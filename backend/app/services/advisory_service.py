from typing import Dict, Any
from app.schemas.schemas import BusinessInputRequest, FullAnalysisResponse
from app.engines.financial_engine import (
    calculate_financial_structure,
    route_scheme,
    calculate_emi,
    calculate_working_capital_plan,
    DISCLAIMER_TEXT,
)
from app.engines.advisory_engine import generate_advisory_profile

def perform_complete_analysis(request: BusinessInputRequest) -> FullAnalysisResponse:
    """
    Executes the deterministic financial structuring and advisory pipeline.
    """
    fin = calculate_financial_structure(request.available_capital)
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    emi, schedule = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    wc = calculate_working_capital_plan(fin.project_cost, emi.monthly_emi)
    adv = generate_advisory_profile(
        location=request.location,
        business_category=request.business_category,
        project_cost=fin.project_cost,
    )

    return FullAnalysisResponse(
        location=request.location,
        business_category=request.business_category,
        available_capital=request.available_capital,
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
