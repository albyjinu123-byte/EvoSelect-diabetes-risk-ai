"""
Page 5: Research Report.
Renders the complete research evaluation report and provides one-click downloads
for PDF, Markdown, JSON data audit, and CSV benchmark tables.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from src.config import REPORTS_DIR, TABLES_DIR
from src.report_generator import (
    generate_research_report_markdown,
    generate_research_report_pdf,
)

st.set_page_config(page_title="Formal Research Report", page_icon="📑", layout="wide")

st.title("📑 Formal Research Report & Clinical Evaluation")
st.markdown(
    "Review and download the comprehensive research monograph documenting multi-cohort data auditing, "
    "algorithm benchmarks, clinical ablation studies, and ethical governance."
)

# Ensure reports are generated
pdf_path = REPORTS_DIR / "diabetes_risk_research_report.pdf"
md_path = REPORTS_DIR / "comprehensive_research_report.md"

if not pdf_path.exists() or not md_path.exists():
    with st.spinner("Compiling formal research monograph..."):
        generate_research_report_markdown()
        generate_research_report_pdf()

# Download Action Bar
st.subheader("📥 Download Research Artifacts")
d1, d2, d3, d4 = st.columns(4)

with d1:
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF Monograph",
                data=f.read(),
                file_name="diabetes_risk_research_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

with d2:
    if md_path.exists():
        with open(md_path, "r") as f:
            st.download_button(
                label="📝 Download Markdown Report",
                data=f.read(),
                file_name="comprehensive_research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

with d3:
    audit_json = REPORTS_DIR / "data_audit_report.json"
    if audit_json.exists():
        with open(audit_json, "r") as f:
            st.download_button(
                label="📊 Download Data Audit JSON",
                data=f.read(),
                file_name="data_audit_report.json",
                mime="application/json",
                use_container_width=True,
            )

with d4:
    clin_csv = TABLES_DIR / "clinical_model_comparison.csv"
    if clin_csv.exists():
        with open(clin_csv, "r") as f:
            st.download_button(
                label="📈 Download Clinical CSV Metrics",
                data=f.read(),
                file_name="clinical_model_comparison.csv",
                mime="text/csv",
                use_container_width=True,
            )

st.markdown("---")

# Render Report Markdown Inline
st.subheader("📖 Monograph Document Viewer")

if md_path.exists():
    with open(md_path, "r") as f:
        report_content = f.read()
    st.markdown(report_content)
else:
    st.info("Report content currently compiling...")
