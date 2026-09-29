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

