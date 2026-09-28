import pytest
from app.engines.financial_engine import (
    calculate_financial_structure,
    route_scheme,
    calculate_emi,
    calculate_working_capital_plan,
)

def test_boundary_10k_capital():
    """₹10,000 capital -> ₹1,00,000 project cost -> Micro Finance Scheme"""
    fin = calculate_financial_structure(10000.0)
    assert fin.project_cost == 100000.0
    assert fin.max_loan_amount == 90000.0
    
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    assert sch.scheme_name == "Micro Finance Scheme"
    assert sch.interest_rate_percent == 6.5
    assert sch.tenure_years == 3
    assert sch.moratorium_months == 3
    assert sch.eligible_funding == 90000.0

def test_boundary_14k_capital():
    """₹14,000 capital -> ₹1,40,000 project cost -> Micro Finance Scheme"""
    fin = calculate_financial_structure(14000.0)
    assert fin.project_cost == 140000.0
    assert fin.max_loan_amount == 126000.0
    
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    assert sch.scheme_name == "Micro Finance Scheme"
    assert sch.interest_rate_percent == 6.5
    assert sch.tenure_years == 3
    assert sch.moratorium_months == 3
    # Max agency funding is ₹1.25 Lakh
    assert sch.eligible_funding == 125000.0

def test_boundary_14001_capital():
    """₹14,001 capital -> ₹1,40,010 project cost -> Term Loan Scheme"""
    fin = calculate_financial_structure(14001.0)
    assert fin.project_cost == 140010.0
    assert fin.max_loan_amount == 126009.0
    
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    assert sch.scheme_name == "Term Loan Scheme"
    assert sch.interest_rate_percent == 8.0
    assert sch.tenure_years == 7
    assert sch.moratorium_months == 6

def test_default_demo_scenario_100k_capital():
    """Default demo scenario: ₹100,000 capital -> ₹10,00,000 project cost -> ₹9,00,000 loan -> Term Loan Scheme"""
    fin = calculate_financial_structure(100000.0)
    assert fin.project_cost == 1000000.0
    assert fin.max_loan_amount == 900000.0
    
    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    assert sch.scheme_name == "Term Loan Scheme"
    assert sch.interest_rate_percent == 8.0
    assert sch.tenure_years == 7
    assert sch.moratorium_months == 6
    assert sch.eligible_funding == 900000.0

    emi, schedule = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    assert emi.principal_amount == 900000.0
    assert emi.tenure_months == 84
    assert emi.moratorium_months == 6
    assert emi.post_moratorium_tenure_months == 78
    assert emi.monthly_emi > 0
    assert len(schedule) == 84
    assert schedule[0].is_moratorium is True
    assert schedule[5].is_moratorium is True
    assert schedule[6].is_moratorium is False

def test_working_capital_calculation():
    wc = calculate_working_capital_plan(1000000.0, 14000.0)
    assert wc.monthly_raw_materials == 45000.0
    assert wc.monthly_labor_wages == 25000.0
    assert wc.total_monthly_operating_expense > 0
    assert wc.recommended_3_months_reserve == wc.total_monthly_operating_expense * 3.0
