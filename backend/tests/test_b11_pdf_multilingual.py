"""
Phase B11 — Fully Multilingual PDF Generation Test Suite
UdyamSaarthi - SIH26091

Tests:
1. PDF generated for en, hi, gu → HTTP 200, application/pdf, non-empty
2. Content-Disposition filename correct (EN/HI/GU suffix)
3. Financial invariance: PDF generated from same inputs across languages must have identical financial figures
4. No-language default falls back to English
5. Existing English PDF generation is preserved (backward compat)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

BASE_PAYLOAD = {
    "location": "Anand, Gujarat",
    "business_category": "Dairy",
    "available_capital": 100000.0,
}


@pytest.mark.parametrize("lang,expected_tag", [
    ("en", "EN"),
    ("hi", "HI"),
    ("gu", "GU"),
])
def test_b11_pdf_generated_correctly_per_language(lang, expected_tag):
    """PDF endpoint returns 200, application/pdf, non-empty bytes for each language."""
    resp = client.post("/report/generate", json={**BASE_PAYLOAD, "language": lang})
    assert resp.status_code == 200, f"Failed for language={lang}: {resp.text}"
    assert resp.headers["content-type"] == "application/pdf"
    assert len(resp.content) > 5000, f"PDF too small for lang={lang}, size={len(resp.content)}"
    # Check PDF magic bytes
    assert resp.content[:4] == b"%PDF", f"Not a valid PDF for lang={lang}"
    # Check filename tag
    cd = resp.headers.get("content-disposition", "")
    assert expected_tag in cd, f"Expected {expected_tag} in Content-Disposition: {cd}"


def test_b11_pdf_default_language_is_english():
    """Omitting language defaults to English PDF."""
    resp = client.post("/report/generate", json=BASE_PAYLOAD)
    assert resp.status_code == 200
    assert resp.content[:4] == b"%PDF"
    cd = resp.headers.get("content-disposition", "")
    assert "EN" in cd


def test_b11_pdf_invalid_language_falls_back_to_english():
    """Unknown language falls back to English."""
    resp = client.post("/report/generate", json={**BASE_PAYLOAD, "language": "fr"})
    assert resp.status_code == 200
    cd = resp.headers.get("content-disposition", "")
    assert "EN" in cd


@pytest.mark.parametrize("category", ["Textile", "Dairy", "Grocery"])
def test_b11_pdf_all_categories_all_languages(category):
    """All 3 categories × 3 languages produce valid PDFs."""
    for lang in ["en", "hi", "gu"]:
        resp = client.post("/report/generate", json={
            "location": "Anand, Gujarat",
            "business_category": category,
            "available_capital": 100000.0,
            "language": lang,
        })
        assert resp.status_code == 200, f"Failed for {category}/{lang}"
        assert resp.content[:4] == b"%PDF", f"Not PDF for {category}/{lang}"
        assert len(resp.content) > 5000, f"PDF too small for {category}/{lang}"


def test_b11_pdf_financial_invariance_across_languages():
    """
    Financial values (project_cost, loan, EMI) used in PDF must be from the
    deterministic engine and identical regardless of language. We verify this
    by checking that the analysis API returns identical numbers.
    """
    fin_values = {}
    for lang in ["en", "hi", "gu"]:
        resp = client.post("/business/analyze", json={**BASE_PAYLOAD, "language": lang})
        assert resp.status_code == 200
        d = resp.json()["data"]["financial"]
        fin_values[lang] = (d["project_cost"], d["max_loan_amount"], d["promoter_contribution"])

    assert fin_values["en"] == fin_values["hi"] == fin_values["gu"], \
        f"Financial mismatch: {fin_values}"


def test_b11_pdf_generator_direct():
    """Directly test pdf_generator with dummy data to verify no crash."""
    from app.utils.pdf_generator import generate_pdf_report

    dummy = {
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "financial": {
            "project_cost": 1000000.0,
            "promoter_contribution": 100000.0,
            "max_loan_amount": 900000.0,
        },
        "scheme": {
            "scheme_name": "PMEGP",
            "scheme_code": "PMEGP-KVIC",
            "interest_rate_percent": 8.0,
            "tenure_years": 7,
            "tenure_months": 84,
            "moratorium_months": 6,
        },
        "emi": {
            "monthly_emi": 14834.86,
            "moratorium_monthly_interest": 6000.0,
            "total_repayment_amount": 1245527.0,
            "principal_amount": 900000.0,
            "total_interest_payable": 345527.0,
        },
        "working_capital": {
            "monthly_raw_materials": 30000.0,
            "monthly_labor_wages": 15000.0,
            "monthly_rent_utilities": 5000.0,
            "monthly_logistics_packaging": 3000.0,
            "monthly_contingency_buffer": 2000.0,
            "total_monthly_operating_expense": 55000.0,
            "recommended_3_months_reserve": 165000.0,
            "break_even_monthly_revenue": 70000.0,
        },
        "swot": {
            "strengths": ["Strong local demand"],
            "weaknesses": ["Limited capital"],
            "opportunities": ["Growing dairy market"],
            "threats": ["Seasonal supply issues"],
        },
        "risks": [{"risk_title": "Price Risk", "severity": "Medium", "mitigation_strategy": "Hedge with contracts"}],
        "competitors": [{"name": "Local Dairy Shop", "type_of_business": "Retail", "proximity": "1 km", "differentiation_strategy": "Quality focus"}],
        "pricing": {
            "benchmark_product_or_service": "1L Fresh Milk",
            "estimated_unit_production_cost": "₹42/L",
            "suggested_retail_price": "₹58-64/L",
            "target_gross_margin_percent": 28.0,
            "pricing_strategy_notes": "Competitive with quality focus",
        },
        "recommendation": {
            "feasibility_score": 98,
            "feasibility_rating": "Highly Feasible",
            "summary": "Excellent opportunity for dairy business in Anand.",
            "mandatory_licenses_and_registrations": ["Udyam MSME", "FSSAI"],
            "first_90_days_milestones": ["Register business", "Procure cattle"],
            "digital_enablement_tips": ["Use UPI", "WhatsApp Business"],
        },
        "market": {"market_reach_summary": "Within 8 km radius, 18000 residents."},
        "opportunities": {"items": [{"title": "High Growth", "description": "Rising dairy demand"}]},
        "ai_explanation": {
            "summary": "Good business opportunity.",
            "market_insight": "Strong local market.",
            "opportunity_explanation": "Growing demand.",
            "risk_explanation": "Manageable risks.",
            "financial_explanation": "Sound financial plan.",
            "scheme_explanation": "PMEGP is applicable.",
            "recommended_actions": ["Start small", "Scale up"],
            "next_steps": ["Register", "Source cattle", "Launch"],
        },
    }

    for lang in ["en", "hi", "gu"]:
        pdf = generate_pdf_report(dummy, language=lang)
        assert pdf[:4] == b"%PDF", f"Not a PDF for lang={lang}"
        assert len(pdf) > 3000, f"PDF too small for lang={lang}"
