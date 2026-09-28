import math
import pytest
from app.engines.financial_engine import (
    calculate_project_cost,
    calculate_maximum_loan,
    select_scheme,
    validate_loan_amount,
    calculate_emi,
    generate_repayment_schedule,
    calculate_working_capital,
    calculate_financial_structure,
    route_scheme,
    calculate_working_capital_plan,
    FinancialValidationError,
    MAX_PROJECT_COST,
    MICRO_FINANCE_THRESHOLD,
    MICRO_FINANCE_MAX_FUNDING,
    TERM_LOAN_MAX_FUNDING,
)


# ==============================================================================
# 1. REQUIRED TEST INPUTS & BOUNDARY TESTS (Section 5 & 12)
# ==============================================================================

def test_required_input_10k_margin():
    """
    Input: Available Margin = ₹10,000
    Project Cost = 10,000 / 0.10 = ₹1,00,000
    Maximum Loan = 90% of 1,00,000 = ₹90,000
    Scheme: Micro Finance Scheme (<= ₹1.40 Lakh)
    """
    cost = calculate_project_cost(10000.0)
    assert cost == 100000.0

    max_loan = calculate_maximum_loan(cost)
    assert max_loan == 90000.0

    sch = select_scheme(cost)
    assert sch.scheme_name == "Micro Finance Scheme"
    assert sch.interest_rate_percent == 6.5
    assert sch.tenure_years == 3
    assert sch.moratorium_months == 3
    assert sch.eligible_funding == 90000.0

    emi = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    assert emi.monthly_emi == 2985.64
    assert float(emi) == 2985.64


def test_boundary_13999_margin():
    """
    Boundary Below: Available Margin = ₹13,999
    Project Cost = ₹1,39,990 (< ₹1.40 Lakh)
    Must route to: Micro Finance Scheme
    """
    cost = calculate_project_cost(13999.0)
    assert cost == 139990.0

    max_loan = calculate_maximum_loan(cost)
    assert max_loan == 125991.0

    sch = select_scheme(cost)
    assert sch.scheme_name == "Micro Finance Scheme"
    assert sch.interest_rate_percent == 6.5
    assert sch.tenure_years == 3
    assert sch.moratorium_months == 3
    # Max agency funding is ₹1.25 Lakh, so ₹1,25,991 is capped at ₹1,25,000
    assert sch.eligible_funding == 125000.0


def test_boundary_14000_margin():
    """
    Exact Boundary: Available Margin = ₹14,000
    Project Cost = 14,000 / 0.10 = ₹1,40,000 (<= ₹1.40 Lakh)
    Must route to: Micro Finance Scheme
    Agency Funding capped at ₹1.25 Lakh
    """
    cost = calculate_project_cost(14000.0)
    assert cost == 140000.0

    max_loan = calculate_maximum_loan(cost)
    assert max_loan == 126000.0

    sch = select_scheme(cost)
    assert sch.scheme_name == "Micro Finance Scheme"
    assert sch.interest_rate_percent == 6.5
    assert sch.tenure_years == 3
    assert sch.moratorium_months == 3
    assert sch.eligible_funding == 125000.0

    emi = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    assert emi.monthly_emi == 4146.72


def test_boundary_14001_margin():
    """
    Boundary Above: Available Margin = ₹14,001
    Project Cost = 14,001 / 0.10 = ₹1,40,010 (> ₹1.40 Lakh)
    Must route to: Term Loan Scheme
    """
    cost = calculate_project_cost(14001.0)
    assert cost == 140010.0

    max_loan = calculate_maximum_loan(cost)
    assert max_loan == 126009.0

    sch = select_scheme(cost)
    assert sch.scheme_name == "Term Loan Scheme"
    assert sch.interest_rate_percent == 8.0
    assert sch.tenure_years == 7
    assert sch.moratorium_months == 6
    assert sch.eligible_funding == 126009.0

    emi = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    assert emi.monthly_emi == 2077.03


def test_required_input_100k_margin():
    """
    Input: Available Margin = ₹1,00,000
    Project Cost = 100,000 / 0.10 = ₹10,00,000
    Maximum Loan = 90% of 10,00,000 = ₹9,00,000
    Scheme: Term Loan Scheme (> ₹1.40 Lakh and <= ₹50 Lakh)
    """
    cost = calculate_project_cost(100000.0)
    assert cost == 1000000.0

    max_loan = calculate_maximum_loan(cost)
    assert max_loan == 900000.0

    sch = select_scheme(cost)
    assert sch.scheme_name == "Term Loan Scheme"
    assert sch.interest_rate_percent == 8.0
    assert sch.tenure_years == 7
    assert sch.moratorium_months == 6
    assert sch.eligible_funding == 900000.0

    emi = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    assert emi.monthly_emi == 14834.86


def test_upper_boundary_50_lakh_ceiling():
    """
    Upper boundary: Project cost exactly ₹50 Lakh (Margin ₹5,00,000).
    Max loan: ₹45 Lakh (Term Loan Scheme ceiling).
    """
    cost = calculate_project_cost(500000.0)
    assert cost == 5000000.0

    max_loan = calculate_maximum_loan(cost)
    assert max_loan == 4500000.0

    sch = select_scheme(cost)
    assert sch.scheme_name == "Term Loan Scheme"
    assert sch.eligible_funding == 4500000.0


# ==============================================================================
# 2. INVALID INPUT VALIDATION TESTS (Section 4 & 12)
# ==============================================================================

def test_zero_margin_rejected():
    """Zero margin must raise FinancialValidationError."""
    with pytest.raises(FinancialValidationError) as exc_info:
        calculate_project_cost(0)
    assert exc_info.value.code == "ZERO_VALUE"
    assert "greater than zero" in str(exc_info.value)


def test_negative_margin_rejected():
    """Negative margin must raise FinancialValidationError."""
    with pytest.raises(FinancialValidationError) as exc_info:
        calculate_project_cost(-5000)
    assert exc_info.value.code == "VALUE_TOO_LOW"
    assert "cannot be less than" in str(exc_info.value)


def test_none_margin_rejected():
    """None margin must raise FinancialValidationError."""
    with pytest.raises(FinancialValidationError) as exc_info:
        calculate_project_cost(None)
    assert exc_info.value.code == "MISSING_VALUE"


def test_non_numeric_margin_rejected():
    """Non-numeric string / boolean margin must raise FinancialValidationError."""
    with pytest.raises(FinancialValidationError) as exc_info:
        calculate_project_cost("invalid_text")
    assert exc_info.value.code == "NON_NUMERIC"

    with pytest.raises(FinancialValidationError) as exc_info_bool:
        calculate_project_cost(True)
    assert exc_info_bool.value.code == "NON_NUMERIC"


def test_extremely_large_margin_exceeding_ceiling():
    """Margin resulting in project cost > ₹50 Lakh must raise FinancialValidationError."""
    with pytest.raises(FinancialValidationError) as exc_info:
        calculate_project_cost(500001.0)
    assert exc_info.value.code == "EXCEEDS_MAX_PROJECT_COST"

    with pytest.raises(FinancialValidationError) as exc_info_huge:
        calculate_project_cost(10_000_000.0)
    assert exc_info_huge.value.code == "EXCEEDS_MAX_PROJECT_COST"


def test_nan_and_inf_rejected():
    """NaN and Infinite values must raise FinancialValidationError."""
    with pytest.raises(FinancialValidationError) as exc_nan:
        calculate_project_cost(float("nan"))
    assert exc_nan.value.code == "NON_FINITE"

    with pytest.raises(FinancialValidationError) as exc_inf:
        calculate_project_cost(float("inf"))
    assert exc_inf.value.code == "NON_FINITE"


def test_invalid_project_costs_for_loan_and_scheme():
    """Test validation on calculate_maximum_loan and select_scheme."""
    with pytest.raises(FinancialValidationError):
        calculate_maximum_loan(0)

    with pytest.raises(FinancialValidationError):
        calculate_maximum_loan(-1000)

    with pytest.raises(FinancialValidationError):
        calculate_maximum_loan(6000000.0)

    with pytest.raises(FinancialValidationError):
        select_scheme(0)

    with pytest.raises(FinancialValidationError):
        select_scheme(-500)

    with pytest.raises(FinancialValidationError):
        select_scheme(5000001.0)


def test_loan_exceeding_applicable_maximum_agency_funding():
    """
    Test validation when loan amount exceeds applicable scheme limits:
    Micro Finance Scheme ceiling: ₹1.25 Lakh
    Term Loan Scheme ceiling: ₹45 Lakh
    """
    micro_sch = select_scheme(100000.0)
    term_sch = select_scheme(2000000.0)

    # Valid within ceiling
    assert validate_loan_amount(125000.0, micro_sch) is True
    assert validate_loan_amount(4500000.0, term_sch) is True

    # Exceeding Micro Finance ceiling
    with pytest.raises(FinancialValidationError) as exc_micro:
        validate_loan_amount(125001.0, micro_sch)
    assert exc_micro.value.code == "LOAN_EXCEEDS_AGENCY_LIMIT"
    assert "125,000.00" in str(exc_micro.value)

    # Exceeding Term Loan ceiling
    with pytest.raises(FinancialValidationError) as exc_term:
        validate_loan_amount(4500001.0, term_sch)
    assert exc_term.value.code == "LOAN_EXCEEDS_AGENCY_LIMIT"
    assert "4,500,000.00" in str(exc_term.value)


# ==============================================================================
# 3. EMI CALCULATION TESTS (Section 6)
# ==============================================================================

def test_calculate_emi_standard_formula():
    """
    Verify standard EMI formula:
    EMI = P × r × (1+r)^n / ((1+r)^n - 1)
    """
    p = 90000.0
    annual_rate = 6.5
    r = (annual_rate / 100.0) / 12.0
    n = 33  # 36 months - 3 months moratorium

    factor = (1.0 + r) ** n
    expected_emi = (p * r * factor) / (factor - 1.0)

    emi = calculate_emi(
        principal=p,
        annual_interest_rate_percent=annual_rate,
        tenure_years=3,
        moratorium_months=3,
    )
    assert abs(float(emi) - round(expected_emi, 2)) < 0.01
    assert emi.post_moratorium_tenure_months == 33
    assert emi.moratorium_months == 3


def test_calculate_emi_zero_interest():
    """
    Verify zero-interest handling:
    EMI = P / n
    """
    p = 60000.0
    emi = calculate_emi(
        principal=p,
        annual_interest_rate_percent=0.0,
        tenure_years=5,
        moratorium_months=0,
    )
    assert float(emi) == 1000.0
    assert emi.monthly_emi == 1000.0
    assert emi.moratorium_monthly_interest == 0.0
    assert emi.total_interest_payable == 0.0


def test_calculate_emi_invalid_parameters():
    """Verify validation when computing EMI with invalid inputs."""
    with pytest.raises(FinancialValidationError):
        calculate_emi(principal=0, annual_interest_rate_percent=6.5, tenure_years=3)

    with pytest.raises(FinancialValidationError):
        calculate_emi(principal=-10000, annual_interest_rate_percent=6.5, tenure_years=3)

    with pytest.raises(FinancialValidationError):
        calculate_emi(principal=90000, annual_interest_rate_percent=None, tenure_years=3)

    with pytest.raises(FinancialValidationError):
        calculate_emi(principal=90000, annual_interest_rate_percent=6.5, tenure_years=None)

    # Moratorium >= total tenure
    with pytest.raises(FinancialValidationError) as exc_morat:
        calculate_emi(principal=90000, annual_interest_rate_percent=6.5, tenure_years=3, moratorium_months=36)
    assert exc_morat.value.code == "INVALID_MORATORIUM"


# ==============================================================================
# 4. REPAYMENT SCHEDULE TESTS (Section 7)
# ==============================================================================

def test_generate_repayment_schedule_structure_and_closure():
    """
    Verify that repayment schedule:
    1. Respects moratorium (is_moratorium=True, principal=0.0)
    2. Clears closing balance to exactly 0.0 without accumulating floating point errors
    3. Total principal repaid exactly equals principal
    4. Populates month, opening_balance, emi, principal, interest, closing_balance
    """
    principal = 90000.0
    schedule = generate_repayment_schedule(
        principal=principal,
        annual_interest_rate_percent=6.5,
        tenure_years=3,
        moratorium_months=3,
    )

    assert len(schedule) == 36

    # Moratorium period verification
    for m in range(3):
        item = schedule[m]
        assert item.month == m + 1
        assert item.is_moratorium is True
        assert item.principal == 0.0
        assert item.principal_component == 0.0
        assert item.interest > 0.0
        assert item.closing_balance == principal

    # Post-moratorium verification
    for m in range(3, 36):
        item = schedule[m]
        assert item.month == m + 1
        assert item.is_moratorium is False
        assert item.principal > 0.0
        assert item.installment_amount > 0.0

    # Final month exact clean closure
    last_item = schedule[-1]
    assert last_item.month == 36
    assert last_item.closing_balance == 0.0

    # Total principal repaid equals principal
    total_principal_repaid = sum(item.principal_component for item in schedule)
    assert round(total_principal_repaid, 2) == principal


# ==============================================================================
# 5. WORKING CAPITAL CALCULATION TESTS (Section 8)
# ==============================================================================

def test_calculate_working_capital_valid():
    """
    Verify working capital calculations:
    Raw materials: 4.5%
    Labor: 2.5%
    Rent/Utilities: 1.2%
    Logistics: 0.8%
    Contingency: 0.5%
    Total OpEx: 9.5%
    3-Month Reserve: Total OpEx × 3
    """
    project_cost = 1000000.0
    monthly_emi = 14834.86

    wc = calculate_working_capital(project_cost=project_cost, monthly_emi=monthly_emi)

    assert wc.monthly_raw_materials == 45000.0
    assert wc.monthly_labor_wages == 25000.0
    assert wc.monthly_rent_utilities == 12000.0
    assert wc.monthly_logistics_packaging == 8000.0
    assert wc.monthly_contingency_buffer == 5000.0
    assert wc.total_monthly_operating_expense == 95000.0
    assert wc.recommended_3_months_reserve == 285000.0
    assert wc.break_even_monthly_revenue == round(95000.0 + monthly_emi, 2)
    assert wc.break_even_occupancy_or_capacity_percent == 74.0


def test_calculate_working_capital_invalid():
    """Verify validation on working capital calculation."""
    with pytest.raises(FinancialValidationError):
        calculate_working_capital(project_cost=0)

    with pytest.raises(FinancialValidationError):
        calculate_working_capital(project_cost=-500)

    with pytest.raises(FinancialValidationError):
        calculate_working_capital(project_cost=6000000.0)

    with pytest.raises(FinancialValidationError):
        calculate_working_capital(project_cost=100000.0, monthly_emi=-100)


# ==============================================================================
# 6. BACKWARD COMPATIBILITY TESTS
# ==============================================================================

def test_backward_compatibility_wrappers():
    """Verify that legacy function calls and unpacking still work seamlessly."""
    fin = calculate_financial_structure(100000.0)
    assert fin.project_cost == 1000000.0
    assert fin.max_loan_amount == 900000.0

    sch = route_scheme(fin.project_cost, fin.max_loan_amount)
    assert sch.scheme_name == "Term Loan Scheme"

    emi, schedule = calculate_emi(
        principal=sch.eligible_funding,
        annual_interest_rate_percent=sch.interest_rate_percent,
        tenure_years=sch.tenure_years,
        moratorium_months=sch.moratorium_months,
    )
    assert emi.principal_amount == 900000.0
    assert len(schedule) == 84

    wc = calculate_working_capital_plan(fin.project_cost, emi.monthly_emi)
    assert wc.total_monthly_operating_expense == 95000.0
