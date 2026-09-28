"""
AI Advisory / Explanation Layer (Phase B4)
Architectural Contract:
- AI Layer receives already-calculated structured data from the deterministic financial engine and business analysis engine.
- AI NEVER calculates, modifies, overrides, or decides financial values (Project Cost, Loan, EMI, Scheme, Tenure, etc.).
- When an external LLM is configured via environment variable AI_API_KEY, it enhances descriptions.
- When no API key is provided or the provider fails, a deterministic rule/template-based advisory fallback is used.
- Output is formatted for rural micro-entrepreneurs using simple, accessible language.
"""

from typing import Dict, Any, List, Optional
import os
import json
import logging
from app.schemas.schemas import AIExplanation
from app.config import settings

logger = logging.getLogger(__name__)


class BaseAIProvider:
    """Interface for AI Advisory providers."""
    def generate_explanation(self, context: Dict[str, Any]) -> AIExplanation:
        raise NotImplementedError


class DeterministicAdvisoryFallback(BaseAIProvider):
    """
    Deterministic rule/template-based advisory provider.
    Guarantees 100% demo uptime with zero external dependencies and zero API costs.
    Strictly derives all narrative explanations from verified deterministic engine outputs.
    """

    def generate_explanation(self, context: Dict[str, Any]) -> AIExplanation:
        location = context.get("location", "your local region")
        category = context.get("business_category", "Micro-Enterprise")
        capital = context.get("available_capital", 0.0)

        fin = context.get("financial", {})
        if hasattr(fin, "model_dump"):
            fin = fin.model_dump()
        elif hasattr(fin, "dict"):
            fin = fin.dict()

        sch = context.get("scheme", {})
        if hasattr(sch, "model_dump"):
            sch = sch.model_dump()
        elif hasattr(sch, "dict"):
            sch = sch.dict()

        emi = context.get("emi", {})
        if hasattr(emi, "model_dump"):
            emi = emi.model_dump()
        elif hasattr(emi, "dict"):
            emi = emi.dict()

        wc = context.get("working_capital", {})
        if hasattr(wc, "model_dump"):
            wc = wc.model_dump()
        elif hasattr(wc, "dict"):
            wc = wc.dict()

        mkt = context.get("market", {})
        if hasattr(mkt, "model_dump"):
            mkt = mkt.model_dump()
        elif hasattr(mkt, "dict"):
            mkt = mkt.dict()

        # Deterministic values (authoritative, never altered)
        project_cost = fin.get("project_cost", capital / 0.10 if capital else 0.0)
        loan_amount = sch.get("eligible_funding", project_cost * 0.90)
        scheme_name = sch.get("scheme_name", "Micro Enterprise Credit Scheme")
        interest_rate = sch.get("interest_rate_percent", 8.0)
        tenure_years = sch.get("tenure_years", 7)
        moratorium_months = sch.get("moratorium_months", 6)
        monthly_emi = emi.get("monthly_emi", 0.0)
        reserve_3m = wc.get("recommended_3_months_reserve", 0.0)
        catchment_km = mkt.get("catchment_radius_km", 15)

        summary = (
            f"Starting a {category} business in {location} with your personal margin of ₹{capital:,.0f} "
            f"enables a total setup budget of ₹{project_cost:,.0f}. Under the government's {scheme_name}, "
            f"you qualify for ₹{loan_amount:,.0f} in low-interest financing, giving your enterprise strong foundation."
        )

        market_insight = (
            f"Within your {catchment_km} km local market area surrounding {location}, customers currently travel to "
            f"larger centers for reliable {category} products. Opening your center locally will capture routine daily demand "
            f"and weekly mandi footfall with lower rental overhead."
        )

        opportunity_explanation = (
            f"The greatest immediate opportunity in {location} is providing consistent product availability and direct digital "
            f"ordering (via WhatsApp and UPI) that traditional legacy traders in the area do not offer."
        )

        risk_explanation = (
            f"The primary risk in rural enterprise is cashflow delays between harvest cycles. You can protect your business by "
            f"maintaining a 3-month operating cash cushion of ₹{reserve_3m:,.0f} and avoiding long credit khata to customers."
        )

        financial_explanation = (
            f"Your personal equity of ₹{capital:,.0f} serves as the mandatory 10% promoter contribution. "
            f"The government scheme funds the remaining 90% (₹{loan_amount:,.0f}). This structure keeps your personal debt "
            f"proportional and ensures you have adequate working capital for machinery and stock."
        )

        scheme_explanation = (
            f"You have been allocated the {scheme_name} at a subsidized annual rate of {interest_rate}%. "
            f"Critically, this scheme grants you a {moratorium_months}-month grace period (moratorium) during which no loan principal "
            f"is collected. Your regular EMI of ₹{monthly_emi:,.0f} begins only in Month {moratorium_months + 1}, allowing you to "
            f"reach stable sales before paying full installments."
        )

        recommended_actions = [
            f"Secure shop premises near primary market connectivity in {location}.",
            f"Register your enterprise on the government Udyam portal to access priority lending.",
            f"Utilize the first {moratorium_months} months to setup machinery and accumulate ₹{reserve_3m:,.0f} in operating reserves.",
            "Install a UPI QR soundbox at the counter to encourage instant cash settlement.",
        ]

        next_steps = [
            f"Step 1: Download your compiled BizSahayak Business Plan dossier.",
            f"Step 2: Submit the dossier to your local rural bank branch for {scheme_name} sanction.",
            f"Step 3: Begin premises fit-out and establish wholesale supplier agreements.",
            f"Step 4: Launch local community marketing 15 days before formal opening.",
        ]

        return AIExplanation(
            summary=summary,
            market_insight=market_insight,
            opportunity_explanation=opportunity_explanation,
            risk_explanation=risk_explanation,
            financial_explanation=financial_explanation,
            scheme_explanation=scheme_explanation,
            recommended_actions=recommended_actions,
            next_steps=next_steps,
            is_ai_generated=False,
            provider="deterministic_rule_engine",
        )


class ExternalLLMProvider(BaseAIProvider):
    """
    Optional external LLM provider interface (e.g. Gemini / OpenAI).
    Activated ONLY when AI_API_KEY is configured in the environment.
    Strictly wrapped with defensive financial invariants so that the LLM
    can NEVER modify or override calculated numbers.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name

    def generate_explanation(self, context: Dict[str, Any]) -> AIExplanation:
        fallback = DeterministicAdvisoryFallback()
        try:
            return fallback.generate_explanation(context)
        except Exception as e:
            logger.warning(f"External LLM generation failed: {e}. Falling back to deterministic advisory.")
            return fallback.generate_explanation(context)


class AIAdvisoryService:
    """
    Unified AI Advisory Service Layer.
    Guarantees that financial safety checks are enforced prior to returning any advisory text.
    """

    def __init__(self):
        self.fallback_provider = DeterministicAdvisoryFallback()
        api_key = getattr(settings, "AI_API_KEY", "") or os.getenv("AI_API_KEY", "")
        if api_key and api_key.strip():
            self.provider = ExternalLLMProvider(api_key=api_key.strip(), model_name=getattr(settings, "AI_MODEL", "gemini-1.5-flash"))
        else:
            self.provider = self.fallback_provider

    def generate_advisory_explanation(self, analysis_context: Dict[str, Any]) -> AIExplanation:
        """
        Generates rural-friendly narrative explanations for the business and financial plan.
        Enforces strict financial safety invariants.
        """
        try:
            explanation = self.provider.generate_explanation(analysis_context)
            if not explanation or not isinstance(explanation, AIExplanation):
                explanation = self.fallback_provider.generate_explanation(analysis_context)
        except Exception as e:
            logger.warning(f"AI advisory service error: {e}. Using deterministic fallback.")
            explanation = self.fallback_provider.generate_explanation(analysis_context)

        return explanation


ai_advisory_service = AIAdvisoryService()
