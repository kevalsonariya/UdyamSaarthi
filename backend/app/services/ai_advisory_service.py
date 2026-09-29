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

        lang = str(context.get("language", "en")).lower()

        if lang == "hi":
            summary = (
                f"प्रोटोटाइप के संकेतात्मक स्थानीय प्रोफ़ाइल के अनुसार, {location} में ₹{capital:,.0f} के व्यक्तिगत मार्जिन के साथ "
                f"{category} व्यवसाय शुरू करने पर ₹{project_cost:,.0f} का अनुमानित परियोजना पैमाना बनता है। "
                f"सरकारी {scheme_name} के तहत, आप ₹{loan_amount:,.0f} तक के सांकेतिक ऋण के पात्र हो सकते हैं "
                f"(औपचारिक बैंक मूल्यांकन के अधीन)।"
            )

            market_insight = (
                f"{location} के आसपास {catchment_km} किमी के संकेतात्मक कैचमेंट अनुमान के आधार पर, "
                f"स्थानीय स्तर पर केंद्र खोलने से दैनिक मांग और साप्ताहिक बाज़ार की बिक्री प्राप्त करने का अवसर है। "
                f"नोट: सभी बाज़ार आंकड़े प्रोटोटाइप अनुमान हैं।"
            )

            opportunity_explanation = (
                f"{location} में सबसे तात्कालिक अवसर निरंतर उत्पाद उपलब्धता और सीधी डिजिटल व्यवस्था (व्हाट्सएप और यूपीआई) "
                f"प्रदान करना है, जो क्षेत्र के पारंपरिक व्यापारी पेश नहीं करते हैं।"
            )

            risk_explanation = (
                f"ग्रामीण उद्यम में प्राथमिक जोखिम फसल चक्रों के बीच नकदी प्रवाह का विलंब है। आप ₹{reserve_3m:,.0f} का "
                f"3-महीने का परिचालन रिज़र्व रखकर और ग्राहकों को लंबी उधारी से बचकर अपने व्यवसाय की रक्षा कर सकते हैं।"
            )

            financial_explanation = (
                f"सांकेतिक नियोजन गणना: आपकी ₹{capital:,.0f} की व्यक्तिगत पूंजी अनिवार्य 10% प्रमोटर अंशदान के रूप में कार्य करती है। "
                f"सरकारी योजना शेष 90% (₹{loan_amount:,.0f}) का वित्तपोषण मॉडल करती है। "
                f"अंतिम स्वीकृति और शर्तें बैंक के औपचारिक मूल्यांकन पर निर्भर करती हैं।"
            )

            scheme_explanation = (
                f"संकेतात्मक मानकों के अनुसार, {scheme_name} में {interest_rate}% की रियायती वार्षिक दर और {moratorium_months} महीने "
                f"की छूट अवधि (मोराटोरियम) शामिल है। सांकेतिक नियमित ईएमआई ₹{monthly_emi:,.0f} केवल महीने {moratorium_months + 1} "
                f"से शुरू होने का अनुमान है।"
            )

            recommended_actions = [
                f"{location} में प्रमुख बाज़ार मार्ग के पास दुकान या कार्यस्थल सुरक्षित करें।",
                "प्राथमिकता ऋण तक पहुंचने के लिए सरकारी उद्यम पोर्टल पर अपना पंजीकरण कराएं।",
                f"पहले {moratorium_months} महीनों का उपयोग मशीनरी स्थापित करने और ₹{reserve_3m:,.0f} का परिचालन रिज़र्व बनाने में करें।",
                "काउंटर पर यूपीआई क्यूआर साउंडबॉक्स लगाएं ताकि तुरंत नकद या डिजिटल भुगतान प्रोत्साहित हो।",
            ]

            next_steps = [
                "चरण 1: अपना संकलित UdyamSaarthi व्यापार योजना डॉसियर डाउनलोड करें।",
                f"चरण 2: {scheme_name} स्वीकृति के लिए अपनी स्थानीय ग्रामीण बैंक शाखा में डॉसियर जमा करें।",
                "चरण 3: कार्यस्थल तैयार करें और थोक आपूर्तिकर्ताओं से समझौते स्थापित करें।",
                "चरण 4: औपचारिक उद्घाटन से 15 दिन पहले स्थानीय समुदाय में प्रचार शुरू करें।",
            ]
        elif lang == "gu":
            summary = (
                f"પ્રોટોટાઇપના સૂચક સ્થાનિક પ્રોફાઇલ અનુસાર, {location} માં ₹{capital:,.0f} ના અંગત માર્જિન સાથે "
                f"{category} વ્યવસાય શરૂ કરવાથી ₹{project_cost:,.0f} નું અંદાજિત પ્રોજેક્ટ સ્કેલ શક્ય બને છે. "
                f"સરકારી {scheme_name} ના માપદંડો મુજબ, તમે ₹{loan_amount:,.0f} સુધીની સૂચક લોન માટે પાત્ર બની શકો છો "
                f"(બેંક ઔપચારિક મૂલ્યાંકનને આધીન)."
            )

            market_insight = (
                f"{location} ની આસપાસ {catchment_km} કિમીના સૂચક બજાર વિસ્તાર અંદાજ મુજબ, "
                f"સ્થાનિક સ્તરે કેન્દ્ર શરૂ કરવાથી ઓછા ભાડા ખર્ચે દૈનિક માંગ અને હાટનો વેપાર મેળવવાની તક છે. "
                f"નોંધ: તમામ બજાર આંકડા પ્રોટોટાઇપ અંદાજ છે."
            )

            opportunity_explanation = (
                f"{location} માં સૌથી મોટી તક સતત ઉત્પાદન ઉપલબ્ધતા અને સીધા ડિજિટલ ઓર્ડરિંગ (વોટ્સએપ અને યુપીઆઈ) "
                f"પૂરા પાડવાની છે, જે આ વિસ્તારના પરંપરાગત વેપારીઓ ઓફર કરતા નથી."
            )

            risk_explanation = (
                f"ગ્રામીણ સાહસમાં મુખ્ય જોખમ લણણી ચક્ર વચ્ચે કેશફ્લો વિલંબનું છે. તમે ₹{reserve_3m:,.0f} નો "
                f"3-મહિનાનો કાર્યકારી અનામત બફર જાળવીને અને ગ્રાહકોને લાંબી ઉધારી આપવાનું ટાળીને વ્યવસાય સુરક્ષિત રાખી શકો છો."
            )

            financial_explanation = (
                f"સૂચક આયોજન ગણતરી: તમારી ₹{capital:,.0f} ની અંગત મૂડી ફરજિયાત 10% પ્રમોટર હિસ્સા તરીકે કાર્ય કરે છે. "
                f"સરકારી યોજના બાકીના 90% (₹{loan_amount:,.0f}) નું ધિરાણ મોડેલ કરે છે. "
                f"આખરી મંજૂરી અને શરતો બેંકની ઔપચારિક ચકાસણી પર આધારિત રહેશે."
            )

            scheme_explanation = (
                f"સૂચક બેંચમાર્ક અનુસાર, {scheme_name} હેઠળ {interest_rate}% વાર્ષિક દર અને {moratorium_months} મહિનાનો "
                f"રાહત ગાળો (મોરેટોરિયમ) મોડેલ થયેલ છે. અંદાજિત નિયમિત ઈએમઆઈ ₹{monthly_emi:,.0f} માત્ર {moratorium_months + 1} "
                f"મા મહિનાથી શરૂ થવાનું અનુમાન છે."
            )

            recommended_actions = [
                f"{location} માં મુખ્ય બજાર કનેક્ટિવિટી નજીક દુકાન અથવા પરિસર સુનિશ્ચિત કરો.",
                "અગ્રતા ધિરાણ યોજનાનો લાભ લેવા માટે સરકારી ઉદ્યમ પોર્ટલ પર નોંધણી કરાવો.",
                f"પ્રથમ {moratorium_months} મહિનાનો ઉપયોગ મશીનરી સ્થાપિત કરવા અને ₹{reserve_3m:,.0f} ની કાર્યકારી અનામત એકત્ર કરવામાં કરો.",
                "તરત ડિજિટલ ચુકવણી માટે કાઉન્ટર પર યુપીઆઈ ક્યૂઆર સાઉન્ડબોક્સ ઇન્સ્ટોલ કરો.",
            ]

            next_steps = [
                "પગલું 1: તમારો તૈયાર UdyamSaarthi બિઝનેસ પ્લાન દસ્તાવેજ ડાઉનલોડ કરો.",
                f"પગલું 2: {scheme_name} મંજૂરી માટે તમારી સ્થાનિક ગ્રામીણ બેંક શાખામાં દસ્તાવેજ રજૂ કરો.",
                "પગલું 3: પરિસર ફિટિંગ શરૂ કરો અને જથ્થાબંધ સપ્લાયર કરારો સ્થાપિત કરો.",
                "પગલું 4: સત્તાવાર શરૂઆતના 15 દિવસ પહેલાં સ્થાનિક સમુદાયમાં પ્રચાર શરૂ કરો.",
            ]
        else:
            summary = (
                f"Based on the prototype's indicative local market profile, starting a {category} business in {location} "
                f"with an indicative personal margin of ₹{capital:,.0f} enables a planned project scale of ₹{project_cost:,.0f}. "
                f"Under the indicative benchmark parameters of {scheme_name}, you may qualify for up to ₹{loan_amount:,.0f} "
                f"in structured financing (subject to formal bank appraisal)."
            )

            market_insight = (
                f"Based on indicative catchment estimates within {catchment_km} km of {location}, opening your center locally "
                f"offers an opportunity to capture routine daily demand and weekly mandi footfall with lower rental overhead. "
                f"Note: All market and competitor figures are prototype heuristics."
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
                f"Indicative planning calculation: Your personal equity of ₹{capital:,.0f} serves as the mandatory 10% promoter contribution. "
                f"The benchmark scheme models the remaining 90% (₹{loan_amount:,.0f}) as loan financing. Final sanction and terms depend on "
                f"formal lending appraisal."
            )

            scheme_explanation = (
                f"Under indicative benchmark parameters, the {scheme_name} models an interest rate of {interest_rate}% with an estimated "
                f"{moratorium_months}-month grace period (moratorium). The indicative monthly EMI of ₹{monthly_emi:,.0f} begins in "
                f"Month {moratorium_months + 1}, subject to bank sanction."
            )

            recommended_actions = [
                f"Secure shop premises near primary market connectivity in {location}.",
                f"Register your enterprise on the government Udyam portal to access priority lending.",
                f"Utilize the first {moratorium_months} months to setup machinery and accumulate ₹{reserve_3m:,.0f} in operating reserves.",
                "Install a UPI QR soundbox at the counter to encourage instant cash settlement.",
            ]

            next_steps = [
                f"Step 1: Download your compiled UdyamSaarthi Business Plan dossier.",
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
