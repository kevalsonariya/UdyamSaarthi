import io
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_pdf_report(data: Dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    PRIMARY_COLOR = colors.HexColor("#1b4332")
    ACCENT_COLOR = colors.HexColor("#d97706")
    LIGHT_BG = colors.HexColor("#f8fafc")
    BORDER_COLOR = colors.HexColor("#cbd5e1")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=PRIMARY_COLOR,
        alignment=TA_LEFT,
    )

    tagline_style = ParagraphStyle(
        "DocTagline",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=11,
        leading=14,
        textColor=ACCENT_COLOR,
        alignment=TA_LEFT,
    )

    section_header = ParagraphStyle(
        "SectionHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=PRIMARY_COLOR,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1e293b"),
    )

    body_bold = ParagraphStyle(
        "BodyDarkBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#0f172a"),
    )

    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#991b1b"),
        alignment=TA_CENTER,
    )

    story = []

    story.append(Paragraph("BizSahayak / UdyamSaarthi", title_style))
    story.append(Paragraph("From Business Idea &rarr; Business Insight &rarr; Financial Plan", tagline_style))
    story.append(Paragraph("SIH26091 &bull; AI-Driven Hyper-Local Business Advisory & Financial Structuring Dossier", body_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY_COLOR, spaceAfter=10))

    meta_table_data = [
        [
            Paragraph("<b>Target Location:</b> " + str(data.get("location", "N/A")), body_style),
            Paragraph("<b>Business Category:</b> " + str(data.get("business_category", "N/A")), body_style),
        ],
        [
            Paragraph(f"<b>Available Margin Capital:</b> &#8377;{data.get('available_capital', 0):,.2f}", body_style),
            Paragraph(f"<b>Feasibility Score:</b> {data.get('recommendation', {}).get('feasibility_score', 'N/A')}/100 ({data.get('recommendation', {}).get('feasibility_rating', 'N/A')})", body_style),
        ],
    ]
    meta_table = Table(meta_table_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Deterministic Financial Structuring & Scheme Allocation", section_header))
    fin = data.get("financial", {})
    sch = data.get("scheme", {})
    emi = data.get("emi", {})

    fin_table_data = [
        [
            Paragraph("<b>Parameter</b>", body_bold),
            Paragraph("<b>Calculated Value</b>", body_bold),
            Paragraph("<b>Regulatory Rule / Scheme Norm</b>", body_bold),
        ],
        [
            Paragraph("Total Project Cost", body_style),
            Paragraph(f"&#8377;{fin.get('project_cost', 0):,.2f}", body_bold),
            Paragraph("Available Margin / 10%", body_style),
        ],
        [
            Paragraph("Promoter Margin Capital", body_style),
            Paragraph(f"&#8377;{fin.get('promoter_contribution', 0):,.2f}", body_style),
            Paragraph("10.0% Minimum mandatory borrower equity", body_style),
        ],
        [
            Paragraph("Maximum Loan Eligible", body_style),
            Paragraph(f"&#8377;{fin.get('max_loan_amount', 0):,.2f}", body_bold),
            Paragraph("90.0% of Total Project Cost", body_style),
        ],
        [
            Paragraph("Recommended Scheme", body_style),
            Paragraph(f"<b>{sch.get('scheme_name', 'N/A')}</b> ({sch.get('scheme_code', '')})", body_style),
            Paragraph("Automatic deterministic routing rule based on &#8377;1.40L threshold", body_style),
        ],
        [
            Paragraph("Concessional Interest Rate", body_style),
            Paragraph(f"<b>{sch.get('interest_rate_percent', 0)}% p.a.</b>", body_style),
            Paragraph("Subsidized priority-sector lending interest rate", body_style),
        ],
        [
            Paragraph("Tenure & Moratorium", body_style),
            Paragraph(f"{sch.get('tenure_years', 0)} Years ({sch.get('tenure_months', 0)} Mo)", body_style),
            Paragraph(f"<b>{sch.get('moratorium_months', 0)} Months</b> Principal Grace/Gestation", body_style),
        ],
        [
            Paragraph("Monthly Installment (Post-Moratorium EMI)", body_style),
            Paragraph(f"<b>&#8377;{emi.get('monthly_emi', 0):,.2f}</b>", body_bold),
            Paragraph(f"Moratorium monthly interest: &#8377;{emi.get('moratorium_monthly_interest', 0):,.2f}", body_style),
        ],
        [
            Paragraph("Total Repayment Amount", body_style),
            Paragraph(f"&#8377;{emi.get('total_repayment_amount', 0):,.2f}", body_style),
            Paragraph(f"Principal: &#8377;{emi.get('principal_amount', 0):,.2f} + Interest: &#8377;{emi.get('total_interest_payable', 0):,.2f}", body_style),
        ],
    ]
    fin_table = Table(fin_table_data, colWidths=[170, 150, 220])
    fin_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(fin_table)
    story.append(Spacer(1, 10))

    wc = data.get("working_capital", {})
    story.append(Paragraph("2. Monthly Working Capital Planning & Cash Reserve", section_header))
    wc_table_data = [
        [
            Paragraph("<b>Cost Category</b>", body_bold),
            Paragraph("<b>Monthly Allocation</b>", body_bold),
            Paragraph("<b>Category</b>", body_bold),
            Paragraph("<b>Monthly Allocation</b>", body_bold),
        ],
        [
            Paragraph("Raw Materials & Goods", body_style),
            Paragraph(f"&#8377;{wc.get('monthly_raw_materials', 0):,.2f}", body_style),
            Paragraph("Labor & Operations Wage", body_style),
            Paragraph(f"&#8377;{wc.get('monthly_labor_wages', 0):,.2f}", body_style),
        ],
        [
            Paragraph("Shop Rent & Utilities", body_style),
            Paragraph(f"&#8377;{wc.get('monthly_rent_utilities', 0):,.2f}", body_style),
            Paragraph("Logistics & Packaging", body_style),
            Paragraph(f"&#8377;{wc.get('monthly_logistics_packaging', 0):,.2f}", body_style),
        ],
        [
            Paragraph("Monthly Contingency Buffer", body_style),
            Paragraph(f"&#8377;{wc.get('monthly_contingency_buffer', 0):,.2f}", body_style),
            Paragraph("Total Monthly Operating Opex", body_bold),
            Paragraph(f"<b>&#8377;{wc.get('total_monthly_operating_expense', 0):,.2f}</b>", body_bold),
        ],
        [
            Paragraph("Recommended 3-Mo Cash Reserve", body_bold),
            Paragraph(f"<b>&#8377;{wc.get('recommended_3_months_reserve', 0):,.2f}</b>", body_bold),
            Paragraph("Monthly Break-Even Revenue", body_bold),
            Paragraph(f"<b>&#8377;{wc.get('break_even_monthly_revenue', 0):,.2f}</b>", body_bold),
        ],
    ]
    wc_table = Table(wc_table_data, colWidths=[140, 130, 140, 130])
    wc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(wc_table)
    story.append(Spacer(1, 10))

    swot = data.get("swot", {})
    story.append(Paragraph("3. Strategic SWOT Matrix", section_header))
    strengths_html = "<br/>&bull; " + "<br/>&bull; ".join(swot.get("strengths", ["N/A"]))
    weaknesses_html = "<br/>&bull; " + "<br/>&bull; ".join(swot.get("weaknesses", ["N/A"]))
    opps_html = "<br/>&bull; " + "<br/>&bull; ".join(swot.get("opportunities", ["N/A"]))
    threats_html = "<br/>&bull; " + "<br/>&bull; ".join(swot.get("threats", ["N/A"]))

    swot_table_data = [
        [
            Paragraph("<b>Strengths</b>" + strengths_html, body_style),
            Paragraph("<b>Weaknesses</b>" + weaknesses_html, body_style),
        ],
        [
            Paragraph("<b>Opportunities</b>" + opps_html, body_style),
            Paragraph("<b>Threats</b>" + threats_html, body_style),
        ],
    ]
    swot_table = Table(swot_table_data, colWidths=[270, 270])
    swot_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#f0fdf4")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#fef2f2")),
        ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#eff6ff")),
        ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#fffbeb")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(swot_table)
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e11d48"), spaceAfter=5))
    story.append(Paragraph("<b>MANDATORY FINANCIAL DISCLAIMER</b>", disclaimer_style))
    story.append(Paragraph(
        "\"Indicative calculation for planning purposes. Verify applicable scheme terms before making financial decisions.\"",
        disclaimer_style,
    ))
    story.append(Paragraph(
        "<i>Note: Hyper-local market reach, competitor maps, and demographic projections represent prototype simulation data.</i>",
        ParagraphStyle("SubNote", parent=styles["Normal"], fontSize=7.5, leading=10, textColor=colors.HexColor("#64748b"), alignment=TA_CENTER)
    ))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
