"""
Location Provider Abstraction for Phase B7.
Provides search and geocoding capabilities for rural, taluka, and town locations.
Guarantees offline resilience, zero hardcoded API keys, zero exposed secrets.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import logging
from app.schemas.schemas import LocationData

logger = logging.getLogger(__name__)

# Pre-populated rich catalog of rural centers, talukas, and town districts in Gujarat and India
RURAL_LOCATION_CATALOG: List[Dict[str, Any]] = [
    # Gujarat - Anand & Kheda Region
    {
        "village_town_city": "Anand",
        "taluka_subdistrict": "Anand Taluka",
        "district": "Anand",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.5645,
        "longitude": 72.9289,
        "tags": ["dairy hub", "amul", "charotar", "vidyanagar", "central gujarat"]
    },
    {
        "village_town_city": "Vallabh Vidyanagar",
        "taluka_subdistrict": "Anand Taluka",
        "district": "Anand",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.5458,
        "longitude": 72.9304,
        "tags": ["education", "charotar", "engineering", "youth market"]
    },
    {
        "village_town_city": "Petlad",
        "taluka_subdistrict": "Petlad Taluka",
        "district": "Anand",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.4742,
        "longitude": 72.8021,
        "tags": ["textile", "rural trade", "tobacco", "mandi"]
    },
    {
        "village_town_city": "Khambhat",
        "taluka_subdistrict": "Khambhat Taluka",
        "district": "Anand",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.3129,
        "longitude": 72.6192,
        "tags": ["agate", "coastal", "halvasan", "handicrafts", "fisheries"]
    },
    {
        "village_town_city": "Borsad",
        "taluka_subdistrict": "Borsad Taluka",
        "district": "Anand",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.4116,
        "longitude": 72.9009,
        "tags": ["charotar", "tobacco", "spices", "agro mandi"]
    },
    {
        "village_town_city": "Nadiad",
        "taluka_subdistrict": "Nadiad Taluka",
        "district": "Kheda",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.6916,
        "longitude": 72.8634,
        "tags": ["santram", "textile", "kheda", "commercial town"]
    },
    {
        "village_town_city": "Dakor",
        "taluka_subdistrict": "Thasra Taluka",
        "district": "Kheda",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.7547,
        "longitude": 73.1501,
        "tags": ["temple town", "pilgrimage", "gota", "cottage industry", "sweets"]
    },
    # Gujarat - Surat & South Gujarat
    {
        "village_town_city": "Bardoli",
        "taluka_subdistrict": "Bardoli Taluka",
        "district": "Surat",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.1214,
        "longitude": 73.1118,
        "tags": ["sugar cooperative", "satyagraha", "agro processing", "south gujarat"]
    },
    {
        "village_town_city": "Mandvi (Surat)",
        "taluka_subdistrict": "Mandvi Taluka",
        "district": "Surat",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.2581,
        "longitude": 73.3039,
        "tags": ["tribal belt", "agriculture", "forestry", "tapi"]
    },
    {
        "village_town_city": "Navsari",
        "taluka_subdistrict": "Navsari Taluka",
        "district": "Navsari",
        "state": "Gujarat",
        "country": "India",
        "latitude": 20.9467,
        "longitude": 72.9520,
        "tags": ["diamonds", "chikoo", "agriculture", "textile"]
    },
    {
        "village_town_city": "Bilimora",
        "taluka_subdistrict": "Gandevi Taluka",
        "district": "Navsari",
        "state": "Gujarat",
        "country": "India",
        "latitude": 20.7600,
        "longitude": 72.9500,
        "tags": ["chikoo processing", "mango pulp", "coastal trade"]
    },
    {
        "village_town_city": "Vyara",
        "taluka_subdistrict": "Vyara Taluka",
        "district": "Tapi",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.1167,
        "longitude": 73.4000,
        "tags": ["tribal crafts", "bamboo", "paddy", "dairy"]
    },
    {
        "village_town_city": "Ahwa",
        "taluka_subdistrict": "Ahwa Taluka",
        "district": "Dang",
        "state": "Gujarat",
        "country": "India",
        "latitude": 20.7578,
        "longitude": 73.6841,
        "tags": ["dang", "bamboo handicrafts", "forest produce", "tribal artisans", "herbal"]
    },
    {
        "village_town_city": "Ankleshwar",
        "taluka_subdistrict": "Ankleshwar Taluka",
        "district": "Bharuch",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.6264,
        "longitude": 73.0152,
        "tags": ["chemical", "msme industrial", "logistics hub"]
    },
    {
        "village_town_city": "Rajpipla",
        "taluka_subdistrict": "Nandod Taluka",
        "district": "Narmada",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.8711,
        "longitude": 73.5028,
        "tags": ["statue of unity corridor", "tourism handicrafts", "horticulture", "banana"]
    },
    # Gujarat - Saurashtra & Kutch
    {
        "village_town_city": "Rajkot",
        "taluka_subdistrict": "Rajkot Taluka",
        "district": "Rajkot",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.3039,
        "longitude": 70.8022,
        "tags": ["engineering", "auto components", "diesel engines", "saurashtra hub"]
    },
    {
        "village_town_city": "Gondal",
        "taluka_subdistrict": "Gondal Taluka",
        "district": "Rajkot",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.9619,
        "longitude": 70.7997,
        "tags": ["chilli mandi", "groundnut", "oil mills", "heritage tourism"]
    },
    {
        "village_town_city": "Morbi",
        "taluka_subdistrict": "Morbi Taluka",
        "district": "Morbi",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.8120,
        "longitude": 70.8378,
        "tags": ["ceramics", "clock manufacturing", "wall tiles", "export cluster"]
    },
    {
        "village_town_city": "Bhuj",
        "taluka_subdistrict": "Bhuj Taluka",
        "district": "Kutch",
        "state": "Gujarat",
        "country": "India",
        "latitude": 23.2420,
        "longitude": 69.6669,
        "tags": ["kutch embroidery", "handicrafts", "rogan art", "handloom", "heritage"]
    },
    {
        "village_town_city": "Mandvi (Kutch)",
        "taluka_subdistrict": "Mandvi Taluka",
        "district": "Kutch",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.8333,
        "longitude": 69.3500,
        "tags": ["wooden shipbuilding", "coastal port", "tourism", "dates harvesting"]
    },
    {
        "village_town_city": "Anjar",
        "taluka_subdistrict": "Anjar Taluka",
        "district": "Kutch",
        "state": "Gujarat",
        "country": "India",
        "latitude": 23.1139,
        "longitude": 70.0278,
        "tags": ["textile", "cutlery", "metalcrafts", "kutch trade"]
    },
    {
        "village_town_city": "Junagadh",
        "taluka_subdistrict": "Junagadh Taluka",
        "district": "Junagadh",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.5222,
        "longitude": 70.4579,
        "tags": ["gir nar", "kesar mango", "groundnut oil", "tourism", "agro mandi"]
    },
    {
        "village_town_city": "Veraval",
        "taluka_subdistrict": "Patan-Veraval Taluka",
        "district": "Gir Somnath",
        "state": "Gujarat",
        "country": "India",
        "latitude": 20.9000,
        "longitude": 70.3667,
        "tags": ["fisheries port", "fish processing", "somnath temple", "marine exports"]
    },
    {
        "village_town_city": "Amreli",
        "taluka_subdistrict": "Amreli Taluka",
        "district": "Amreli",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.6032,
        "longitude": 71.2221,
        "tags": ["cotton ginning", "diamond polishing", "sesame", "groundnut"]
    },
    {
        "village_town_city": "Bhavnagar",
        "taluka_subdistrict": "Bhavnagar Taluka",
        "district": "Bhavnagar",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.7645,
        "longitude": 72.1519,
        "tags": ["onion dehydration", "ganthiya snacks", "ship recycling", "diamond"]
    },
    {
        "village_town_city": "Mahuva",
        "taluka_subdistrict": "Mahuva Taluka",
        "district": "Bhavnagar",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.0914,
        "longitude": 71.7634,
        "tags": ["dehydrated onion", "garlic", "wooden toys", "coconut farming"]
    },
    {
        "village_town_city": "Surendranagar",
        "taluka_subdistrict": "Wadhwan Taluka",
        "district": "Surendranagar",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.7277,
        "longitude": 71.6370,
        "tags": ["cotton hub", "ginning", "salt production", "ceramics"]
    },
    # Gujarat - North & Central Gujarat
    {
        "village_town_city": "Gandhinagar",
        "taluka_subdistrict": "Gandhinagar Taluka",
        "district": "Gandhinagar",
        "state": "Gujarat",
        "country": "India",
        "latitude": 23.2156,
        "longitude": 72.6369,
        "tags": ["state capital", "it hub", "green city", "electronics"]
    },
    {
        "village_town_city": "Sanand",
        "taluka_subdistrict": "Sanand Taluka",
        "district": "Ahmedabad",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.9868,
        "longitude": 72.3813,
        "tags": ["auto manufacturing", "semiconductor corridor", "fmcg cluster"]
    },
    {
        "village_town_city": "Mehsana",
        "taluka_subdistrict": "Mehsana Taluka",
        "district": "Mehsana",
        "state": "Gujarat",
        "country": "India",
        "latitude": 23.5880,
        "longitude": 72.3693,
        "tags": ["dudh sagar dairy", "oil and gas", "spices mandi", "cumin", "fennel"]
    },
    {
        "village_town_city": "Unjha",
        "taluka_subdistrict": "Unjha Taluka",
        "district": "Mehsana",
        "state": "Gujarat",
        "country": "India",
        "latitude": 23.8039,
        "longitude": 72.3925,
        "tags": ["asia largest spice market", "cumin", "isabgol", "mustard", "coriander"]
    },
    {
        "village_town_city": "Palanpur",
        "taluka_subdistrict": "Palanpur Taluka",
        "district": "Banaskantha",
        "state": "Gujarat",
        "country": "India",
        "latitude": 24.1724,
        "longitude": 72.4346,
        "tags": ["banas dairy", "potato cold storage", "diamond traders", "attar perfumes"]
    },
    {
        "village_town_city": "Deesa",
        "taluka_subdistrict": "Deesa Taluka",
        "district": "Banaskantha",
        "state": "Gujarat",
        "country": "India",
        "latitude": 24.2586,
        "longitude": 72.1797,
        "tags": ["potato hub", "cold storage cluster", "groundnut", "banas river"]
    },
    {
        "village_town_city": "Himatnagar",
        "taluka_subdistrict": "Himatnagar Taluka",
        "district": "Sabarkantha",
        "state": "Gujarat",
        "country": "India",
        "latitude": 23.5977,
        "longitude": 72.9698,
        "tags": ["sabar dairy", "ceramic tiles", "groundnut oil", "cotton"]
    },
    {
        "village_town_city": "Dahod",
        "taluka_subdistrict": "Dahod Taluka",
        "district": "Dahod",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.8375,
        "longitude": 74.2536,
        "tags": ["tribal hub", "railway locomotive", "maize", "pulses", "border trade"]
    },
    {
        "village_town_city": "Godhra",
        "taluka_subdistrict": "Godhra Taluka",
        "district": "Panchmahal",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.7758,
        "longitude": 73.6149,
        "tags": ["panchamrut dairy", "flour mills", "timber", "granite"]
    },
    {
        "village_town_city": "Chhota Udaipur",
        "taluka_subdistrict": "Chhota Udaipur Taluka",
        "district": "Chhota Udaipur",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.3089,
        "longitude": 74.0150,
        "tags": ["pithora painting", "tribal crafts", "dolomite mining", "forestry"]
    },
    # Key National Rural/Agrarian Centers across India
    {
        "village_town_city": "Kolhapur",
        "taluka_subdistrict": "Karveer Taluka",
        "district": "Kolhapur",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 16.7050,
        "longitude": 74.2433,
        "tags": ["kolhapuri chappal", "jaggery mandi", "sugarcane", "foundry"]
    },
    {
        "village_town_city": "Baramati",
        "taluka_subdistrict": "Baramati Taluka",
        "district": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 18.1517,
        "longitude": 74.5770,
        "tags": ["agro tourism", "sugarcane", "dairy", "poultry cluster"]
    },
    {
        "village_town_city": "Varanasi",
        "taluka_subdistrict": "Varanasi Taluka",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "country": "India",
        "latitude": 25.3176,
        "longitude": 82.9739,
        "tags": ["banarasi saree", "silk weaving", "handloom cluster", "tourism"]
    },
    {
        "village_town_city": "Gorakhpur",
        "taluka_subdistrict": "Gorakhpur Sadar",
        "district": "Gorakhpur",
        "state": "Uttar Pradesh",
        "country": "India",
        "latitude": 26.7606,
        "longitude": 83.3732,
        "tags": ["terracotta craft", "agro mandi", "sugarcane", "handicrafts"]
    },
    {
        "village_town_city": "Indore",
        "taluka_subdistrict": "Indore Taluka",
        "district": "Indore",
        "state": "Madhya Pradesh",
        "country": "India",
        "latitude": 22.7196,
        "longitude": 75.8577,
        "tags": ["soybean mandi", "namkeen snacks", "textile", "commercial hub"]
    },
    {
        "village_town_city": "Jodhpur",
        "taluka_subdistrict": "Jodhpur Taluka",
        "district": "Jodhpur",
        "state": "Rajasthan",
        "country": "India",
        "latitude": 26.2389,
        "longitude": 73.0243,
        "tags": ["wooden furniture export", "handicrafts", "spices", "marwar"]
    },
    {
        "village_town_city": "Coimbatore",
        "taluka_subdistrict": "Coimbatore South",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "country": "India",
        "latitude": 11.0168,
        "longitude": 76.9558,
        "tags": ["textile machinery", "motor pumps", "poultry", "agro engineering"]
    }
]


class BaseLocationProvider(ABC):
    """Abstract interface for location search, autocomplete, and geocoding."""

    @abstractmethod
    def search_locations(self, query: str, limit: int = 8) -> List[LocationData]:
        """Search and return location models matching query string."""
        pass


class LocalCatalogLocationProvider(BaseLocationProvider):
    """
    Offline-first rural location provider backed by structured regional data.
    Provides immediate zero-latency matches without external internet dependency.
    """

    def __init__(self, catalog: Optional[List[Dict[str, Any]]] = None):
        self.catalog = catalog or RURAL_LOCATION_CATALOG

    def search_locations(self, query: str, limit: int = 8) -> List[LocationData]:
        if not query or not query.strip():
            # Return top 5 representative hubs when empty query requested
            top_hubs = self.catalog[:limit]
            return [self._to_location_data(item, query) for item in top_hubs]

        q = query.strip().lower()
        results: List[Dict[str, Any]] = []

        # 1. Exact or prefix matches on village/town/city
        for item in self.catalog:
            city = item.get("village_town_city", "").lower()
            if city.startswith(q) or q in city:
                if item not in results:
                    results.append(item)

        # 2. Matches on Taluka or District
        for item in self.catalog:
            taluka = item.get("taluka_subdistrict", "").lower()
            district = item.get("district", "").lower()
            state = item.get("state", "").lower()
            if q in taluka or q in district or q in state:
                if item not in results:
                    results.append(item)

        # 3. Matches on descriptive tags
        for item in self.catalog:
            tags = [t.lower() for t in item.get("tags", [])]
            if any(q in t for t in tags):
                if item not in results:
                    results.append(item)

        # Return up to limit matches
        final_list = [self._to_location_data(item, query) for item in results[:limit]]

        # If zero matches found in local catalog, return fallback custom location item
        if not final_list:
            final_list.append(
                LocationData(
                    raw_input=query.strip(),
                    village_town_city=query.strip(),
                    state="Gujarat" if "gujarat" in q else None,
                    country="India",
                    formatted_address=f"{query.strip()}, India",
                    provider="user_custom",
                )
            )

        return final_list

    def _to_location_data(self, item: Dict[str, Any], raw_query: str) -> LocationData:
        parts = [
            item.get("village_town_city"),
            item.get("taluka_subdistrict"),
            item.get("district"),
            item.get("state"),
            item.get("country", "India"),
        ]
        # Build clean formatted address
        clean_parts = [p for p in parts if p]
        formatted = ", ".join(clean_parts)

        return LocationData(
            raw_input=raw_query or formatted,
            village_town_city=item.get("village_town_city"),
            taluka_subdistrict=item.get("taluka_subdistrict"),
            district=item.get("district"),
            state=item.get("state"),
            country=item.get("country", "India"),
            latitude=item.get("latitude"),
            longitude=item.get("longitude"),
            formatted_address=formatted,
            provider="local_catalog",
        )


# Singleton instance
_location_provider_instance: Optional[BaseLocationProvider] = None


def get_location_provider() -> BaseLocationProvider:
    """Factory function returning active location provider."""
    global _location_provider_instance
    if _location_provider_instance is None:
        _location_provider_instance = LocalCatalogLocationProvider()
    return _location_provider_instance
