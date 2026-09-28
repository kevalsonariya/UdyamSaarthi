from typing import List, Dict, Any
from app.schemas.schemas import (
    MarketReachAnalysis,
    OpportunityAnalysis,
    SWOTAnalysis,
    RiskItem,
    CompetitorItem,
    PricingGuidance,
    BusinessRecommendation,
)

def generate_advisory_profile(
    location: str,
    business_category: str,
    project_cost: float,
) -> Dict[str, Any]:
    """
    Generates structured hyper-local advisory intelligence.
    Clearly flagged as prototype demo intelligence with realistic market domain insight.
    """
    loc_clean = location.strip()
    cat_clean = business_category.strip().title()

    if "Textile" in cat_clean or "Cloth" in cat_clean or "Apparel" in cat_clean:
        market = MarketReachAnalysis(
            catchment_radius_km=18,
            estimated_target_population=185000,
            primary_customer_segments=[
                "Semi-urban households seeking readymade family ethnic & casual wear",
                "Agricultural farm community purchasing durable everyday cotton wear",
                "School and institutional bulk uniform requirements in taluka vicinity",
                "Festive, wedding, and seasonal celebration shoppers in peri-urban markets",
            ],
            high_demand_local_channels=[
                "Weekly Haat (local bazaars) across Anand, Karamsad & Borsad corridors",
                "Direct storefront located near bus stand or taluka market square",
                "WhatsApp catalog ordering for village self-help groups & extended families",
            ],
            peak_demand_seasons=[
                "Diwali & Navratri festival season (September - November)",
                "Winter wedding season (December - February)",
                "School re-opening term (June - July)",
            ],
            market_reach_summary=(
                f"In the {loc_clean} commercial catchment, textile and garments show resilient, repeat demand. "
                "The rural and semi-urban population prioritizes durable fabrics, competitive bulk pricing, and local trust."
            ),
            is_demo_data=True,
        )

        opportunities = OpportunityAnalysis(
            high_growth_segments=[
                "Blended cotton everyday wear with reinforced stitching for agrarian workers",
                "Low-cost stitched women's kurtis and traditional ethnic wear",
                "Value-tier children's seasonal clothing kits",
            ],
            unmet_local_needs=[
                "Lack of on-the-spot tailoring & alteration alongside retail purchase",
                "Limited transparent pricing without aggressive haggling in weekly haats",
                "Shortage of organized inventory for school & local workforce uniforms",
            ],
            ecosystem_growth_drivers=[
                "Close supply chain proximity to Surat and Ahmedabad textile wholesale mandis",
                "Robust rural road connectivity across Anand district talukas",
                "Government handloom and khadi weaver subsidy linkage opportunities",
            ],
            is_demo_data=True,
        )

        swot = SWOTAnalysis(
            strengths=[
                "Direct sourcing leverage from nearby Gujarat textile manufacturing hubs",
                "Low overhead operating model compared to urban mall retail outlets",
                "Deep community goodwill and high customer retention through personalized service",
            ],
            weaknesses=[
                "Working capital pressure during pre-festival heavy stocking months",
                "Initial vulnerability to fabric wastage without computerized cutting",
                "Dependence on cash liquidity patterns aligned with crop harvest cycles",
            ],
            opportunities=[
                "Establishing supply ties with local schools, colleges, and factory workforces",
                "Leveraging digital payment (UPI) and localized WhatsApp marketing",
                "Expanding into customized bridal stitching during winter wedding peaks",
            ],
            threats=[
                "Fluctuation in yarn/cotton raw material benchmark prices",
                "Competition from seasonal itinerant vendors in weekly village markets",
                "Fast-fashion online e-commerce discounting penetration in younger demographics",
            ],
            is_demo_data=True,
        )

        risks = [
            RiskItem(
                risk_title="Inventory Stagnation (Unsold Dead Stock)",
                severity="High",
                category="Operational",
                mitigation_strategy="Implement phased procurement: stock 60% standard evergreen items (cotton shirts, dhotis, plain kurtis) and only 40% trend-driven designs.",
            ),
            RiskItem(
                risk_title="Harvest Season Credit Cycle Delays",
                severity="Medium",
                category="Cash Flow",
                mitigation_strategy="Limit informal book credit (udhar) to a maximum 15-day cycle with strict customer ledger tracking on micro-accounting apps.",
            ),
            RiskItem(
                risk_title="Monsoon & Moisture Fabric Damage",
                severity="Low",
                category="Storage",
                mitigation_strategy="Ensure raised pallet shelving at least 1 foot above ground floor level and use silica gel dehumidifying packs.",
            ),
        ]

        competitors = [
            CompetitorItem(
                name="Shree Ram Textiles & Vastralaya",
                type_of_business="Traditional Family Clothing Retailer",
                proximity="1.2 km (Taluka Main Road)",
                strengths="Long standing 20-year presence and deep local credit accounts",
                differentiation_strategy="Offer modern trend cuts, transparent fixed pricing with free alteration, and instant digital payments.",
            ),
            CompetitorItem(
                name="Anand Weekly Haat Vendors",
                type_of_business="Itinerant Weekend Stalls",
                proximity="2.5 km (Weekly Market Ground)",
                strengths="Ultra-low overheads and aggressive discount pricing",
                differentiation_strategy="Guarantee fabric wash-durability, permanent shop availability for returns/exchanges, and superior stitching quality.",
            ),
            CompetitorItem(
                name="Kisan Garment Mart",
                type_of_business="Budget Workwear Shop",
                proximity="3.8 km (Railway Crossing Market)",
                strengths="Strong bulk stocking of heavy-duty denim and work shirts",
                differentiation_strategy="Bundle complimentary tailoring alterations and expand family-wide ethnic collection under one roof.",
            ),
        ]

        pricing = PricingGuidance(
            benchmark_product_or_service="Standard Ready-to-Wear Cotton Kurti / Work Shirt",
            estimated_unit_production_cost="₹180 - ₹240 per unit (fabric sourcing + stitching)",
            suggested_retail_price="₹350 - ₹480 per unit",
            target_gross_margin_percent=38.5,
            pricing_strategy_notes=(
                "Adopt a cost-plus value pricing model. Keep staple daily garments at a lean 30% margin "
                "to drive rapid footfall, while applying 45%-55% margins on festive embroidery and wedding pieces."
            ),
            is_demo_data=True,
        )

        recommendation = BusinessRecommendation(
            feasibility_score=86,
            feasibility_rating="Highly Feasible",
            summary=(
                f"The proposed Textile & Clothing enterprise in {loc_clean} shows strong commercial viability. "
                "With ₹10,00,000 project funding, the venture can balance high-margin retail sales with a 2-machine "
                "rapid alteration/custom stitching unit, unlocking reliable recurring cash flows."
            ),
            first_90_days_milestones=[
                "Days 1-20: Complete Udyam Registration, GST enrollment, and secure high-footfall shop premises.",
                "Days 21-45: Procure inventory from wholesale hubs (Ahmedabad/Surat) and install 2 industrial sewing workstations.",
                "Days 46-60: Soft launch in weekly market corridor with inaugural promotional discounts and WhatsApp catalog.",
                "Days 61-90: Establish corporate/institutional ties for school uniforms and achieve break-even baseline revenue.",
            ],
            mandatory_licenses_and_registrations=[
                "Udyam MSME Registration Certificate (Govt of India)",
                "Local Gram Panchayat / Municipal Corporation Trade Shop & Establishment Act License",
                "GST Registration (Mandatory if turnover exceeds ₹40 Lakhs or for inter-state purchasing)",
                "Current Bank Account linked with MSME Scheme subsidy disbursal",
            ],
            digital_enablement_tips=[
                "Deploy BharatQR / UPI soundbox for friction-free micro-transactions.",
                "Setup WhatsApp Business with digital product catalog and automated greeting.",
                "Maintain digital khata (ledger) via Khatabook or Vyapar to track inventory turns.",
            ],
            is_demo_data=True,
        )

    elif "Dairy" in cat_clean or "Agro" in cat_clean or "Food" in cat_clean:
        market = MarketReachAnalysis(
            catchment_radius_km=25,
            estimated_target_population=210000,
            primary_customer_segments=[
                "Local cooperative societies and bulk procurement aggregators",
                "Town restaurants, sweet marts, and tea stalls requiring daily fresh delivery",
                "Health-conscious semi-urban families seeking pure unadulterated food products",
            ],
            high_demand_local_channels=[
                "Direct morning milk delivery routes to residential wards",
                "B2B tie-ups with district dairy processing federations",
                "Farm-gate retail kiosk near arterial highway junction",
            ],
            peak_demand_seasons=[
                "Summer season for curd, buttermilk, and cold processing (March - June)",
                "Festival and wedding season for ghee, mawa, and sweets (October - January)",
            ],
            market_reach_summary=f"Strong perennial demand in {loc_clean} backed by world-renowned cooperative dairy infrastructure.",
            is_demo_data=True,
        )

        opportunities = OpportunityAnalysis(
            high_growth_segments=[
                "Value-added dairy products: Paneer, cultured Ghee, and vacuum-sealed curd",
                "Organic fodder supply and cattle nutrition supplements",
            ],
            unmet_local_needs=[
                "Consistent cold-chain storage at village collection points",
                "Adulteration-tested certified pure cow and buffalo milk directly to households",
            ],
            ecosystem_growth_drivers=[
                "Presence of GCMMF/Amul cooperative ecosystem in Anand district",
                "Subsidies under National Livestock Mission and NABARD Agri-Infra fund",
            ],
            is_demo_data=True,
        )

        swot = SWOTAnalysis(
            strengths=["Guaranteed daily liquidity and continuous cash sales", "Abundant local agrarian feedstock"],
            weaknesses=["Perishable nature of product requires immediate cooling", "High initial cattle acquisition cost"],
            opportunities=["Direct consumer delivery with 20% premium pricing", "Bio-gas and organic vermicompost byproduct sales"],
            threats=["Animal health and seasonal foot-and-mouth disease outbreaks", "Fodder price surges during dry summer months"],
            is_demo_data=True,
        )

        risks = [
            RiskItem(
                risk_title="Cold Chain Breakdown",
                severity="High",
                category="Operational",
                mitigation_strategy="Install a solar-backed battery inverter for the 500-liter bulk milk chiller.",
            ),
            RiskItem(
                risk_title="Livestock Mortality",
                severity="Medium",
                category="Asset Risk",
                mitigation_strategy="Mandatory microchipping and comprehensive cattle insurance under government subsidy programs.",
            ),
        ]

        competitors = [
            CompetitorItem(
                name="Village Cooperative Collection Centre",
                type_of_business="Cooperative Mandi",
                proximity="0.8 km",
                strengths="Guaranteed purchase of whatever quantity produced",
                differentiation_strategy="Retain higher margins through direct retail sale of paneer and bottled fresh milk.",
            )
        ]

        pricing = PricingGuidance(
            benchmark_product_or_service="Fresh Buffalo Milk (6.5% Fat, 9.0% SNF)",
            estimated_unit_production_cost="₹42 - ₹46 per liter",
            suggested_retail_price="₹62 - ₹68 per liter",
            target_gross_margin_percent=32.0,
            pricing_strategy_notes="Provide competitive bulk rate to sweet makers while commanding premium for bottled doorstep delivery.",
            is_demo_data=True,
        )

        recommendation = BusinessRecommendation(
            feasibility_score=88,
            feasibility_rating="Highly Feasible",
            summary=f"Excellent potential in {loc_clean} due to established dairy backward linkages and strong urban-rural connectivity.",
            first_90_days_milestones=[
                "Days 1-30: Site shelter construction and procurement of high-yielding vaccinated milch animals.",
                "Days 31-60: Installation of chiller unit and establishment of morning residential distribution route.",
                "Days 61-90: Scale up paneer processing unit to absorb evening surplus production.",
            ],
            mandatory_licenses_and_registrations=[
                "FSSAI Food Safety Registration / License",
                "Udyam MSME Registration",
                "Local Gram Panchayat NOC",
                "Livestock Insurance Policy Documentation",
            ],
            digital_enablement_tips=[
                "Use automated Fat/SNF testing digital milk analyzer.",
                "Customer monthly billing via recurring UPI auto-pay.",
            ],
            is_demo_data=True,
        )

    else:
        market = MarketReachAnalysis(
            catchment_radius_km=15,
            estimated_target_population=140000,
            primary_customer_segments=[
                "Local agricultural households and village retail consumers",
                "Service trade workers, mechanics, and small workshop owners",
                "Gram Panchayat institutions and public utility offices",
            ],
            high_demand_local_channels=[
                "Direct storefront on main village/taluka connectivity road",
                "Word of mouth referrals through local self-help groups and trade guilds",
            ],
            peak_demand_seasons=[
                "Post-harvest festival celebrations (October - January)",
                "Pre-monsoon preparation months (May - June)",
            ],
            market_reach_summary=f"Consistent local community demand in {loc_clean} across standard micro-enterprise lines.",
            is_demo_data=True,
        )

        opportunities = OpportunityAnalysis(
            high_growth_segments=[
                "Convenient doorstep delivery and localized repair services",
                "Modern quality packaged offerings with transparent billing",
            ],
            unmet_local_needs=[
                "Dependable after-sales service and warranty support",
                "Digital transaction enablement in semi-rural hamlets",
            ],
            ecosystem_growth_drivers=[
                "Expanding rural electrification and high-speed mobile internet penetration",
                "State government priority lending for backward district enterprises",
            ],
            is_demo_data=True,
        )

        swot = SWOTAnalysis(
            strengths=["Low fixed facility cost", "Familiarity with local language, trust, and community needs"],
            weaknesses=["Limited initial inventory depth", "Single-point owner dependency"],
            opportunities=["Expanding radius into neighboring villages", "Adding allied micro-services"],
            threats=["Price undercutting by established town wholesalers", "Seasonal agrarian income volatility"],
            is_demo_data=True,
        )

        risks = [
            RiskItem(
                risk_title="Working Capital Squeeze",
                severity="High",
                category="Financial",
                mitigation_strategy="Maintain strict 3-month operating contingency reserve as calculated by UdyamSaarthi.",
            ),
            RiskItem(
                risk_title="Supply Chain Transport Disruptions",
                severity="Medium",
                category="Logistics",
                mitigation_strategy="Identify at least 2 alternate suppliers within a 40 km radius.",
            ),
        ]

        competitors = [
            CompetitorItem(
                name="Regional Taluka Traders",
                type_of_business="General Merchant",
                proximity="2.0 km",
                strengths="Bulk capital and deep established vendor networks",
                differentiation_strategy="Provide customized prompt service, transparent digital receipts, and higher reliability.",
            )
        ]

        pricing = PricingGuidance(
            benchmark_product_or_service="Standard Service / Retail Package Unit",
            estimated_unit_production_cost="₹100 baseline cost",
            suggested_retail_price="₹145 - ₹160",
            target_gross_margin_percent=35.0,
            pricing_strategy_notes="Ensure price parity with nearest town while highlighting time and fuel savings for village buyers.",
            is_demo_data=True,
        )

        recommendation = BusinessRecommendation(
            feasibility_score=82,
            feasibility_rating="Moderately Feasible",
            summary=f"Viable micro-venture in {loc_clean} with solid local demand fundamentals when backed by scheme-linked capital.",
            first_90_days_milestones=[
                "Days 1-30: Legal incorporation, bank account opening, and premises setup.",
                "Days 31-60: Equipment installation, vendor sourcing, and initial local marketing.",
                "Days 61-90: Regular operations, customer feedback loops, and cash flow stabilization.",
            ],
            mandatory_licenses_and_registrations=[
                "Udyam MSME Registration",
                "Local Panchayat / Municipal Trade License",
                "Applicable Sectoral Safety / Tax Registration",
            ],
            digital_enablement_tips=[
                "Setup UPI QR payment soundbox.",
                "Maintain digital customer ledgers and automated SMS receipts.",
            ],
            is_demo_data=True,
        )

    return {
        "market": market,
        "opportunities": opportunities,
        "swot": swot,
        "risks": risks,
        "competitors": competitors,
        "pricing": pricing,
        "recommendation": recommendation,
    }
