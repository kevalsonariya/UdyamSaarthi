"""
Tests for Phase B7 — Dynamic Location & Business Category Foundation.
Verifies:
1. Centralized 31 categories registry and GET /categories endpoint.
2. Location data model and GET /locations/suggest autocomplete endpoint.
3. Analysis execution with new categories and location models.
4. Financial calculation invariance.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data.categories_config import CATEGORIES_REGISTRY, CentralizedCategoriesConfig
from app.data.location_provider import get_location_provider

client = TestClient(app)


def test_categories_registry_count_and_metadata():
    """Verify registry contains all 31 categories with required structured fields."""
    assert len(CATEGORIES_REGISTRY) >= 31

    required_fields = [
        "id",
        "name",
        "display_name",
        "sector",
        "subcategories",
        "competitor_search_terms",
        "pricing_profile",
        "market_profile",
        "location_factors",
        "opportunity_profile",
        "risk_profile",
        "typical_capex_min",
        "typical_capex_max",
    ]

    for cat in CATEGORIES_REGISTRY:
        for field in required_fields:
            assert field in cat, f"Missing '{field}' in category {cat.get('id')}"
        assert len(cat["subcategories"]) > 0
        assert len(cat["competitor_search_terms"]) > 0
        assert cat["typical_capex_min"] > 0
        assert cat["typical_capex_max"] >= cat["typical_capex_min"]


def test_categories_endpoint():
    """Verify GET /categories API endpoint returns structured catalog."""
    resp = client.get("/categories")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total"] >= 31
    assert len(data["categories"]) >= 31

    # Check key requested categories are present
    names = [c["name"] for c in data["categories"]]
    assert "Poultry" in names
    assert "Two-Wheeler Repair" in names
    assert "Bakery" in names
    assert "Pottery" in names
    assert "Bamboo Products" in names
    assert "Beauty & Salon" in names
    assert "Grocery / Kirana" in names
    assert "Textile & Clothing" in names


def test_location_suggest_known_hubs():
    """Verify GET /locations/suggest returns accurate taluka/district data for rural hubs."""
    resp = client.get("/locations/suggest?q=Anand")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total"] > 0
    top = data["suggestions"][0]
    assert "Anand" in top["village_town_city"]
    assert top["district"] == "Anand"
    assert top["state"] == "Gujarat"
    assert top["country"] == "India"
    assert top["latitude"] is not None
    assert top["longitude"] is not None
    assert "Anand, Gujarat" in top["formatted_address"]


def test_location_suggest_bardoli():
    """Verify Bardoli (Surat district, Gujarat) returns accurately."""
    resp = client.get("/locations/suggest?q=Bardoli")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    match = next((s for s in data["suggestions"] if "Bardoli" in s["village_town_city"]), None)
    assert match is not None
    assert match["district"] == "Surat"
    assert match["state"] == "Gujarat"


def test_location_suggest_fallback_for_custom():
    """Verify unknown location gracefully returns structured custom model without errors."""
    resp = client.get("/locations/suggest?q=CustomVillageUnknown99")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    custom = data["suggestions"][0]
    assert custom["village_town_city"] == "CustomVillageUnknown99"
    assert "CustomVillageUnknown99" in custom["formatted_address"]


@pytest.mark.parametrize("category_test_name", [
    "Poultry",
    "Two-Wheeler Repair",
    "Bakery",
    "Bamboo Products",
    "Beauty & Salon",
    "Pickles & Papad",
    "Grocery / Kirana",
])
def test_analyze_with_new_b7_categories(category_test_name):
    """Verify end-to-end /business/analyze successfully handles new B7 categories."""
    payload = {
        "location": "Anand, Gujarat",
        "business_category": category_test_name,
        "available_capital": 100000.0,
        "language": "en",
        "location_detail": {
            "raw_input": "Anand, Gujarat",
            "village_town_city": "Anand",
            "taluka_subdistrict": "Anand Taluka",
            "district": "Anand",
            "state": "Gujarat",
            "country": "India",
            "latitude": 22.5645,
            "longitude": 72.9289,
            "formatted_address": "Anand, Anand Taluka, Anand, Gujarat, India",
            "provider": "local_catalog",
        }
    }
    resp = client.post("/business/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True

    # Financial engine values strictly invariant
    assert data["financial"]["project_cost"] == 1000000.0
    assert data["financial"]["promoter_contribution"] == 100000.0
    assert data["scheme"]["eligible_funding"] == 900000.0
    assert data["emi"]["monthly_emi"] > 0

    # Business profile generated
    assert data["business"]["category_name"] != ""
    assert len(data["business"]["primary_activities"]) > 0
    assert data["location_detail"] is not None
    assert data["location_detail"]["district"] == "Anand"
