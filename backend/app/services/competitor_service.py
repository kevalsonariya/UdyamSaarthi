"""
Phase B9 — Real Local Competitor Mapping & Provider Abstraction.
SIH26091 — AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant.

Provides location-aware competitor discovery with:
- Abstract Provider interface (CompetitorProvider)
- GooglePlacesProvider using CURRENT Google Places API (New)
- DemoCompetitorProvider fallback preserving B8.2 transparency
- Zero hardcoded API keys / zero secrets in client
- Strict field masks (no wildcard '*')
- Category-aware relevance ranking & filtering
- Real distance calculation (Haversine)
- Safe caching to avoid redundant requests
- Graceful degradation on network / key / quota failure
"""

import os
import math
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone

import httpx

from app.config import settings
from app.schemas.schemas import CompetitorItem, LocationData
from app.data.categories_config import CentralizedCategoriesConfig
from app.data.location_provider import get_location_provider

logger = logging.getLogger(__name__)


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates spherical distance between two points in kilometers."""
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 1)


# Irrelevant place types to filter out per broad trade sector
IRRELEVANT_TYPES_BY_SECTOR: Dict[str, List[str]] = {
    "Agriculture & Allied": [
        "restaurant", "cafe", "lodging", "hotel", "bank", "atm", "hospital", "doctor",
        "movie_theater", "night_club", "beauty_salon"
    ],
    "Food Processing": [
        "hospital", "bank", "atm", "gas_station", "hardware_store", "auto_repair",
        "car_dealer", "electronics_store"
    ],
    "Textile & Handloom": [
        "restaurant", "cafe", "gas_station", "car_dealer", "hardware_store", "pharmacy",
        "hospital", "bank"
    ],
    "Retail & Kirana": [
        "hospital", "bank", "school", "university", "police", "fire_station", "courthouse"
    ],
    "Artisanal & Crafts": [
        "hospital", "bank", "gas_station", "car_dealer", "auto_repair"
    ],
    "Repairs & Digital Services": [
        "restaurant", "cafe", "clothing_store", "bakery", "grocery_store", "supermarket"
    ],
    "Rural Services": [
        "night_club", "movie_theater", "bowling_alley"
    ]
}


class CompetitorProvider(ABC):
    """Abstract base class for competitor discovery providers."""

    @abstractmethod
    def search_competitors(
        self,
        location: str,
        category: str,
        coordinates: Optional[Dict[str, float]] = None,
        radius_km: float = 5.0,
        max_results: int = 4,
        language: str = "en",
    ) -> List[CompetitorItem]:
        """Discover and return structured competitor records."""
        pass


class GooglePlacesProvider(CompetitorProvider):
    """
    Real competitor discovery provider using the Google Places API (New).
    Uses minimal field masks, searchText with locationBias, and strict security.
    """

    PLACES_SEARCH_TEXT_URL = "https://places.googleapis.com/v1/places:searchText"

    # Minimal field mask — requests only necessary fields, never '*'
    FIELD_MASK = (
        "places.id,"
        "places.displayName,"
        "places.formattedAddress,"
        "places.location,"
        "places.primaryType,"
        "places.types,"
        "places.googleMapsUri,"
        "places.rating,"
        "places.userRatingCount,"
        "places.websiteUri"
    )

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GOOGLE_PLACES_API_KEY or os.getenv("GOOGLE_MAPS_API_KEY", "")

    def search_competitors(
        self,
        location: str,
        category: str,
        coordinates: Optional[Dict[str, float]] = None,
        radius_km: float = 5.0,
        max_results: int = 4,
        language: str = "en",
    ) -> List[CompetitorItem]:
        if not self.api_key or not self.api_key.strip():
            logger.info("Google Places API key is not configured. Falling back to demo provider.")
            return []

        cat_meta = CentralizedCategoriesConfig.get_category_by_name(category) or {}
        search_terms = cat_meta.get("competitor_search_terms", [category])
        primary_term = search_terms[0] if search_terms else category
        town = location.split(",")[0].strip()

        # Build query: e.g. "dairy in Anand" or "kirana store in Anand"
        query_text = f"{primary_term} in {town}"

        # Construct request body for Places API (New)
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key.strip(),
            "X-Goog-FieldMask": self.FIELD_MASK,
        }

        body: Dict[str, Any] = {
            "textQuery": query_text,
            "maxResultCount": 10,  # Retrieve top 10 candidates for ranking/filtering
        }

        # Add language code
        lang = (language or "en").lower().strip()
        if lang in ("hi", "gu", "en"):
            body["languageCode"] = lang

        # Add locationBias circle restriction if coordinates are available
        center_lat = coordinates.get("latitude") if coordinates else None
        center_lng = coordinates.get("longitude") if coordinates else None

        if center_lat is not None and center_lng is not None:
            body["locationBias"] = {
                "circle": {
                    "center": {
                        "latitude": float(center_lat),
                        "longitude": float(center_lng),
                    },
                    "radius": float(radius_km * 1000.0),  # meters
                }
            }

        try:
            logger.info("Executing Google Places (New) searchText query for '%s' around %s", query_text, town)
            with httpx.Client(timeout=4.0) as client:
                response = client.post(self.PLACES_SEARCH_TEXT_URL, headers=headers, json=body)

            if response.status_code != 200:
                logger.warning(
                    "Google Places API returned HTTP status %d: %s",
                    response.status_code,
                    response.text[:200] if response.text else "",
                )
                return []

            data = response.json()
            raw_places = data.get("places", [])
            if not raw_places:
                logger.info("Google Places returned 0 places for '%s'.", query_text)
                return []

            return self._filter_and_rank_places(
                raw_places=raw_places,
                category=category,
                cat_meta=cat_meta,
                town=town,
                center_coords=(center_lat, center_lng) if (center_lat and center_lng) else None,
                radius_km=radius_km,
                max_results=max_results,
            )

        except Exception as e:
            logger.warning("Google Places request failed gracefully with error: %s", str(e))
            return []

    def _filter_and_rank_places(
        self,
        raw_places: List[Dict[str, Any]],
        category: str,
        cat_meta: Dict[str, Any],
        town: str,
        center_coords: Optional[Tuple[float, float]],
        radius_km: float,
        max_results: int,
    ) -> List[CompetitorItem]:
        sector = cat_meta.get("sector", "Rural Enterprise")
        banned_types = set(IRRELEVANT_TYPES_BY_SECTOR.get(sector, []))
        search_terms = [t.lower() for t in cat_meta.get("competitor_search_terms", [])]

        scored_places: List[Tuple[float, Dict[str, Any], Optional[float]]] = []

        for p in raw_places:
            p_name = p.get("displayName", {}).get("text", "")
            if not p_name or not p_name.strip():
                continue

            types = [t.lower() for t in p.get("types", [])]
            primary_type = (p.get("primaryType") or "").lower()

            # Filter out explicitly irrelevant types
            if primary_type in banned_types or any(t in banned_types for t in types):
                continue

            # Calculate distance if coordinates available
            p_loc = p.get("location", {})
            p_lat = p_loc.get("latitude")
            p_lng = p_loc.get("longitude")
            dist_km: Optional[float] = None

            if center_coords and p_lat is not None and p_lng is not None:
                dist_km = haversine_distance_km(center_coords[0], center_coords[1], float(p_lat), float(p_lng))
                # Reject places excessively outside the requested catchment (e.g. > 2.5x radius)
                if dist_km > (radius_km * 2.5):
                    continue

            # Relevance score
            score = 10.0
            name_lower = p_name.lower()

            # Bonus for matching search terms in name
            for term in search_terms:
                if term in name_lower:
                    score += 5.0

            # Bonus for having verified rating
            rating = p.get("rating")
            reviews = p.get("userRatingCount") or 0
            if rating:
                score += min(rating, 5.0)
            if reviews > 5:
                score += 2.0

            # Distance penalty (closer places rank higher)
            if dist_km is not None:
                score -= min(dist_km * 0.5, 8.0)

            scored_places.append((score, p, dist_km))

        # Sort descending by score
        scored_places.sort(key=lambda x: x[0], reverse=True)

        results: List[CompetitorItem] = []
        now_iso = datetime.now(timezone.utc).isoformat()

        for _, place, dist_km in scored_places[:max_results]:
            name = place.get("displayName", {}).get("text", "").strip()
            formatted_address = place.get("formattedAddress", f"{town}, Gujarat, India")
            place_id = place.get("id")
            primary_type = place.get("primaryType") or "Local Enterprise"
            readable_type = primary_type.replace("_", " ").title()

            # Real Google Maps URI
            map_url = place.get("googleMapsUri")
            if not map_url and place_id:
                map_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

            rating = place.get("rating")
            review_count = place.get("userRatingCount")
            website_url = place.get("websiteUri")
            p_loc = place.get("location", {})

            proximity_desc = f"{dist_km} km from {town} center" if dist_km is not None else f"Operating in {town} area"

            if rating and review_count:
                strengths = f"Established provider rating ({rating}★ across {review_count} verified reviews)"
            elif rating:
                strengths = f"Established provider rating ({rating}★)"
            else:
                strengths = "Verified business listing with active local presence"

            diff_strategy = (
                f"Differentiate {category} operations through transparent billing, direct WhatsApp ordering, "
                f"and dedicated rural doorstep fulfillment."
            )

            item = CompetitorItem(
                name=name,
                type_of_business=readable_type,
                proximity=proximity_desc,
                strengths=strengths,
                differentiation_strategy=diff_strategy,
                is_demo_data=False,
                data_source="Google Places API",
                location_status="Verified provider location",
                category=category,
                address=formatted_address,
                distance_km=dist_km,
                latitude=p_loc.get("latitude"),
                longitude=p_loc.get("longitude"),
                place_id=place_id,
                map_url=map_url,
                website_url=website_url,
                rating=float(rating) if rating is not None else None,
                review_count=int(review_count) if review_count is not None else None,
                source="Google Places",
                is_estimate=False,
                retrieved_at=now_iso,
            )
            results.append(item)

        return results


class DemoCompetitorProvider(CompetitorProvider):
    """
    Fallback provider producing generic, structured competitor archetypes.
    Guarantees strict B8.2 compliance:
    - is_demo_data = True
    - is_estimate = True
    - data_source = 'Indicative category-location profile'
    - location_status = 'Location unavailable — live mapping unavailable'
    - No fake coordinates, no fake map links, no fake reviews.
    """

    def search_competitors(
        self,
        location: str,
        category: str,
        coordinates: Optional[Dict[str, float]] = None,
        radius_km: float = 5.0,
        max_results: int = 4,
        language: str = "en",
    ) -> List[CompetitorItem]:
        from app.services.local_intelligence_service import LocalIntelligenceService

        cat = LocalIntelligenceService.resolve_category_meta(category)
        loc_info = LocalIntelligenceService.parse_location_details(location)

        # Delegate to LocalIntelligenceService for localized archetypes
        items = LocalIntelligenceService.generate_competitors(
            cat=cat,
            loc_info=loc_info,
            capital=100000.0,
            language=language,
        )

        lang = (language or "en").lower().strip()
        loc_status = (
            "स्थान अनुपलब्ध — लाइव मैपिंग अनुपलब्ધ (चरण B9 नियोजित)"
            if lang == "hi"
            else (
                "સ્થાન ઉપલબ્ધ નથી — લાઇવ મેપિંગ ઉપલબ્ધ નથી (ફેઝ B9 આયોજિત)"
                if lang == "gu"
                else "Location unavailable — live mapping unavailable (planned for Phase B9)"
            )
        )

        sanitized: List[CompetitorItem] = []
        for it in items[:max_results]:
            # Ensure demo metadata is explicitly enforced
            it.is_demo_data = True
            it.is_estimate = True
            it.data_source = "Indicative category-location profile"
            it.location_status = loc_status
            it.map_url = None
            it.latitude = None
            it.longitude = None
            it.distance_km = None
            it.place_id = None
            it.rating = None
            it.review_count = None
            it.website_url = None
            it.source = "Indicative Benchmark"
            sanitized.append(it)

        return sanitized


class CompetitorService:
    """
    Master competitor discovery service orchestrating location geocoding,
    provider execution, in-memory caching, and transparent fallback.
    """

    def __init__(
        self,
        google_provider: Optional[CompetitorProvider] = None,
        demo_provider: Optional[CompetitorProvider] = None,
    ):
        self.google_provider = google_provider or GooglePlacesProvider()
        self.demo_provider = demo_provider or DemoCompetitorProvider()
        # In-memory cache: key -> (timestamp, List[CompetitorItem])
        self._cache: Dict[str, Tuple[float, List[CompetitorItem]]] = {}
        self.cache_ttl_seconds = 3600  # 1 hour TTL

    def resolve_coordinates(
        self, location: str, location_detail: Optional[Any] = None
    ) -> Optional[Dict[str, float]]:
        """Resolves target geographic coordinates from input model or catalog."""
        # 1. Check if location_detail is provided with coordinates
        if location_detail is not None:
            lat = getattr(location_detail, "latitude", None)
            lng = getattr(location_detail, "longitude", None)
            if lat is not None and lng is not None:
                return {"latitude": float(lat), "longitude": float(lng)}
            if isinstance(location_detail, dict):
                lat = location_detail.get("latitude")
                lng = location_detail.get("longitude")
                if lat is not None and lng is not None:
                    return {"latitude": float(lat), "longitude": float(lng)}

        # 2. Query LocalCatalogLocationProvider
        provider = get_location_provider()
        matches = provider.search_locations(query=location, limit=3)
        for m in matches:
            if m.latitude is not None and m.longitude is not None:
                return {"latitude": float(m.latitude), "longitude": float(m.longitude)}

        return None

    def find_competitors(
        self,
        location: str,
        category: str,
        capital: float = 100000.0,
        location_detail: Optional[Any] = None,
        language: str = "en",
        radius_km: Optional[float] = None,
        max_results: Optional[int] = None,
    ) -> List[CompetitorItem]:
        """
        Main competitor discovery method.
        Attempts real provider first; gracefully falls back to demo provider.
        """
        clean_loc = (location or "Anand, Gujarat").strip()
        clean_cat = (category or "Dairy").strip()
        rad = float(radius_km or settings.COMPETITOR_SEARCH_RADIUS_KM or 5.0)
        limit = int(max_results or settings.COMPETITOR_MAX_RESULTS or 4)
        lang = (language or "en").lower().strip()

        coords = self.resolve_coordinates(clean_loc, location_detail)
        lat_key = round(coords["latitude"], 3) if coords else 0.0
        lng_key = round(coords["longitude"], 3) if coords else 0.0

        cache_key = f"{clean_loc.lower()}|{lat_key}|{lng_key}|{clean_cat.lower()}|{rad}|{lang}"

        # Check cache
        if cache_key in self._cache:
            ts, cached_items = self._cache[cache_key]
            if (time.time() - ts) < self.cache_ttl_seconds:
                logger.info("Returning %d cached competitors for key: %s", len(cached_items), cache_key)
                return cached_items

        results: List[CompetitorItem] = []

        # Attempt real provider if API key is present
        if settings.GOOGLE_PLACES_API_KEY:
            try:
                results = self.google_provider.search_competitors(
                    location=clean_loc,
                    category=clean_cat,
                    coordinates=coords,
                    radius_km=rad,
                    max_results=limit,
                    language=lang,
                )
            except Exception as e:
                logger.warning("Error in real competitor discovery: %s", str(e))
                results = []

        # Fallback to demo provider if zero real results or no key
        if not results:
            logger.info("No real provider results obtained for %s in %s; using demo fallback.", clean_cat, clean_loc)
            results = self.demo_provider.search_competitors(
                location=clean_loc,
                category=clean_cat,
                coordinates=coords,
                radius_km=rad,
                max_results=limit,
                language=lang,
            )

        # Store in cache
        if results:
            self._cache[cache_key] = (time.time(), results)

        return results[:limit]


# Global singleton instance
competitor_service = CompetitorService()
