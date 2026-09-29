"""
Phase B3 — Business Analysis Engine
Implements dynamic business, market, SWOT, competitive, and pricing analysis.
Decoupled from data loading via BaseDataProvider.
"""

import math
from typing import Any, Dict, List, Optional
from app.data.data_provider import BaseDataProvider, get_data_provider
from app.schemas.schemas import (
    MarketReachAnalysis,
    OpportunityAnalysis,
    SWOTAnalysis,
    RiskItem,
    CompetitorItem,
    PricingGuidance,
    BusinessRecommendation,
)


class BusinessAnalysisValidationError(Exception):
    """Exception raised when business analysis input validation fails."""
    def __init__(self, message: str, field: Optional[str] = None, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code


def validate_business_inputs(
    location: Any,
    business_category: Any,
    available_capital: Any,
    data_provider: Optional[BaseDataProvider] = None,
) -> Dict[str, Any]:
    """
    Validates all inputs for business analysis:
    - Rejects missing / empty location
    - Rejects missing / empty / unsupported business category
    - Rejects missing / non-numeric / zero / negative / excessive capital
    Returns normalized dictionary of validated inputs and category metadata.
    """
    if data_provider is None:
        data_provider = get_data_provider()

    # 1. Location Validation
    if location is None:
        raise BusinessAnalysisValidationError(
            "Missing required field: 'location' cannot be None.",
            field="location",
            code="MISSING_LOCATION",
        )
    if not isinstance(location, str) or not location.strip():
        raise BusinessAnalysisValidationError(
            "Location cannot be empty. Please specify a valid target town, village, or district.",
            field="location",
            code="EMPTY_LOCATION",
        )
    clean_location = location.strip()

    # 2. Business Category Validation
    if business_category is None:
        raise BusinessAnalysisValidationError(
            "Missing required field: 'business_category' cannot be None.",
            field="business_category",
            code="MISSING_CATEGORY",
        )
    if not isinstance(business_category, str) or not business_category.strip():
        raise BusinessAnalysisValidationError(
            "Business category cannot be empty.",
            field="business_category",
            code="EMPTY_CATEGORY",
        )
    clean_category = business_category.strip()

    resolved_category = data_provider.resolve_category(clean_category)
    if resolved_category is None:
        supported = ", ".join(data_provider.get_supported_categories())
        raise BusinessAnalysisValidationError(
            f"Unsupported business category: '{clean_category}'. Supported categories are: {supported}.",
            field="business_category",
            code="UNSUPPORTED_CATEGORY",
        )

    # 3. Available Capital Validation
    if available_capital is None:
        raise BusinessAnalysisValidationError(
            "Missing required field: 'available_capital' cannot be None.",
            field="available_capital",
            code="MISSING_CAPITAL",
        )

    if isinstance(available_capital, bool):
        raise BusinessAnalysisValidationError(
            "Invalid non-numeric value for 'available_capital': boolean is not permitted.",
            field="available_capital",
            code="NON_NUMERIC",
        )

    if not isinstance(available_capital, (int, float, str)):
        raise BusinessAnalysisValidationError(
            f"Invalid non-numeric value for 'available_capital': type {type(available_capital).__name__} is not supported.",
            field="available_capital",
            code="NON_NUMERIC",
        )

    try:
        cap = float(available_capital)
    except (ValueError, TypeError):
        raise BusinessAnalysisValidationError(
            f"Invalid non-numeric value for 'available_capital': '{available_capital}'.",
            field="available_capital",
            code="NON_NUMERIC",
        )

    if math.isnan(cap) or math.isinf(cap):
        raise BusinessAnalysisValidationError(
            "Available capital must be a finite real number.",
            field="available_capital",
            code="NON_FINITE",
        )

    if cap == 0.0:
        raise BusinessAnalysisValidationError(
            "Available capital must be greater than zero.",
            field="available_capital",
            code="ZERO_CAPITAL",
        )

    if cap < 0.0:
        raise BusinessAnalysisValidationError(
            f"Available capital cannot be negative, got {cap:,.2f}.",
            field="available_capital",
            code="NEGATIVE_CAPITAL",
        )

    if cap > 500000.0:
        raise BusinessAnalysisValidationError(
            f"Available capital ₹{cap:,.2f} produces project cost exceeding ₹50,00,000 maximum scheme ceiling.",
            field="available_capital",
            code="EXCEEDS_MAX_CAPITAL",
        )

    return {
        "location": clean_location,
        "business_category": clean_category,
        "resolved_category": resolved_category,
        "available_capital": cap,
    }


def analyze_business_profile(
    location: str,
    business_category: str,
    available_capital: float,
    data_provider: Optional[BaseDataProvider] = None,
    location_detail: Optional[Any] = None,
    language: str = "en",
) -> Dict[str, Any]:
    """
    Executes dynamic business analysis based on location, business_category, available_capital, and language.
    Produces:
    - business
    - market
    - opportunities
    - swot
    - risks
    - competitors
    - pricing
    - recommendation
    - metadata (transparency flag)
    """
    if data_provider is None:
        data_provider = get_data_provider()

    validated = validate_business_inputs(
        location=location,
        business_category=business_category,
        available_capital=available_capital,
        data_provider=data_provider,
    )

    loc = validated["location"]
    cap = validated["available_capital"]
    cat = validated["resolved_category"]
    cat_id = cat["id"]
    cat_name = cat["name"]
    raw_cat = validated["business_category"]
    from app.services.local_intelligence_service import LocalIntelligenceService
    from app.data.categories_config import CentralizedCategoriesConfig

    resolved_cat_name = (
        raw_cat
        if CentralizedCategoriesConfig.get_category_by_name(raw_cat)
        else cat_name
    )

    return LocalIntelligenceService.generate_complete_intelligence(
        location=loc,
        business_category=resolved_cat_name,
        available_capital=cap,
        location_detail=location_detail,
        language=language,
    )

