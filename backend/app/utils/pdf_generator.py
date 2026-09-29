# -*- coding: utf-8 -*-
"""
Phase B11 — Fully Multilingual UdyamSaarthi PDF Generation
Supports: English (en), Hindi (hi), Gujarati (gu)
Uses bundled Noto Sans fonts for correct Unicode rendering.
Financial values are invariant across languages — only labels change.
"""
import io
import os
from typing import Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Font Registration
# ---------------------------------------------------------------------------
_FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
_FONTS_REGISTERED = False


def _register_fonts():
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    try:
        pdfmetrics.registerFont(TTFont(
            "NotoDevanagari",
            os.path.join(_FONTS_DIR, "NotoSansDevanagari-Regular.ttf")))
        pdfmetrics.registerFont(TTFont(
            "NotoDevanagari-Bold",
            os.path.join(_FONTS_DIR, "NotoSansDevanagari-Bold.ttf")))
        pdfmetrics.registerFont(TTFont(
            "NotoGujarati",
            os.path.join(_FONTS_DIR, "NotoSansGujarati-Regular.ttf")))
        pdfmetrics.registerFont(TTFont(
            "NotoGujarati-Bold",
            os.path.join(_FONTS_DIR, "NotoSansGujarati-Bold.ttf")))
        _FONTS_REGISTERED = True
    except Exception as e:
        # Graceful fallback: use Helvetica if fonts not found
        pass


# ---------------------------------------------------------------------------
# Language-aware font selector
# ---------------------------------------------------------------------------
def _fonts(lang: str) -> Dict[str, str]:
    if lang == "hi":
        return {"regular": "NotoDevanagari", "bold": "NotoDevanagari-Bold"}
    elif lang == "gu":
        return {"regular": "NotoGujarati", "bold": "NotoGujarati-Bold"}
    else:
        return {"regular": "Helvetica", "bold": "Helvetica-Bold"}


# ---------------------------------------------------------------------------
# PDF label translations
# ---------------------------------------------------------------------------
PDF_LABELS = {
    "en": {
        "title": "UdyamSaarthi",
        "tagline": "From Business Idea → Business Insight → Financial Plan",
        "sih": "SIH26091 • AI-Driven Hyper-Local Business Advisory & Financial Structuring Dossier",
        "target_location": "Target Location",
        "business_category": "Business Category",
        "margin_capital": "Available Margin Capital",
        "feasibility": "Feasibility Score",
        "sec1": "1. Deterministic Financial Structuring & Scheme Allocation",
        "param": "Parameter",
        "calc_value": "Calculated Value",
        "rule": "Regulatory Rule / Scheme Norm",
        "project_cost": "Total Project Cost",
        "promoter_contrib": "Promoter Margin Capital",
        "max_loan": "Maximum Loan Eligible",
        "rec_scheme": "Recommended Scheme",
        "interest_rate": "Concessional Interest Rate",
        "tenure_morat": "Tenure & Moratorium",
        "emi_label": "Monthly Installment (Post-Moratorium EMI)",
        "total_repay": "Total Repayment Amount",
        "rule_10pct": "Available Margin / 10%",
        "rule_10pct_eq": "10.0% Minimum mandatory borrower equity",
        "rule_90pct": "90.0% of Total Project Cost",
        "rule_scheme": "Automatic deterministic routing rule based on ₹1.40L threshold",
        "rule_interest": "Subsidized priority-sector lending interest rate",
        "tenure_detail": "{ty} Years ({tm} Mo)",
        "morat_detail": "{mm} Months Principal Grace/Gestation",
        "morat_interest": "Moratorium monthly interest: ₹{mi:,.2f}",
        "prin_int": "Principal: ₹{p:,.2f} + Interest: ₹{i:,.2f}",
        "sec2": "2. Monthly Working Capital Planning & Cash Reserve",
        "raw_materials": "Raw Materials & Goods",
        "labor": "Labor & Operations Wage",
        "rent": "Shop Rent & Utilities",
        "logistics": "Logistics & Packaging",
        "contingency": "Monthly Contingency Buffer",
        "total_opex": "Total Monthly Operating Opex",
        "reserve_3m": "Recommended 3-Month Cash Reserve",
        "breakeven": "Monthly Break-Even Revenue",
        "monthly_alloc": "Monthly Allocation",
        "category_label": "Category",
        "sec3": "3. Strategic SWOT Matrix",
        "strengths": "Strengths",
        "weaknesses": "Weaknesses",
        "opportunities": "Opportunities",
        "threats": "Threats",
        "sec4": "4. Market Reach & Opportunities",
        "market_reach": "Market Reach Summary",
        "top_opp": "Top Opportunities",
        "sec5": "5. Risks & Mitigation",
        "risk_title": "Risk",
        "severity": "Severity",
        "mitigation": "Mitigation",
        "sec6": "6. Competitor Landscape",
        "competitor": "Competitor",
        "type": "Type",
        "proximity": "Proximity",
        "diff_strategy": "Differentiation Strategy",
        "sec7": "7. Product Market Value & Pricing Guidance",
        "benchmark": "Benchmark Product/Service",
        "unit_cost": "Unit Production Cost",
        "retail_price": "Suggested Retail Price",
        "gross_margin": "Target Gross Margin",
        "pricing_notes": "Pricing Strategy Notes",
        "sec8": "8. Business Recommendation & Milestones",
        "feasibility_rating": "Feasibility Rating",
        "summary": "Summary",
        "licenses": "Mandatory Licenses & Registrations",
        "milestones": "First 90-Day Milestones",
        "digital_tips": "Digital Enablement Tips",
        "sec9": "9. AI Advisory",
        "exec_summary": "Executive Summary",
        "market_insight": "Local Market Insight",
        "opp_explanation": "Opportunity Explanation",
        "risk_explanation": "Risk Explanation",
        "fin_explanation": "Financial Explanation",
        "scheme_explanation": "Scheme Explanation",
        "actions": "Recommended Actions",
        "next_steps": "Recommended Next Steps",
        "disclaimer_title": "MANDATORY FINANCIAL DISCLAIMER",
        "disclaimer_body": '"Indicative calculation for planning purposes. Verify applicable scheme terms before making financial decisions."',
        "disclaimer_note": "Note: Hyper-local market reach, competitor maps, and demographic projections represent prototype simulation data.",
        "pa": "p.a.",
        "yes": "Yes",
        "no": "No",
        "na": "N/A",
        "demo_label": "[Indicative Demo Data]",
        "lang_label": "EN",
    },
    "hi": {
        "title": "उद्यम सारथी",
        "tagline": "व्यावसायिक विचार → व्यावसायिक अंतर्दृष्टि → वित्तीय योजना",
        "sih": "SIH26091 • AI-आधारित हाइपर-लोकल व्यवसाय सलाह एवं वित्तीय संरचना दस्तावेज़",
        "target_location": "लक्षित स्थान",
        "business_category": "व्यवसाय श्रेणी",
        "margin_capital": "उपलब्ध मार्जिन पूंजी",
        "feasibility": "व्यवहार्यता स्कोर",
        "sec1": "1. निर्धारक वित्तीय संरचना एवं योजना आवंटन",
        "param": "पैरामीटर",
        "calc_value": "परिकलित मूल्य",
        "rule": "विनियामक नियम / योजना मानदंड",
        "project_cost": "कुल परियोजना लागत",
        "promoter_contrib": "प्रमोटर मार्जिन पूंजी",
        "max_loan": "अधिकतम पात्र ऋण",
        "rec_scheme": "अनुशंसित योजना",
        "interest_rate": "रियायती ब्याज दर",
        "tenure_morat": "कार्यकाल एवं मोरेटोरियम",
        "emi_label": "मासिक किस्त (मोरेटोरियम के बाद EMI)",
        "total_repay": "कुल चुकौती राशि",
        "rule_10pct": "उपलब्ध मार्जिन / 10%",
        "rule_10pct_eq": "10.0% न्यूनतम अनिवार्य उधारकर्ता इक्विटी",
        "rule_90pct": "कुल परियोजना लागत का 90.0%",
        "rule_scheme": "₹1.40 लाख की सीमा पर स्वचालित निर्धारक रूटिंग नियम",
        "rule_interest": "सब्सिडाइज्ड प्राथमिकता क्षेत्र ऋण ब्याज दर",
        "tenure_detail": "{ty} वर्ष ({tm} माह)",
        "morat_detail": "{mm} माह मूलधन छूट/गेस्टेशन",
        "morat_interest": "मोरेटोरियम मासिक ब्याज: ₹{mi:,.2f}",
        "prin_int": "मूलधन: ₹{p:,.2f} + ब्याज: ₹{i:,.2f}",
        "sec2": "2. मासिक कार्यशील पूंजी नियोजन एवं नकद आरक्षित",
        "raw_materials": "कच्चा माल एवं सामग्री",
        "labor": "श्रम एवं परिचालन वेतन",
        "rent": "दुकान किराया एवं उपयोगिताएं",
        "logistics": "लॉजिस्टिक्स एवं पैकेजिंग",
        "contingency": "मासिक आकस्मिक बफर",
        "total_opex": "कुल मासिक परिचालन व्यय",
        "reserve_3m": "अनुशंसित 3-माह नकद आरक्षित",
        "breakeven": "मासिक ब्रेक-ईवन राजस्व",
        "monthly_alloc": "मासिक आवंटन",
        "category_label": "श्रेणी",
        "sec3": "3. रणनीतिक SWOT विश्लेषण",
        "strengths": "ताकत",
        "weaknesses": "कमजोरियां",
        "opportunities": "अवसर",
        "threats": "खतरे",
        "sec4": "4. बाज़ार पहुंच एवं अवसर",
        "market_reach": "बाज़ार पहुंच सारांश",
        "top_opp": "शीर्ष अवसर",
        "sec5": "5. जोखिम एवं शमन",
        "risk_title": "जोखिम",
        "severity": "गंभीरता",
        "mitigation": "शमन उपाय",
        "sec6": "6. प्रतिस्पर्धी परिदृश्य",
        "competitor": "प्रतिस्पर्धी",
        "type": "प्रकार",
        "proximity": "निकटता",
        "diff_strategy": "विभेदन रणनीति",
        "sec7": "7. उत्पाद बाज़ार मूल्य एवं मूल्य निर्धारण मार्गदर्शन",
        "benchmark": "बेंचमार्क उत्पाद/सेवा",
        "unit_cost": "इकाई उत्पादन लागत",
        "retail_price": "सुझाया गया खुदरा मूल्य",
        "gross_margin": "लक्ष्य सकल मार्जिन",
        "pricing_notes": "मूल्य निर्धारण रणनीति नोट्स",
        "sec8": "8. व्यवसाय अनुशंसा एवं मील के पत्थर",
        "feasibility_rating": "व्यवहार्यता रेटिंग",
        "summary": "सारांश",
        "licenses": "अनिवार्य लाइसेंस एवं पंजीकरण",
        "milestones": "प्रथम 90 दिन के लक्ष्य",
        "digital_tips": "डिजिटल सशक्तिकरण सुझाव",
        "sec9": "9. AI सलाह",
        "exec_summary": "कार्यकारी सारांश",
        "market_insight": "स्थानीय बाज़ार अंतर्दृष्टि",
        "opp_explanation": "अवसर व्याख्या",
        "risk_explanation": "जोखिम व्याख्या",
        "fin_explanation": "वित्तीय व्याख्या",
        "scheme_explanation": "योजना व्याख्या",
        "actions": "अनुशंसित कार्रवाइयां",
        "next_steps": "अनुशंसित अगले कदम",
        "disclaimer_title": "अनिवार्य वित्तीय अस्वीकरण",
        "disclaimer_body": '"नियोजन उद्देश्यों के लिए संकेतात्मक गणना। वित्तीय निर्णय लेने से पहले लागू योजना शर्तें सत्यापित करें।"',
        "disclaimer_note": "नोट: हाइपर-लोकल बाज़ार पहुंच, प्रतिस्पर्धी मानचित्र एवं जनसांख्यिकीय अनुमान प्रोटोटाइप सिमुलेशन डेटा का प्रतिनिधित्व करते हैं।",
        "pa": "प्रति वर्ष",
        "yes": "हाँ",
        "no": "नहीं",
        "na": "उपलब्ध नहीं",
        "demo_label": "[संकेतात्मक डेमो डेटा]",
        "lang_label": "HI",
    },
    "gu": {
        "title": "ઉદ્યમ સારથી",
        "tagline": "વ્યવસાય વિચાર → વ્યવસાય અંતર્દૃષ્ટિ → નાણાકીય યોજના",
        "sih": "SIH26091 • AI-આધારિત હાઇપર-લોકલ વ્યવસાય સલાહ અને નાણાકીય માળખું દસ્તાવેજ",
        "target_location": "લક્ષ્ય સ્થાન",
        "business_category": "વ્યવસાય શ્રેણી",
        "margin_capital": "ઉપલબ્ધ માર્જિન મૂડી",
        "feasibility": "શક્યતા સ્કોર",
        "sec1": "1. નિર્ધારક નાણાકીય માળખું અને યોજના ફાળવણી",
        "param": "પ્રાચલ",
        "calc_value": "ગણવામાં આવેલ મૂલ્ય",
        "rule": "નિયમનકારી નિયમ / યોજના ધોરણ",
        "project_cost": "કુલ પ્રોજેક્ટ ખર્ચ",
        "promoter_contrib": "પ્રમોટર માર્જિન મૂડી",
        "max_loan": "મહત્તમ પાત્ર લોન",
        "rec_scheme": "ભલામણ કરેલ યોજના",
        "interest_rate": "રાહત વ્યાજ દર",
        "tenure_morat": "કાર્યકાળ અને મોરેટોરિયમ",
        "emi_label": "માસિક હપ્તો (મોરેટોરિયમ પછી EMI)",
        "total_repay": "કુલ ચુકવણી રકમ",
        "rule_10pct": "ઉપલબ્ધ માર્જિન / 10%",
        "rule_10pct_eq": "10.0% ન્યૂનતમ ફરજિયાત ઉધારકર્તા ઇક્વિટી",
        "rule_90pct": "કુલ પ્રોજેક્ટ ખર્ચના 90.0%",
        "rule_scheme": "₹1.40 લાખ મર્યાદા પર સ્વચાલિત નિર્ધારક રૂટિંગ નિયમ",
        "rule_interest": "સબ્સિડાઇઝ્ડ પ્રાધાન્ય ક્ષેત્ર ઋણ વ્યાજ દર",
        "tenure_detail": "{ty} વર્ષ ({tm} મહિના)",
        "morat_detail": "{mm} મહિના મૂળ છૂટ/ગેસ્ટેશન",
        "morat_interest": "મોરેટોરિયમ માસિક વ્યાજ: ₹{mi:,.2f}",
        "prin_int": "મૂળ: ₹{p:,.2f} + વ્યાજ: ₹{i:,.2f}",
        "sec2": "2. માસિક કાર્યકારી મૂડી આયોજન અને રોકડ અનામત",
        "raw_materials": "કાચો માલ અને સામગ્રી",
        "labor": "શ્રમ અને સંચાલન વેતન",
        "rent": "દુકાન ભાડું અને ઉપયોગિતાઓ",
        "logistics": "લૉજિસ્ટિક્સ અને પેકેજિંગ",
        "contingency": "માસિક આકસ્મિક બફર",
        "total_opex": "કુલ માસિક સંચાલન ખર્ચ",
        "reserve_3m": "ભલામણ કરેલ 3-માસ રોકડ અનામત",
        "breakeven": "માસિક બ્રેક-ઇવન આવક",
        "monthly_alloc": "માસિક ફાળવણી",
        "category_label": "શ્રેણી",
        "sec3": "3. વ્યૂહાત્મક SWOT વિશ્લેષણ",
        "strengths": "શક્તિઓ",
        "weaknesses": "નબળાઈઓ",
        "opportunities": "તકો",
        "threats": "જોખમો",
        "sec4": "4. બજાર પહોંચ અને તકો",
        "market_reach": "બજાર પહોંચ સારાંશ",
        "top_opp": "ટોચની તકો",
        "sec5": "5. જોખમ અને શમન",
        "risk_title": "જોખમ",
        "severity": "ગંભીરતા",
        "mitigation": "શમન ઉપાય",
        "sec6": "6. સ્પર્ધાત્મક પરિદ્રશ્ય",
        "competitor": "સ્પર્ધક",
        "type": "પ્રકાર",
        "proximity": "નિકટતા",
        "diff_strategy": "ભેદ વ્યૂહ",
        "sec7": "7. ઉત્પાદ બજાર મૂલ્ય અને ભાવ નિર્ધારણ",
        "benchmark": "બેન્ચમાર્ક ઉત્પાદ/સેવા",
        "unit_cost": "એકમ ઉત્પાદન ખર્ચ",
        "retail_price": "સૂચવેલ છૂટક ભાવ",
        "gross_margin": "લક્ષ્ય સ્થૂળ માર્જિન",
        "pricing_notes": "ભાવ નિર્ધારણ રણનીતિ નોંધ",
        "sec8": "8. વ્યવસાય ભલામણ અને માઈલસ્ટોન",
        "feasibility_rating": "શક્યતા રેટિંગ",
        "summary": "સારાંશ",
        "licenses": "ફરજિયાત લાઇસન્સ અને નોંધણી",
        "milestones": "પ્રથમ 90 દિવસના લક્ષ્ય",
        "digital_tips": "ડિજિટલ સક્ષમીકરણ સૂચનો",
        "sec9": "9. AI સલાહ",
        "exec_summary": "કાર્યકારી સારાંશ",
        "market_insight": "સ્થાનિક બજાર અંતર્દૃષ્ટિ",
        "opp_explanation": "તક સ્પષ્ટીકરણ",
        "risk_explanation": "જોખમ સ્પષ્ટીકરણ",
        "fin_explanation": "નાણાકીય સ્પષ્ટીકરણ",
        "scheme_explanation": "યોજના સ્પષ્ટીકરણ",
        "actions": "ભલામણ કરેલ પગલાં",
        "next_steps": "ભલામણ કરેલ આગળના પગલા",
        "disclaimer_title": "ફરજિયાત નાણાકીય અસ્વીકૃતિ",
        "disclaimer_body": '"આયોજન હેતુઓ માટે સૂચક ગણતરી. નાણાકીય નિર્ણય લેતા પહેલા લાગુ યોજના શરતો ચકાસો."',
        "disclaimer_note": "નોંધ: હાઇપર-લોકલ બજાર પહોંચ, સ્પર્ધક નકશા અને વસ્તી અનુમાન પ્રોટોટાઇપ સિમ્યુલેશન ડેટા છે.",
        "pa": "વાર્ષિક",
        "yes": "હા",
        "no": "ના",
        "na": "ઉપલબ્ધ નથી",
        "demo_label": "[સૂચક ડેમો ડેટા]",
        "lang_label": "GU",
    },
}


# ---------------------------------------------------------------------------
# Style builder
# ---------------------------------------------------------------------------
def _build_styles(lang: str):
    _register_fonts()
    f = _fonts(lang)
    reg, bold = f["regular"], f["bold"]

    PRIMARY_COLOR = colors.HexColor("#1b4332")
    ACCENT_COLOR = colors.HexColor("#d97706")

    base = getSampleStyleSheet()

    def ps(name, font, size, leading, color=None, align=TA_LEFT, space_before=0, space_after=0):
        return ParagraphStyle(
            name,
            parent=base["Normal"],
            fontName=font,
            fontSize=size,
            leading=leading,
            textColor=color or colors.HexColor("#1e293b"),
            alignment=align,
            spaceBefore=space_before,
            spaceAfter=space_after,
        )

    return {
        "title": ps("T", bold, 20, 24, PRIMARY_COLOR),
        "tagline": ps("TL", reg, 10, 14, ACCENT_COLOR),
        "sih": ps("SIH", reg, 8.5, 12, colors.HexColor("#475569")),
        "section": ps("SH", bold, 11, 15, PRIMARY_COLOR, space_before=6, space_after=4),
        "body": ps("B", reg, 8.5, 12),
        "body_bold": ps("BB", bold, 8.5, 12, colors.HexColor("#0f172a")),
        "bullet": ps("BL", reg, 8, 11.5, colors.HexColor("#334155")),
        "disclaimer": ps("D", bold, 8, 11, colors.HexColor("#991b1b"), TA_CENTER),
        "subnote": ps("SN", reg, 7.5, 10, colors.HexColor("#64748b"), TA_CENTER),
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
BORDER = colors.HexColor("#cbd5e1")
LIGHT_BG = colors.HexColor("#f8fafc")
HEADER_BG = colors.HexColor("#e2e8f0")
PRIMARY = colors.HexColor("#1b4332")


def _grid_style(header_row=True):
    s = [
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    if header_row:
        s.append(("BACKGROUND", (0, 0), (-1, 0), HEADER_BG))
    return TableStyle(s)


def _para(text, style):
    """Safe paragraph that falls back on encode error."""
    try:
        return Paragraph(str(text), style)
    except Exception:
        return Paragraph("—", style)


def _bullet_list(items, style):
    """Return single Paragraph with bullet lines."""
    if not items:
        return _para("—", style)
    lines = "<br/>".join(f"• {str(i)}" for i in items)
    return _para(lines, style)


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _section_financial(data, L, s):
    fin = data.get("financial", {})
    sch = data.get("scheme", {})
    emi = data.get("emi", {})

    def v(key, default=0):
        val = fin.get(key) if isinstance(fin, dict) else getattr(fin, key, default)
        return val if val is not None else default

    def sv(key, default=""):
        val = sch.get(key) if isinstance(sch, dict) else getattr(sch, key, default)
        return val if val is not None else default

    def ev(key, default=0):
        val = emi.get(key) if isinstance(emi, dict) else getattr(emi, key, default)
        return val if val is not None else default

    ty = sv("tenure_years", 0)
    tm = sv("tenure_months", 0)
    mm = sv("moratorium_months", 0)
    mi = ev("moratorium_monthly_interest", 0)
    p = ev("principal_amount", 0)
    i_val = ev("total_interest_payable", 0)

    rows = [
        [_para(L["param"], s["body_bold"]),
         _para(L["calc_value"], s["body_bold"]),
         _para(L["rule"], s["body_bold"])],
        [_para(L["project_cost"], s["body"]),
         _para(f"₹{v('project_cost'):,.2f}", s["body_bold"]),
         _para(L["rule_10pct"], s["body"])],
        [_para(L["promoter_contrib"], s["body"]),
         _para(f"₹{v('promoter_contribution'):,.2f}", s["body"]),
         _para(L["rule_10pct_eq"], s["body"])],
        [_para(L["max_loan"], s["body"]),
         _para(f"₹{v('max_loan_amount'):,.2f}", s["body_bold"]),
         _para(L["rule_90pct"], s["body"])],
        [_para(L["rec_scheme"], s["body"]),
         _para(f"{sv('scheme_name')} ({sv('scheme_code')})", s["body"]),
         _para(L["rule_scheme"], s["body"])],
        [_para(L["interest_rate"], s["body"]),
         _para(f"{sv('interest_rate_percent')}% {L['pa']}", s["body_bold"]),
         _para(L["rule_interest"], s["body"])],
        [_para(L["tenure_morat"], s["body"]),
         _para(L["tenure_detail"].format(ty=ty, tm=tm), s["body"]),
         _para(L["morat_detail"].format(mm=mm), s["body_bold"])],
        [_para(L["emi_label"], s["body"]),
         _para(f"₹{ev('monthly_emi'):,.2f}", s["body_bold"]),
         _para(L["morat_interest"].format(mi=mi), s["body"])],
        [_para(L["total_repay"], s["body"]),
         _para(f"₹{ev('total_repayment_amount'):,.2f}", s["body"]),
         _para(L["prin_int"].format(p=p, i=i_val), s["body"])],
    ]
    t = Table(rows, colWidths=[165, 150, 225])
    t.setStyle(_grid_style())
    return t


def _section_working_capital(data, L, s):
    wc = data.get("working_capital", {})

    def w(key, default=0):
        val = wc.get(key) if isinstance(wc, dict) else getattr(wc, key, default)
        return val if val is not None else default

    rows = [
        [_para(L["raw_materials"], s["body_bold"]),
         _para(L["monthly_alloc"], s["body_bold"]),
         _para(L["category_label"], s["body_bold"]),
         _para(L["monthly_alloc"], s["body_bold"])],
        [_para(L["raw_materials"], s["body"]),
         _para(f"₹{w('monthly_raw_materials'):,.2f}", s["body"]),
         _para(L["labor"], s["body"]),
         _para(f"₹{w('monthly_labor_wages'):,.2f}", s["body"])],
        [_para(L["rent"], s["body"]),
         _para(f"₹{w('monthly_rent_utilities'):,.2f}", s["body"]),
         _para(L["logistics"], s["body"]),
         _para(f"₹{w('monthly_logistics_packaging'):,.2f}", s["body"])],
        [_para(L["contingency"], s["body"]),
         _para(f"₹{w('monthly_contingency_buffer'):,.2f}", s["body"]),
         _para(L["total_opex"], s["body_bold"]),
         _para(f"₹{w('total_monthly_operating_expense'):,.2f}", s["body_bold"])],
        [_para(L["reserve_3m"], s["body_bold"]),
         _para(f"₹{w('recommended_3_months_reserve'):,.2f}", s["body_bold"]),
         _para(L["breakeven"], s["body_bold"]),
         _para(f"₹{w('break_even_monthly_revenue'):,.2f}", s["body_bold"])],
    ]
    t = Table(rows, colWidths=[140, 120, 140, 140])
    t.setStyle(_grid_style())
    return t


def _section_swot(data, L, s):
    swot = data.get("swot", {})

    def g(key):
        v = swot.get(key) if isinstance(swot, dict) else getattr(swot, key, [])
        return v if v else []

    def cell(header, items, bg):
        content = f"<b>{header}</b><br/>" + "<br/>".join(f"• {i}" for i in items[:5])
        p = _para(content, s["bullet"])
        return p, bg

    st_p, st_bg = cell(L["strengths"], g("strengths"), colors.HexColor("#f0fdf4"))
    wk_p, wk_bg = cell(L["weaknesses"], g("weaknesses"), colors.HexColor("#fef2f2"))
    op_p, op_bg = cell(L["opportunities"], g("opportunities"), colors.HexColor("#eff6ff"))
    th_p, th_bg = cell(L["threats"], g("threats"), colors.HexColor("#fffbeb"))

    rows = [[st_p, wk_p], [op_p, th_p]]
    t = Table(rows, colWidths=[270, 270])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("BACKGROUND", (0, 0), (0, 0), st_bg),
        ("BACKGROUND", (1, 0), (1, 0), wk_bg),
        ("BACKGROUND", (0, 1), (0, 1), op_bg),
        ("BACKGROUND", (1, 1), (1, 1), th_bg),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def _section_risks(data, L, s):
    risks = data.get("risks", [])
    if not risks:
        return _para("—", s["body"])
    rows = [[_para(L["risk_title"], s["body_bold"]),
             _para(L["severity"], s["body_bold"]),
             _para(L["mitigation"], s["body_bold"])]]
    for r in risks[:6]:
        if isinstance(r, dict):
            title = r.get("risk_title", "")
            sev = r.get("severity", "")
            mit = r.get("mitigation_strategy", "")
        else:
            title = getattr(r, "risk_title", "")
            sev = getattr(r, "severity", "")
            mit = getattr(r, "mitigation_strategy", "")
        rows.append([_para(title, s["body"]),
                     _para(sev, s["body"]),
                     _para(mit, s["body"])])
    t = Table(rows, colWidths=[140, 60, 340])
    t.setStyle(_grid_style())
    return t


def _section_competitors(data, L, s):
    comps = data.get("competitors", [])
    if not comps:
        return _para("—", s["body"])
    rows = [[_para(L["competitor"], s["body_bold"]),
             _para(L["type"], s["body_bold"]),
             _para(L["proximity"], s["body_bold"]),
             _para(L["diff_strategy"], s["body_bold"])]]
    for c in comps[:4]:
        if isinstance(c, dict):
            name = c.get("name", "")
            typ = c.get("type_of_business", "")
            prox = c.get("proximity", "")
            diff = c.get("differentiation_strategy", "")
        else:
            name = getattr(c, "name", "")
            typ = getattr(c, "type_of_business", "")
            prox = getattr(c, "proximity", "")
            diff = getattr(c, "differentiation_strategy", "")
        rows.append([_para(name, s["body"]),
                     _para(typ, s["body"]),
                     _para(prox, s["body"]),
                     _para(diff, s["body"])])
    t = Table(rows, colWidths=[130, 100, 100, 210])
    t.setStyle(_grid_style())
    return t


def _section_pricing(data, L, s):
    pr = data.get("pricing", {})

    def p(key, default=""):
        if isinstance(pr, dict):
            return pr.get(key, default) or default
        return getattr(pr, key, default) or default

    gm = p("target_gross_margin_percent", 0)
    try:
        gm = f"{float(gm):.1f}%"
    except Exception:
        gm = str(gm)

    rows = [
        [_para(L["benchmark"], s["body_bold"]), _para(p("benchmark_product_or_service"), s["body"])],
        [_para(L["unit_cost"], s["body_bold"]), _para(p("estimated_unit_production_cost"), s["body"])],
        [_para(L["retail_price"], s["body_bold"]), _para(p("suggested_retail_price"), s["body"])],
        [_para(L["gross_margin"], s["body_bold"]), _para(gm, s["body"])],
        [_para(L["pricing_notes"], s["body_bold"]), _para(p("pricing_strategy_notes"), s["body"])],
    ]
    t = Table(rows, colWidths=[160, 380])
    t.setStyle(_grid_style(header_row=False))
    return t


def _section_recommendation(data, L, s):
    rec = data.get("recommendation", {})

    def r(key, default=""):
        if isinstance(rec, dict):
            return rec.get(key, default)
        return getattr(rec, key, default)

    story = []
    rows = [
        [_para(L["feasibility_rating"], s["body_bold"]),
         _para(f"{r('feasibility_score', 'N/A')}/100 — {r('feasibility_rating', '')}", s["body_bold"])],
        [_para(L["summary"], s["body_bold"]),
         _para(r("summary", ""), s["body"])],
    ]
    t = Table(rows, colWidths=[160, 380])
    t.setStyle(_grid_style(header_row=False))
    story.append(t)
    story.append(Spacer(1, 5))

    lic = r("mandatory_licenses_and_registrations", [])
    mil = r("first_90_days_milestones", [])
    dig = r("digital_enablement_tips", [])

    if lic:
        story.append(_para(f"<b>{L['licenses']}</b>", s["body_bold"]))
        story.append(_bullet_list(lic, s["bullet"]))
        story.append(Spacer(1, 3))
    if mil:
        story.append(_para(f"<b>{L['milestones']}</b>", s["body_bold"]))
        story.append(_bullet_list(mil, s["bullet"]))
        story.append(Spacer(1, 3))
    if dig:
        story.append(_para(f"<b>{L['digital_tips']}</b>", s["body_bold"]))
        story.append(_bullet_list(dig, s["bullet"]))
    return story


def _section_ai(data, L, s):
    ai = data.get("ai_explanation", {})
    if not ai:
        return []

    def a(key, default=""):
        if isinstance(ai, dict):
            return ai.get(key, default) or default
        return getattr(ai, key, default) or default

    story = []
    pairs = [
        (L["exec_summary"], a("summary")),
        (L["market_insight"], a("market_insight")),
        (L["opp_explanation"], a("opportunity_explanation")),
        (L["risk_explanation"], a("risk_explanation")),
        (L["fin_explanation"], a("financial_explanation")),
        (L["scheme_explanation"], a("scheme_explanation")),
    ]
    for label, val in pairs:
        if val:
            story.append(_para(f"<b>{label}:</b> {val}", s["body"]))
            story.append(Spacer(1, 3))

    actions = a("recommended_actions", [])
    next_s = a("next_steps", [])
    if actions:
        story.append(_para(f"<b>{L['actions']}</b>", s["body_bold"]))
        story.append(_bullet_list(actions, s["bullet"]))
        story.append(Spacer(1, 3))
    if next_s:
        story.append(_para(f"<b>{L['next_steps']}</b>", s["body_bold"]))
        story.append(_bullet_list(next_s, s["bullet"]))
    return story


# ---------------------------------------------------------------------------
# Main public API
# ---------------------------------------------------------------------------

def generate_pdf_report(data: Dict[str, Any], language: str = "en") -> bytes:
    """
    Generate a fully multilingual UdyamSaarthi PDF report.
    language: 'en', 'hi', or 'gu'. Defaults to 'en' if unrecognised.
    Financial values are invariant — only labels change.
    """
    lang = (language or "en").lower().strip()
    if lang not in PDF_LABELS:
        lang = "en"

    L = PDF_LABELS[lang]
    _register_fonts()
    s = _build_styles(lang)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36,
    )

    story = []

    # --- Header ---
    story.append(_para(L["title"], s["title"]))
    story.append(_para(L["tagline"], s["tagline"]))
    story.append(_para(L["sih"], s["sih"]))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=8))

    # --- Meta table ---
    rec = data.get("recommendation", {})
    fs = rec.get("feasibility_score", "N/A") if isinstance(rec, dict) else getattr(rec, "feasibility_score", "N/A")
    fr = rec.get("feasibility_rating", "") if isinstance(rec, dict) else getattr(rec, "feasibility_rating", "")
    cap = data.get("available_capital", 0) or 0

    meta_rows = [
        [_para(f"<b>{L['target_location']}:</b> {data.get('location', 'N/A')}", s["body"]),
         _para(f"<b>{L['business_category']}:</b> {data.get('business_category', 'N/A')}", s["body"])],
        [_para(f"<b>{L['margin_capital']}:</b> ₹{float(cap):,.2f}", s["body"]),
         _para(f"<b>{L['feasibility']}:</b> {fs}/100 ({fr})", s["body"])],
    ]
    mt = Table(meta_rows, colWidths=[270, 270])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 1, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(mt)
    story.append(Spacer(1, 8))

    # --- Sec 1: Financial ---
    story.append(_para(L["sec1"], s["section"]))
    story.append(_section_financial(data, L, s))
    story.append(Spacer(1, 8))

    # --- Sec 2: Working Capital ---
    story.append(_para(L["sec2"], s["section"]))
    story.append(_section_working_capital(data, L, s))
    story.append(Spacer(1, 8))

    # --- Sec 3: SWOT ---
    story.append(_para(L["sec3"], s["section"]))
    story.append(_section_swot(data, L, s))
    story.append(Spacer(1, 8))

    # --- Sec 4: Market & Opportunities ---
    story.append(_para(L["sec4"], s["section"]))
    market = data.get("market", {})
    mreach = market.get("market_reach_summary") if isinstance(market, dict) else getattr(market, "market_reach_summary", "")
    story.append(_para(f"<b>{L['market_reach']}:</b> {mreach or '—'}", s["body"]))
    story.append(Spacer(1, 4))

    opps = data.get("opportunities", {})
    items = opps.get("items") if isinstance(opps, dict) else getattr(opps, "items", [])
    if items:
        story.append(_para(f"<b>{L['top_opp']}</b>", s["body_bold"]))
        opp_lines = []
        for opp in (items if isinstance(items, list) else [])[:4]:
            if isinstance(opp, dict):
                opp_lines.append(f"• {opp.get('title', '')} — {opp.get('description', '')}")
            else:
                opp_lines.append(f"• {getattr(opp, 'title', '')} — {getattr(opp, 'description', '')}")
        story.append(_para("<br/>".join(opp_lines), s["bullet"]))
    story.append(Spacer(1, 8))

    # --- Sec 5: Risks ---
    story.append(_para(L["sec5"], s["section"]))
    story.append(_section_risks(data, L, s))
    story.append(Spacer(1, 8))

    # --- Sec 6: Competitors ---
    story.append(_para(L["sec6"], s["section"]))
    story.append(_section_competitors(data, L, s))
    story.append(Spacer(1, 8))

    # --- Sec 7: Pricing ---
    story.append(_para(L["sec7"], s["section"]))
    story.append(_section_pricing(data, L, s))
    story.append(Spacer(1, 8))

    # --- Sec 8: Recommendation ---
    story.append(_para(L["sec8"], s["section"]))
    for elem in _section_recommendation(data, L, s):
        story.append(elem)
    story.append(Spacer(1, 8))

    # --- Sec 9: AI Advisory ---
    ai_elems = _section_ai(data, L, s)
    if ai_elems:
        story.append(_para(L["sec9"], s["section"]))
        for elem in ai_elems:
            story.append(elem)
        story.append(Spacer(1, 8))

    # --- Disclaimer ---
    story.append(HRFlowable(width="100%", thickness=1,
                            color=colors.HexColor("#e11d48"), spaceAfter=5))
    story.append(_para(f"<b>{L['disclaimer_title']}</b>", s["disclaimer"]))
    story.append(_para(L["disclaimer_body"], s["disclaimer"]))
    story.append(_para(f"<i>{L['disclaimer_note']}</i>", s["subnote"]))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
