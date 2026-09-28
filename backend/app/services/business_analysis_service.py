"""
Phase B3 — Business Analysis Service
Coordinates business analysis and acts as the service layer between API and Engine/Repository.
"""

from typing import Any, Dict, Optional
from app.engines.business_analysis_engine import (
    analyze_business_profile,
    validate_business_inputs,
    BusinessAnalysisValidationError,
)
from app.data.data_provider import BaseDataProvider, get_data_provider


class BusinessAnalysisService:
    """Service layer coordinating dynamic business intelligence analysis."""

    def __init__(self, data_provider: Optional[BaseDataProvider] = None):
        self.data_provider = data_provider or get_data_provider()

    def analyze(
        self,
        location: Any,
        business_category: Any,
        available_capital: Any,
    ) -> Dict[str, Any]:
        """
        Validates inputs and returns structured business analysis intelligence.
        """
        validated = validate_business_inputs(
            location=location,
            business_category=business_category,
            available_capital=available_capital,
            data_provider=self.data_provider,
        )

        return analyze_business_profile(
            location=validated["location"],
            business_category=validated["business_category"],
            available_capital=validated["available_capital"],
            data_provider=self.data_provider,
        )


# Singleton service instance
_service_instance: Optional[BusinessAnalysisService] = None


def get_business_analysis_service() -> BusinessAnalysisService:
    global _service_instance
    if _service_instance is None:
        _service_instance = BusinessAnalysisService()
    return _service_instance
