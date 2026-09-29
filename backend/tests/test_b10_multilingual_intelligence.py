"""
Phase B10 - Complete Dynamic English/Hindi/Gujarati Translation Test Suite
UdyamSaarthi - SIH26091

Tests:
1. Language reaches backend API and AI Advisory Service
2. Dynamic local intelligence localized (Market Reach, Opportunities, SWOT, Risks, Competitors, Pricing, Recommendations)
3. Matrix verification for Anand + Textile, Anand + Dairy, Anand + Grocery across en, hi, gu
4. Financial invariance (numbers identical across languages)
5. Fallback safety (no broken keys, undefined, or unformatted templates)
"""

import pytest
import re
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

DEVANAGARI_REGEX = re.compile(r'[\u0900-\u097F]')
GUJARATI_REGEX = re.compile(r'[\u0A80-\u0AFF]')


def test_language_reaches_backend_and_advisory():
    """Verify language parameter flows through API endpoint to Advisory & Local Intelligence."""
    payload_en = {
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en"
    }
    payload_hi = {
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "hi"
    }
    payload_gu = {
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "gu"
    }

    res_en = client.post("/business/analyze", json=payload_en)
    res_hi = client.post("/business/analyze", json=payload_hi)
    res_gu = client.post("/business/analyze", json=payload_gu)

    assert res_en.status_code == 200
    assert res_hi.status_code == 200
    assert res_gu.status_code == 200

    data_en = res_en.json()["data"]
    data_hi = res_hi.json()["data"]
    data_gu = res_gu.json()["data"]

    # Verify AI advisory reaches backend and is localized
    assert data_en["ai_explanation"]["summary"] != data_hi["ai_explanation"]["summary"]
    assert data_en["ai_explanation"]["summary"] != data_gu["ai_explanation"]["summary"]
    assert DEVANAGARI_REGEX.search(data_hi["ai_explanation"]["summary"]) is not None
    assert GUJARATI_REGEX.search(data_gu["ai_explanation"]["summary"]) is not None


@pytest.mark.parametrize("category", ["Textile", "Dairy", "Grocery"])
def test_b10_matrix_anand_categories_across_languages(category):
    """
    Test matrix required by Phase B10:
    - Anand + Textile
    - Anand + Dairy
    - Anand + Grocery
    Each tested across English, Hindi, and Gujarati.
    """
    capital = 100000.0
    responses = {}

    for lang in ["en", "hi", "gu"]:
        resp = client.post("/business/analyze", json={
            "location": "Anand, Gujarat",
            "business_category": category,
            "available_capital": capital,
            "language": lang
        })
        assert resp.status_code == 200, f"Failed for {category} in {lang}"
        responses[lang] = resp.json()["data"]

    en_bi = responses["en"]
    hi_bi = responses["hi"]
    gu_bi = responses["gu"]

    # 1. Market Reach localized
    assert DEVANAGARI_REGEX.search(hi_bi["market"]["market_reach_summary"]) is not None
    assert GUJARATI_REGEX.search(gu_bi["market"]["market_reach_summary"]) is not None

    # 2. Opportunities localized
    assert len(en_bi["opportunities"]["items"]) > 0
    assert len(hi_bi["opportunities"]["items"]) > 0
    assert len(gu_bi["opportunities"]["items"]) > 0
    assert DEVANAGARI_REGEX.search(hi_bi["opportunities"]["items"][0]["description"]) is not None
    assert GUJARATI_REGEX.search(gu_bi["opportunities"]["items"][0]["description"]) is not None

    # 3. SWOT localized
    assert len(hi_bi["swot"]["strengths"]) > 0
    assert len(gu_bi["swot"]["strengths"]) > 0
    assert DEVANAGARI_REGEX.search(hi_bi["swot"]["strengths"][0]) is not None
    assert GUJARATI_REGEX.search(gu_bi["swot"]["strengths"][0]) is not None

    # 4. Risks localized
    assert len(hi_bi["risks"]) > 0
    assert len(gu_bi["risks"]) > 0
    assert DEVANAGARI_REGEX.search(hi_bi["risks"][0]["mitigation_strategy"]) is not None
    assert GUJARATI_REGEX.search(gu_bi["risks"][0]["mitigation_strategy"]) is not None

    # 5. Pricing localized
    assert DEVANAGARI_REGEX.search(hi_bi["pricing"]["benchmark_product_or_service"]) is not None
    assert GUJARATI_REGEX.search(gu_bi["pricing"]["benchmark_product_or_service"]) is not None

    # 6. Competitors localized
    assert len(hi_bi["competitors"]) > 0
    assert len(gu_bi["competitors"]) > 0
    assert DEVANAGARI_REGEX.search(hi_bi["competitors"][0]["name"]) is not None
    assert GUJARATI_REGEX.search(gu_bi["competitors"][0]["name"]) is not None
    assert DEVANAGARI_REGEX.search(hi_bi["competitors"][0]["differentiation_strategy"]) is not None
    assert GUJARATI_REGEX.search(gu_bi["competitors"][0]["differentiation_strategy"]) is not None

    # 7. Recommendations localized
    assert DEVANAGARI_REGEX.search(hi_bi["recommendation"]["mandatory_licenses_and_registrations"][0]) is not None
    assert GUJARATI_REGEX.search(gu_bi["recommendation"]["mandatory_licenses_and_registrations"][0]) is not None

    # 8. AI Advisory localized
    hi_adv = responses["hi"]["ai_explanation"]
    gu_adv = responses["gu"]["ai_explanation"]
    assert DEVANAGARI_REGEX.search(hi_adv["summary"]) is not None
    assert GUJARATI_REGEX.search(gu_adv["summary"]) is not None
    assert DEVANAGARI_REGEX.search(hi_adv["market_insight"]) is not None
    assert GUJARATI_REGEX.search(gu_adv["market_insight"]) is not None

    # 9. Financial Invariance: Numbers MUST remain strictly identical between languages
    en_fin = responses["en"]["financial"]
    hi_fin = responses["hi"]["financial"]
    gu_fin = responses["gu"]["financial"]

    assert en_fin["project_cost"] == hi_fin["project_cost"] == gu_fin["project_cost"]
    assert en_fin["max_loan_amount"] == hi_fin["max_loan_amount"] == gu_fin["max_loan_amount"]
    assert en_fin["promoter_contribution"] == hi_fin["promoter_contribution"] == gu_fin["promoter_contribution"]
    assert responses["en"]["emi"]["monthly_emi"] == responses["hi"]["emi"]["monthly_emi"] == responses["gu"]["emi"]["monthly_emi"]
    assert responses["en"]["scheme"]["interest_rate_percent"] == responses["hi"]["scheme"]["interest_rate_percent"] == responses["gu"]["scheme"]["interest_rate_percent"]


def test_safe_deterministic_fallbacks_no_broken_keys_or_placeholders():
    """Ensure no '{loc_cat_name}' or raw placeholder templates leak into UI content."""
    for category in ["Textile", "Dairy", "Grocery"]:
        for lang in ["en", "hi", "gu"]:
            resp = client.post("/business/analyze", json={
                "location": "Anand, Gujarat",
                "business_category": category,
                "available_capital": 100000.0,
                "language": lang
            })
            assert resp.status_code == 200
            data_str = resp.text

            # Check that template placeholders are not leaked as raw strings
            assert "{loc_cat_name}" not in data_str
            assert "{town}" not in data_str
            assert "{district}" not in data_str
            assert "{state}" not in data_str
            assert "undefined" not in data_str
