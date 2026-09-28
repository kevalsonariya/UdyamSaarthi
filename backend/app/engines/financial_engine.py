"""
Phase B2 — Deterministic Financial Engine
Pure Python financial engine module.
Completely independent of FastAPI and AI/LLM runtime calculations.
"""

import math
from typing import Any, List, Optional, Tuple
from app.schemas.schemas import (
    FinancialStructuring,
    SchemeRecommendation,
    EMIBreakdown,
    RepaymentScheduleItem,
    QuarterlyRepaymentItem,
    WorkingCapitalPlan,
)

DISCLAIMER_TEXT = (
    "Indicative calculation for planning purposes. "
    "Verify applicable scheme terms before making financial decisions."
)

MAX_PROJECT_COST = 5_000_000.0  # ₹50 Lakh MSME ceiling
MICRO_FINANCE_THRESHOLD = 140_000.0  # ₹1.40 Lakh boundary
MICRO_FINANCE_MAX_FUNDING = 125_000.0  # ₹1.25 Lakh
TERM_LOAN_MAX_FUNDING = 4_500_000.0  # ₹45 Lakh
DEFAULT_MARGIN_PERCENT = 10.0
DEFAULT_LOAN_PERCENT = 90.0


class FinancialEngineError(Exception):
    """Base exception for financial engine."""
    pass


class FinancialValidationError(FinancialEngineError):
    """Structured validation error for financial calculations."""
    def __init__(self, message: str, field: Optional[str] = None, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code


class EMIResult(float):
    """
    Subclass of float representing monthly EMI amount.
    Supports unpacking as (breakdown, schedule) for backward compatibility
    and attribute access to financial breakdown details.
    """
    def __new__(
        cls,
        value: float,
        breakdown: Optional[EMIBreakdown] = None,
        schedule: Optional[List[RepaymentScheduleItem]] = None,
    ):
        obj = super().__new__(cls, value)
        obj.monthly_emi = float(value)
        obj.breakdown = breakdown
        obj.schedule = schedule or []
        if breakdown:
            obj.principal_amount = breakdown.principal_amount
            obj.annual_interest_rate_percent = breakdown.annual_interest_rate_percent
            obj.tenure_months = breakdown.tenure_months
            obj.moratorium_months = breakdown.moratorium_months
            obj.post_moratorium_tenure_months = breakdown.post_moratorium_tenure_months
            obj.moratorium_monthly_interest = breakdown.moratorium_monthly_interest
            obj.total_interest_payable = breakdown.total_interest_payable
            obj.total_repayment_amount = breakdown.total_repayment_amount
        return obj

    def __iter__(self):
        # Enables: emi, schedule = calculate_emi(...)
        target = self.breakdown if self.breakdown is not None else self
        return iter((target, self.schedule))


def validate_numeric(
    value: Any,
    field_name: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    allow_zero: bool = False,
) -> float:
    """
    Strictly validates numeric inputs:
    Rejects None, booleans, non-numeric types, NaN, Inf, zero/negative (if not allowed), and out-of-range values.
    """
    if value is None:
        raise FinancialValidationError(
            f"Missing required parameter: '{field_name}' cannot be None.",
            field=field_name,
            code="MISSING_VALUE",
        )

    # Boolean is a subclass of int in Python, so check explicitly
    if isinstance(value, bool):
        raise FinancialValidationError(
            f"Invalid non-numeric value for '{field_name}': boolean value {value} is not permitted.",
            field=field_name,
            code="NON_NUMERIC",
        )

    if not isinstance(value, (int, float, str)):
        raise FinancialValidationError(
            f"Invalid non-numeric value for '{field_name}': type {type(value).__name__} is not supported.",
            field=field_name,
            code="NON_NUMERIC",
        )

    try:
        num = float(value)
    except (ValueError, TypeError):
        raise FinancialValidationError(
            f"Invalid non-numeric value for '{field_name}': '{value}'.",
            field=field_name,
            code="NON_NUMERIC",
        )

    if math.isnan(num) or math.isinf(num):
        raise FinancialValidationError(
            f"Value for '{field_name}' must be a finite real number.",
            field=field_name,
            code="NON_FINITE",
        )

    if not allow_zero and num == 0.0:
        raise FinancialValidationError(
            f"Value for '{field_name}' must be greater than zero.",
            field=field_name,
            code="ZERO_VALUE",
        )

    if min_value is not None and num < min_value:
        raise FinancialValidationError(
            f"Value for '{field_name}' cannot be less than {min_value}, got {num}.",
            field=field_name,
            code="VALUE_TOO_LOW",
        )

    if max_value is not None and num > max_value:
        raise FinancialValidationError(
            f"Value for '{field_name}' cannot exceed {max_value:,.2f}, got {num:,.2f}.",
            field=field_name,
            code="VALUE_TOO_HIGH",
        )

    return num


def calculate_project_cost(
    available_margin: float,
    margin_percentage: float = DEFAULT_MARGIN_PERCENT,
) -> float:
    """
    Deterministic calculation:
    Project Cost = Available Margin / 10%
    Equivalent: Project Cost = Available Margin / 0.10

    Validates inputs and enforces scheme maximum project cost ceiling (₹50 Lakh).
    """
    margin = validate_numeric(available_margin, "available_margin", min_value=0.01)
    pct = validate_numeric(margin_percentage, "margin_percentage", min_value=0.01, max_value=100.0)

    project_cost = margin / (pct / 100.0)

    if project_cost > MAX_PROJECT_COST:
        raise FinancialValidationError(
            f"Available margin ₹{margin:,.2f} produces project cost ₹{project_cost:,.2f} "
            f"which exceeds the maximum scheme ceiling of ₹{MAX_PROJECT_COST:,.2f} (₹50 Lakh).",
            field="available_margin",
            code="EXCEEDS_MAX_PROJECT_COST",
        )

    return project_cost


def calculate_maximum_loan(
    project_cost: float,
    loan_percentage: float = DEFAULT_LOAN_PERCENT,
) -> float:
    """
    Deterministic calculation:
    Maximum Loan = 90% of Project Cost
    Equivalent: Maximum Loan = Project Cost × 0.90
    """
    cost = validate_numeric(
        project_cost,
        "project_cost",
        min_value=0.01,
        max_value=MAX_PROJECT_COST,
    )
    pct = validate_numeric(loan_percentage, "loan_percentage", min_value=0.01, max_value=100.0)

    return cost * (pct / 100.0)


def select_scheme(
    project_cost: float,
    loan_amount: Optional[float] = None,
) -> SchemeRecommendation:
    """
    Deterministic Scheme Selection:

    Micro Finance Scheme:
      Condition: Project Cost <= ₹1.40 lakh
      Interest Rate: 6.5%
      Tenure: 3 years
      Moratorium: 3 months
      Maximum Agency Funding: ₹1.25 lakh

    Term Loan Scheme:
      Condition: Project Cost > ₹1.40 lakh AND Project Cost <= ₹50 lakh
      Interest Rate: 8%
      Tenure: 7 years
      Moratorium: 6 months
      Maximum Agency Funding: ₹45 lakh
    """
    cost = validate_numeric(
        project_cost,
        "project_cost",
        min_value=0.01,
        max_value=MAX_PROJECT_COST,
    )

    if loan_amount is not None:
        requested_loan = validate_numeric(
            loan_amount,
            "loan_amount",
            min_value=0.01,
            max_value=cost,
        )
    else:
        requested_loan = calculate_maximum_loan(cost)

    if cost <= MICRO_FINANCE_THRESHOLD:
        scheme_name = "Micro Finance Scheme"
        scheme_code = "MFS-RURAL-01"
        interest_rate = 6.5
        tenure_years = 3
        moratorium_months = 3
        max_agency_funding = MICRO_FINANCE_MAX_FUNDING
        eligible_funding = min(requested_loan, max_agency_funding)
        governing_body = "National Rural Livelihood Mission (NRLM) / Micro-credit Division"
        eligibility = [
            "Project cost must not exceed INR 1.40 Lakh.",
            "Rural micro-entrepreneurs, self-help groups (SHGs), and solo artisans.",
            "Simple Aadhaar & Village Panchayat / Ward recommendation required.",
            "No collateral security required up to scheme ceiling.",
        ]
        benefits = [
            "Concessional 6.5% per annum fixed interest rate.",
            "3-month initial moratorium to setup production and sales.",
            "Low paperwork with direct bank disbursement.",
            "Eligibility for prompt repayment incentive rebate (up to 1%).",
        ]
        notes = (
            f"Eligible under Micro Finance Scheme (Project Cost ₹{cost:,.2f} <= ₹1,40,000.00). "
            f"Agency funding capped at ₹{max_agency_funding:,.2f}."
        )
    else:
        scheme_name = "Term Loan Scheme"
        scheme_code = "TLS-MSME-02"
        interest_rate = 8.0
        tenure_years = 7
        moratorium_months = 6
        max_agency_funding = TERM_LOAN_MAX_FUNDING
        eligible_funding = min(requested_loan, max_agency_funding)
        governing_body = "CGTMSE / Rural Enterprise Development Board / PMEGP"
        eligibility = [
            "Project cost above INR 1.40 Lakh and up to INR 50.00 Lakh.",
            "Formal or semi-formal micro enterprises in rural/peri-urban locations.",
            "Udyam Registration Certificate & basic project report required.",
            "Covered under Credit Guarantee cover without third-party collateral.",
        ]
        benefits = [
            "Attractive 8.0% annual interest rate for long-term capital deployment.",
            "Extended 7-year repayment tenure for relaxed liquidity management.",
            "6-month moratorium period during initial gestation and ramp-up.",
            "Covers both machinery capital expenditure and initial working capital.",
        ]
        notes = (
            f"Routed to Term Loan Scheme (Project Cost ₹{cost:,.2f} > ₹1,40,000.00). "
            f"Agency funding limit up to ₹{max_agency_funding:,.2f}."
        )

    return SchemeRecommendation(
        scheme_name=scheme_name,
        scheme_code=scheme_code,
        interest_rate_percent=interest_rate,
        tenure_years=tenure_years,
        tenure_months=tenure_years * 12,
        moratorium_months=moratorium_months,
        max_agency_funding=max_agency_funding,
        eligible_funding=eligible_funding,
        governing_body=governing_body,
        eligibility_criteria=eligibility,
        key_benefits=benefits,
        notes=notes,
    )


def validate_loan_amount(loan_amount: float, scheme: SchemeRecommendation) -> bool:
    """
    Validates if a loan amount exceeds the applicable scheme's maximum agency funding.
    """
    amt = validate_numeric(loan_amount, "loan_amount", min_value=0.01)
    if amt > scheme.max_agency_funding:
        raise FinancialValidationError(
            f"Requested loan amount ₹{amt:,.2f} exceeds maximum agency funding "
            f"ceiling of ₹{scheme.max_agency_funding:,.2f} for {scheme.scheme_name}.",
            field="loan_amount",
            code="LOAN_EXCEEDS_AGENCY_LIMIT",
        )
    return True


def calculate_emi(
    principal: float,
    annual_interest_rate_percent: Optional[float] = None,
    tenure_years: Optional[int] = None,
    moratorium_months: int = 0,
    tenure_months: Optional[int] = None,
    annual_interest_rate: Optional[float] = None,
    monthly_interest_rate: Optional[float] = None,
    num_installments: Optional[int] = None,
) -> EMIResult:
    """
    Calculates monthly EMI using the standard formula:
    EMI = P × r × (1+r)^n / ((1+r)^n - 1)

    Where:
    P = Principal loan amount
    r = Monthly interest rate
    n = Number of monthly installments (post-moratorium repayment period)

    Handles zero-interest loans correctly (EMI = P / n).
    Does not round intermediate calculations.
    Returns EMIResult (subclasses float, supports unpacking for backward compatibility).
    """
    p = validate_numeric(principal, "principal", min_value=0.01)

    # Resolve interest rate
    if monthly_interest_rate is not None:
        r = validate_numeric(monthly_interest_rate, "monthly_interest_rate", min_value=0.0, allow_zero=True)
        ann_rate = r * 12.0 * 100.0
    else:
        rate_val = annual_interest_rate_percent if annual_interest_rate_percent is not None else annual_interest_rate
        if rate_val is None:
            raise FinancialValidationError(
                "Missing required parameter: interest rate must be provided.",
                field="annual_interest_rate",
                code="MISSING_VALUE",
            )
        ann_rate = validate_numeric(rate_val, "annual_interest_rate", min_value=0.0, max_value=100.0, allow_zero=True)
        r = (ann_rate / 100.0) / 12.0

    # Resolve tenure and moratorium
    morat = int(validate_numeric(moratorium_months, "moratorium_months", min_value=0, allow_zero=True))

    if num_installments is not None:
        n = int(validate_numeric(num_installments, "num_installments", min_value=1))
        tot_months = n + morat
        tenure_y = max(1, math.ceil(tot_months / 12))
    elif tenure_months is not None:
        tot_months = int(validate_numeric(tenure_months, "tenure_months", min_value=1))
        tenure_y = max(1, math.ceil(tot_months / 12))
        if morat >= tot_months:
            raise FinancialValidationError(
                f"Moratorium period ({morat} months) cannot be greater than or equal to total tenure ({tot_months} months).",
                field="moratorium_months",
                code="INVALID_MORATORIUM",
            )
        n = tot_months - morat
    elif tenure_years is not None:
        tenure_y = int(validate_numeric(tenure_years, "tenure_years", min_value=1, max_value=30))
        tot_months = tenure_y * 12
        if morat >= tot_months:
            raise FinancialValidationError(
                f"Moratorium period ({morat} months) cannot be greater than or equal to total tenure ({tot_months} months).",
                field="moratorium_months",
                code="INVALID_MORATORIUM",
            )
        n = tot_months - morat
    else:
        raise FinancialValidationError(
            "Missing required parameter: tenure_years or tenure_months must be provided.",
            field="tenure_years",
            code="MISSING_VALUE",
        )

    # Standard EMI formula calculation without premature rounding
    if r == 0.0:
        monthly_emi = p / float(n)
        moratorium_monthly_interest = 0.0
    else:
        factor = math.pow(1.0 + r, n)
        monthly_emi = (p * r * factor) / (factor - 1.0)
        moratorium_monthly_interest = p * r

    # Generate full repayment schedule to extract exact aggregate totals
    schedule = generate_repayment_schedule(
        principal=p,
        annual_interest_rate_percent=ann_rate,
        tenure_years=tenure_y,
        moratorium_months=morat,
    )

    total_interest_payable = sum(item.interest_component for item in schedule)
    total_repayment_amount = p + total_interest_payable

    breakdown = EMIBreakdown(
        principal_amount=round(p, 2),
        annual_interest_rate_percent=ann_rate,
        tenure_months=tot_months,
        moratorium_months=morat,
        post_moratorium_tenure_months=n,
        monthly_emi=round(monthly_emi, 2),
        moratorium_monthly_interest=round(moratorium_monthly_interest, 2),
        total_interest_payable=round(total_interest_payable, 2),
        total_repayment_amount=round(total_repayment_amount, 2),
    )

    return EMIResult(value=round(monthly_emi, 2), breakdown=breakdown, schedule=schedule)


def generate_repayment_schedule(
    principal: float,
    annual_interest_rate_percent: float,
    tenure_years: int,
    moratorium_months: int = 0,
) -> List[RepaymentScheduleItem]:
    """
    Generates a structured, deterministic month-by-month repayment schedule.

    During moratorium:
      Interest servicing period; principal balance remains unchanged.

    Post moratorium:
      Fully amortized EMI payments.
      The final month balance is cleared exactly to 0.0 to prevent floating-point accumulation.
    """
    p = validate_numeric(principal, "principal", min_value=0.01)
    ann_rate = validate_numeric(annual_interest_rate_percent, "annual_interest_rate_percent", min_value=0.0, max_value=100.0, allow_zero=True)
    tenure_y = int(validate_numeric(tenure_years, "tenure_years", min_value=1, max_value=30))
    morat = int(validate_numeric(moratorium_months, "moratorium_months", min_value=0, allow_zero=True))

    total_months = tenure_y * 12
    if morat >= total_months:
        raise FinancialValidationError(
            f"Moratorium period ({morat} months) cannot be greater than or equal to total tenure ({total_months} months).",
            field="moratorium_months",
            code="INVALID_MORATORIUM",
        )

    post_moratorium_months = total_months - morat
    monthly_rate = (ann_rate / 100.0) / 12.0

    if monthly_rate > 0.0:
        factor = math.pow(1.0 + monthly_rate, post_moratorium_months)
        unrounded_emi = (p * monthly_rate * factor) / (factor - 1.0)
    else:
        unrounded_emi = p / float(post_moratorium_months)

    monthly_emi_rounded = round(unrounded_emi, 2)

    schedule: List[RepaymentScheduleItem] = []
    current_balance = p

    # 1. Moratorium Period
    for m in range(1, morat + 1):
        year_num = (m - 1) // 12 + 1
        interest_comp = round(current_balance * monthly_rate, 2)
        principal_comp = 0.0
        installment = interest_comp

        schedule.append(
            RepaymentScheduleItem(
                month=m,
                year=year_num,
                is_moratorium=True,
                opening_balance=round(current_balance, 2),
                installment_amount=round(installment, 2),
                principal_component=round(principal_comp, 2),
                interest_component=round(interest_comp, 2),
                closing_balance=round(current_balance, 2),
                emi=round(installment, 2),
                principal=round(principal_comp, 2),
                interest=round(interest_comp, 2),
            )
        )

    # 2. Amortization Period
    for m in range(morat + 1, total_months + 1):
        year_num = (m - 1) // 12 + 1
        interest_comp = round(current_balance * monthly_rate, 2)

        if m == total_months:
            # Final month: clean closure without residual float drift
            principal_comp = round(current_balance, 2)
            installment = round(principal_comp + interest_comp, 2)
            closing_balance = 0.0
        else:
            principal_comp = round(monthly_emi_rounded - interest_comp, 2)
            if principal_comp > current_balance:
                principal_comp = round(current_balance, 2)
            closing_balance = round(current_balance - principal_comp, 2)
            installment = monthly_emi_rounded

        schedule.append(
            RepaymentScheduleItem(
                month=m,
                year=year_num,
                is_moratorium=False,
                opening_balance=round(current_balance, 2),
                installment_amount=round(installment, 2),
                principal_component=round(principal_comp, 2),
                interest_component=round(interest_comp, 2),
                closing_balance=round(max(0.0, closing_balance), 2),
                emi=round(installment, 2),
                principal=round(principal_comp, 2),
                interest=round(interest_comp, 2),
            )
        )
        current_balance = closing_balance
        if current_balance <= 0.001:
            current_balance = 0.0

    return schedule


def aggregate_quarterly_repayment(
    monthly_schedule: List[RepaymentScheduleItem],
) -> List[QuarterlyRepaymentItem]:
    """
    Derives deterministic quarterly roll-up from month-by-month repayment schedule.
    Preserves exact deterministic totals:
      Quarter principal = month 1 principal + month 2 principal + month 3 principal
      Quarter interest = month 1 interest + month 2 interest + month 3 interest
      Quarter total payment = month 1 payment + month 2 payment + month 3 payment
      Remaining balance = closing balance of the final month in the quarter.
    """
    if not monthly_schedule:
        return []

    quarterly_schedule: List[QuarterlyRepaymentItem] = []
    chunk_size = 3

    for i in range(0, len(monthly_schedule), chunk_size):
        chunk = monthly_schedule[i : i + chunk_size]
        quarter_num = (i // chunk_size) + 1
        year_num = (quarter_num - 1) // 4 + 1

        q_principal = round(sum(item.principal_component for item in chunk), 2)
        q_interest = round(sum(item.interest_component for item in chunk), 2)
        q_payment = round(sum(item.installment_amount for item in chunk), 2)
        q_opening = chunk[0].opening_balance
        q_closing = chunk[-1].closing_balance
        is_morat = all(item.is_moratorium for item in chunk)

        quarterly_schedule.append(
            QuarterlyRepaymentItem(
                quarter=quarter_num,
                year=year_num,
                is_moratorium=is_morat,
                opening_balance=round(q_opening, 2),
                principal_paid=q_principal,
                interest_paid=q_interest,
                total_payment=q_payment,
                remaining_balance=round(q_closing, 2),
                principal_component=q_principal,
                interest_component=q_interest,
                installment_amount=q_payment,
                closing_balance=round(q_closing, 2),
            )
        )

    return quarterly_schedule


def calculate_working_capital(
    project_cost: float,
    monthly_emi: float = 0.0,
) -> WorkingCapitalPlan:
    """
    Deterministic Working Capital and operational cash flow calculations.
    Uses established project ratios (9.5% total monthly OpEx).
    """
    cost = validate_numeric(
        project_cost,
        "project_cost",
        min_value=0.01,
        max_value=MAX_PROJECT_COST,
    )
    emi = validate_numeric(monthly_emi, "monthly_emi", min_value=0.0, allow_zero=True)

    monthly_raw_materials = cost * 0.045
    monthly_labor = cost * 0.025
    monthly_rent = cost * 0.008
    monthly_utilities = cost * 0.004
    monthly_rent_utilities = monthly_rent + monthly_utilities
    monthly_logistics = cost * 0.008
    monthly_marketing = cost * 0.003
    monthly_contingency = cost * 0.002
    monthly_contingency_buffer = monthly_marketing + monthly_contingency

    total_monthly_opex = (
        monthly_raw_materials
        + monthly_labor
        + monthly_rent_utilities
        + monthly_logistics
        + monthly_contingency_buffer
    )

    recommended_3_months_reserve = total_monthly_opex * 3.0
    break_even_monthly_revenue = total_monthly_opex + emi
    projected_monthly_revenue = break_even_monthly_revenue * 1.35
    projected_monthly_net_profit = projected_monthly_revenue - total_monthly_opex - emi

    return WorkingCapitalPlan(
        monthly_raw_materials=round(monthly_raw_materials, 2),
        monthly_labor_wages=round(monthly_labor, 2),
        monthly_rent_utilities=round(monthly_rent_utilities, 2),
        monthly_logistics_packaging=round(monthly_logistics, 2),
        monthly_contingency_buffer=round(monthly_contingency_buffer, 2),
        total_monthly_operating_expense=round(total_monthly_opex, 2),
        recommended_3_months_reserve=round(recommended_3_months_reserve, 2),
        projected_monthly_revenue=round(projected_monthly_revenue, 2),
        projected_monthly_net_profit=round(projected_monthly_net_profit, 2),
        break_even_monthly_revenue=round(break_even_monthly_revenue, 2),
        break_even_occupancy_or_capacity_percent=74.0,
        monthly_operating_cost=round(total_monthly_opex, 2),
        inventory=round(monthly_raw_materials, 2),
        utilities=round(monthly_utilities, 2),
        rent=round(monthly_rent, 2),
        labour=round(monthly_labor, 2),
        transportation=round(monthly_logistics, 2),
        marketing=round(monthly_marketing, 2),
        other=round(monthly_contingency, 2),
        recommended_reserve=round(recommended_3_months_reserve, 2),
        total_working_capital=round(recommended_3_months_reserve, 2),
        is_indicative_estimate=True,
    )


# --- Backward Compatible Aliases ---

def calculate_financial_structure(available_capital: float) -> FinancialStructuring:
    """
    Legacy wrapper for calculate_project_cost and calculate_maximum_loan.
    """
    margin = validate_numeric(available_capital, "available_capital", min_value=0.01)
    project_cost = calculate_project_cost(margin)
    max_loan = calculate_maximum_loan(project_cost)
    subsidy_estimate = round(project_cost * 0.15, 2)

    return FinancialStructuring(
        available_capital=round(margin, 2),
        margin_percentage=DEFAULT_MARGIN_PERCENT,
        project_cost=round(project_cost, 2),
        promoter_contribution=round(margin, 2),
        max_loan_amount=round(max_loan, 2),
        subsidy_or_grant_estimate=subsidy_estimate,
        financial_disclaimer=DISCLAIMER_TEXT,
    )


def route_scheme(project_cost: float, max_loan_amount: float) -> SchemeRecommendation:
    """
    Legacy wrapper for select_scheme.
    """
    return select_scheme(project_cost=project_cost, loan_amount=max_loan_amount)


def calculate_working_capital_plan(project_cost: float, monthly_emi: float) -> WorkingCapitalPlan:
    """
    Legacy alias for calculate_working_capital.
    """
    return calculate_working_capital(project_cost=project_cost, monthly_emi=monthly_emi)
