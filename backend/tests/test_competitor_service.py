"""
Phase B9 — Competitor Service Unit & Integration Tests.
Verifies:
1. Google provider parses valid results.
2. Missing fields remain null (no fake data).
3. Relevant category results are selected.
4. Irrelevant businesses are filtered.
5. Maximum 4 competitors returned.
6. Real provider result: is_demo_data == False.
7. Real provider result: is_estimate == False.
8. Real provider result: map_url is actual provider URL when available.
9. Demo fallback: is_demo_data == True.
10. Demo fallback: no fake map URL.
11. Provider failure falls back safely.
12. Missing API key falls back safely.
13. Request ID is preserved.
14. Input snapshot is preserved.
15. B8.1 Dairy -> Poultry regression still passes.
"""

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.services.competitor_service import (
    GooglePlacesProvider,
    DemoCompetitorProvider,
    CompetitorService,
    haversine_distance_km,
)
from app.schemas.schemas import CompetitorItem

client = TestClient(app)

MOCK_GOOGLE_PLACES_PAYLOAD = {
    "places": [
        {
            "id": "place-dairy-001",
            "displayName": {"text": "Amul Milk Parlour & Dairy Depot", "languageCode": "en"},
            "formattedAddress": "Station Road, Anand, Gujarat 388001, India",
            "location": {"latitude": 22.565, "longitude": 72.930},
            "primaryType": "dairy_store",
            "types": ["dairy_store", "store", "food"],
            "googleMapsUri": "https://maps.google.com/?cid=1028584820",
            "rating": 4.5,
            "userRatingCount": 128,
            "websiteUri": "https://amul.com",
        },
        {
            "id": "place-dairy-002",
            "displayName": {"text": "Charotar Dudh Mandali Co-op", "languageCode": "en"},
            "formattedAddress": "Gam Road, Anand, Gujarat 388001, India",
            "location": {"latitude": 22.568, "longitude": 72.932},
            "primaryType": "dairy_store",
            "types": ["dairy_store", "food"],
            "googleMapsUri": "https://maps.google.com/?cid=999888",
            "rating": 4.2,
            "userRatingCount": 35,
        },
        {
            "id": "place-irrelevant-003",
            "displayName": {"text": "Grand Luxury Hotel & Banquet", "languageCode": "en"},
            "formattedAddress": "Expressway, Anand, Gujarat",
            "location": {"latitude": 22.570, "longitude": 72.935},
            "primaryType": "lodging",
            "types": ["lodging", "hotel", "restaurant"],
            "googleMapsUri": "https://maps.google.com/?cid=111111",
            "rating": 4.8,
            "userRatingCount": 500,
        },
        {
            "id": "place-dairy-004",
            "displayName": {"text": "Shreeji Dairy & Sweets Collection", "languageCode": "en"},
            "formattedAddress": "Bazaar, Anand, Gujarat 388001, India",
            "location": {"latitude": 22.562, "longitude": 72.925},
            "primaryType": "dairy_store",
            "types": ["dairy_store", "food"],
            "googleMapsUri": "https://maps.google.com/?cid=777666",
            "rating": 4.0,
            "userRatingCount": 12,
        },
        {
            "id": "place-dairy-005",
            "displayName": {"text": "Krishna Milk Collection Hub", "languageCode": "en"},
            "formattedAddress": "Main Road, Anand, Gujarat 388001, India",
            "location": {"latitude": 22.561, "longitude": 72.922},
            "primaryType": "dairy_store",
            "types": ["dairy_store"],
            "googleMapsUri": "https://maps.google.com/?cid=555444",
        },
        {
            "id": "place-dairy-faraway",
            "displayName": {"text": "Distant Dairy 80km Away", "languageCode": "en"},
            "formattedAddress": "Vadodara Highway, Gujarat",
            "location": {"latitude": 23.500, "longitude": 73.500},
            "primaryType": "dairy_store",
            "types": ["dairy_store"],
        },
    ]
}


def test_haversine_distance():
    """Verify haversine distance calculation is accurate."""
    # Anand (22.5645, 72.9289) to Nadiad (22.6916, 72.8634) is approx 15.6 km
    d = haversine_distance_km(22.5645, 72.9289, 22.6916, 72.8634)
    assert 14.0 <= d <= 17.0


def test_1_google_provider_parses_valid_results():
    """Test 1: Google provider parses valid places into CompetitorItem models."""
    provider = GooglePlacesProvider(api_key="mock_key_for_testing")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = MOCK_GOOGLE_PLACES_PAYLOAD

    with patch("httpx.Client.post", return_value=mock_resp):
        items = provider.search_competitors(
            location="Anand, Gujarat",
            category="Dairy",
            coordinates={"latitude": 22.5645, "longitude": 72.9289},
            radius_km=5.0,
            max_results=4,
        )

    assert len(items) >= 1
    first = items[0]
    assert isinstance(first, CompetitorItem)
    assert first.name == "Amul Milk Parlour & Dairy Depot"
    assert first.address == "Station Road, Anand, Gujarat 388001, India"
    assert first.distance_km is not None
    assert first.distance_km < 5.0
    assert first.place_id == "place-dairy-001"
    assert first.map_url == "https://maps.google.com/?cid=1028584820"
    assert first.website_url == "https://amul.com"
    assert first.rating == 4.5
    assert first.review_count == 128


def test_2_missing_fields_remain_null():
    """Test 2: Missing optional fields like rating/website must remain None, not fabricated."""
    provider = GooglePlacesProvider(api_key="mock_key")
    # place-dairy-005 in mock payload has no rating, review count, or website
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "places": [
            {
                "id": "place-minimal",
                "displayName": {"text": "Simple Village Milk Shop"},
                "formattedAddress": "Anand Village Road, Anand, Gujarat",
                "location": {"latitude": 22.564, "longitude": 72.928},
                "primaryType": "dairy_store",
            }
        ]
    }

    with patch("httpx.Client.post", return_value=mock_resp):
        items = provider.search_competitors(
            location="Anand, Gujarat",
            category="Dairy",
            coordinates={"latitude": 22.5645, "longitude": 72.9289},
        )

    assert len(items) == 1
    p = items[0]
    assert p.rating is None
    assert p.review_count is None
    assert p.website_url is None
    assert p.name == "Simple Village Milk Shop"


def test_3_relevant_category_results_are_selected():
    """Test 3: Relevant category competitors are prioritized and returned."""
    provider = GooglePlacesProvider(api_key="mock_key")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = MOCK_GOOGLE_PLACES_PAYLOAD

    with patch("httpx.Client.post", return_value=mock_resp):
        items = provider.search_competitors(
            location="Anand, Gujarat",
            category="Dairy",
            coordinates={"latitude": 22.5645, "longitude": 72.9289},
        )

    names = [it.name for it in items]
    assert any("Milk" in n or "Dairy" in n or "Dudh" in n for n in names)


def test_4_irrelevant_businesses_are_filtered():
    """Test 4: Irrelevant places (like luxury hotels) are filtered out of Dairy search."""
    provider = GooglePlacesProvider(api_key="mock_key")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = MOCK_GOOGLE_PLACES_PAYLOAD

    with patch("httpx.Client.post", return_value=mock_resp):
        items = provider.search_competitors(
            location="Anand, Gujarat",
            category="Dairy",
            coordinates={"latitude": 22.5645, "longitude": 72.9289},
        )

    names = [it.name for it in items]
    assert "Grand Luxury Hotel & Banquet" not in names


def test_5_maximum_4_competitors_returned():
    """Test 5: Maximum of 4 competitors returned to keep UI clean."""
    provider = GooglePlacesProvider(api_key="mock_key")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = MOCK_GOOGLE_PLACES_PAYLOAD

    with patch("httpx.Client.post", return_value=mock_resp):
        items = provider.search_competitors(
            location="Anand, Gujarat",
            category="Dairy",
            coordinates={"latitude": 22.5645, "longitude": 72.9289},
            max_results=4,
        )

    assert len(items) <= 4


def test_6_and_7_real_provider_result_flags():
    """Test 6 & 7: Real provider results have is_demo_data == False and is_estimate == False."""
    provider = GooglePlacesProvider(api_key="mock_key")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = MOCK_GOOGLE_PLACES_PAYLOAD

    with patch("httpx.Client.post", return_value=mock_resp):
        items = provider.search_competitors(
            location="Anand, Gujarat",
            category="Dairy",
            coordinates={"latitude": 22.5645, "longitude": 72.9289},
        )

    for item in items:
        assert item.is_demo_data is False
        assert item.is_estimate is False
        assert item.data_source == "Google Places API"
        assert item.location_status == "Verified provider location"


def test_8_real_provider_map_url():
    """Test 8: Real provider result has actual provider map URL."""
    provider = GooglePlacesProvider(api_key="mock_key")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = MOCK_GOOGLE_PLACES_PAYLOAD

    with patch("httpx.Client.post", return_value=mock_resp):
        items = provider.search_competitors(
            location="Anand, Gujarat",
            category="Dairy",
            coordinates={"latitude": 22.5645, "longitude": 72.9289},
        )

    first = items[0]
    assert first.map_url == "https://maps.google.com/?cid=1028584820"


def test_9_and_10_demo_fallback_metadata_and_no_fake_map_url():
    """Test 9 & 10: Demo fallback has is_demo_data == True and no fake map URL."""
    demo_provider = DemoCompetitorProvider()
    items = demo_provider.search_competitors(
        location="Anand, Gujarat",
        category="Dairy",
        coordinates={"latitude": 22.5645, "longitude": 72.9289},
    )

    assert len(items) >= 3
    for it in items:
        assert it.is_demo_data is True
        assert it.is_estimate is True
        assert it.data_source == "Indicative category-location profile"
        assert it.map_url is None
        assert it.latitude is None
        assert it.longitude is None
        assert "unavailable" in it.location_status.lower()


def test_11_provider_failure_falls_back_safely():
    """Test 11: HTTP error in provider falls back seamlessly to demo competitors."""
    service = CompetitorService()
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.text = "Internal Server Error"

    with patch("app.config.settings.GOOGLE_PLACES_API_KEY", "mock_key"):
        with patch("httpx.Client.post", return_value=mock_resp):
            items = service.find_competitors(
                location="Anand, Gujarat",
                category="Dairy",
            )

    assert len(items) >= 3
    # Gracefully degraded to demo data
    assert items[0].is_demo_data is True


def test_12_missing_api_key_falls_back_safely():
    """Test 12: When API key is empty, service falls back to demo data without error."""
    service = CompetitorService()
    with patch("app.config.settings.GOOGLE_PLACES_API_KEY", ""):
        items = service.find_competitors(
            location="Anand, Gujarat",
            category="Dairy",
        )

    assert len(items) >= 3
    assert items[0].is_demo_data is True
    assert items[0].data_source == "Indicative category-location profile"


def test_13_and_14_request_id_and_input_snapshot_preserved():
    """Test 13 & 14: Dedicated /competitors/search endpoint preserves request_id and input snapshot."""
    req_id = "test-comp-req-12345"
    payload = {
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "request_id": req_id,
        "language": "en",
    }
    resp = client.post("/competitors/search", json=payload)
    assert resp.status_code == 200
    res = resp.json()
    assert res["success"] is True
    data = res["data"]
    assert data["request_id"] == req_id
    assert data["input"]["location"] == "Anand, Gujarat"
    assert data["input"]["business_category"] == "Dairy"
    assert len(data["competitors"]) >= 3


def test_15_b8_1_dairy_to_poultry_isolation_with_competitor_service():
    """
    Test 15: Dairy -> Poultry consecutive search ensures no competitor bleed or stale data.
    """
    resp_dairy = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Dairy",
        "available_capital": 100000.0,
        "language": "en",
        "request_id": "req-dairy-iso",
    })
    assert resp_dairy.status_code == 200
    d_dairy = resp_dairy.json()["data"]

    resp_poultry = client.post("/business/analyze", json={
        "location": "Anand, Gujarat",
        "business_category": "Poultry",
        "available_capital": 75000.0,
        "language": "en",
        "request_id": "req-poultry-iso",
    })
    assert resp_poultry.status_code == 200
    d_poultry = resp_poultry.json()["data"]

    dairy_comps = [c["name"] for c in d_dairy["competitors"]]
    poultry_comps = [c["name"] for c in d_poultry["competitors"]]

    # No overlap in names between Dairy and Poultry
    assert not set(dairy_comps).intersection(set(poultry_comps))
    assert d_dairy["financial"]["project_cost"] == 1000000.0
    assert d_poultry["financial"]["project_cost"] == 750000.0
