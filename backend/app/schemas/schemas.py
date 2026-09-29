from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = "ok"

class LocationData(BaseModel):
    raw_input: str
    village_town_city: Optional[str] = None
    taluka_subdistrict: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "India"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    formatted_address: Optional[str] = None
    provider: Optional[str] = "local_catalog"

class BusinessInputRequest(BaseModel):
    location: Optional[Any] = Field(None, json_schema_extra={"example": "Anand, Gujarat"})
    business_category: Optional[Any] = Field(None, json_schema_extra={"example": "Textile & Clothing"})
    available_capital: Optional[Any] = Field(None, description="Available margin capital in INR")
    language: Optional[str] = Field("en", description="Presentation language: en, hi, gu")
    location_detail: Optional[LocationData] = Field(None, description="Structured location model if available")
    request_id: Optional[str] = Field(None, description="Optional client request ID for concurrency tracking")


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
    emi: Optional[float] = None
    principal: Optional[float] = None
    interest: Optional[float] = None

class QuarterlyRepaymentItem(BaseModel):
    quarter: int
    year: int
    is_moratorium: bool
    opening_balance: float
    principal_paid: float
    interest_paid: float
    total_payment: float
    remaining_balance: float
    principal_component: Optional[float] = None
    interest_component: Optional[float] = None
    installment_amount: Optional[float] = None
    closing_balance: Optional[float] = None

class FinancialCalculateRequest(BaseModel):
    available_margin: Optional[float] = Field(None, description="Available margin capital in INR")
    available_capital: Optional[float] = Field(None, description="Available capital alias for margin in INR")
    location: Optional[str] = None
    business_category: Optional[str] = None

class SchemeRecommendRequest(BaseModel):
    project_cost: Optional[float] = Field(None, description="Total project cost in INR")
    available_margin: Optional[float] = Field(None, description="Available margin in INR")
    available_capital: Optional[float] = Field(None, description="Alias for available margin")
    requested_loan_amount: Optional[float] = Field(None, description="Requested loan amount in INR")

class EMICalculateRequest(BaseModel):
    principal: Optional[float] = Field(None, description="Principal loan amount in INR")
    annual_interest_rate: Optional[float] = Field(None, description="Annual interest rate percentage")
    annual_interest_rate_percent: Optional[float] = Field(None, description="Annual interest rate percentage alias")
    tenure_years: Optional[int] = Field(None, description="Loan tenure in years")
    moratorium_months: Optional[int] = Field(0, description="Moratorium period in months")
    available_margin: Optional[float] = Field(None, description="Deduce from margin if principal not provided")
    available_capital: Optional[float] = None

class RepaymentCalculateRequest(BaseModel):
    principal: Optional[float] = Field(None, description="Principal loan amount in INR")
    annual_interest_rate: Optional[float] = Field(None, description="Annual interest rate percentage")
    annual_interest_rate_percent: Optional[float] = Field(None, description="Annual interest rate percentage alias")
    tenure_years: Optional[int] = Field(None, description="Loan tenure in years")
    moratorium_months: Optional[int] = Field(0, description="Moratorium period in months")
    available_margin: Optional[float] = None
    available_capital: Optional[float] = None

class WorkingCapitalCalculateRequest(BaseModel):
    project_cost: Optional[float] = Field(None, description="Project cost in INR")
    monthly_emi: Optional[float] = Field(0.0, description="Monthly EMI in INR")
    available_margin: Optional[float] = None
    available_capital: Optional[float] = None

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
    # Phase B5 Enhanced Structured Breakdown
    monthly_operating_cost: Optional[float] = None
    inventory: Optional[float] = None
    utilities: Optional[float] = None
    rent: Optional[float] = None
    labour: Optional[float] = None
    transportation: Optional[float] = None
    marketing: Optional[float] = None
    other: Optional[float] = None
    recommended_reserve: Optional[float] = None
    total_working_capital: Optional[float] = None
    is_indicative_estimate: bool = True

class MarketReachAnalysis(BaseModel):
    catchment_radius_km: int
    estimated_target_population: int
    primary_customer_segments: List[str]
    high_demand_local_channels: List[str]
    peak_demand_seasons: List[str]
    market_reach_summary: str
    is_demo_data: bool = True
    is_estimate: bool = True
    data_source: str = "Prototype heuristic"

class OpportunityItem(BaseModel):
    title: str
    type: str = Field(..., description="High Growth, Unmet Need, Ecosystem Driver, Seasonal Opportunity, Customer Segment Opportunity, or Channel Opportunity")
    description: str
    reason: str
    local_factor: str
    impact: Optional[str] = "High"

class OpportunityAnalysis(BaseModel):
    high_growth_segments: List[str] = Field(default_factory=list)
    unmet_local_needs: List[str] = Field(default_factory=list)
    ecosystem_growth_drivers: List[str] = Field(default_factory=list)
    items: List[OpportunityItem] = Field(default_factory=list)
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
    is_demo_data: bool = True
    data_source: str = "Indicative category-location profile"
    location_status: str = "Location unavailable — live mapping planned for Phase B9"
    # Phase B9 Real Provider Fields
    category: Optional[str] = None
    address: Optional[str] = None
    distance_km: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_id: Optional[str] = None
    map_url: Optional[str] = None
    website_url: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    source: Optional[str] = None
    is_estimate: bool = False
    retrieved_at: Optional[str] = None

class CompetitorSearchRequest(BaseModel):
    location: str
    business_category: str
    request_id: Optional[str] = None
    language: Optional[str] = "en"
    radius_km: Optional[float] = None
    location_detail: Optional[LocationData] = None

class CompetitorSearchData(BaseModel):
    request_id: Optional[str] = None
    input: Dict[str, Any]
    competitors: List[CompetitorItem]
    is_live_data: bool = False
    source: str = "Google Places API"

class CompetitorSearchResponse(BaseModel):
    success: bool = True
    data: CompetitorSearchData


class PricingGuidance(BaseModel):
    benchmark_product_or_service: str
    estimated_unit_production_cost: str
    suggested_retail_price: str
    target_gross_margin_percent: float
    pricing_strategy_notes: str
    is_demo_data: bool = True
    is_estimate: bool = True
    data_source: str = "Prototype category benchmark"


class BusinessRecommendation(BaseModel):
    feasibility_score: int
    feasibility_rating: str
    summary: str
    first_90_days_milestones: List[str]
    mandatory_licenses_and_registrations: List[str]
    digital_enablement_tips: List[str]
    is_demo_data: bool = True

class BusinessProfile(BaseModel):
    category_id: str
    category_name: str
    description: str
    primary_activities: List[str] = Field(default_factory=list)
    key_equipment: List[str] = Field(default_factory=list)
    typical_capex_range: str
    capital_adequacy: str
    target_location: str

class BusinessAnalysisMetadata(BaseModel):
    data_source: str = "prototype_demo_data"
    is_live_data: bool = False
    note: str = "Prototype demo datasets. Not verified live/real-time market data."
    version: str = "1.0-prototype"

class AIExplanation(BaseModel):
    summary: str
    market_insight: str
    opportunity_explanation: str
    risk_explanation: str
    financial_explanation: str
    scheme_explanation: str
    recommended_actions: List[str]
    next_steps: List[str]
    is_ai_generated: bool = False
    provider: str = "deterministic_rule_engine"

class FullAnalysisResponse(BaseModel):
    success: bool = True
    request_id: Optional[str] = None
    input: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    business: Optional[Dict[str, Any]] = None
    location: str
    business_category: str
    available_capital: float
    financial: FinancialStructuring
    scheme: SchemeRecommendation
    emi: EMIBreakdown
    repayment: List[RepaymentScheduleItem]
    quarterly_repayment: Optional[List[QuarterlyRepaymentItem]] = None
    working_capital: WorkingCapitalPlan
    market: MarketReachAnalysis
    opportunities: OpportunityAnalysis
    swot: SWOTAnalysis
    risks: List[RiskItem]
    competitors: List[CompetitorItem]
    pricing: PricingGuidance
    recommendation: BusinessRecommendation
    location_detail: Optional[LocationData] = None
    ai_explanation: Optional[AIExplanation] = None
    disclaimer: str

class CategoryMetadataItem(BaseModel):
    id: str
    name: str
    display_name: str
    sector: str
    typical_capex_min: float
    typical_capex_max: float
    subcategories: List[str]
    competitor_search_terms: List[str]
    primary_activities: List[str]
    key_equipment: List[str]
    mandatory_licenses: List[str]
    location_factors: Optional[Dict[str, Any]] = None
    market_profile: Optional[Dict[str, Any]] = None
    opportunity_profile: Optional[Dict[str, Any]] = None
    risk_profile: Optional[Dict[str, Any]] = None
    pricing_profile: Optional[Dict[str, Any]] = None

class CategoriesListResponse(BaseModel):
    success: bool = True
    total: int
    categories: List[CategoryMetadataItem]

class LocationSuggestResponse(BaseModel):
    success: bool = True
    total: int
    query: str
    suggestions: List[LocationData]

