"""
Phase B8 — Dynamic Local Business Intelligence Test Suite
Verifies:
1. Category-driven dynamic intelligence (pricing, opportunities, SWOT, competitors, equipment)
2. Location-driven dynamic intelligence (town, district, state adaptation, reach, local factors)
3. Capital-driven dynamic intelligence (adequacy, feasibility score, strategy notes, scale opportunities)
4. Structured Opportunity item schema (title, type, description, reason, local_factor)
5. API contract integration on POST /business/analyze
6. Demo/indicative data transparency markers
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.local_intelligence_service import LocalIntelligenceService
from app.engines.business_analysis_engine import analyze_business_profile
from app.schemas.schemas import OpportunityItem

client = TestClient(app)


# ==============================================================================
# 1. CATEGORY DIFFERENTIATION TESTS
# ==============================================================================

@pytest.mark.parametrize("category_a,category_b", [
    ("Dairy", "Poultry"),
    ("Textile & Clothing", "Food Processing"),
    ("Grocery / Kirana", "Agriculture"),
    ("Handicrafts", "Services"),
])
def test_category_differentiates_intelligence(category_a, category_b):
    """Different categories must yield completely distinct products, pricing, and competitors."""
    res_a = LocalIntelligenceService.generate_complete_intelligence("Anand, Gujarat", category_a, 75000.0)
    res_b = LocalIntelligenceService.generate_complete_intelligence("Anand, Gujarat", category_b, 75000.0)

    # Business profile
    assert res_a["business"]["category_name"] != res_b["business"]["category_name"]
    assert res_a["business"]["key_equipment"] != res_b["business"]["key_equipment"]
    assert res_a["business"]["primary_activities"] != res_b["business"]["primary_activities"]

    # Pricing guidance
    assert res_a["pricing"].benchmark_product_or_service != res_b["pricing"].benchmark_product_or_service
    assert res_a["pricing"].suggested_retail_price != res_b["pricing"].suggested_retail_price

    # Competitors
    assert res_a["competitors"][0].name != res_b["competitors"][0].name

    # SWOT
    assert res_a["swot"].strengths != res_b["swot"].strengths


# ==============================================================================
# 2. LOCATION DIFFERENTIATION TESTS
# ==============================================================================

def test_location_differentiates_intelligence():
    """Different locations must dynamically adjust market reach, local factors, and competitors."""
    anand = LocalIntelligenceService.generate_complete_intelligence("Anand, Gujarat", "Dairy", 80000.0)
    baramati = LocalIntelligenceService.generate_complete_intelligence("Baramati, Maharashtra", "Dairy", 80000.0)

    # Market summary mentions specific territory
    assert "Anand, Gujarat" in anand["market"].market_reach_summary
    assert "Baramati, Maharashtra" in baramati["market"].market_reach_summary
    assert anand["market"].market_reach_summary != baramati["market"].market_reach_summary

    # Competitor proximity/names adapt to location
    assert "Anand" in anand["competitors"][0].name or "Anand" in anand["competitors"][0].proximity
    assert "Baramati" in baramati["competitors"][0].name or "Baramati" in baramati["competitors"][0].proximity

    # Opportunities local factors reflect location
    assert "Anand" in anand["opportunities"].items[0].local_factor
    assert "Baramati" in baramati["opportunities"].items[0].local_factor


# ==============================================================================
# 3. CAPITAL DIFFERENTIATION TESTS
# ==============================================================================

def test_capital_differentiation():
    """Capital adjustments must alter feasibility rating, adequacy, and scale opportunities."""
    lean = LocalIntelligenceService.generate_complete_intelligence("Anand, Gujarat", "Dairy", 5000.0)
    optimal = LocalIntelligenceService.generate_complete_intelligence("Anand, Gujarat", "Dairy", 250000.0)

    # Feasibility score and ratings
    assert lean["recommendation"].feasibility_score < optimal["recommendation"].feasibility_score
    assert "Capital Constrained" in lean["recommendation"].feasibility_rating
    assert "Well Capitalized" in optimal["recommendation"].feasibility_rating

    # Adequacy
    assert lean["business"]["capital_adequacy"] == "Lean"
    assert optimal["business"]["capital_adequacy"] == "Optimal"

    # Pricing strategy note adapts
    assert "Low-capital entry strategy" in lean["pricing"].pricing_strategy_notes
    assert "Well-capitalized strategy" in optimal["pricing"].pricing_strategy_notes

    # Well capitalized enterprise gains a scale/customer segment opportunity
    assert len(optimal["opportunities"].items) >= len(lean["opportunities"].items)


# ==============================================================================
# 4. STRUCTURED OPPORTUNITY FIELDS (MANDATORY B8)
# ==============================================================================

def test_structured_opportunity_items():
    """Every opportunity must contain title, type, description, reason, and local_factor."""
    res = LocalIntelligenceService.generate_complete_intelligence("Anand, Gujarat", "Dairy", 60000.0)
    opps = res["opportunities"]

    assert len(opps.items) >= 4

    valid_types = {
        "High Growth",
        "Unmet Need",
        "Ecosystem Driver",
        "Seasonal Opportunity",
        "Customer Segment Opportunity",
        "Channel Opportunity",
    }

    for item in opps.items:
        assert isinstance(item, OpportunityItem)
        assert item.title.strip() != ""
        assert item.type in valid_types
        assert item.description.strip() != ""
        assert item.reason.strip() != ""
        assert item.local_factor.strip() != ""
        assert "Anand" in item.local_factor or "Gujarat" in item.local_factor


# ==============================================================================
# 5. API ENDPOINT VALIDATION (POST /business/analyze)
# ==============================================================================

def test_api_business_analyze_returns_b8_structured_opportunities():
    """POST /business/analyze returns structured opportunity items and dynamic intelligence."""
    response = client.post("/business/analyze", json={
        "location": "Mehsana, Gujarat",
        "business_category": "Poultry",
        "available_capital": 50000.0,
    })
    assert response.status_code == 200
    data = response.json()["data"]

    # Opportunities structured items
    opps = data["opportunities"]
    assert "items" in opps
    assert len(opps["items"]) >= 4
    first_opp = opps["items"][0]
    assert "title" in first_opp
    assert "type" in first_opp
    assert "description" in first_opp
    assert "reason" in first_opp
    assert "local_factor" in first_opp

    # Pricing adapts to Poultry
    assert "bird" in data["pricing"]["suggested_retail_price"].lower() or "egg" in data["pricing"]["benchmark_product_or_service"].lower() or "poultry" in data["pricing"]["benchmark_product_or_service"].lower()

    # Competitors adapt to Mehsana
    assert any("Mehsana" in c["name"] or "Mehsana" in c["proximity"] for c in data["competitors"])


# ==============================================================================
# 6. DEMO DATA TRANSPARENCY
# ==============================================================================

def test_b8_demo_data_transparency():
    """All components explicitly flag demo/indicative simulated estimates."""
    res = LocalIntelligenceService.generate_complete_intelligence("Anand, Gujarat", "Textile & Clothing", 100000.0)

    assert res["metadata"]["is_live_data"] is False
    assert res["metadata"]["data_source"] == "prototype_demo_data"
    assert res["market"].is_demo_data is True
    assert res["opportunities"].is_demo_data is True
    assert res["swot"].is_demo_data is True
    assert res["pricing"].is_demo_data is True
    assert res["recommendation"].is_demo_data is True


# ==============================================================================
# 7. PHASE B8.1 STALE STATE PREVENTION & REQUEST SYNCHRONIZATION
# ==============================================================================

def test_b8_1_consecutive_searches_isolation():
    """
    Verifies Phase B8.1 fix:
    Consecutive searches with different parameters (Dairy vs Poultry) must return
    independent atomic payloads with matching request_id, input snapshot, and isolated AI advisory.
    """
    # Search 1: Dairy in Anand with ₹1,00,000 capital
    req_1_id = "test-req-dairy-100k"
    resp_1 = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
        "request_id": req_1_id,
    })
    assert resp_1.status_code == 200
    body_1 = resp_1.json()
    data_1 = body_1["data"]

    # Request ID and input snapshot check
    assert body_1.get("request_id") == req_1_id
    assert data_1.get("request_id") == req_1_id
    assert data_1["input"]["business_category"] == "Dairy"
    assert data_1["input"]["available_capital"] == 100000.0
    assert data_1["input"]["location"] == "Anand, Gujarat"

    # Financial sizing for ₹1,00,000 capital: Project cost = ₹10,00,000, Max loan = ₹9,00,000
    assert data_1["financial"]["project_cost"] == 1000000.0
    assert data_1["financial"]["max_loan_amount"] == 900000.0

    # AI Advisory for Dairy
    ai_1 = data_1["ai_explanation"]
    assert "dairy" in ai_1["summary"].lower()
    assert "poultry" not in ai_1["summary"].lower()

    # Search 2: Poultry in Anand with ₹75,000 capital
    req_2_id = "test-req-poultry-75k"
    resp_2 = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Poultry",
        "available_capital": 75000.0,
        "language": "en",
        "request_id": req_2_id,
    })
    assert resp_2.status_code == 200
    body_2 = resp_2.json()
    data_2 = body_2["data"]

    # Request ID and input snapshot check
    assert body_2.get("request_id") == req_2_id
    assert data_2.get("request_id") == req_2_id
    assert data_2["input"]["business_category"] == "Poultry"
    assert data_2["input"]["available_capital"] == 75000.0
    assert data_2["input"]["location"] == "Anand, Gujarat"

    # Financial sizing for ₹75,000 capital: Project cost = ₹7,50,000, Max loan = ₹6,75,000
    assert data_2["financial"]["project_cost"] == 750000.0
    assert data_2["financial"]["max_loan_amount"] == 675000.0

    # AI Advisory for Poultry - must NOT contain stale Dairy content
    ai_2 = data_2["ai_explanation"]
    assert "poultry" in ai_2["summary"].lower()
    assert "dairy" not in ai_2["summary"].lower()

    # Competitor mapping and business profile isolation
    assert data_1["business"]["category_name"] == "Dairy"
    assert data_2["business"]["category_name"] == "Poultry"
    assert data_1["pricing"]["suggested_retail_price"] != data_2["pricing"]["suggested_retail_price"]


def test_b8_1_language_synchronization():
    """Verifies that language switches carry properly through input metadata."""
    req_id = "test-req-lang-hi"
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "hi",
        "request_id": req_id,
    })
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["input"]["language"] == "hi"
    assert data["request_id"] == req_id


# ==============================================================================
# 8. MANDATORY 7 B8 MATRIX TESTS (REQUIREMENT 18)
# ==============================================================================

@pytest.mark.parametrize("location,category,capital", [
    ("Anand, Gujarat", "Textile & Clothing", 100000.0),    # TEST 1
    ("Anand, Gujarat", "Dairy", 100000.0),                 # TEST 2
    ("Anand, Gujarat", "Poultry", 75000.0),                # TEST 3
    ("Anand, Gujarat", "Grocery / Kirana", 50000.0),       # TEST 4
    ("Anand, Gujarat", "Agriculture", 60000.0),            # TEST 5
    ("Mehsana, Gujarat", "Dairy", 100000.0),               # TEST 6
    ("Ahmedabad, Gujarat", "Textile & Clothing", 150000.0),# TEST 7
])
def test_b8_mandatory_matrix_endpoints(location, category, capital):
    """
    Verifies that all 7 required scenarios execute successfully and generate
    category-specific, location-aware, and deterministic financial outputs.
    """
    resp = client.post("/business/analyze", json={
        "location": location,
        "business_category": category,
        "available_capital": capital,
        "language": "en",
    })
    assert resp.status_code == 200
    res = resp.json()["data"]

    # 1. Financial values must strictly adhere to deterministic rules
    expected_project_cost = capital / 0.10
    expected_loan = expected_project_cost * 0.90
    assert res["financial"]["project_cost"] == expected_project_cost
    assert res["financial"]["max_loan_amount"] == expected_loan
    assert res["scheme"]["eligible_funding"] == expected_loan

    # 2. Location-aware output
    town = location.split(",")[0].strip()
    assert town in res["market"]["market_reach_summary"] or town in res["recommendation"]["summary"]

    # 3. Category-specific opportunities, SWOT, risks, pricing
    opps = res["opportunities"]
    assert len(opps["items"]) >= 3
    assert len(res["swot"]["strengths"]) >= 3
    assert len(res["risks"]) >= 3
    assert res["pricing"]["suggested_retail_price"] != ""
    assert res["pricing"]["benchmark_product_or_service"] != ""

    # 4. Recommendation and AI Explanation exist
    assert res["recommendation"]["feasibility_score"] >= 50
    assert res["recommendation"]["summary"] != ""
    assert res["ai_explanation"]["summary"] != ""
    assert res["ai_explanation"]["market_insight"] != ""


# ==============================================================================
# 9. CROSS-CATEGORY DIFFERENTIATION (REQUIREMENT 18)
# ==============================================================================

def test_b8_cross_category_distinctness():
    """Dairy, Poultry, and Grocery must produce materially distinct business intelligence."""
    r_dairy = client.post("/business/analyze", json={
        "location": "Anand, Gujarat", "business_category": "Dairy", "available_capital": 80000.0,
    }).json()["data"]

    r_poultry = client.post("/business/analyze", json={
        "location": "Anand, Gujarat", "business_category": "Poultry", "available_capital": 80000.0,
    }).json()["data"]

    r_grocery = client.post("/business/analyze", json={
        "location": "Anand, Gujarat", "business_category": "Grocery / Kirana", "available_capital": 80000.0,
    }).json()["data"]

    # Pricing benchmark distinctness
    assert r_dairy["pricing"]["benchmark_product_or_service"] != r_poultry["pricing"]["benchmark_product_or_service"]
    assert r_poultry["pricing"]["benchmark_product_or_service"] != r_grocery["pricing"]["benchmark_product_or_service"]

    # Retail price distinctness
    assert r_dairy["pricing"]["suggested_retail_price"] != r_poultry["pricing"]["suggested_retail_price"]
    assert r_poultry["pricing"]["suggested_retail_price"] != r_grocery["pricing"]["suggested_retail_price"]

    # Equipment distinctness
    assert r_dairy["business"]["key_equipment"] != r_poultry["business"]["key_equipment"]
    assert r_poultry["business"]["key_equipment"] != r_grocery["business"]["key_equipment"]

    # Opportunities distinctness
    assert r_dairy["opportunities"]["items"][0]["title"] != r_poultry["opportunities"]["items"][0]["title"]



# ==============================================================================
# 10. LOCATION-AWARE DIFFERENTIATION (REQUIREMENT 25)
# ==============================================================================

def test_b8_location_differentiation_anand_vs_mehsana():
    """Anand + Dairy vs Mehsana + Dairy must produce distinct territory narratives and demographics."""
    r_anand = client.post("/business/analyze", json={
        "location": "Anand, Gujarat", "business_category": "Dairy", "available_capital": 100000.0,
    }).json()["data"]

    r_mehsana = client.post("/business/analyze", json={
        "location": "Mehsana, Gujarat", "business_category": "Dairy", "available_capital": 100000.0,
    }).json()["data"]

    # Market narrative reflects specific town
    assert "Anand" in r_anand["market"]["market_reach_summary"]
    assert "Mehsana" in r_mehsana["market"]["market_reach_summary"]
    assert r_anand["market"]["market_reach_summary"] != r_mehsana["market"]["market_reach_summary"]

    # Competitor mapping adapts
    assert any("Anand" in c["name"] or "Anand" in c["proximity"] for c in r_anand["competitors"])
    assert any("Mehsana" in c["name"] or "Mehsana" in c["proximity"] for c in r_mehsana["competitors"])

    # Demographics differ due to district economic profiles
    assert r_anand["market"]["estimated_target_population"] != r_mehsana["market"]["estimated_target_population"]


# ==============================================================================
# 11. MULTILINGUAL CONTENT GENERATION (REQUIREMENT 26)
# ==============================================================================

def test_b8_multilingual_intelligence_generation():
    """
    Verifies that English, Hindi, and Gujarati requests generate localized
    market, opportunities, SWOT, risks, recommendation, and AI advisory text,
    while leaving deterministic financial numbers strictly identical.
    """
    params = {"location": "Anand, Gujarat", "business_category": "Poultry", "available_capital": 75000.0}

    r_en = client.post("/business/analyze", json={**params, "language": "en"}).json()["data"]
    r_hi = client.post("/business/analyze", json={**params, "language": "hi"}).json()["data"]
    r_gu = client.post("/business/analyze", json={**params, "language": "gu"}).json()["data"]

    # 1. Deterministic financial metrics are strictly invariant across languages
    for res in [r_en, r_hi, r_gu]:
        assert res["financial"]["project_cost"] == 750000.0
        assert res["financial"]["max_loan_amount"] == 675000.0
        assert res["scheme"]["interest_rate_percent"] == 8.0

    # 2. Market Reach is localized
    assert "Within the" in r_en["market"]["market_reach_summary"]
    assert "वाणिज्यिक क्षेत्र" in r_hi["market"]["market_reach_summary"]
    assert "વ્યાપારી ક્ષેત્ર" in r_gu["market"]["market_reach_summary"]

    # 3. Opportunities are localized
    assert "Rapidly growing" in r_en["opportunities"]["items"][0]["description"]
    assert "बढ़ती मांग" in r_hi["opportunities"]["items"][0]["description"]
    assert "વધતી માંગ" in r_gu["opportunities"]["items"][0]["description"]


    # 4. SWOT is localized
    assert "✓" not in r_en["swot"]["strengths"][0]  # raw text
    assert "સ્થાનિક" in r_gu["swot"]["strengths"][0] or "પરિવારો" in r_gu["swot"]["strengths"][0]
    assert "स्थानीय" in r_hi["swot"]["strengths"][0] or "परिवारों" in r_hi["swot"]["strengths"][0]

    # 5. Risks are localized
    assert "Seasonal" in r_en["risks"][0]["risk_title"]
    assert "मौसमी" in r_hi["risks"][0]["risk_title"]
    assert "મોસમી" in r_gu["risks"][0]["risk_title"]

    # 6. Recommendation is localized
    assert "Feasible" in r_en["recommendation"]["feasibility_rating"]
    assert "व्यवहार्य" in r_hi["recommendation"]["feasibility_rating"]
    assert "અનુકૂળ" in r_gu["recommendation"]["feasibility_rating"]

    # 7. AI Explanation is localized
    assert r_en["ai_explanation"]["summary"] != r_hi["ai_explanation"]["summary"]
    assert r_hi["ai_explanation"]["summary"] != r_gu["ai_explanation"]["summary"]
    assert "उद्यम" in r_hi["ai_explanation"]["summary"] or "ऋण" in r_hi["ai_explanation"]["summary"]
    assert "સાહસ" in r_gu["ai_explanation"]["summary"] or "લોન" in r_gu["ai_explanation"]["summary"]


# ==============================================================================
# 12. PHASE B8.2 DEMO DATA TRANSPARENCY & HARDENING
# ==============================================================================

def test_b8_2_competitor_transparency_and_metadata():
    """Verify competitor profiles are clearly labeled as demo data with B9 disclaimer and generic names."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code == 200
    data = resp.json()["data"]

    competitors = data["competitors"]
    assert len(competitors) >= 3

    for comp in competitors:
        # A. Competitor profiles have is_demo_data = true
        assert comp.get("is_demo_data") is True
        # Transparent data source
        assert comp.get("data_source") == "Indicative category-location profile"
        # No fake coordinates or fake map links; clear B9 notice
        assert "planned for Phase B9" in comp.get("location_status", "")
        # No fabricated real-world brand names such as "Anand Amul"
        assert "amul" not in comp.get("name", "").lower()


def test_b8_2_market_catchment_and_pricing_transparency():
    """Verify market catchment and pricing have is_estimate=True and indicative data sources."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Poultry",
        "available_capital": 75000.0,
        "language": "en",
    })
    assert resp.status_code == 200
    data = resp.json()["data"]

    market = data["market"]
    assert market.get("is_estimate") is True
    assert market.get("data_source") == "Prototype heuristic"

    pricing = data["pricing"]
    assert pricing.get("is_estimate") is True
    assert pricing.get("data_source") == "Prototype category benchmark"

    # Financial engine invariants remain untouched
    assert data["financial"]["project_cost"] == 750000.0
    assert data["financial"]["max_loan_amount"] == 675000.0


def test_b8_2_dairy_to_poultry_strict_regression():
    """
    Search 1: Anand, Dairy, ₹1,00,000
    Search 2: Anand, Poultry, ₹75,000
    Verify Search 2 contains Poultry intelligence, ₹7,50,000 cost, ₹6,75,000 loan, and 0 stale Dairy references.
    """
    req_1_id = "b82-search1-dairy"
    resp_1 = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
        "request_id": req_1_id,
    })
    assert resp_1.status_code == 200
    data_1 = resp_1.json()["data"]
    assert data_1["financial"]["project_cost"] == 1000000.0
    assert data_1["financial"]["max_loan_amount"] == 900000.0
    assert "dairy" in data_1["business"]["category_name"].lower()

    req_2_id = "b82-search2-poultry"
    resp_2 = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Poultry",
        "available_capital": 75000.0,
        "language": "en",
        "request_id": req_2_id,
    })
    assert resp_2.status_code == 200
    data_2 = resp_2.json()["data"]

    # Verify Search 2 financials
    assert data_2["financial"]["project_cost"] == 750000.0
    assert data_2["financial"]["max_loan_amount"] == 675000.0
    assert data_2["business"]["category_name"] == "Poultry"

    # AI Advisory must contain 0 stale Dairy references
    ai_summary = data_2["ai_explanation"]["summary"].lower()
    ai_market = data_2["ai_explanation"]["market_insight"].lower()
    assert "poultry" in ai_summary
    assert "dairy" not in ai_summary
    assert "dairy" not in ai_market

    # Opportunities must contain 0 stale Dairy references
    opp_titles = [item["title"].lower() for item in data_2["opportunities"]["items"]]
    assert not any("milk" in t or "dairy" in t for t in opp_titles)



