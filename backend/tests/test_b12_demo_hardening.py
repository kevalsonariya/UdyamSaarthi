"""
Phase B12 — Final UdyamSaarthi SIH Demo Hardening
Comprehensive verification suite covering:
- Full location × category × language matrix
- Financial boundary regression
- Error handling
- Competitor regression
- PDF generation
- Security checks
"""
import re
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ============================================================
# 1. LOCATION TEST MATRIX
# ============================================================

@pytest.mark.parametrize("location", [
    "Anand, Gujarat",
    "Ahmedabad, Gujarat",
    "Mehsana, Gujarat",
])
def test_b12_location_matrix(location):
    """All 3 demo locations return valid analysis."""
    resp = client.post("/business/analyze", json={
        "location": location,
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code == 200, f"Failed for {location}: {resp.text}"
    d = resp.json()
    assert d["success"] is True
    assert d["data"]["financial"]["project_cost"] > 0
    assert len(d["data"]["swot"]["strengths"]) > 0


# ============================================================
# 2. BUSINESS CATEGORY TEST MATRIX
# ============================================================

ALL_CATEGORIES = [
    "Textile & Clothing",
    "Dairy",
    "Grocery",
    "Agriculture",
    "Food Processing",
    "Handicrafts",
    "Services",
    "Poultry",
    "Textile",
    "Kirana",
]

@pytest.mark.parametrize("category", ALL_CATEGORIES)
def test_b12_category_matrix(category):
    """Every supported category returns a complete analysis."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": category,
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code in (200, 400), f"Unexpected status for {category}"
    if resp.status_code == 200:
        d = resp.json()["data"]
        assert d["financial"]["project_cost"] > 0
        assert len(d["opportunities"]["items"]) > 0
        assert len(d["swot"]["strengths"]) > 0
        assert len(d["risks"]) > 0


# ============================================================
# 3. LANGUAGE TEST MATRIX — Full flow
# ============================================================

DEVANAGARI = re.compile(r'[\u0900-\u097F]')
GUJARATI_RE = re.compile(r'[\u0A80-\u0AFF]')


@pytest.mark.parametrize("lang,regex", [
    ("hi", DEVANAGARI),
    ("gu", GUJARATI_RE),
])
def test_b12_language_flow_complete(lang, regex):
    """Full analysis flow in Hindi and Gujarati returns localized content."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": lang,
    })
    assert resp.status_code == 200
    d = resp.json()["data"]
    # Dynamic content localized
    assert regex.search(d["market"]["market_reach_summary"]) is not None
    assert regex.search(d["swot"]["strengths"][0]) is not None
    assert regex.search(d["opportunities"]["items"][0]["description"]) is not None
    assert regex.search(d["risks"][0]["mitigation_strategy"]) is not None
    assert regex.search(d["competitors"][0]["name"]) is not None
    assert regex.search(d["pricing"]["benchmark_product_or_service"]) is not None
    assert regex.search(d["recommendation"]["feasibility_rating"]) is not None
    assert regex.search(d["ai_explanation"]["summary"]) is not None


def test_b12_language_pdf_all_three():
    """PDF endpoint produces valid PDFs for en, hi, gu."""
    for lang, tag in [("en", "EN"), ("hi", "HI"), ("gu", "GU")]:
        resp = client.post("/report/generate", json={
            "location": "Anand, Gujarat",
            "business_category": "Dairy",
            "available_capital": 100000.0,
            "language": lang,
        })
        assert resp.status_code == 200
        assert resp.content[:4] == b"%PDF"
        assert tag in resp.headers.get("content-disposition", "")


# ============================================================
# 4. FINANCIAL BOUNDARY REGRESSION
# ============================================================

BOUNDARY_CASES = [
    # (capital, expected_scheme_code_fragment, expected_project_cost)
    (10000.0,  "MICRO FINANCE",   100000.0),   # ₹10,000 → Micro Finance Scheme
    (14000.0,  "MICRO FINANCE",   140000.0),   # ₹14,000 → still below threshold
    (14001.0,  None,              140010.0),   # ₹14,001 → crosses threshold (scheme routing changes)
    (100000.0, None,              1000000.0),  # ₹1,00,000 → standard case
]

@pytest.mark.parametrize("capital,scheme_fragment,expected_cost", BOUNDARY_CASES)
def test_b12_financial_boundary_regression(capital, scheme_fragment, expected_cost):
    """Financial engine produces correct project_cost at boundary values."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": capital,
        "language": "en",
    })
    assert resp.status_code == 200
    d = resp.json()["data"]
    fin = d["financial"]
    # Project cost = capital / 0.10
    assert abs(fin["project_cost"] - expected_cost) < 0.01, \
        f"Project cost {fin['project_cost']} != {expected_cost} for capital={capital}"
    # Promoter contribution = capital exactly
    assert abs(fin["promoter_contribution"] - capital) < 0.01
    # Loan = 90% of project cost
    assert abs(fin["max_loan_amount"] - expected_cost * 0.9) < 0.01
    # EMI must be positive
    assert d["emi"]["monthly_emi"] > 0
    # Scheme name not empty
    assert d["scheme"]["scheme_name"] != ""
    # Check specific scheme routing if provided
    if scheme_fragment:
        assert scheme_fragment.upper() in d["scheme"]["scheme_name"].upper() or \
               scheme_fragment.upper() in d["scheme"]["scheme_code"].upper(), \
            f"Expected scheme containing '{scheme_fragment}' but got '{d['scheme']['scheme_name']}'"


def test_b12_financial_invariance_across_all_languages():
    """Financial numbers are strictly identical across en, hi, gu for boundary values."""
    for capital in [10000.0, 14000.0, 100000.0]:
        vals = {}
        for lang in ["en", "hi", "gu"]:
            resp = client.post("/business/analyze", json={
                "location": "Anand, Gujarat",
                "business_category": "Dairy",
                "available_capital": capital,
                "language": lang,
            })
            assert resp.status_code == 200
            d = resp.json()["data"]
            vals[lang] = (
                d["financial"]["project_cost"],
                d["financial"]["max_loan_amount"],
                d["emi"]["monthly_emi"],
                d["scheme"]["interest_rate_percent"],
            )
        assert vals["en"] == vals["hi"] == vals["gu"], \
            f"Financial mismatch at capital={capital}: {vals}"


# ============================================================
# 5. COMPETITOR REGRESSION
# ============================================================

def test_b12_competitors_present_for_standard_input():
    """Standard inputs always yield at least 1 competitor (demo fallback)."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code == 200
    comps = resp.json()["data"]["competitors"]
    assert len(comps) >= 1, "Expected at least 1 competitor"


def test_b12_competitors_have_required_fields():
    """Competitor items have all required fields, no fabricated coordinates."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code == 200
    comps = resp.json()["data"]["competitors"]
    for comp in comps:
        assert "name" in comp and comp["name"]
        assert "type_of_business" in comp
        assert "differentiation_strategy" in comp
        # Demo data must be flagged as such
        assert "is_demo_data" in comp
        # No fabricated GPS coordinates should be present for demo data
        if comp.get("is_demo_data"):
            assert comp.get("latitude") is None
            assert comp.get("longitude") is None


def test_b12_competitor_search_endpoint():
    """Dedicated competitor search endpoint returns valid response."""
    resp = client.post("/competitors/search", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "language": "en",
    })
    assert resp.status_code == 200
    d = resp.json()
    assert d["success"] is True
    assert "competitors" in d["data"]


# ============================================================
# 6. ERROR HANDLING
# ============================================================

def test_b12_error_empty_location():
    """Empty location returns 400, not 500."""
    resp = client.post("/business/analyze", json={
        "location": "   ",
        "business_category": "Dairy",
        "available_capital": 100000.0,
    })
    assert resp.status_code == 400
    assert resp.json()["success"] is False


def test_b12_error_missing_category():
    """Missing category returns 400."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "",
        "available_capital": 100000.0,
    })
    assert resp.status_code == 400


def test_b12_error_zero_capital():
    """Zero capital returns 400."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 0.0,
    })
    assert resp.status_code == 400


def test_b12_error_negative_capital():
    """Negative capital returns 400."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": -5000.0,
    })
    assert resp.status_code == 400


def test_b12_health_endpoint():
    """Health check returns 200 ok."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_b12_pdf_error_handling_bad_lang():
    """Bad language in PDF endpoint gracefully falls back, not 500."""
    resp = client.post("/report/generate", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "xyz",
    })
    assert resp.status_code == 200  # Falls back to English, doesn't crash
    assert resp.content[:4] == b"%PDF"


# ============================================================
# 7. SECURITY CHECKS
# ============================================================

def test_b12_security_no_secrets_in_api_responses():
    """API responses do not leak API keys or sensitive tokens."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code == 200
    text = resp.text
    # No raw API key patterns
    assert not re.search(r'AIza[0-9A-Za-z\-_]{35}', text)
    assert not re.search(r'sk-[a-zA-Z0-9]{32}', text)
    # No .env patterns
    assert "SECRET_KEY" not in text
    assert "DATABASE_URL" not in text


# ============================================================
# 8. LOCATION AUTOCOMPLETE
# ============================================================

def test_b12_location_suggest_anand():
    """Location suggest returns results for Anand."""
    resp = client.get("/locations/suggest?q=Anand")
    assert resp.status_code == 200
    d = resp.json()
    assert d["success"] is True
    assert d["total"] >= 1
    names = [s.get("village_town_city", "") or s.get("raw_input", "") for s in d["suggestions"]]
    assert any("Anand" in n for n in names), f"Anand not in suggestions: {names}"


def test_b12_location_suggest_ahmedabad():
    """Location suggest returns results for Ahmedabad."""
    resp = client.get("/locations/suggest?q=Ahmedabad")
    assert resp.status_code == 200
    d = resp.json()
    assert d["success"] is True
    assert d["total"] >= 1


def test_b12_location_suggest_empty():
    """Empty query returns list, not error."""
    resp = client.get("/locations/suggest?q=")
    assert resp.status_code == 200
    assert resp.json()["success"] is True


# ============================================================
# 9. PDF GENERATION — All 7 categories
# ============================================================

@pytest.mark.parametrize("category", [
    "Textile & Clothing", "Dairy", "Grocery",
    "Agriculture", "Food Processing", "Handicrafts", "Services"
])
def test_b12_pdf_all_seven_categories(category):
    """PDF generates successfully for all 7 official categories."""
    resp = client.post("/report/generate", json={
        "location": "Anand, Gujarat",
        "business_category": category,
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code == 200, f"PDF failed for {category}: {resp.text[:200]}"
    assert resp.content[:4] == b"%PDF"
    assert len(resp.content) > 3000


# ============================================================
# 10. BACKWARD COMPATIBILITY
# ============================================================

def test_b12_backward_compat_no_language_field():
    """Requests without language field still work (backward compat)."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
    })
    assert resp.status_code == 200
    assert resp.json()["success"] is True


def test_b12_backward_compat_pdf_no_language():
    """PDF without language field defaults to English."""
    resp = client.post("/report/generate", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
    })
    assert resp.status_code == 200
    assert resp.content[:4] == b"%PDF"
    assert "EN" in resp.headers.get("content-disposition", "")


# ============================================================
# 11. REPAYMENT & WORKING CAPITAL
# ============================================================

def test_b12_repayment_schedule_present():
    """Repayment schedule returned and has entries."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code == 200
    d = resp.json()
    assert len(d["repayment"]) > 0
    assert d["repayment"][0]["installment_amount"] >= 0


def test_b12_working_capital_fields_present():
    """Working capital has all required computed fields."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
    })
    assert resp.status_code == 200
    wc = resp.json()["data"]["working_capital"]
    required = [
        "monthly_raw_materials", "monthly_labor_wages",
        "monthly_rent_utilities", "monthly_logistics_packaging",
        "total_monthly_operating_expense", "recommended_3_months_reserve",
        "break_even_monthly_revenue",
    ]
    for field in required:
        assert field in wc, f"Missing field: {field}"
        assert wc[field] >= 0


# ============================================================
# 12. NO PLACEHOLDER LEAK (all categories, all languages)
# ============================================================

@pytest.mark.parametrize("category,lang", [
    ("Dairy", "en"), ("Dairy", "hi"), ("Dairy", "gu"),
    ("Textile & Clothing", "hi"), ("Grocery", "gu"),
    ("Food Processing", "en"), ("Agriculture", "hi"),
])
def test_b12_no_placeholder_leak(category, lang):
    """No raw template placeholders in any response."""
    resp = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": category,
        "available_capital": 100000.0,
        "language": lang,
    })
    assert resp.status_code == 200
    text = resp.text
    for placeholder in ["{loc_cat_name}", "{town}", "{district}", "{state}", "undefined"]:
        assert placeholder not in text, f"Placeholder '{placeholder}' leaked for {category}/{lang}"
