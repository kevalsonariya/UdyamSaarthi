import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data.data_provider import get_data_provider, LocalJsonDataProvider, BaseDataProvider
from app.engines.business_analysis_engine import (
    analyze_business_profile,
    validate_business_inputs,
    BusinessAnalysisValidationError,
)

client = TestClient(app)


# ==============================================================================
# 1. CATEGORY SUPPORT TESTS (All 7 required categories)
# ==============================================================================

@pytest.mark.parametrize("category_name", [
    "Textile & Clothing",
    "Dairy",
    "Grocery",
    "Food Processing",
    "Agriculture",
    "Handicrafts",
    "Services",
])
def test_all_seven_supported_categories(category_name):
    """Verify that each required category produces a complete, structured analysis."""
    result = analyze_business_profile(
        location="Anand, Gujarat",
        business_category=category_name,
        available_capital=50000.0,
    )

    assert result["business"]["category_name"] == category_name
    assert result["business"]["typical_capex_range"] != ""
    assert len(result["business"]["primary_activities"]) > 0
    assert len(result["business"]["key_equipment"]) > 0

    assert result["market"].catchment_radius_km > 0
    assert result["market"].estimated_target_population > 0
    assert len(result["market"].primary_customer_segments) > 0
    assert len(result["market"].high_demand_local_channels) > 0

    assert len(result["opportunities"].high_growth_segments) > 0
    assert len(result["opportunities"].unmet_local_needs) > 0

    assert len(result["swot"].strengths) > 0
    assert len(result["swot"].weaknesses) > 0
    assert len(result["swot"].opportunities) > 0
    assert len(result["swot"].threats) > 0

    assert len(result["risks"]) >= 2
    assert len(result["competitors"]) >= 1

    assert result["pricing"].benchmark_product_or_service != ""
    assert result["pricing"].target_gross_margin_percent > 0

    assert result["recommendation"].feasibility_score > 0
    assert len(result["recommendation"].first_90_days_milestones) > 0
    assert len(result["recommendation"].mandatory_licenses_and_registrations) > 0


@pytest.mark.parametrize("alias_input,expected_canonical", [
    ("textile", "Textile & Clothing"),
    ("garment", "Textile & Clothing"),
    ("milk collection", "Dairy"),
    ("kirana store", "Grocery"),
    ("bakery", "Food Processing"),
    ("organic farming", "Agriculture"),
    ("pottery", "Handicrafts"),
    ("automotive repair", "Services"),
])
def test_category_alias_normalization(alias_input, expected_canonical):
    """Verify flexible user alias matching resolves to standard category canonical names."""
    provider = get_data_provider()
    resolved = provider.resolve_category(alias_input)
    assert resolved is not None
    assert resolved["name"] == expected_canonical


# ==============================================================================
# 2. DYNAMIC ANALYSIS & INPUT ADAPTATION TESTS
# ==============================================================================

def test_dynamic_location_influence():
    """Verify that location influences market population, channels, and summary."""
    anand_analysis = analyze_business_profile(
        location="Anand, Gujarat",
        business_category="Dairy",
        available_capital=100000.0,
    )
    kutch_analysis = analyze_business_profile(
        location="Kutch, Gujarat",
        business_category="Dairy",
        available_capital=100000.0,
    )

    # Market summary reflects location
    assert "Anand, Gujarat" in anand_analysis["market"].market_reach_summary
    assert "Kutch, Gujarat" in kutch_analysis["market"].market_reach_summary
    assert anand_analysis["market"].market_reach_summary != kutch_analysis["market"].market_reach_summary


def test_dynamic_capital_influence_on_feasibility_and_pricing():
    """Verify that different available capital values adjust feasibility scores, ratings, and strategies."""
    lean_analysis = analyze_business_profile(
        location="Anand, Gujarat",
        business_category="Dairy",
        available_capital=5000.0,  # Produces project cost ₹50k, below typical Dairy min capex ₹75k
    )
    strong_analysis = analyze_business_profile(
        location="Anand, Gujarat",
        business_category="Dairy",
        available_capital=300000.0,  # Well-capitalized
    )

    assert lean_analysis["recommendation"].feasibility_score < strong_analysis["recommendation"].feasibility_score
    assert "Capital Constrained" in lean_analysis["recommendation"].feasibility_rating
    assert "Well Capitalized" in strong_analysis["recommendation"].feasibility_rating
    assert lean_analysis["business"]["capital_adequacy"] == "Lean"
    assert strong_analysis["business"]["capital_adequacy"] == "Optimal"
    assert lean_analysis["pricing"].pricing_strategy_notes != strong_analysis["pricing"].pricing_strategy_notes


def test_different_categories_produce_different_results():
    """Verify that distinct business categories produce completely differentiated analyses."""
    textile = analyze_business_profile("Anand, Gujarat", "Textile & Clothing", 100000.0)
    services = analyze_business_profile("Anand, Gujarat", "Services", 100000.0)

    assert textile["pricing"].benchmark_product_or_service != services["pricing"].benchmark_product_or_service
    assert textile["business"]["key_equipment"] != services["business"]["key_equipment"]
    assert textile["swot"].strengths != services["swot"].strengths
    assert textile["competitors"][0].name != services["competitors"][0].name


# ==============================================================================
# 3. DEMO DATA TRANSPARENCY TESTS
# ==============================================================================

def test_demo_data_transparency_flags():
    """Verify that the engine explicitly marks all output as prototype demo data, not live."""
    analysis = analyze_business_profile(
        location="Anand, Gujarat",
        business_category="Textile & Clothing",
        available_capital=100000.0,
    )

    meta = analysis["metadata"]
    assert meta["data_source"] == "prototype_demo_data"
    assert meta["is_live_data"] is False
    assert "Prototype demo" in meta["note"]

    # Component level demo flags
    assert analysis["market"].is_demo_data is True
    assert analysis["opportunities"].is_demo_data is True
    assert analysis["swot"].is_demo_data is True
    assert analysis["pricing"].is_demo_data is True
    assert analysis["recommendation"].is_demo_data is True


# ==============================================================================
# 4. VALIDATION TESTS (Input Edge Cases & Invalid Values)
# ==============================================================================

def test_empty_location_rejected():
    """Empty or whitespace-only location must raise BusinessAnalysisValidationError."""
    with pytest.raises(BusinessAnalysisValidationError) as exc1:
        validate_business_inputs(location="", business_category="Dairy", available_capital=10000.0)
    assert exc1.value.code == "EMPTY_LOCATION"

    with pytest.raises(BusinessAnalysisValidationError) as exc2:
        validate_business_inputs(location="   ", business_category="Dairy", available_capital=10000.0)
    assert exc2.value.code == "EMPTY_LOCATION"

    with pytest.raises(BusinessAnalysisValidationError) as exc3:
        validate_business_inputs(location=None, business_category="Dairy", available_capital=10000.0)
    assert exc3.value.code == "MISSING_LOCATION"


def test_empty_category_rejected():
    """Empty or missing category must raise BusinessAnalysisValidationError."""
    with pytest.raises(BusinessAnalysisValidationError) as exc1:
        validate_business_inputs(location="Anand", business_category="", available_capital=10000.0)
    assert exc1.value.code == "EMPTY_CATEGORY"

    with pytest.raises(BusinessAnalysisValidationError) as exc2:
        validate_business_inputs(location="Anand", business_category=None, available_capital=10000.0)
    assert exc2.value.code == "MISSING_CATEGORY"


def test_unsupported_category_rejected():
    """Unsupported business category must raise BusinessAnalysisValidationError with supported list."""
    with pytest.raises(BusinessAnalysisValidationError) as exc:
        validate_business_inputs(location="Anand", business_category="Cryptocurrency Mining", available_capital=10000.0)
    assert exc.value.code == "UNSUPPORTED_CATEGORY"
    assert "Textile & Clothing" in str(exc.value)
    assert "Dairy" in str(exc.value)


def test_zero_capital_rejected():
    """Zero capital must raise BusinessAnalysisValidationError."""
    with pytest.raises(BusinessAnalysisValidationError) as exc:
        validate_business_inputs(location="Anand", business_category="Dairy", available_capital=0)
    assert exc.value.code == "ZERO_CAPITAL"


def test_negative_capital_rejected():
    """Negative capital must raise BusinessAnalysisValidationError."""
    with pytest.raises(BusinessAnalysisValidationError) as exc:
        validate_business_inputs(location="Anand", business_category="Dairy", available_capital=-5000.0)
    assert exc.value.code == "NEGATIVE_CAPITAL"


def test_non_numeric_capital_rejected():
    """Non-numeric string and boolean capital must raise BusinessAnalysisValidationError."""
    with pytest.raises(BusinessAnalysisValidationError) as exc_str:
        validate_business_inputs(location="Anand", business_category="Dairy", available_capital="five_thousand")
    assert exc_str.value.code == "NON_NUMERIC"

    with pytest.raises(BusinessAnalysisValidationError) as exc_bool:
        validate_business_inputs(location="Anand", business_category="Dairy", available_capital=True)
    assert exc_bool.value.code == "NON_NUMERIC"

    with pytest.raises(BusinessAnalysisValidationError) as exc_none:
        validate_business_inputs(location="Anand", business_category="Dairy", available_capital=None)
    assert exc_none.value.code == "MISSING_CAPITAL"


def test_excessive_capital_rejected():
    """Capital > ₹5 Lakh (which produces project cost > ₹50 Lakh) must be rejected."""
    with pytest.raises(BusinessAnalysisValidationError) as exc:
        validate_business_inputs(location="Anand", business_category="Dairy", available_capital=600000.0)
    assert exc.value.code == "EXCEEDS_MAX_CAPITAL"


# ==============================================================================
# 5. FASTAPI ENDPOINT TESTS: POST /business/analyze
# ==============================================================================

def test_api_business_analyze_valid():
    """Test successful POST /business/analyze execution."""
    payload = {
        "location": "Anand, Gujarat",
        "business_category": "Textile & Clothing",
        "available_capital": 100000.0,
    }
    response = client.post("/business/analyze", json=payload)
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["success"] is True
    assert "data" in json_data
    assert "metadata" in json_data

    # Check transparency in metadata
    assert json_data["metadata"]["data_source"] == "prototype_demo_data"
    assert json_data["metadata"]["is_live_data"] is False

    # Check all required analysis sections
    data = json_data["data"]
    assert "business" in data
    assert "market" in data
    assert "opportunities" in data
    assert "swot" in data
    assert "risks" in data
    assert "competitors" in data
    assert "pricing" in data
    assert "recommendation" in data

    # Check financial coordination
    assert data["financial"]["project_cost"] == 1000000.0
    assert data["scheme"]["scheme_name"] == "Term Loan Scheme"


def test_api_business_analyze_empty_location():
    """Test POST /business/analyze with empty location -> 400 error."""
    payload = {
        "location": "   ",
        "business_category": "Dairy",
        "available_capital": 50000.0,
    }
    response = client.post("/business/analyze", json=payload)
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "EMPTY_LOCATION"


def test_api_business_analyze_unsupported_category():
    """Test POST /business/analyze with unsupported category -> 400 error."""
    payload = {
        "location": "Anand, Gujarat",
        "business_category": "Nuclear Energy",
        "available_capital": 50000.0,
    }
    response = client.post("/business/analyze", json=payload)
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "UNSUPPORTED_CATEGORY"


def test_api_business_analyze_zero_capital():
    """Test POST /business/analyze with zero capital -> 400 error."""
    payload = {
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 0,
    }
    response = client.post("/business/analyze", json=payload)
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "ZERO_CAPITAL"


def test_api_business_analyze_negative_capital():
    """Test POST /business/analyze with negative capital -> 400 error."""
    payload = {
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": -1000,
    }
    response = client.post("/business/analyze", json=payload)
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "NEGATIVE_CAPITAL"


# ==============================================================================
# 6. MODULARITY & DATA PROVIDER ISOLATION TESTS
# ==============================================================================

def test_data_provider_implements_interface():
    """Verify that LocalJsonDataProvider properly implements BaseDataProvider."""
    provider = get_data_provider()
    assert isinstance(provider, BaseDataProvider)
    categories = provider.get_supported_categories()
    assert len(categories) >= 7
    assert "Textile & Clothing" in categories
    assert "Dairy" in categories
    assert "Services" in categories
