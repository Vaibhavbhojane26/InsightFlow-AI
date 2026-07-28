from io import BytesIO
from datetime import datetime
import os

import pandas as pd
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)


# ==========================================================
# PROFESSIONAL PDF REPORT
# ==========================================================

def generate_pdf_report(df):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(8.27 * inch, 11.69 * inch),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#0F4C81")

    heading = styles["Heading1"]
    heading.textColor = colors.HexColor("#2563EB")

    sub_heading = styles["Heading2"]
    sub_heading.textColor = colors.HexColor("#1F2937")

    normal = styles["BodyText"]

    elements = []

    # ==========================================================
    # LOGO
    # ==========================================================

    logo_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "assets",
        "logo.png"
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=210,
            height=85
        )

        elements.append(logo)
        elements.append(Spacer(1,20))

    # ==========================================================
    # COVER PAGE
    # ==========================================================

    elements.append(
        Paragraph(
            "<b>PROJECT REPORT</b>",
            title_style
        )
    )

    elements.append(Spacer(1,25))

    elements.append(
        Paragraph(
            "<b>Enterprise Data Intelligence Platform</b>",
            sub_heading
        )
    )

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            f"<b>Generated :</b> {datetime.now().strftime('%d-%m-%Y %I:%M %p')}",
            normal
        )
    )

    elements.append(
        Paragraph(
            "<b>Application :</b> InsightFlow AI",
            normal
        )
    )

    elements.append(
        Paragraph(
            "<b>Developer :</b> Vaibhav Bhojane",
            normal
        )
    )

    elements.append(
        Paragraph(
            "<b>Version :</b> 2.0",
            normal
        )
    )

    elements.append(PageBreak())

        # ==========================================================
    # EXECUTIVE SUMMARY
    # ==========================================================

    elements.append(
        Paragraph(
            "Executive Summary",
            heading
        )
    )

    elements.append(Spacer(1,10))

    summary = """
    InsightFlow AI is an enterprise-level data analytics platform
    designed to simplify the complete data analysis workflow.

    The application enables users to upload datasets,
    clean and preprocess data,
    perform statistical analysis,
    generate visualizations,
    create AI-driven insights,
    and export professional reports.

    The objective of this platform is to reduce manual effort,
    improve productivity,
    and support data-driven decision making.
    """

    elements.append(
        Paragraph(
            summary,
            normal
        )
    )

    elements.append(Spacer(1,25))

    # ==========================================================
    # DATASET OVERVIEW
    # ==========================================================

    rows = df.shape[0]
    cols = df.shape[1]

    missing = int(df.isnull().sum().sum())
    duplicate = int(df.duplicated().sum())

    memory = round(
        df.memory_usage(deep=True).sum()/1024/1024,
        2
    )

    numeric_columns = len(
        df.select_dtypes(include="number").columns
    )

    categorical_columns = len(
        df.select_dtypes(
            include=["object","category"]
        ).columns
    )

    quality_score = round(
        ((rows * cols - missing) /
        (rows * cols)) * 100,
        2
    )

    if quality_score >= 90:
        dataset_status = "Excellent"

    elif quality_score >= 70:
        dataset_status = "Good"

    elif quality_score >= 50:
        dataset_status = "Average"

    else:
        dataset_status = "Poor"

    elements.append(
        Paragraph(
            "Dataset Overview",
            heading
        )
    )

    overview = [

        ["Metric","Value"],

        ["Total Rows",f"{rows:,}"],

        ["Total Columns",cols],

        ["Memory Usage",f"{memory} MB"],

        ["Missing Values",missing],

        ["Duplicate Rows",duplicate],

        ["Numeric Columns",numeric_columns],

        ["Categorical Columns",categorical_columns],

        ["Quality Score",f"{quality_score}%"],

        ["Dataset Status",dataset_status]

    ]

    overview_table = Table(
        overview,
        colWidths=[220,220]
    )

    overview_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),10)

    ]))

    elements.append(overview_table)

    elements.append(Spacer(1,25))

        # ==========================================================
    # DATA QUALITY ANALYSIS
    # ==========================================================

    elements.append(
        Paragraph(
            "Data Quality Analysis",
            heading
        )
    )

    elements.append(Spacer(1,10))

    quality_data = [

        ["Validation","Result"],

        ["Missing Values", str(missing)],

        ["Duplicate Rows", str(duplicate)],

        ["Numeric Columns", str(numeric_columns)],

        ["Categorical Columns", str(categorical_columns)],

        ["Overall Quality", f"{quality_score}%"],

        ["Dataset Status", dataset_status]

    ]

    quality_table = Table(
        quality_data,
        colWidths=[220,220]
    )

    quality_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#16A34A")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

    ]))

    elements.append(quality_table)

    elements.append(Spacer(1,25))

    # ==========================================================
    # COLUMN SUMMARY
    # ==========================================================

    elements.append(
        Paragraph(
            "Column Summary",
            heading
        )
    )

    column_summary = [[

        "Column",

        "Datatype",

        "Missing",

        "Unique"

    ]]

    for column in df.columns:

        column_summary.append([

            str(column),

            str(df[column].dtype),

            str(df[column].isnull().sum()),

            str(df[column].nunique())

        ])

    column_table = Table(column_summary)

    column_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1D4ED8")),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

    ]))

    elements.append(column_table)

    elements.append(Spacer(1,25))

    # ==========================================================
    # NUMERICAL STATISTICS
    # ==========================================================

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:

        elements.append(
            Paragraph(
                "Numerical Statistics",
                heading
            )
        )

        statistics = [[

            "Column",

            "Mean",

            "Median",

            "Minimum",

            "Maximum",

            "Std Dev"

        ]]

        for column in numeric_df.columns:

            statistics.append([

                str(column),

                f"{numeric_df[column].mean():.2f}",

                f"{numeric_df[column].median():.2f}",

                f"{numeric_df[column].min():.2f}",

                f"{numeric_df[column].max():.2f}",

                f"{numeric_df[column].std():.2f}"

            ])

        statistics_table = Table(statistics)

        statistics_table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0F766E")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

        ]))

        elements.append(statistics_table)

        elements.append(Spacer(1,25))

            # ==========================================================
    # AI BUSINESS INSIGHTS
    # ==========================================================

    elements.append(
        Paragraph(
            "AI Business Insights",
            heading
        )
    )

    elements.append(Spacer(1, 10))

    insights = []

    insights.append(
        f"• The dataset contains <b>{rows:,}</b> records and <b>{cols}</b> columns."
    )

    if missing == 0:
        insights.append(
            "• No missing values were detected in the dataset."
        )
    else:
        insights.append(
            f"• A total of <b>{missing}</b> missing values were detected."
        )

    if duplicate == 0:
        insights.append(
            "• No duplicate records were found."
        )
    else:
        insights.append(
            f"• The dataset contains <b>{duplicate}</b> duplicate records."
        )

    if quality_score >= 90:
        insights.append(
            "• The dataset quality is excellent and suitable for advanced analytics."
        )
    elif quality_score >= 70:
        insights.append(
            "• The dataset quality is good but minor preprocessing is recommended."
        )
    else:
        insights.append(
            "• The dataset requires cleaning before analysis."
        )

    for col in numeric_df.columns:

        insights.append(
            f"• {col}: Average = {numeric_df[col].mean():.2f}, "
            f"Maximum = {numeric_df[col].max():.2f}, "
            f"Minimum = {numeric_df[col].min():.2f}"
        )

    for item in insights:

        elements.append(
            Paragraph(item, normal)
        )

    elements.append(Spacer(1,20))

    # ==========================================================
    # RECOMMENDATIONS
    # ==========================================================

    elements.append(
        Paragraph(
            "Recommendations",
            heading
        )
    )

    recommendations = [

        "Clean missing values before performing Machine Learning.",

        "Remove duplicate records to improve accuracy.",

        "Validate data types before visualization.",

        "Detect and remove outliers from numerical columns.",

        "Create dashboards for better business understanding.",

        "Use predictive analytics for future business forecasting."

    ]

    for rec in recommendations:

        elements.append(
            Paragraph(
                "• " + rec,
                normal
            )
        )

    elements.append(Spacer(1,20))

    # ==========================================================
    # CONCLUSION
    # ==========================================================

    elements.append(
        Paragraph(
            "Conclusion",
            heading
        )
    )

    conclusion = f"""
    This report has been automatically generated by <b>InsightFlow AI</b>.

    The uploaded dataset consists of <b>{rows:,}</b> records and
    <b>{cols}</b> columns with an overall data quality score of
    <b>{quality_score}%</b>.

    Based on the statistical analysis, quality assessment and AI-generated
    insights, the dataset is suitable for business analytics after applying
    the recommended preprocessing steps.

    InsightFlow AI provides an end-to-end platform for uploading datasets,
    cleaning data, analysing information, generating visualizations,
    producing AI-driven insights and exporting professional reports.
    """

    elements.append(
        Paragraph(
            conclusion,
            normal
        )
    )

    elements.append(Spacer(1,30))

    elements.append(
        Paragraph(
            "<b>Generated by InsightFlow AI</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "Developed by Vaibhav Bhojane",
            normal
        )
    )

    # ==========================================================
    # BUILD PDF
    # ==========================================================

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    st.download_button(
        "📄 Download Professional PDF Report",
        data=pdf,
        file_name="InsightFlow_AI_Professional_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )