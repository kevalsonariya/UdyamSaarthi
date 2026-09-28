import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.ai_advisory_service import (
    AIAdvisoryService,
    DeterministicAdvisoryFallback,
    ExternalLLMProvider,
)
from app.schemas.schemas import AIExplanation

client = TestClient(app)

SAMPLE_CONTEXT = {
    "location": "Anand, Gujarat",
    "business_category": "Textile & Clothing",
    "available_capital": 100000.0,
    "financial": {
        "project_cost": 1000000.0,
        "promoter_contribution": 100000.0,
        "max_loan_amount": 900000.0,
    },
    "scheme": {
        "scheme_name": "Term Loan Scheme",
        "interest_rate_percent": 8.0,
        "tenure_years": 7,
        "moratorium_months": 6,
        "eligible_funding": 900000.0,
    },
    "emi": {
        "monthly_emi": 14197.83,
    },
    "working_capital": {
        "recommended_3_months_reserve": 234500.0,
    },
    "market": {
        "catchment_radius_km": 18,
    },
}


def test_deterministic_ai_fallback_produces_valid_structure():
    """Verify fallback advisory produces all required rural-friendly explanation fields."""
    provider = DeterministicAdvisoryFallback()
    result = provider.generate_explanation(SAMPLE_CONTEXT)

    assert isinstance(result, AIExplanation)
    assert "Textile & Clothing" in result.summary
    assert "1,000,000" in result.summary or "10,00,000" in result.summary or "1000000" in result.summary
    assert "Anand, Gujarat" in result.market_insight
    assert "Term Loan Scheme" in result.scheme_explanation
    assert len(result.recommended_actions) >= 3
    assert len(result.next_steps) >= 3
    assert result.is_ai_generated is False
    assert result.provider == "deterministic_rule_engine"


def test_ai_service_financial_invariance():
    """Verify that financial values are authoritative and unchanged by the AI layer."""
    service = AIAdvisoryService()
    result = service.generate_advisory_explanation(SAMPLE_CONTEXT)

    assert isinstance(result, AIExplanation)
    # The financial figures in context must remain untouched
    assert SAMPLE_CONTEXT["financial"]["project_cost"] == 1000000.0
    assert SAMPLE_CONTEXT["scheme"]["eligible_funding"] == 900000.0
    assert SAMPLE_CONTEXT["scheme"]["interest_rate_percent"] == 8.0


def test_ai_provider_missing_api_key_graceful_fallback():
    """Verify that when no API key is provided, the service defaults gracefully to deterministic fallback."""
    service = AIAdvisoryService()
    explanation = service.generate_advisory_explanation(SAMPLE_CONTEXT)
    assert explanation.provider == "deterministic_rule_engine"
    assert len(explanation.summary) > 20


def test_external_llm_provider_error_falls_back():
    """Verify that an exception in external provider fails gracefully without crashing."""
    provider = ExternalLLMProvider(api_key="invalid_mock_key")
    # Will gracefully return deterministic fallback output
    result = provider.generate_explanation(SAMPLE_CONTEXT)
    assert isinstance(result, AIExplanation)
    assert len(result.recommended_actions) >= 3


def test_post_ai_explain_endpoint():
    """Verify POST /ai/explain returns structured advisory with financial invariants."""
    payload = {
        "location": "Anand, Gujarat",
        "business_category": "Textile & Clothing",
        "available_capital": 100000.0,
    }
    response = client.post("/ai/explain", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "data" in res
    assert "financial_invariants" in res
    assert res["financial_invariants"]["project_cost"] == 1000000.0
    assert res["financial_invariants"]["eligible_funding"] == 900000.0
    assert res["financial_invariants"]["scheme_name"] == "Term Loan Scheme"
    assert "summary" in res["data"]
    assert "market_insight" in res["data"]
    assert "scheme_explanation" in res["data"]


def test_post_business_analyze_includes_ai_explanation():
    """Verify POST /business/analyze returns full analysis with ai_explanation intact."""
    payload = {
        "location": "Anand, Gujarat",
        "business_category": "Textile & Clothing",
        "available_capital": 100000.0,
    }
    response = client.post("/business/analyze", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "ai_explanation" in res
    assert res["ai_explanation"] is not None
    assert "summary" in res["ai_explanation"]
    assert res["financial"]["project_cost"] == 1000000.0
