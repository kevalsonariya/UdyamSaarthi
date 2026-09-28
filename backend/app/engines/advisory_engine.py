"""
Advisory Engine - delegates to the modular Business Analysis Engine.
Maintains backward compatibility for existing services.
"""

from typing import Dict, Any
from app.engines.business_analysis_engine import analyze_business_profile


def generate_advisory_profile(
    location: str,
    business_category: str,
    project_cost: float,
) -> Dict[str, Any]:
    """
    Generates structured hyper-local advisory intelligence using the modular Business Analysis Engine.
    """
    # Estimate available margin capital (10% of project cost)
    available_capital = max(1000.0, project_cost * 0.10)

    analysis = analyze_business_profile(
        location=location,
        business_category=business_category,
        available_capital=available_capital,
    )

    return {
        "business": analysis["business"],
        "market": analysis["market"],
        "opportunities": analysis["opportunities"],
        "swot": analysis["swot"],
        "risks": analysis["risks"],
        "competitors": analysis["competitors"],
        "pricing": analysis["pricing"],
        "recommendation": analysis["recommendation"],
        "metadata": analysis["metadata"],
    }
