"""
Data Provider abstraction and Local JSON implementation for Phase B3.
Enables clean separation between data access and business-analysis logic.
"""

from abc import ABC, abstractmethod
import json
import os
from typing import Any, Dict, List, Optional


class BaseDataProvider(ABC):
    """
    Abstract interface for retrieving market, competitive, and pricing datasets.
    Can be implemented by local demo providers or future live API integrations.
    """

    @abstractmethod
    def get_supported_categories(self) -> List[str]:
        """Return list of supported standard category names."""
        pass

    @abstractmethod
    def resolve_category(self, raw_category_name: str) -> Optional[Dict[str, Any]]:
        """Finds matching category metadata given user-supplied string, or None if unsupported."""
        pass

    @abstractmethod
    def get_market_profile(self, category_id: str, location: str) -> Optional[Dict[str, Any]]:
        """Returns market reach, customer segments, channels, and SWOT data."""
        pass

    @abstractmethod
    def get_location_profile(self, location: str) -> Dict[str, Any]:
        """Returns regional economic characteristics and favorable multiplier for location."""
        pass

    @abstractmethod
    def get_competitors(self, category_id: str, location: str) -> List[Dict[str, Any]]:
        """Returns list of typical competitors for category & location."""
        pass

    @abstractmethod
    def get_pricing_profile(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Returns pricing benchmarks, unit cost, suggested retail, and margins."""
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Returns data source provenance indicating whether data is live or demo."""
        pass


class LocalJsonDataProvider(BaseDataProvider):
    """
    Local JSON data provider implementation.
    Reads datasets from app/data/ directory and serves structured intelligence.
    """

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = data_dir

        self.categories_data: Dict[str, Any] = self._load_json("business_categories.json")
        self.market_data: Dict[str, Any] = self._load_json("market_data.json")
        self.competitors_data: Dict[str, Any] = self._load_json("competitors.json")
        self.pricing_data: Dict[str, Any] = self._load_json("pricing_data.json")

    def _load_json(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def get_supported_categories(self) -> List[str]:
        return [cat["name"] for cat in self.categories_data.get("categories", [])]

    def resolve_category(self, raw_category_name: str) -> Optional[Dict[str, Any]]:
        if not raw_category_name or not isinstance(raw_category_name, str):
            return None

        query = raw_category_name.strip().lower()
        if not query:
            return None

        # 1. Exact match on name
        for cat in self.categories_data.get("categories", []):
            if cat["name"].lower() == query:
                return cat

        # 2. Match on aliases
        for cat in self.categories_data.get("categories", []):
            for alias in cat.get("aliases", []):
                if alias.lower() in query or query in alias.lower():
                    return cat

        # 3. Partial substring match
        for cat in self.categories_data.get("categories", []):
            if cat["name"].lower() in query or query in cat["name"].lower():
                return cat

        return None

    def get_location_profile(self, location: str) -> Dict[str, Any]:
        loc_clean = location.strip().lower() if location else ""
        locations = self.market_data.get("location_profiles", {})

        for key, loc_data in locations.items():
            if key in loc_clean or loc_data.get("name", "").lower() in loc_clean:
                return loc_data

        # Fallback to default rural/semi-urban profile
        default_prof = locations.get("default_rural", {
            "name": location.strip() if location else "Local Catchment",
            "characteristics": "Agrarian economy with periodic harvest liquidity and growing digital smartphone adoption.",
            "favorable_categories": ["Grocery", "Services", "Dairy", "Agriculture"],
            "multiplier": 1.0,
        })
        return default_prof

    def get_market_profile(self, category_id: str, location: str) -> Optional[Dict[str, Any]]:
        return self.market_data.get("market_profiles", {}).get(category_id)

    def get_competitors(self, category_id: str, location: str) -> List[Dict[str, Any]]:
        comps = self.competitors_data.get("competitor_profiles", {}).get(category_id, [])
        return comps

    def get_pricing_profile(self, category_id: str) -> Optional[Dict[str, Any]]:
        return self.pricing_data.get("pricing_profiles", {}).get(category_id)

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "data_source": "prototype_demo_data",
            "is_live_data": False,
            "note": "Prototype demo datasets. Not verified live/real-time market data.",
            "version": "1.0-prototype",
        }


# Singleton instance for repository access
_provider_instance: Optional[BaseDataProvider] = None


def get_data_provider() -> BaseDataProvider:
    """Factory function returning the active Data Provider implementation."""
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = LocalJsonDataProvider()
    return _provider_instance
