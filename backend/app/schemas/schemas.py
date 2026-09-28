from typing import List, Optional
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = "ok"

class BusinessInputRequest(BaseModel):
    location: str = Field(..., json_schema_extra={"example": "Anand, Gujarat"})
    business_category: str = Field(..., json_schema_extra={"example": "Textile & Clothing"})
    available_capital: float = Field(..., ge=1000, description="Available margin capital in INR")

class FinancialStructuring(BaseModel):
    available_capital: float
    margin_percentage: float = 10.0
    project_cost: float
    promoter_contribution: float
    max_loan_amount: float
    subsidy_or_grant_estimate: float
    financial_disclaimer: str = (
        "Indicative calculation for planning purposes. "
        "Verify applicable scheme terms before making financial decisions."
    )

class SchemeRecommendation(BaseModel):
    scheme_name: str
    scheme_code: str
    interest_rate_percent: float
    tenure_years: int
    tenure_months: int
    moratorium_months: int
    max_agency_funding: float
    eligible_funding: float
    governing_body: str
    eligibility_criteria: List[str]
    key_benefits: List[str]
    notes: str

class EMIBreakdown(BaseModel):
    principal_amount: float
    annual_interest_rate_percent: float
    tenure_months: int
    moratorium_months: int
    post_moratorium_tenure_months: int
    monthly_emi: float
    moratorium_monthly_interest: float
    total_interest_payable: float
    total_repayment_amount: float

class RepaymentScheduleItem(BaseModel):
    month: int
    year: int
    is_moratorium: bool
    opening_balance: float
    installment_amount: float
    principal_component: float
    interest_component: float
    closing_balance: float

class WorkingCapitalPlan(BaseModel):
    monthly_raw_materials: float
    monthly_labor_wages: float
    monthly_rent_utilities: float
    monthly_logistics_packaging: float
    monthly_contingency_buffer: float
    total_monthly_operating_expense: float
    recommended_3_months_reserve: float
    projected_monthly_revenue: float
    projected_monthly_net_profit: float
    break_even_monthly_revenue: float
    break_even_occupancy_or_capacity_percent: float

class MarketReachAnalysis(BaseModel):
    catchment_radius_km: int
    estimated_target_population: int
    primary_customer_segments: List[str]
    high_demand_local_channels: List[str]
    peak_demand_seasons: List[str]
    market_reach_summary: str
    is_demo_data: bool = True

class OpportunityAnalysis(BaseModel):
    high_growth_segments: List[str]
    unmet_local_needs: List[str]
    ecosystem_growth_drivers: List[str]
    is_demo_data: bool = True

class SWOTAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    is_demo_data: bool = True

class RiskItem(BaseModel):
    risk_title: str
    severity: str
    category: str
    mitigation_strategy: str

class CompetitorItem(BaseModel):
    name: str
    type_of_business: str
    proximity: str
    strengths: str
    differentiation_strategy: str

class PricingGuidance(BaseModel):
    benchmark_product_or_service: str
    estimated_unit_production_cost: str
    suggested_retail_price: str
    target_gross_margin_percent: float
    pricing_strategy_notes: str
    is_demo_data: bool = True

class BusinessRecommendation(BaseModel):
    feasibility_score: int
    feasibility_rating: str
    summary: str
    first_90_days_milestones: List[str]
    mandatory_licenses_and_registrations: List[str]
    digital_enablement_tips: List[str]
    is_demo_data: bool = True

class FullAnalysisResponse(BaseModel):
    location: str
    business_category: str
    available_capital: float
    financial: FinancialStructuring
    scheme: SchemeRecommendation
    emi: EMIBreakdown
    repayment: List[RepaymentScheduleItem]
    working_capital: WorkingCapitalPlan
    market: MarketReachAnalysis
    opportunities: OpportunityAnalysis
    swot: SWOTAnalysis
    risks: List[RiskItem]
    competitors: List[CompetitorItem]
    pricing: PricingGuidance
    recommendation: BusinessRecommendation
    disclaimer: str
