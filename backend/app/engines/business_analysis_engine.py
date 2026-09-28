"""
Phase B3 — Business Analysis Engine
Implements dynamic business, market, SWOT, competitive, and pricing analysis.
Decoupled from data loading via BaseDataProvider.
"""

import math
from typing import Any, Dict, List, Optional
from app.data.data_provider import BaseDataProvider, get_data_provider
from app.schemas.schemas import (
    MarketReachAnalysis,
    OpportunityAnalysis,
    SWOTAnalysis,
    RiskItem,
    CompetitorItem,
    PricingGuidance,
    BusinessRecommendation,
)


class BusinessAnalysisValidationError(Exception):
    """Exception raised when business analysis input validation fails."""
    def __init__(self, message: str, field: Optional[str] = None, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code


def validate_business_inputs(
    location: Any,
    business_category: Any,
    available_capital: Any,
    data_provider: Optional[BaseDataProvider] = None,
) -> Dict[str, Any]:
    """
    Validates all inputs for business analysis:
    - Rejects missing / empty location
    - Rejects missing / empty / unsupported business category
    - Rejects missing / non-numeric / zero / negative / excessive capital
    Returns normalized dictionary of validated inputs and category metadata.
    """
    if data_provider is None:
        data_provider = get_data_provider()

    # 1. Location Validation
    if location is None:
        raise BusinessAnalysisValidationError(
            "Missing required field: 'location' cannot be None.",
            field="location",
            code="MISSING_LOCATION",
        )
    if not isinstance(location, str) or not location.strip():
        raise BusinessAnalysisValidationError(
            "Location cannot be empty. Please specify a valid target town, village, or district.",
            field="location",
            code="EMPTY_LOCATION",
        )
    clean_location = location.strip()

    # 2. Business Category Validation
    if business_category is None:
        raise BusinessAnalysisValidationError(
            "Missing required field: 'business_category' cannot be None.",
            field="business_category",
            code="MISSING_CATEGORY",
        )
    if not isinstance(business_category, str) or not business_category.strip():
        raise BusinessAnalysisValidationError(
            "Business category cannot be empty.",
            field="business_category",
            code="EMPTY_CATEGORY",
        )
    clean_category = business_category.strip()

    resolved_category = data_provider.resolve_category(clean_category)
    if resolved_category is None:
        supported = ", ".join(data_provider.get_supported_categories())
        raise BusinessAnalysisValidationError(
            f"Unsupported business category: '{clean_category}'. Supported categories are: {supported}.",
            field="business_category",
            code="UNSUPPORTED_CATEGORY",
        )

    # 3. Available Capital Validation
    if available_capital is None:
        raise BusinessAnalysisValidationError(
            "Missing required field: 'available_capital' cannot be None.",
            field="available_capital",
            code="MISSING_CAPITAL",
        )

    if isinstance(available_capital, bool):
        raise BusinessAnalysisValidationError(
            "Invalid non-numeric value for 'available_capital': boolean is not permitted.",
            field="available_capital",
            code="NON_NUMERIC",
        )

    if not isinstance(available_capital, (int, float, str)):
        raise BusinessAnalysisValidationError(
            f"Invalid non-numeric value for 'available_capital': type {type(available_capital).__name__} is not supported.",
            field="available_capital",
            code="NON_NUMERIC",
        )

    try:
        cap = float(available_capital)
    except (ValueError, TypeError):
        raise BusinessAnalysisValidationError(
            f"Invalid non-numeric value for 'available_capital': '{available_capital}'.",
            field="available_capital",
            code="NON_NUMERIC",
        )

    if math.isnan(cap) or math.isinf(cap):
        raise BusinessAnalysisValidationError(
            "Available capital must be a finite real number.",
            field="available_capital",
            code="NON_FINITE",
        )

    if cap == 0.0:
        raise BusinessAnalysisValidationError(
            "Available capital must be greater than zero.",
            field="available_capital",
            code="ZERO_CAPITAL",
        )

    if cap < 0.0:
        raise BusinessAnalysisValidationError(
            f"Available capital cannot be negative, got {cap:,.2f}.",
            field="available_capital",
            code="NEGATIVE_CAPITAL",
        )

    if cap > 500000.0:
        raise BusinessAnalysisValidationError(
            f"Available capital ₹{cap:,.2f} produces project cost exceeding ₹50,00,000 maximum scheme ceiling.",
            field="available_capital",
            code="EXCEEDS_MAX_CAPITAL",
        )

    return {
        "location": clean_location,
        "business_category": clean_category,
        "resolved_category": resolved_category,
        "available_capital": cap,
    }


def analyze_business_profile(
    location: str,
    business_category: str,
    available_capital: float,
    data_provider: Optional[BaseDataProvider] = None,
) -> Dict[str, Any]:
    """
    Executes dynamic business analysis based on location, business_category, and available_capital.
    Produces:
    - business
    - market
    - opportunities
    - swot
    - risks
    - competitors
    - pricing
    - recommendation
    - metadata (transparency flag)
    """
    if data_provider is None:
        data_provider = get_data_provider()

    validated = validate_business_inputs(
        location=location,
        business_category=business_category,
        available_capital=available_capital,
        data_provider=data_provider,
    )

    loc = validated["location"]
    cap = validated["available_capital"]
    cat = validated["resolved_category"]
    cat_id = cat["id"]
    cat_name = cat["name"]

    # 1. Fetch domain intelligence from repository
    loc_prof = data_provider.get_location_profile(loc)
    mkt_raw = data_provider.get_market_profile(cat_id, loc) or {}
    comp_raw = data_provider.get_competitors(cat_id, loc)
    pricing_raw = data_provider.get_pricing_profile(cat_id) or {}
    meta = data_provider.get_metadata()

    # 2. Dynamic Feasibility Calculation based on Capital & Location
    min_capex = cat.get("typical_capex_min", 50000.0)
    max_capex = cat.get("typical_capex_max", 1000000.0)
    project_cost = cap / 0.10

    # Calculate capital adequacy ratio
    capital_ratio = project_cost / min_capex
    base_score = 75
    if capital_ratio < 1.0:
        base_score = max(55, int(60 + capital_ratio * 15))
        rating = "Marginally Feasible (Capital Constrained)"
        capital_note = f"Initial capital ₹{cap:,.0f} (Project Cost ₹{project_cost:,.0f}) is on the lean side for typical {cat_name} entry. Recommended to start with a micro model or seek additional collateral-free agency subsidy."
    elif capital_ratio >= 2.5:
        base_score = min(96, int(86 + (capital_ratio - 2.5) * 2))
        rating = "Highly Feasible (Well Capitalized)"
        capital_note = f"Healthy margin capital ₹{cap:,.0f} enables strong commercial launch with full machinery and 3-month inventory cushion."
    else:
        base_score = int(78 + (capital_ratio - 1.0) * 5)
        rating = "Moderately Feasible (Viable Micro-Venture)"
        capital_note = f"Available capital ₹{cap:,.0f} aligns solidly with standard {cat_name} startup capex requirements."

    # Location favorability bonus
    if cat_name in loc_prof.get("favorable_categories", []):
        base_score = min(98, base_score + 6)
        location_synergy = f"Strong regional tailwinds: {loc} features established supply chains and high commercial absorption for {cat_name}."
    else:
        location_synergy = f"Stable community demand for {cat_name} in {loc} across standard localized retail/service channels."

    feasibility_score = base_score

    # 3. Dynamic Market Reach Analysis
    loc_mult = loc_prof.get("multiplier", 1.0)
    base_pop = mkt_raw.get("base_target_population", 150000)
    estimated_pop = int(base_pop * loc_mult)
    catchment_km = mkt_raw.get("base_catchment_radius_km", 20)

    market = MarketReachAnalysis(
        catchment_radius_km=catchment_km,
        estimated_target_population=estimated_pop,
        primary_customer_segments=mkt_raw.get("primary_customer_segments", [
            f"Local families and rural households in {loc} vicinity",
            "Small business merchants and agrarian workers requiring daily supplies",
        ]),
        high_demand_local_channels=[
            ch.replace("market corridors", f"{loc} market square & corridors")
            for ch in mkt_raw.get("high_demand_local_channels", [
                f"Direct storefront in {loc} central market square",
                "WhatsApp catalog ordering for local village self-help groups",
            ])
        ],
        peak_demand_seasons=mkt_raw.get("peak_demand_seasons", [
            "Post-harvest festival celebrations (October - January)",
            "Pre-monsoon preparation months (May - June)",
        ]),
        market_reach_summary=(
            f"In the {loc} commercial catchment (~{catchment_km} km radius, {estimated_pop:,} population), "
            f"{cat_name} exhibits resilient, repeat demand. {location_synergy}"
        ),
        is_demo_data=True,
    )

    # 4. Dynamic Opportunities
    growth_segments = list(mkt_raw.get("unmet_local_needs", []))
    if cap <= 25000:
        growth_segments.append(f"Lean micro-fulfillment model with doorstep delivery across {loc} hamlets.")
    else:
        growth_segments.append(f"Semi-mechanized production and regional retail B2B distribution in {loc} taluka.")

    opportunities = OpportunityAnalysis(
        high_growth_segments=mkt_raw.get("primary_customer_segments", [
            f"Value-added {cat_name} products for semi-urban households",
            f"Institutional bulk orders across schools and local enterprises in {loc}",
        ])[:3],
        unmet_local_needs=mkt_raw.get("unmet_local_needs", [
            "Consistent quality with transparent pricing",
            "Doorstep fulfillment and digital payment enablement",
        ]),
        ecosystem_growth_drivers=mkt_raw.get("ecosystem_growth_drivers", [
            f"Expanding road connectivity and UPI mobile penetration in {loc}",
            "Central and State MSME priority lending initiatives",
        ]),
        is_demo_data=True,
    )

    # 5. Dynamic SWOT
    swot_dict = mkt_raw.get("swot", {})
    swot = SWOTAnalysis(
        strengths=swot_dict.get("strengths", [
            "Direct local customer relationships and zero urban mall overheads",
            "Fast inventory turnover on everyday high-demand products",
        ]),
        weaknesses=swot_dict.get("weaknesses", [
            "Initial dependence on local supplier credit terms",
            "Working capital pressure during peak festive stocking months",
        ]),
        opportunities=swot_dict.get("opportunities", [
            f"Expanding market radius into adjoining villages surrounding {loc}",
            "Deploying WhatsApp Business catalog and digital payment soundbox",
        ]),
        threats=swot_dict.get("threats", [
            "Fluctuations in raw material procurement prices",
            "Competition from seasonal itinerant vendors during weekly haats",
        ]),
        is_demo_data=True,
    )

    # 6. Dynamic Risks & Mitigations
    risks = [
        RiskItem(
            risk_title="Working Capital Fluctuation",
            severity="High" if cap < min_capex else "Medium",
            category="Financial",
            mitigation_strategy=(
                f"Maintain the mandatory 3-month operating expense reserve calculated by UdyamSaarthi. "
                "Limit customer credit khata to trusted regulars with a 15-day settlement cycle."
            ),
        ),
        RiskItem(
            risk_title="Supplier Sourcing Dependency",
            severity="Medium",
            category="Operational",
            mitigation_strategy=(
                f"Identify at least 2 alternate wholesale suppliers within a 50 km radius of {loc} "
                "to prevent stock-outs during peak seasonal demand."
            ),
        ),
        RiskItem(
            risk_title="Price Undercutting by Established Competitors",
            severity="Medium",
            category="Market",
            mitigation_strategy=(
                "Differentiate through transparent billing, reliable after-sales support, "
                "and personalized doorstep delivery rather than entering destructive price wars."
            ),
        ),
    ]

    # 7. Dynamic Competitors
    competitors = [
        CompetitorItem(
            name=c.get("name", "Local Merchant"),
            type_of_business=c.get("type_of_business", "Traditional Retailer"),
            proximity=c.get("proximity", f"Near {loc} market"),
            strengths=c.get("strengths", "Long-standing local presence"),
            differentiation_strategy=c.get("differentiation_strategy", "Provide higher reliability and digital receipts."),
        )
        for c in comp_raw
    ]

    # 8. Dynamic Pricing Guidance
    strategy_note = pricing_raw.get("pricing_strategy_notes", "Maintain price parity with nearest town.")
    if cap < min_capex * 1.5:
        cap_strategy = pricing_raw.get("low_capital_strategy", "Focus on high cash-turnover lines.")
    else:
        cap_strategy = pricing_raw.get("high_capital_strategy", "Leverage bulk purchasing discounts.")

    pricing = PricingGuidance(
        benchmark_product_or_service=pricing_raw.get("benchmark_product_or_service", f"Standard {cat_name} Package Unit"),
        estimated_unit_production_cost=pricing_raw.get("estimated_unit_production_cost", "₹100 baseline unit cost"),
        suggested_retail_price=pricing_raw.get("suggested_retail_price", "₹140 - ₹160 per unit"),
        target_gross_margin_percent=float(pricing_raw.get("target_gross_margin_percent", 35.0)),
        pricing_strategy_notes=f"{strategy_note} Capital Strategy: {cap_strategy}",
        is_demo_data=True,
    )

    # 9. Dynamic Recommendation
    recommendation = BusinessRecommendation(
        feasibility_score=feasibility_score,
        feasibility_rating=rating,
        summary=f"{capital_note} {location_synergy}",
        first_90_days_milestones=cat.get("first_90_days_milestones", [
            f"Days 1-30: Secure premises in {loc}, complete Udyam registration, and open current account.",
            "Days 31-60: Procure core machinery/inventory and setup digital payment soundbox.",
            "Days 61-90: Inaugural launch, onboard 40+ local customers, and stabilize monthly cash flows.",
        ]),
        mandatory_licenses_and_registrations=cat.get("mandatory_licenses", [
            "Udyam MSME Registration Certificate",
            "Local Gram Panchayat / Municipal Trade License",
        ]),
        digital_enablement_tips=cat.get("digital_enablement", [
            "Deploy UPI QR payment soundbox at billing counter.",
            "Setup WhatsApp Business with digital product catalog.",
        ]),
        is_demo_data=True,
    )

    # 10. Core Business Profile
    business = {
        "category_id": cat_id,
        "category_name": cat_name,
        "description": cat["description"],
        "primary_activities": cat.get("primary_activities", []),
        "key_equipment": cat.get("key_equipment", []),
        "typical_capex_range": f"₹{min_capex:,.0f} - ₹{max_capex:,.0f}",
        "capital_adequacy": "Optimal" if cap >= min_capex * 1.5 else ("Adequate" if cap >= min_capex else "Lean"),
        "target_location": loc,
    }

    return {
        "business": business,
        "market": market,
        "opportunities": opportunities,
        "swot": swot,
        "risks": risks,
        "competitors": competitors,
        "pricing": pricing,
        "recommendation": recommendation,
        "metadata": meta,
    }
