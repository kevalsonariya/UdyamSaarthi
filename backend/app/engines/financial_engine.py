import math
from typing import List, Tuple
from app.schemas.schemas import (
    FinancialStructuring,
    SchemeRecommendation,
    EMIBreakdown,
    RepaymentScheduleItem,
    WorkingCapitalPlan,
)

DISCLAIMER_TEXT = (
    "Indicative calculation for planning purposes. "
    "Verify applicable scheme terms before making financial decisions."
)

def calculate_financial_structure(available_capital: float) -> FinancialStructuring:
    """
    Deterministic calculation:
    Project Cost = Available Margin / 10%
    Maximum Loan = 90% of Project Cost
    """
    margin_percentage = 10.0
    project_cost = round(available_capital / (margin_percentage / 100.0), 2)
    promoter_contribution = round(available_capital, 2)
    max_loan_amount = round(project_cost * 0.90, 2)
    subsidy_estimate = round(project_cost * 0.15, 2)

    return FinancialStructuring(
        available_capital=promoter_contribution,
        margin_percentage=margin_percentage,
        project_cost=project_cost,
        promoter_contribution=promoter_contribution,
        max_loan_amount=max_loan_amount,
        subsidy_or_grant_estimate=subsidy_estimate,
        financial_disclaimer=DISCLAIMER_TEXT,
    )

def route_scheme(project_cost: float, max_loan_amount: float) -> SchemeRecommendation:
    """
    Scheme routing rules:
    If Project Cost <= 1.40 lakh (140,000 INR):
      Scheme: Micro Finance Scheme
      Interest: 6.5%
      Tenure: 3 years
      Moratorium: 3 months
      Max agency funding: 1.25 lakh (125,000 INR)

    If 1.40 lakh < Project Cost <= 50 lakh (5,000,000 INR):
      Scheme: Term Loan Scheme
      Interest: 8%
      Tenure: 7 years
      Moratorium: 6 months
      Max agency funding: 45 lakh (4,500,000 INR)
    """
    if project_cost <= 140000.00:
        scheme_name = "Micro Finance Scheme"
        scheme_code = "MFS-RURAL-01"
        interest_rate = 6.5
        tenure_years = 3
        moratorium_months = 3
        max_agency_funding = 125000.00
        eligible_funding = min(max_loan_amount, max_agency_funding)
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
            f"Eligible under Micro Finance Scheme (Project Cost ₹{project_cost:,.2f} <= ₹1,40,000.00). "
            f"Agency funding capped at ₹{max_agency_funding:,.2f}."
        )
    else:
        scheme_name = "Term Loan Scheme"
        scheme_code = "TLS-MSME-02"
        interest_rate = 8.0
        tenure_years = 7
        moratorium_months = 6
        max_agency_funding = 4500000.00
        eligible_funding = min(max_loan_amount, max_agency_funding)
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
            f"Routed to Term Loan Scheme (Project Cost ₹{project_cost:,.2f} > ₹1,40,000.00). "
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

def calculate_emi(
    principal: float,
    annual_interest_rate_percent: float,
    tenure_years: int,
    moratorium_months: int,
) -> Tuple[EMIBreakdown, List[RepaymentScheduleItem]]:
    """
    Computes exact EMI and amortization schedule.
    During moratorium: interest-servicing period (simple monthly interest), principal balance unchanged.
    Post moratorium: amortized EMI for remaining tenure.
    """
    total_months = tenure_years * 12
    post_moratorium_months = total_months - moratorium_months
    monthly_rate = (annual_interest_rate_percent / 100.0) / 12.0

    moratorium_monthly_interest = round(principal * monthly_rate, 2)

    if monthly_rate > 0 and post_moratorium_months > 0:
        factor = math.pow(1.0 + monthly_rate, post_moratorium_months)
        monthly_emi = round(principal * monthly_rate * factor / (factor - 1.0), 2)
    else:
        monthly_emi = round(principal / max(1, post_moratorium_months), 2)

    schedule: List[RepaymentScheduleItem] = []
    current_balance = principal
    total_repayment_interest = 0.0

    for m in range(1, moratorium_months + 1):
        year_num = (m - 1) // 12 + 1
        interest_comp = round(current_balance * monthly_rate, 2)
        principal_comp = 0.0
        installment = interest_comp
        total_repayment_interest += interest_comp

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
            )
        )

    for m in range(moratorium_months + 1, total_months + 1):
        year_num = (m - 1) // 12 + 1
        interest_comp = round(current_balance * monthly_rate, 2)

        if m == total_months:
            principal_comp = round(current_balance, 2)
            installment = round(principal_comp + interest_comp, 2)
            closing_balance = 0.0
        else:
            principal_comp = round(monthly_emi - interest_comp, 2)
            if principal_comp > current_balance:
                principal_comp = round(current_balance, 2)
            closing_balance = round(current_balance - principal_comp, 2)
            installment = monthly_emi

        total_repayment_interest += interest_comp
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
            )
        )
        current_balance = closing_balance
        if current_balance <= 0.001:
            current_balance = 0.0

    total_interest_payable = round(total_repayment_interest, 2)
    total_repayment_amount = round(principal + total_interest_payable, 2)

    emi_breakdown = EMIBreakdown(
        principal_amount=round(principal, 2),
        annual_interest_rate_percent=annual_interest_rate_percent,
        tenure_months=total_months,
        moratorium_months=moratorium_months,
        post_moratorium_tenure_months=post_moratorium_months,
        monthly_emi=monthly_emi,
        moratorium_monthly_interest=moratorium_monthly_interest,
        total_interest_payable=total_interest_payable,
        total_repayment_amount=total_repayment_amount,
    )

    return emi_breakdown, schedule

def calculate_working_capital_plan(project_cost: float, monthly_emi: float) -> WorkingCapitalPlan:
    monthly_raw_materials = round(project_cost * 0.045, 2)
    monthly_labor = round(project_cost * 0.025, 2)
    monthly_rent_utilities = round(project_cost * 0.012, 2)
    monthly_logistics = round(project_cost * 0.008, 2)
    monthly_contingency = round(project_cost * 0.005, 2)

    total_monthly_opex = round(
        monthly_raw_materials
        + monthly_labor
        + monthly_rent_utilities
        + monthly_logistics
        + monthly_contingency,
        2,
    )

    recommended_3_months_reserve = round(total_monthly_opex * 3.0, 2)
    break_even_monthly_revenue = round(total_monthly_opex + monthly_emi, 2)
    projected_monthly_revenue = round(break_even_monthly_revenue * 1.35, 2)
    projected_monthly_net_profit = round(
        projected_monthly_revenue - total_monthly_opex - monthly_emi, 2
    )

    return WorkingCapitalPlan(
        monthly_raw_materials=monthly_raw_materials,
        monthly_labor_wages=monthly_labor,
        monthly_rent_utilities=monthly_rent_utilities,
        monthly_logistics_packaging=monthly_logistics,
        monthly_contingency_buffer=monthly_contingency,
        total_monthly_operating_expense=total_monthly_opex,
        recommended_3_months_reserve=recommended_3_months_reserve,
        projected_monthly_revenue=projected_monthly_revenue,
        projected_monthly_net_profit=projected_monthly_net_profit,
        break_even_monthly_revenue=break_even_monthly_revenue,
        break_even_occupancy_or_capacity_percent=74.0,
    )
