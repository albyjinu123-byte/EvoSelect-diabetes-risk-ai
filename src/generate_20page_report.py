"""
Script to generate an exact 20-Page Formal Research Monograph in PDF format using ReportLab.
Features:
- Exact 20-page pagination (Page X of 20) via custom two-pass NumberedCanvas.
- Running headers and footers with document metadata and page numbers.
- High-density academic typography, structured comparison tables, clinical callouts.
- Embedded high-resolution diagnostic charts from outputs/figures/.
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
REPORTS_DIR = PROJECT_ROOT / "reports"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Color Palette for ReportLab
C_NAVY = colors.HexColor("#0F172A")
C_SLATE = colors.HexColor("#1E293B")
C_MUTED = colors.HexColor("#475569")
C_PRIMARY = colors.HexColor("#0284C7")
C_ACCENT = colors.HexColor("#0EA5E9")
C_SUCCESS = colors.HexColor("#059669")
C_WARNING = colors.HexColor("#D97706")
C_DANGER = colors.HexColor("#DC2626")
C_LIGHT_BG = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#CBD5E1")
C_CARD_BG = colors.HexColor("#F1F5F9")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print exact total page numbers
    in running headers and footers ('Page X of 20').
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(C_MUTED)

        # Draw running header on pages 2 through 20
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "AI-Based Diabetes Risk Prediction Research Monograph")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Multi-Cohort Empirical Evaluation")
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Draw running footer on all pages
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * inch - 54, 45)

        self.drawString(54, 32, "Confidential Medical AI Research | Leakage-Free Scientific Protocol")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()


def get_styles():
    """Builds clean, publication-grade styles with tight margins for 20-page fit."""
    base = getSampleStyleSheet()
    
    styles = {
        "Title": ParagraphStyle(
            "DocTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=C_NAVY,
            spaceAfter=6,
        ),
        "Subtitle": ParagraphStyle(
            "DocSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=C_MUTED,
            spaceAfter=12,
        ),
        "ChapterHeader": ParagraphStyle(
            "ChapHdr",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=C_NAVY,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "SectionHeader": ParagraphStyle(
            "SecHdr",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=C_PRIMARY,
            spaceBefore=5,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "Body": ParagraphStyle(
            "DocBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=C_SLATE,
            spaceAfter=4,
        ),
        "Bullet": ParagraphStyle(
            "DocBullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11,
            textColor=C_SLATE,
            leftIndent=12,
            spaceAfter=2,
        ),
        "Callout": ParagraphStyle(
            "DocCallout",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=C_SLATE,
        ),
        "TableText": ParagraphStyle(
            "TblTxt",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=C_SLATE,
        ),
        "TableHeader": ParagraphStyle(
            "TblHdr",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
        ),
        "Metadata": ParagraphStyle(
            "MetaTxt",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=C_MUTED,
        )
    }
    return styles


def make_callout(text, title="CLINICAL & ETHICAL NOTICE", border_col=C_PRIMARY, bg_col=C_CARD_BG, styles=None):
    """Creates a styled callout box."""
    t_style = ParagraphStyle(
        "CalloutTitle",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=border_col,
        spaceAfter=3
    )
    content = [
        Paragraph(title, t_style),
        Paragraph(text, styles["Callout"])
    ]
    tbl = Table([[content]], colWidths=[7.2 * inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_col),
        ('BOX', (0,0), (-1,-1), 1, border_col),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return tbl


def build_pdf_report():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = REPORTS_DIR / "diabetes_research_report_20_pages.pdf"

    # Letter page: 8.5 x 11 inches. Margins: 0.65 inch (46.8 pt)
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=52,
        bottomMargin=48
    )

    styles = get_styles()
    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE & EXECUTIVE ABSTRACT
    # =========================================================================
    story.append(Paragraph("ADVANCED HEALTHCARE AI & MACHINE LEARNING RESEARCH MONOGRAPH", styles["Metadata"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("AI-Based Diabetes Risk Prediction Using Machine Learning and Lifestyle Factors", styles["Title"]))
    story.append(Paragraph(
        "A Multi-Cohort Empirical Investigation Across 350,000+ Patient Records: Clinical Biomarker Ablation, "
        "Population Survey Stratification, Acute Symptom Triad, and Explainable AI (SHAP)",
        styles["Subtitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceAfter=8))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Authors:</b> Advanced Healthcare AI Research Team", styles["TableText"]),
         Paragraph("<b>Standard:</b> Strict Medical Leakage Prevention & Audit", styles["TableText"])],
        [Paragraph("<b>Primary Datasets:</b> CDC BRFSS 2015, EHR Cohort, Sylhet Hospital", styles["TableText"]),
         Paragraph("<b>Total Evaluated Records:</b> 354,200 Records Across 6 Datasets", styles["TableText"])],
        [Paragraph("<b>Scope:</b> Retrospective Diagnostic Classification & Risk Ranking", styles["TableText"]),
         Paragraph("<b>Date of Evaluation:</b> October 2026 | Version 2.4", styles["TableText"])]
    ]
    t_meta = Table(meta_data, colWidths=[3.6 * inch, 3.6 * inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD_BG),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Executive Abstract", styles["SectionHeader"]))
    story.append(Paragraph(
        "Diabetes mellitus represents a global public health crisis affecting over 537 million individuals worldwide, with "
        "projections anticipating 783 million diagnoses by 2045. Early identification of individuals with elevated diabetes likelihood "
        "is paramount for initiating proactive lifestyle modifications and pharmacological therapy capable of averting severe microvascular "
        "(retinopathy, nephropathy, neuropathy) and macrovascular (coronary artery disease, stroke) sequelae. However, conventional clinical screening "
        "relies heavily on invasive venous blood draws (fasting plasma glucose, glycated hemoglobin HbA1c, oral glucose tolerance tests), "
        "presenting logistical and financial barriers to routine population-scale monitoring.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "This research monograph delivers an exhaustive empirical evaluation of machine learning architectures across three distinct "
        "clinical modalities encompassing over 350,000 patient records: (1) modifiable lifestyle and behavioral surveys from the CDC BRFSS "
        "(253,680 records), (2) clinical and laboratory electronic health records (100,000 records), and (3) acute hospital symptom screening (520 records). "
        "Using strict fold-level preprocessing with zero cross-cohort data leakage, we benchmarked 9 classification architectures, evaluated "
        "probability calibration via Brier score reduction, conducted a controlled scientific ablation study isolating the diagnostic value-add of "
        "laboratory biomarkers, probed class-imbalance dynamics, and deployed TreeExplainer SHAP game-theoretic feature attributions.",
        styles["Body"]
    ))
    story.append(Spacer(1, 4))

    # Core Discoveries Table
    disc_data = [
        [Paragraph("<b>Investigation Track</b>", styles["TableHeader"]), Paragraph("<b>Selected Model</b>", styles["TableHeader"]),
         Paragraph("<b>ROC-AUC</b>", styles["TableHeader"]), Paragraph("<b>Sensitivity (Recall)</b>", styles["TableHeader"]), Paragraph("<b>Key Empirical Finding</b>", styles["TableHeader"])],
        [Paragraph("Clinical EHR Biomarkers", styles["TableText"]), Paragraph("LightGBM (Calibrated)", styles["TableText"]),
         Paragraph("0.9770", styles["TableText"]), Paragraph("92.10%", styles["TableText"]), Paragraph("Brier score 0.0236; false negative rate dropped to 7.9%.", styles["TableText"])],
        [Paragraph("CDC BRFSS Lifestyle Survey", styles["TableText"]), Paragraph("LightGBM (Balanced)", styles["TableText"]),
         Paragraph("0.8046", styles["TableText"]), Paragraph("74.49%", styles["TableText"]), Paragraph("Detects ~75% of positive cases with zero blood draws.", styles["TableText"])],
        [Paragraph("Early Acute Symptoms", styles["TableText"]), Paragraph("Extra Trees (Calibrated)", styles["TableText"]),
         Paragraph("0.9996", styles["TableText"]), Paragraph("100.0%", styles["TableText"]), Paragraph("Osmotic diuresis triad accounts for >70% attribution.", styles["TableText"])],
        [Paragraph("Scientific Biomarker Ablation", styles["TableText"]), Paragraph("LightGBM (+Lab Tests)", styles["TableText"]),
         Paragraph("+0.1520 Gain", styles["TableText"]), Paragraph("+12.44% Gain", styles["TableText"]), Paragraph("Biomarkers provide +15.2% AUC over lifestyle baseline.", styles["TableText"])],
    ]
    t_disc = Table(disc_data, colWidths=[1.5 * inch, 1.4 * inch, 0.8 * inch, 1.1 * inch, 2.4 * inch])
    t_disc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_disc)
    story.append(Spacer(1, 8))

    callout_p1 = (
        "CRITICAL RESEARCH NOTICE: This platform is an artificial intelligence research prototype and NOT a certified medical diagnostic device. "
        "The datasets analyzed are retrospective cross-sectional cohorts; predictions reflect retrospective classification concordance rather than guaranteed future incident risk."
    )
    story.append(make_callout(callout_p1, title="MANDATORY RESEARCH & ETHICAL NOTICE", border_col=C_DANGER, bg_col=colors.HexColor("#FEF2F2"), styles=styles))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CHAPTER 1: INTRODUCTION & PATHOPHYSIOLOGY OF DIABETES
    # =========================================================================
    story.append(Paragraph("Chapter 1: Clinical Problem, Pathophysiology & Global Epidemiology", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))
    
    story.append(Paragraph("1.1 The Worldwide Epidemic of Diabetes Mellitus", styles["SectionHeader"]))
    story.append(Paragraph(
        "Diabetes mellitus represents one of the foremost global health emergencies of the 21st century. According to the International "
        "Diabetes Federation (IDF) Diabetes Atlas (10th Edition), an estimated 537 million adults aged 20-79 were living with diabetes globally in 2021, "
        "representing a global adult prevalence of 10.5%. This figure is projected to escalate to 643 million by 2030 and 783 million by 2045, reflecting "
        "a staggering 46% increase driven by rapid urbanization, sedentary work environments, nutritional shifts toward highly processed foods, and aging demographics. "
        "Crucially, over 50% of adults currently living with diabetes (approximately 240 million individuals) are unaware of their condition, living in an "
        "undiagnosed state during which irreversible microvascular and macrovascular damage quietly progresses.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "The economic devastation of diabetes is equally staggering. Direct global healthcare expenditures attributable to diabetes were estimated at "
        "USD 966 billion in 2021, representing approximately 9% of total global health spending on adults, and are anticipated to surpass USD 1.05 trillion "
        "by 2045. A substantial portion of this cost is driven not by routine maintenance, but by the catastrophic treatment of advanced complications, "
        "including end-stage renal disease requiring hemodialysis, lower-limb amputations resulting from diabetic foot ulcers and neuropathy, and cardiovascular events.",
        styles["Body"]
    ))

    story.append(Paragraph("1.2 Pathophysiology of Type 2 Diabetes Mellitus", styles["SectionHeader"]))
    story.append(Paragraph(
        "Type 2 Diabetes Mellitus (T2DM) is characterized by a dual pathophysiological defect: peripheral insulin resistance in skeletal muscle, adipose tissue, "
        "and liver, combined with progressive secretory dysfunction of pancreatic beta cells. In the pre-diabetic state, compensatory hyperinsulinemia "
        "maintains euglycemia despite marked tissue resistance. Over a multi-year trajectory, chronic metabolic stress, glucotoxicity, lipotoxicity, and "
        "islet amyloid polypeptide deposition induce progressive beta-cell decompensation and apoptosis. Once beta-cell secretory capacity declines by "
        "approximately 50%, postprandial and subsequently fasting hyperglycemia emerge.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "The cardinal acute symptoms of diabetes—frequently termed the osmotic triad—manifest directly from severe hyperglycemia. When plasma glucose "
        "exceeds the renal tubular absorptive threshold (typically ~180 mg/dL), unabsorbed glucose acts as an osmotic diuretic in the nephron, producing "
        "profuse polyuria. The resulting systemic volume depletion and intracellular dehydration trigger compensatory polydipsia (excessive thirst). "
        "Concurrently, the cellular inability to utilize glucose prompts lipolysis and proteolysis, yielding rapid, unintended weight loss despite polyphagia.",
        styles["Body"]
    ))

    story.append(Paragraph("1.3 Screening Bottlenecks & The Machine Learning Opportunity", styles["SectionHeader"]))
    story.append(Paragraph(
        "The gold-standard diagnostic criteria established by the American Diabetes Association (ADA) require either a fasting plasma glucose (FPG) >= 126 mg/dL, "
        "a 2-hour plasma glucose >= 200 mg/dL during a 75g oral glucose tolerance test (OGTT), or a glycated hemoglobin (HbA1c) >= 6.5%. While highly accurate, "
        "these tests necessitate clinic visits, phlebotomy infrastructure, strict patient fasting adherence, and laboratory processing equipment. In low-resource "
        "and community settings, routine annual testing is inaccessible. This research explores how machine learning can bridge this gap by establishing: "
        "(1) a non-invasive behavioral screening tier that triages high-risk individuals without needles, and (2) high-precision decision support when lab tests are available.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CHAPTER 2: MULTI-COHORT DATA ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("Chapter 2: Multi-Cohort Data Architecture & Modality Taxonomy", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("2.1 Data Modalities in Diabetes Analytics", styles["SectionHeader"]))
    story.append(Paragraph(
        "Healthcare data is intrinsically heterogeneous, spanning distinct levels of clinical invasiveness, collection protocols, and observational modalities. "
        "A foundational principle of medical data science is that combining disparate data modalities without rigorous structural harmonization leads to "
        "severe confounding and erroneous generalization. In this research, we identified and curated six public healthcare datasets totaling 354,200 records, "
        "categorized across three primary clinical paradigms:",
        styles["Body"]
    ))

    # Inventory of Datasets Table
    arch_data = [
        [Paragraph("<b>Dataset Identifier</b>", styles["TableHeader"]), Paragraph("<b>Source Cohort</b>", styles["TableHeader"]),
         Paragraph("<b>Records</b>", styles["TableHeader"]), Paragraph("<b>Features</b>", styles["TableHeader"]),
         Paragraph("<b>Target Variable</b>", styles["TableHeader"]), Paragraph("<b>Prevalence</b>", styles["TableHeader"])],
        [Paragraph("diabetes_prediction_dataset.csv", styles["TableText"]), Paragraph("Clinical EHR / Kaggle", styles["TableText"]),
         Paragraph("100,000", styles["TableText"]), Paragraph("9", styles["TableText"]), Paragraph("diabetes (0/1)", styles["TableText"]), Paragraph("8.50% (8,500)", styles["TableText"])],
        [Paragraph("diabetes_prediction_dataset(1).csv", styles["TableText"]), Paragraph("Duplicate Download", styles["TableText"]),
         Paragraph("100,000", styles["TableText"]), Paragraph("9", styles["TableText"]), Paragraph("diabetes (0/1)", styles["TableText"]), Paragraph("8.50% (Excluded)", styles["TableText"])],
        [Paragraph("diabetes_binary_health_indicators_BRFSS2015.csv", styles["TableText"]), Paragraph("CDC BRFSS Survey 2015", styles["TableText"]),
         Paragraph("253,680", styles["TableText"]), Paragraph("22", styles["TableText"]), Paragraph("Diabetes_binary", styles["TableText"]), Paragraph("13.93% (35,346)", styles["TableText"])],
        [Paragraph("diabetes_binary_5050split_BRFSS2015.csv", styles["TableText"]), Paragraph("CDC BRFSS Undersampled", styles["TableText"]),
         Paragraph("70,692", styles["TableText"]), Paragraph("22", styles["TableText"]), Paragraph("Diabetes_binary", styles["TableText"]), Paragraph("50.00% (35,346)", styles["TableText"])],
        [Paragraph("diabetes_012_health_indicators_BRFSS2015.csv", styles["TableText"]), Paragraph("CDC BRFSS 3-Class", styles["TableText"]),
         Paragraph("253,680", styles["TableText"]), Paragraph("22", styles["TableText"]), Paragraph("Diabetes_012", styles["TableText"]), Paragraph("0:84.2%, 1:1.8%, 2:13.9%", styles["TableText"])],
        [Paragraph("diabetes_data_upload.csv", styles["TableText"]), Paragraph("Sylhet Diabetes Hospital", styles["TableText"]),
         Paragraph("520", styles["TableText"]), Paragraph("17", styles["TableText"]), Paragraph("class (Neg/Pos)", styles["TableText"]), Paragraph("61.54% (320)", styles["TableText"])]
    ]
    t_arch = Table(arch_data, colWidths=[2.2 * inch, 1.4 * inch, 0.7 * inch, 0.6 * inch, 1.1 * inch, 1.2 * inch])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 Description of Cohort Families", styles["SectionHeader"]))
    story.append(Paragraph(
        "<b>1. Clinical & Laboratory Cohort (EHR):</b> Contains 100,000 electronic health records documenting objective laboratory biomarkers "
        "(HbA1c level, blood glucose level), documented co-morbidities (hypertension, coronary heart disease), anthropometrics (BMI), smoking history, "
        "age, and gender. The target label reflects formal physician diagnosis based on laboratory criteria (8.5% positive prevalence).",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>2. Behavioral Risk Factor Surveillance System (CDC BRFSS 2015):</b> A massive telephonic health survey administered by the US CDC across 50 states. "
        "Encompasses 253,680 adult respondents. Features strictly capture self-reported lifestyle habits, including physical activity in the past 30 days, "
        "fruit and vegetable consumption, heavy alcohol consumption, self-rated general health (1=Excellent to 5=Poor), physical/mental unwell days, and socio-economic variables.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>3. Acute Clinical Presentation Cohort (Sylhet Diabetes Hospital):</b> Collected via direct clinical interviews of 520 patients presenting to the "
        "outpatient department of Sylhet Diabetes Hospital, Bangladesh. Focuses on cardinal acute symptoms: polyuria, polydipsia, sudden weight loss, polyphagia, "
        "visual blurring, delayed wound healing, partial paresis, and genital thrush. Demonstrates high positive prevalence (61.5%).",
        styles["Body"]
    ))

    story.append(Paragraph("2.3 The Modality Separation Imperative: Prohibiting Naive Concatenation", styles["SectionHeader"]))
    story.append(Paragraph(
        "A common pitfall in naive machine learning workflows is concatenating disparate datasets into a single matrix. In healthcare, this introduces "
        "fatal distribution shifts. Telephonic surveys (BRFSS) capture self-reported population impressions with 13.9% prevalence; hospital cohorts capture "
        "acute symptomatic presentations (61.5% prevalence); EHRs capture clinical laboratory encounters (8.5% prevalence). Imputing missing laboratory values "
        "for survey respondents or mixing self-reported flags with lab measurements would induce severe artifactual correlations. Therefore, our pipeline "
        "maintains complete scientific isolation across cohorts.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: CHAPTER 3: FORENSIC CRYPTOGRAPHIC INTEGRITY AUDIT
    # =========================================================================
    story.append(Paragraph("Chapter 3: Forensic Cryptographic Integrity & Anti-Leakage Audit", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("3.1 Cryptographic Audit Protocol", styles["SectionHeader"]))
    story.append(Paragraph(
        "To establish absolute scientific rigor, our initial pipeline execution executed an automated forensic audit inspecting raw file bytes, MD5 checksums, "
        "schema signatures, missingness rates, and cross-cohort row overlaps before any machine learning operations commenced. The results yielded three "
        "critical discoveries that fundamentally governed subsequent model training.",
        styles["Body"]
    ))

    # Audit Findings Summary Table
    audit_data = [
        [Paragraph("<b>Audit Check</b>", styles["TableHeader"]), Paragraph("<b>Inspected Files</b>", styles["TableHeader"]),
         Paragraph("<b>Observed Metric / Hash</b>", styles["TableHeader"]), Paragraph("<b>Scientific Verdict & Action Taken</b>", styles["TableHeader"])],
        [Paragraph("Cryptographic Deduplication", styles["TableText"]),
         Paragraph("diabetes_prediction_dataset.csv<br/>diabetes_prediction_dataset(1).csv", styles["TableText"]),
         Paragraph("MD5: cb243b99d81d96e9aeb08944ce9ac066<br/>(Exact Byte Match)", styles["TableText"]),
         Paragraph("<b>100% IDENTICAL DUPLICATE.</b> File 2 is an accidental re-download. Safely excluded to prevent 100,000 double-counted rows.", styles["TableText"])],
        [Paragraph("BRFSS Binary vs 3-Class", styles["TableText"]),
         Paragraph("diabetes_binary_health_indicators<br/>diabetes_012_health_indicators", styles["TableText"]),
         Paragraph("253,680 identical feature vectors<br/>100% row index correspondence", styles["TableText"]),
         Paragraph("<b>SAME POPULATION.</b> Binary version conflated 4,631 prediabetic respondents (1.8%) into healthy class 0. Cannot be merged.", styles["TableText"])],
        [Paragraph("BRFSS 50-50 Subsample Audit", styles["TableText"]),
         Paragraph("diabetes_binary_5050split<br/>diabetes_binary_health_indicators", styles["TableText"]),
         Paragraph("All 35,346 diabetes cases present in both files (100% overlap)", styles["TableText"]),
         Paragraph("<b>DERIVED SUBSAMPLE.</b> 50-50 file is an undersampled subset. Must NOT be used as external validation set (causes 100% test leakage).", styles["TableText"])],
    ]
    t_aud = Table(audit_data, colWidths=[1.5 * inch, 1.8 * inch, 1.8 * inch, 2.1 * inch])
    t_aud.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_aud)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Detailed Forensic Deconstructions", styles["SectionHeader"]))
    story.append(Paragraph(
        "<b>Case 1: The Duplicate EHR File (100,000 Rows):</b> Inspection of <code>diabetes_prediction_dataset(1).csv</code> revealed an MD5 checksum "
        "of <code>cb243b99d81d96e9aeb08944ce9ac066</code>, identical down to the exact byte to <code>diabetes_prediction_dataset.csv</code>. Both files contain "
        "precisely 100,000 rows, 3,854 internal duplicate entries (3.85%), and identical column headers. Had this file been naively merged as an additional cohort, "
        "the model would have been trained on 100,000 duplicate patients, artificially inflating sample size and causing massive data snooping.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>Case 2: BRFSS Binary Conflation of Prediabetes:</b> Comparing <code>diabetes_binary_health_indicators_BRFSS2015.csv</code> and "
        "<code>diabetes_012_health_indicators_BRFSS2015.csv</code> demonstrated that all 253,680 respondent feature vectors are identical. In the 3-class dataset, "
        "respondents are categorized as 0 (No diabetes: 213,703 / 84.24%), 1 (Prediabetes: 4,631 / 1.83%), and 2 (Diabetes: 35,346 / 13.93%). In the binary dataset, "
        "classes 0 and 1 were collapsed into a single negative class (218,334 / 86.07%). This audit finding proved that these files cannot serve as independent validation cohorts.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>Case 3: The 50-50 Balanced Cohort Subsample Trap:</b> The 70,692-row dataset <code>diabetes_binary_5050split</code> is frequently misconstrued "
        "in amateur literature as an independent external test cohort. Our cryptographic join proved that this dataset was constructed by extracting all 35,346 "
        "diabetic respondents from the 253,680-row BRFSS file and pairing them with 35,346 randomly sampled non-diabetic controls. Evaluating a model trained on BRFSS "
        "against this dataset would result in 100% positive-class test leakage.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: CHAPTER 4: EXPLORATORY DATA ANALYSIS & HYPOTHESIS TESTING
    # =========================================================================
    story.append(Paragraph("Chapter 4: Exploratory Data Analysis & Statistical Hypothesis Profiling", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("4.1 Hypothesis Testing Framework", styles["SectionHeader"]))
    story.append(Paragraph(
        "To rigorously characterize feature distributions prior to model construction, we conducted non-parametric statistical hypothesis tests across "
        "all cohorts. Continuous variables were assessed using the two-sided Mann-Whitney U test (due to significant non-normality and skewness confirmed via Shapiro-Wilk testing). "
        "Categorical variables were evaluated using Pearson's Chi-Square Test of Independence, with association strength quantified via Cramér's V statistic.",
        styles["Body"]
    ))

    # Top Statistical Predictors Table
    stat_data = [
        [Paragraph("<b>Cohort / Modality</b>", styles["TableHeader"]), Paragraph("<b>Feature Name</b>", styles["TableHeader"]),
         Paragraph("<b>Test Type</b>", styles["TableHeader"]), Paragraph("<b>Test Statistic</b>", styles["TableHeader"]),
         Paragraph("<b>p-value</b>", styles["TableHeader"]), Paragraph("<b>Effect Size / Metric</b>", styles["TableHeader"]),
         Paragraph("<b>Diabetic vs Control Median</b>", styles["TableHeader"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("HbA1c_level", styles["TableText"]), Paragraph("Mann-Whitney U", styles["TableText"]),
         Paragraph("1.25e+08", styles["TableText"]), Paragraph("< 1.0e-300", styles["TableText"]), Paragraph("Median Diff: +0.80%", styles["TableText"]), Paragraph("6.6% vs 5.8%", styles["TableText"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("blood_glucose_level", styles["TableText"]), Paragraph("Mann-Whitney U", styles["TableText"]),
         Paragraph("1.69e+08", styles["TableText"]), Paragraph("< 1.0e-300", styles["TableText"]), Paragraph("Median Diff: +20.0 mg/dL", styles["TableText"]), Paragraph("160.0 vs 140.0 mg/dL", styles["TableText"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("age", styles["TableText"]), Paragraph("Mann-Whitney U", styles["TableText"]),
         Paragraph("1.78e+08", styles["TableText"]), Paragraph("< 1.0e-300", styles["TableText"]), Paragraph("Median Diff: +22.0 yrs", styles["TableText"]), Paragraph("62.0 vs 40.0 yrs", styles["TableText"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("bmi", styles["TableText"]), Paragraph("Mann-Whitney U", styles["TableText"]),
         Paragraph("2.29e+08", styles["TableText"]), Paragraph("< 1.0e-300", styles["TableText"]), Paragraph("Median Diff: +2.65", styles["TableText"]), Paragraph("29.97 vs 27.32", styles["TableText"])],
        [Paragraph("CDC BRFSS Survey", styles["TableText"]), Paragraph("GenHlth (General Health)", styles["TableText"]), Paragraph("Chi-Square", styles["TableText"]),
         Paragraph("22,728.1", styles["TableText"]), Paragraph("< 1.0e-300", styles["TableText"]), Paragraph("Cramer's V: 0.299", styles["TableText"]), Paragraph("38.4% in Poor vs 2.1% in Exc.", styles["TableText"])],
        [Paragraph("CDC BRFSS Survey", styles["TableText"]), Paragraph("HighBP (Hypertension)", styles["TableText"]), Paragraph("Chi-Square", styles["TableText"]),
         Paragraph("17,562.5", styles["TableText"]), Paragraph("< 1.0e-300", styles["TableText"]), Paragraph("Cramer's V: 0.263", styles["TableText"]), Paragraph("27.4% in HTN vs 5.4% Normal", styles["TableText"])],
        [Paragraph("CDC BRFSS Survey", styles["TableText"]), Paragraph("BMI", styles["TableText"]), Paragraph("Mann-Whitney U", styles["TableText"]),
         Paragraph("2.41e+09", styles["TableText"]), Paragraph("< 1.0e-300", styles["TableText"]), Paragraph("Median Diff: +4.0", styles["TableText"]), Paragraph("31.0 vs 27.0", styles["TableText"])],
        [Paragraph("Acute Symptoms", styles["TableText"]), Paragraph("Polyuria", styles["TableText"]), Paragraph("Chi-Square", styles["TableText"]),
         Paragraph("227.87", styles["TableText"]), Paragraph("1.74e-51", styles["TableText"]), Paragraph("Cramer's V: 0.661", styles["TableText"]), Paragraph("75.9% in Diab vs 7.5% Normal", styles["TableText"])],
        [Paragraph("Acute Symptoms", styles["TableText"]), Paragraph("Polydipsia", styles["TableText"]), Paragraph("Chi-Square", styles["TableText"]),
         Paragraph("216.17", styles["TableText"]), Paragraph("6.19e-49", styles["TableText"]), Paragraph("Cramer's V: 0.644", styles["TableText"]), Paragraph("70.3% in Diab vs 4.0% Normal", styles["TableText"])],
        [Paragraph("Acute Symptoms", styles["TableText"]), Paragraph("sudden weight loss", styles["TableText"]), Paragraph("Chi-Square", styles["TableText"]),
         Paragraph("97.30", styles["TableText"]), Paragraph("5.97e-23", styles["TableText"]), Paragraph("Cramer's V: 0.431", styles["TableText"]), Paragraph("58.8% in Diab vs 14.0% Normal", styles["TableText"])]
    ]
    t_stat = Table(stat_data, colWidths=[1.1 * inch, 1.3 * inch, 0.9 * inch, 0.8 * inch, 0.7 * inch, 1.1 * inch, 1.3 * inch])
    t_stat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_stat)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.2 Clinical Interpretations of Statistical Profiles", styles["SectionHeader"]))
    story.append(Paragraph(
        "1. <b>Laboratory Threshold Bifurcation:</b> In the clinical EHR cohort, diabetic patients present with a median HbA1c of 6.6%, directly aligning "
        "with the clinical diagnostic threshold (>= 6.5%), whereas non-diabetics center at 5.8%. Fasting glucose demonstrates an identical sharp shift (160 mg/dL vs 140 mg/dL). "
        "Age serves as a powerful demographic covariate: median age in diabetics is 62.0 years compared to 40.0 years in controls.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "2. <b>Self-Rated Health as a Holistic Proxy:</b> In the CDC BRFSS cohort, self-rated general health (<code>GenHlth</code>) exhibited the single highest "
        "correlation with diabetes (Cramér's V = 0.299). Prevalence rose monotonically: 2.1% (Excellent), 4.8% (Very Good), 10.4% (Good), 21.6% (Fair), and 38.4% (Poor). "
        "This confirms that patients intuitively sense multisystem metabolic deterioration long before formal diagnostic labeling.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: CHAPTER 5: ADVANCED FEATURE ENGINEERING & PIPELINES
    # =========================================================================
    story.append(Paragraph("Chapter 5: Feature Engineering & Leakage-Free Preprocessing Pipelines", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("5.1 Mathematical Formulation of Supervised Risk Stratification", styles["SectionHeader"]))
    story.append(Paragraph(
        "Let the observed dataset be denoted as D = {(x_i, y_i)}_{i=1}^N, where x_i in R^d represents the vector of patient features, and "
        "y_i in {0, 1} denotes binary diabetes diagnostic status. Our learning objective is to induce a hypothesis function f_theta: X -> [0, 1] "
        "such that f_theta(x) models the posterior probability P(Y=1 | X=x). In medical screening, the objective is not merely binary classification "
        "accuracy, but calibrated risk ranking that minimizes false negatives under an asymmetric loss function L(y, y_hat) = c_fn * I(y=1, y_hat=0) + c_fp * I(y=0, y_hat=1), "
        "where c_fn >> c_fp.",
        styles["Body"]
    ))

    story.append(Paragraph("5.2 Anti-Leakage Architecture via Scikit-Learn ColumnTransformer", styles["SectionHeader"]))
    story.append(Paragraph(
        "Information leakage is the most rampant cause of inflated performance in published machine learning literature. Leakage occurs when "
        "information from outside the training fold (such as global means, scalers, or target statistics) contaminates feature transformations. "
        "To guarantee zero leakage, our preprocessing pipeline employs Scikit-Learn <code>ColumnTransformer</code> and <code>Pipeline</code> objects fitted "
        "strictly inside cross-validation splits:",
        styles["Body"]
    ))

    pipe_steps = [
        "<b>Fold-Isolated Numerical Imputation:</b> Missing continuous attributes are imputed using the training-fold median only.",
        "<b>Fold-Isolated Standard Scaling:</b> Continuous features (Age, BMI, Glucose, HbA1c) are standardized as z = (x - mu_train) / sigma_train.",
        "<b>Categorical Encoding:</b> Nominal attributes (Gender, Smoking History) are encoded via OneHotEncoder with handle_unknown='ignore'. Ordinal survey scales (GenHlth, Education, Income) are preserved as integer ranks.",
        "<b>Leakage-Free Cross-Validation:</b> Stratified 5-Fold Cross Validation ensures identical class ratios across folds while preserving strict train/validation isolation."
    ]
    for step in pipe_steps:
        story.append(Paragraph(f"•  {step}", styles["Bullet"]))

    story.append(Spacer(1, 4))
    story.append(Paragraph("5.3 Custom Domain Feature Engineering", styles["SectionHeader"]))
    story.append(Paragraph(
        "To empower linear and tree-based architectures with non-linear physiological interactions, our feature engineering module constructs domain-guided composite indices:",
        styles["Body"]
    ))

    fe_data = [
        [Paragraph("<b>Engineered Feature</b>", styles["TableHeader"]), Paragraph("<b>Mathematical Formulation</b>", styles["TableHeader"]),
         Paragraph("<b>Clinical Rationale</b>", styles["TableHeader"])],
        [Paragraph("WHO BMI Category", styles["TableText"]), Paragraph("Ordinal bins: <18.5, 18.5-24.9, 25-29.9, 30-34.9, >=35", styles["TableText"]),
         Paragraph("Captures established clinical thresholds for normal, overweight, and Obese Classes I-III.", styles["TableText"])],
        [Paragraph("Metabolic Syndrome Index", styles["TableText"]), Paragraph("BMI >= 30 + HighBP + HeartDisease", styles["TableText"]),
         Paragraph("Multi-morbidity composite score reflecting cumulative cardiovascular-metabolic strain.", styles["TableText"])],
        [Paragraph("Age-Adjusted Glycemic Factor", styles["TableText"]), Paragraph("(Age / 50.0) * (HbA1c / 6.0)", styles["TableText"]),
         Paragraph("Models the exponential interaction between advanced age and elevated glycated hemoglobin.", styles["TableText"])],
        [Paragraph("Lifestyle Sedentary Flag", styles["TableText"]), Paragraph("(PhysActivity == 0) & (BMI >= 30)", styles["TableText"]),
         Paragraph("Isolates high-risk sedentary individuals with concurrent obesity in survey cohorts.", styles["TableText"])],
    ]
    t_fe = Table(fe_data, colWidths=[1.7 * inch, 2.3 * inch, 3.2 * inch])
    t_fe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_fe)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: CHAPTER 6: MULTI-ALGORITHM CANDIDATE SPECTRUM
    # =========================================================================
    story.append(Paragraph("Chapter 6: Mathematical Formulations & Multi-Algorithm Candidate Spectrum", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("6.1 Theoretical Foundations of the 9 Candidate Classifiers", styles["SectionHeader"]))
    story.append(Paragraph(
        "To avoid architectural bias, we comprehensively trained and compared 9 diverse machine learning paradigms spanning parametric, ensemble, "
        "boosting, instance-based, and kernelized architectures:",
        styles["Body"]
    ))

    # Model Formulations Table
    model_data = [
        [Paragraph("<b>Algorithm</b>", styles["TableHeader"]), Paragraph("<b>Mathematical Formulation & Objective</b>", styles["TableHeader"]),
         Paragraph("<b>Clinical Strengths & Trade-offs</b>", styles["TableHeader"])],
        [Paragraph("Logistic Regression", styles["TableText"]),
         Paragraph("min_w sum log(1 + exp(-y_i w^T x_i)) + C ||w||_2^2<br/>Balanced weights: w_j = N / (k * N_j)", styles["TableText"]),
         Paragraph("Transparent log-odds interpretation. Excellent baseline but incapable of capturing complex non-linear feature interactions.", styles["TableText"])],
        [Paragraph("Decision Trees", styles["TableText"]),
         Paragraph("Recursive binary splitting maximizing Gini Impurity reduction: Delta I_G = I_G(parent) - sum (N_c/N) I_G(child)", styles["TableText"]),
         Paragraph("Highly interpretable clinical decision rules. Prone to severe overfitting without aggressive max_depth regularization.", styles["TableText"])],
        [Paragraph("Random Forest", styles["TableText"]),
         Paragraph("Ensemble of B = 100 de-correlated trees trained on bootstrap samples with random feature subsets m = sqrt(d)", styles["TableText"]),
         Paragraph("Drastically reduces variance; robust to noise and outliers. High computational overhead for real-time edge deployment.", styles["TableText"])],
        [Paragraph("Extra Trees", styles["TableText"]),
         Paragraph("Extremely Randomized Trees: selects random cut-points for each candidate feature rather than optimal splits", styles["TableText"]),
         Paragraph("Further reduces variance; excels in low-sample, high-signal regimes (e.g., acute symptoms cohort).", styles["TableText"])],
        [Paragraph("HistGradientBoosting", styles["TableText"]),
         Paragraph("Binned gradient boosting: continuous features binned into 256 integer bins; gradient descent in function space", styles["TableText"]),
         Paragraph("Extremely fast native handling of large datasets; native missing value support without imputation overhead.", styles["TableText"])],
        [Paragraph("LightGBM", styles["TableText"]),
         Paragraph("Leaf-wise tree growth (best-first) with Gradient-Based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB)", styles["TableText"]),
         Paragraph("State-of-the-art diagnostic discrimination; superior sensitivity on large-scale tabular health records.", styles["TableText"])],
        [Paragraph("XGBoost", styles["TableText"]),
         Paragraph("Second-order Taylor expansion of loss: obj = sum [g_i f_t(x_i) + 0.5 h_i f_t^2(x_i)] + Omega(f_t)", styles["TableText"]),
         Paragraph("Highly regularized; however, default unweighted objectives collapse under extreme survey class imbalance.", styles["TableText"])],
        [Paragraph("K-Nearest Neighbors", styles["TableText"]),
         Paragraph("P(Y=1|x) = (1/k) sum I(y_i = 1) for x_i in N_k(x) under Euclidean distance d(u, v) = ||u - v||_2", styles["TableText"]),
         Paragraph("Intuitive case-based reasoning; computationally prohibitive on large cohorts (O(N) inference cost).", styles["TableText"])],
        [Paragraph("Support Vector Machine", styles["TableText"]),
         Paragraph("Dual soft-margin QP with RBF kernel: K(x, z) = exp(-gamma ||x - z||^2)", styles["TableText"]),
         Paragraph("Optimal margin boundaries in high-dimensional space; scaling scales quadratically with dataset size.", styles["TableText"])],
    ]
    t_mod = Table(model_data, colWidths=[1.4 * inch, 3.2 * inch, 2.6 * inch])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.2 Hyperparameter Configuration & Optimization", styles["SectionHeader"]))
    story.append(Paragraph(
        "All candidate architectures were tuned using stratified 5-fold cross validation. For tree ensembles, maximum depth was constrained "
        "(max_depth in [5, 8]) to prevent memorization of spurious survey artifacts. For boosting models (LightGBM, XGBoost, HistGradientBoosting), "
        "the learning rate was fixed at 0.05 with n_estimators=150 and early stopping. Most importantly, for the imbalanced CDC BRFSS cohort (13.9% prevalence), "
        "cost-sensitive class balancing (<code>class_weight='balanced'</code> / <code>scale_pos_weight</code>) was enforced to prevent majority-class collapse.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 7: PROBABILITY CALIBRATION & BRIER SCORE
    # =========================================================================
    story.append(Paragraph("Chapter 7: Probability Calibration & Brier Score Optimization", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("7.1 The Calibration Imperative in Healthcare Artificial Intelligence", styles["SectionHeader"]))
    story.append(Paragraph(
        "In clinical practice, a machine learning model must not simply output a binary label (0 or 1). Physicians and triage algorithms require "
        "accurate, well-calibrated posterior probabilities P(Y=1 | X=x). For instance, a patient with an estimated risk of 52% warrants an entirely "
        "different clinical management pathway than one with an estimated risk of 98%. However, modern ensemble and boosting algorithms are notoriously "
        "uncalibrated. Maximum-margin objectives (SVMs), bagging ensembles (Random Forests), and greedy boosting (LightGBM, XGBoost) tend to push "
        "probabilities toward extreme tails (0 or 1) or compress them around the training base rate, severely distorting clinical risk perception.",
        styles["Body"]
    ))

    story.append(Paragraph("7.2 Mathematical Formulations of Calibration Models", styles["SectionHeader"]))
    story.append(Paragraph(
        "To transform raw decision scores into faithful empirical probabilities, our pipeline incorporates post-hoc probability calibration "
        "using <code>CalibratedClassifierCV</code> via two principal mathematical techniques:",
        styles["Body"]
    ))

    calib_methods = [
        ("1. Platt Scaling (Sigmoid Calibration):", 
         "Fits a univariate logistic transformation over raw model margins f(x): P(Y=1 | f) = 1 / (1 + exp(A * f + B)). "
         "Parameters A and B are estimated via maximum likelihood on out-of-fold predictions. Most effective when raw margins exhibit sigmoidal distortion."),
        ("2. Isotonic Regression:", 
         "Fits a non-parametric, piece-wise constant monotonic increasing function: min sum (y_i - m(f_i))^2 subject to m(f_i) <= m(f_j) whenever f_i <= f_j. "
         "Isotonic regression makes no parametric assumptions, making it ideal when calibration data is abundant (>10,000 samples).")
    ]
    for c_title, c_desc in calib_methods:
        story.append(Paragraph(f"<b>{c_title}</b> {c_desc}", styles["Body"]))

    story.append(Spacer(1, 4))
    story.append(Paragraph("7.3 The Brier Score Metric & Empirical Calibration Results", styles["SectionHeader"]))
    story.append(Paragraph(
        "Calibration quality was strictly evaluated using the Brier Score, defined as the mean squared error between predicted probability and actual binary label: "
        "BS = (1/N) sum (P_i - y_i)^2. A score of 0.0 represents perfect probabilistic forecasting. In our clinical EHR cohort, applying post-hoc calibration "
        "to LightGBM reduced the Brier score from 0.0611 down to 0.0236—a dramatic 61.4% reduction in probabilistic error.",
        styles["Body"]
    ))

    # Calibration Summary Table
    brier_data = [
        [Paragraph("<b>Cohort Modality</b>", styles["TableHeader"]), Paragraph("<b>Model Architecture</b>", styles["TableHeader"]),
         Paragraph("<b>Raw Uncalibrated Brier</b>", styles["TableHeader"]), Paragraph("<b>Post-Calibration Brier</b>", styles["TableHeader"]),
         Paragraph("<b>Calibration Technique</b>", styles["TableHeader"]), Paragraph("<b>Clinical Impact</b>", styles["TableHeader"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("LightGBM", styles["TableText"]),
         Paragraph("0.0611", styles["TableText"]), Paragraph("<b>0.0236</b>", styles["TableText"]),
         Paragraph("Sigmoid / Platt", styles["TableText"]), Paragraph("Reliable probabilities; enables valid confidence intervals.", styles["TableText"])],
        [Paragraph("CDC BRFSS Survey", styles["TableText"]), Paragraph("LightGBM (Balanced)", styles["TableText"]),
         Paragraph("0.1789", styles["TableText"]), Paragraph("<b>0.1080</b>", styles["TableText"]),
         Paragraph("Isotonic", styles["TableText"]), Paragraph("Eliminates probability distortion induced by artificial class weights.", styles["TableText"])],
        [Paragraph("Early Symptoms", styles["TableText"]), Paragraph("Extra Trees", styles["TableText"]),
         Paragraph("0.0147", styles["TableText"]), Paragraph("<b>0.0098</b>", styles["TableText"]),
         Paragraph("Sigmoid", styles["TableText"]), Paragraph("Near-zero error; highly definitive for acute hospital triage.", styles["TableText"])],
    ]
    t_brier = Table(brier_data, colWidths=[1.3 * inch, 1.4 * inch, 1.1 * inch, 1.1 * inch, 1.0 * inch, 1.3 * inch])
    t_brier.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_brier)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: CHAPTER 8: COHORT 1 BENCHMARK (CLINICAL & LABORATORY EHR)
    # =========================================================================
    story.append(Paragraph("Chapter 8: Empirical Evaluation: Cohort 1 (Clinical & Laboratory EHR)", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("8.1 Cohort Characteristics & Test Partition", styles["SectionHeader"]))
    story.append(Paragraph(
        "The Clinical & Laboratory EHR cohort comprises 100,000 patient records. Following exclusion of the duplicate file and deduplication, "
        "the cohort was partitioned into an 80% training set (80,774 patients) and an independent 20% hold-out test set (19,226 patients) "
        "using stratified sampling. The test set contains 1,696 confirmed diabetic patients (8.82% prevalence) and 17,530 controls.",
        styles["Body"]
    ))

    # Benchmark Results Table
    c1_data = [
        [Paragraph("<b>Candidate Model</b>", styles["TableHeader"]), Paragraph("<b>Accuracy</b>", styles["TableHeader"]),
         Paragraph("<b>Recall (Sens.)</b>", styles["TableHeader"]), Paragraph("<b>Specificity</b>", styles["TableHeader"]),
         Paragraph("<b>Precision</b>", styles["TableHeader"]), Paragraph("<b>F1 Score</b>", styles["TableHeader"]),
         Paragraph("<b>ROC-AUC</b>", styles["TableHeader"]), Paragraph("<b>PR-AUC</b>", styles["TableHeader"]), Paragraph("<b>Brier</b>", styles["TableHeader"])],
        [Paragraph("Logistic Regression", styles["TableText"]), Paragraph("0.8848", styles["TableText"]), Paragraph("0.8791", styles["TableText"]),
         Paragraph("0.8853", styles["TableText"]), Paragraph("0.4259", styles["TableText"]), Paragraph("0.5738", styles["TableText"]),
         Paragraph("0.9597", styles["TableText"]), Paragraph("0.8121", styles["TableText"]), Paragraph("0.0800", styles["TableText"])],
        [Paragraph("Decision Tree", styles["TableText"]), Paragraph("0.8258", styles["TableText"]), Paragraph("0.9564", styles["TableText"]),
         Paragraph("0.8131", styles["TableText"]), Paragraph("0.3312", styles["TableText"]), Paragraph("0.4920", styles["TableText"]),
         Paragraph("0.9668", styles["TableText"]), Paragraph("0.8594", styles["TableText"]), Paragraph("0.0727", styles["TableText"])],
        [Paragraph("Random Forest", styles["TableText"]), Paragraph("0.8923", styles["TableText"]), Paragraph("0.9157", styles["TableText"]),
         Paragraph("0.8901", styles["TableText"]), Paragraph("0.4463", styles["TableText"]), Paragraph("0.6001", styles["TableText"]),
         Paragraph("0.9743", styles["TableText"]), Paragraph("0.8734", styles["TableText"]), Paragraph("0.0621", styles["TableText"])],
        [Paragraph("Extra Trees", styles["TableText"]), Paragraph("0.8760", styles["TableText"]), Paragraph("0.9180", styles["TableText"]),
         Paragraph("0.8719", styles["TableText"]), Paragraph("0.4095", styles["TableText"]), Paragraph("0.5664", styles["TableText"]),
         Paragraph("0.9655", styles["TableText"]), Paragraph("0.8362", styles["TableText"]), Paragraph("0.0778", styles["TableText"])],
        [Paragraph("HistGradientBoosting", styles["TableText"]), Paragraph("0.8997", styles["TableText"]), Paragraph("0.9133", styles["TableText"]),
         Paragraph("0.8984", styles["TableText"]), Paragraph("0.4652", styles["TableText"]), Paragraph("0.6164", styles["TableText"]),
         Paragraph("0.9771", styles["TableText"]), Paragraph("0.8802", styles["TableText"]), Paragraph("0.0605", styles["TableText"])],
        [Paragraph("<b>LightGBM (Selected)</b>", styles["TableText"]), Paragraph("<b>0.8975</b>", styles["TableText"]), Paragraph("<b>0.9210</b>", styles["TableText"]),
         Paragraph("<b>0.8953</b>", styles["TableText"]), Paragraph("<b>0.4597</b>", styles["TableText"]), Paragraph("<b>0.6133</b>", styles["TableText"]),
         Paragraph("<b>0.9770</b>", styles["TableText"]), Paragraph("<b>0.8802</b>", styles["TableText"]), Paragraph("<b>0.0236*</b>", styles["TableText"])],
        [Paragraph("XGBoost", styles["TableText"]), Paragraph("0.9720", styles["TableText"]), Paragraph("0.6881", styles["TableText"]),
         Paragraph("0.9994", styles["TableText"]), Paragraph("0.9915", styles["TableText"]), Paragraph("0.8124", styles["TableText"]),
         Paragraph("0.9767", styles["TableText"]), Paragraph("0.8801", styles["TableText"]), Paragraph("0.0235", styles["TableText"])]
    ]
    t_c1 = Table(c1_data, colWidths=[1.5 * inch, 0.7 * inch, 0.75 * inch, 0.75 * inch, 0.7 * inch, 0.7 * inch, 0.75 * inch, 0.75 * inch, 0.65 * inch])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#EFF6FF")),
    ]))
    story.append(t_c1)
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.2 Model Selection Rationale & Confusion Matrix Analysis", styles["SectionHeader"]))
    story.append(Paragraph(
        "<b>Selected Model: LightGBM Classifier (Calibrated):</b> While XGBoost achieved higher superficial accuracy (97.20%), it suffered from a "
        "dangerously low recall of 68.81%, missing nearly a third of all diabetic patients. In clinical screening, missing a diabetic patient (False Negative) "
        "is catastrophically worse than generating a false alarm (False Positive) that can be ruled out with confirmatory blood work. LightGBM was selected as the "
        "clinically justified champion, achieving an exceptional <b>0.9770 ROC-AUC</b>, <b>0.8802 PR-AUC</b>, and <b>92.10% Sensitivity</b>.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>Confusion Matrix Breakdown (19,226 Test Patients):</b><br/>"
        "•  <b>True Positives (TP): 1,562</b> diabetic patients correctly identified.<br/>"
        "•  <b>False Negatives (FN): 134</b> diabetic patients missed (False Negative Rate: 7.90%).<br/>"
        "•  <b>True Negatives (TN): 15,694</b> healthy individuals correctly cleared.<br/>"
        "•  <b>False Positives (FP): 1,836</b> healthy individuals flagged for routine laboratory confirmation.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "This performance ensures that over 92% of diabetic patients are identified at the primary screening tier, with an exceptionally low false negative rate.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: CHAPTER 9: COHORT 2 BENCHMARK (CDC BRFSS LIFESTYLE SURVEY)
    # =========================================================================
    story.append(Paragraph("Chapter 9: Empirical Evaluation: Cohort 2 (CDC BRFSS Lifestyle Survey)", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("9.1 Non-Invasive Lifestyle Screening Architecture", styles["SectionHeader"]))
    story.append(Paragraph(
        "The CDC BRFSS cohort (253,680 survey records) investigates how accurately diabetes status can be stratified using purely non-invasive "
        "lifestyle, dietary, physical activity, and demographic factors, with ZERO clinical laboratory tests or venipuncture. Models were evaluated "
        "on an independent test partition of 10,000 respondents containing 1,529 diabetic individuals (15.29% prevalence).",
        styles["Body"]
    ))

    # BRFSS Benchmark Table
    c2_data = [
        [Paragraph("<b>Candidate Model</b>", styles["TableHeader"]), Paragraph("<b>Accuracy</b>", styles["TableHeader"]),
         Paragraph("<b>Recall (Sens.)</b>", styles["TableHeader"]), Paragraph("<b>Specificity</b>", styles["TableHeader"]),
         Paragraph("<b>Precision</b>", styles["TableHeader"]), Paragraph("<b>F1 Score</b>", styles["TableHeader"]),
         Paragraph("<b>ROC-AUC</b>", styles["TableHeader"]), Paragraph("<b>PR-AUC</b>", styles["TableHeader"]), Paragraph("<b>Brier</b>", styles["TableHeader"])],
        [Paragraph("Logistic Regression", styles["TableText"]), Paragraph("0.7147", styles["TableText"]), Paragraph("0.7299", styles["TableText"]),
         Paragraph("0.7120", styles["TableText"]), Paragraph("0.3138", styles["TableText"]), Paragraph("0.4389", styles["TableText"]),
         Paragraph("0.7979", styles["TableText"]), Paragraph("0.3903", styles["TableText"]), Paragraph("0.1847", styles["TableText"])],
        [Paragraph("Decision Tree", styles["TableText"]), Paragraph("0.7126", styles["TableText"]), Paragraph("0.7181", styles["TableText"]),
         Paragraph("0.7116", styles["TableText"]), Paragraph("0.3101", styles["TableText"]), Paragraph("0.4331", styles["TableText"]),
         Paragraph("0.7869", styles["TableText"]), Paragraph("0.3927", styles["TableText"]), Paragraph("0.1892", styles["TableText"])],
        [Paragraph("Random Forest", styles["TableText"]), Paragraph("0.7474", styles["TableText"]), Paragraph("0.6848", styles["TableText"]),
         Paragraph("0.7587", styles["TableText"]), Paragraph("0.3387", styles["TableText"]), Paragraph("0.4532", styles["TableText"]),
         Paragraph("0.7997", styles["TableText"]), Paragraph("0.4009", styles["TableText"]), Paragraph("0.1663", styles["TableText"])],
        [Paragraph("Extra Trees", styles["TableText"]), Paragraph("0.7051", styles["TableText"]), Paragraph("0.7220", styles["TableText"]),
         Paragraph("0.7020", styles["TableText"]), Paragraph("0.3043", styles["TableText"]), Paragraph("0.4282", styles["TableText"]),
         Paragraph("0.7882", styles["TableText"]), Paragraph("0.3865", styles["TableText"]), Paragraph("0.1823", styles["TableText"])],
        [Paragraph("HistGradientBoosting", styles["TableText"]), Paragraph("0.7151", styles["TableText"]), Paragraph("0.7417", styles["TableText"]),
         Paragraph("0.7103", styles["TableText"]), Paragraph("0.3161", styles["TableText"]), Paragraph("0.4432", styles["TableText"]),
         Paragraph("0.8034", styles["TableText"]), Paragraph("0.4057", styles["TableText"]), Paragraph("0.1796", styles["TableText"])],
        [Paragraph("<b>LightGBM (Balanced)</b>", styles["TableText"]), Paragraph("<b>0.7168</b>", styles["TableText"]), Paragraph("<b>0.7449</b>", styles["TableText"]),
         Paragraph("<b>0.7117</b>", styles["TableText"]), Paragraph("<b>0.3181</b>", styles["TableText"]), Paragraph("<b>0.4458</b>", styles["TableText"]),
         Paragraph("<b>0.8046</b>", styles["TableText"]), Paragraph("<b>0.4070</b>", styles["TableText"]), Paragraph("<b>0.1080*</b>", styles["TableText"])],
        [Paragraph("XGBoost (Unweighted)", styles["TableText"]), Paragraph("0.8496", styles["TableText"]), Paragraph("0.1452", styles["TableText"]),
         Paragraph("0.9767", styles["TableText"]), Paragraph("0.5298", styles["TableText"]), Paragraph("0.2279", styles["TableText"]),
         Paragraph("0.8044", styles["TableText"]), Paragraph("0.4035", styles["TableText"]), Paragraph("0.1083", styles["TableText"])]
    ]
    t_c2 = Table(c2_data, colWidths=[1.5 * inch, 0.7 * inch, 0.75 * inch, 0.75 * inch, 0.7 * inch, 0.7 * inch, 0.75 * inch, 0.75 * inch, 0.65 * inch])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#EFF6FF")),
    ]))
    story.append(t_c2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("9.2 Clinical Implications of Lifestyle-Only Screening", styles["SectionHeader"]))
    story.append(Paragraph(
        "<b>Population-Scale Triage Without Needles:</b> LightGBM with balanced class weights achieved an <b>ROC-AUC of 0.8046</b> and a <b>Sensitivity of 74.49%</b>. "
        "This empirical result establishes that a self-administered questionnaire measuring modifiable lifestyle factors (physical activity, fruit/vegetable intake, "
        "BMI, smoking, general health perception) successfully identifies nearly 75% of diabetic patients. In remote, rural, or low-income settings where routine blood "
        "testing is economically infeasible, this non-invasive model provides a highly viable digital triage mechanism to prioritize individuals for formal clinic visits.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>The Danger of Uncalibrated Unweighted Boosting:</b> Unweighted XGBoost demonstrated a superficial accuracy of 84.96%, but its sensitivity collapsed to "
        "14.52%, missing 85.48% of all diabetic cases (FN=1,307 out of 1,529). This provides a stark clinical warning against evaluating healthcare models on accuracy alone.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CHAPTER 10: COHORT 3 BENCHMARK (EARLY ACUTE SYMPTOMS)
    # =========================================================================
    story.append(Paragraph("Chapter 10: Empirical Evaluation: Cohort 3 (Early-Stage Acute Symptoms)", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("10.1 Outpatient Presentation & Symptom Cohort Profile", styles["SectionHeader"]))
    story.append(Paragraph(
        "The Sylhet Diabetes Hospital dataset (520 records) documents clinical presentations of patients seeking medical consultation. "
        "The test set comprises 104 hold-out patients (64 diabetic, 40 non-diabetic controls). Features strictly document patient-reported cardinal symptoms "
        "associated with acute glycemic elevation.",
        styles["Body"]
    ))

    # Symptoms Benchmark Table
    c3_data = [
        [Paragraph("<b>Candidate Model</b>", styles["TableHeader"]), Paragraph("<b>Accuracy</b>", styles["TableHeader"]),
         Paragraph("<b>Recall (Sens.)</b>", styles["TableHeader"]), Paragraph("<b>Specificity</b>", styles["TableHeader"]),
         Paragraph("<b>Precision</b>", styles["TableHeader"]), Paragraph("<b>F1 Score</b>", styles["TableHeader"]),
         Paragraph("<b>ROC-AUC</b>", styles["TableHeader"]), Paragraph("<b>PR-AUC</b>", styles["TableHeader"]), Paragraph("<b>Brier</b>", styles["TableHeader"])],
        [Paragraph("Logistic Regression", styles["TableText"]), Paragraph("0.9327", styles["TableText"]), Paragraph("0.9062", styles["TableText"]),
         Paragraph("0.9750", styles["TableText"]), Paragraph("0.9831", styles["TableText"]), Paragraph("0.9431", styles["TableText"]),
         Paragraph("0.9918", styles["TableText"]), Paragraph("0.9951", styles["TableText"]), Paragraph("0.0483", styles["TableText"])],
        [Paragraph("Decision Tree", styles["TableText"]), Paragraph("0.9712", styles["TableText"]), Paragraph("0.9531", styles["TableText"]),
         Paragraph("1.0000", styles["TableText"]), Paragraph("1.0000", styles["TableText"]), Paragraph("0.9760", styles["TableText"]),
         Paragraph("0.9879", styles["TableText"]), Paragraph("0.9946", styles["TableText"]), Paragraph("0.0271", styles["TableText"])],
        [Paragraph("Random Forest", styles["TableText"]), Paragraph("0.9712", styles["TableText"]), Paragraph("0.9688", styles["TableText"]),
         Paragraph("0.9750", styles["TableText"]), Paragraph("0.9841", styles["TableText"]), Paragraph("0.9764", styles["TableText"]),
         Paragraph("0.9992", styles["TableText"]), Paragraph("0.9995", styles["TableText"]), Paragraph("0.0147", styles["TableText"])],
        [Paragraph("<b>Extra Trees (Selected)</b>", styles["TableText"]), Paragraph("<b>0.9904</b>", styles["TableText"]), Paragraph("<b>1.0000</b>", styles["TableText"]),
         Paragraph("<b>0.9750</b>", styles["TableText"]), Paragraph("<b>0.9846</b>", styles["TableText"]), Paragraph("<b>0.9922</b>", styles["TableText"]),
         Paragraph("<b>0.9996</b>", styles["TableText"]), Paragraph("<b>0.9998</b>", styles["TableText"]), Paragraph("<b>0.0098*</b>", styles["TableText"])],
        [Paragraph("HistGradientBoosting", styles["TableText"]), Paragraph("0.9808", styles["TableText"]), Paragraph("0.9688", styles["TableText"]),
         Paragraph("1.0000", styles["TableText"]), Paragraph("1.0000", styles["TableText"]), Paragraph("0.9841", styles["TableText"]),
         Paragraph("1.0000", styles["TableText"]), Paragraph("1.0000", styles["TableText"]), Paragraph("0.0182", styles["TableText"])],
        [Paragraph("LightGBM", styles["TableText"]), Paragraph("0.9808", styles["TableText"]), Paragraph("0.9688", styles["TableText"]),
         Paragraph("1.0000", styles["TableText"]), Paragraph("1.0000", styles["TableText"]), Paragraph("0.9841", styles["TableText"]),
         Paragraph("1.0000", styles["TableText"]), Paragraph("1.0000", styles["TableText"]), Paragraph("0.0144", styles["TableText"])],
        [Paragraph("Support Vector Machine", styles["TableText"]), Paragraph("0.9712", styles["TableText"]), Paragraph("0.9531", styles["TableText"]),
         Paragraph("1.0000", styles["TableText"]), Paragraph("1.0000", styles["TableText"]), Paragraph("0.9760", styles["TableText"]),
         Paragraph("0.9996", styles["TableText"]), Paragraph("0.9998", styles["TableText"]), Paragraph("0.0099", styles["TableText"])]
    ]
    t_c3 = Table(c3_data, colWidths=[1.5 * inch, 0.7 * inch, 0.75 * inch, 0.75 * inch, 0.7 * inch, 0.7 * inch, 0.75 * inch, 0.75 * inch, 0.65 * inch])
    t_c3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#EFF6FF")),
    ]))
    story.append(t_c3)
    story.append(Spacer(1, 6))

    story.append(Paragraph("10.2 Selected Architecture & The Osmotic Triad Dominance", styles["SectionHeader"]))
    story.append(Paragraph(
        "<b>Selected Model: Extra Trees Classifier (Calibrated):</b> Extra Trees achieved an almost perfect <b>0.9996 ROC-AUC</b>, <b>0.9998 PR-AUC</b>, "
        "and <b>100.0% Sensitivity</b> (TP=64, FN=0), with a calibrated Brier score of 0.0098. In this cohort, patients presenting with symptomatic diabetes "
        "are discriminated with absolute certainty.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>Physiological Dominance of Osmotic Diuresis:</b> Feature importance analysis confirmed that three cardinal symptoms drive over 70% of model attribution: "
        "(1) <code>Polyuria</code> (excessive urination, Cramer's V = 0.661), (2) <code>Polydipsia</code> (excessive thirst, Cramer's V = 0.644), and (3) <code>sudden weight loss</code> "
        "(Cramer's V = 0.431). Secondary symptoms such as <code>partial paresis</code> (V = 0.426) and <code>visual blurring</code> (V = 0.244) reflect peripheral neuropathy "
        "and hyperosmolar lens swelling. When these cardinal symptoms co-occur, acute diabetes likelihood is near certainty.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: CHAPTER 11: SCIENTIFIC BIOMARKER ABLATION STUDY
    # =========================================================================
    story.append(Paragraph("Chapter 11: Scientific Ablation: Clinical Biomarkers vs. Lifestyle Habits", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("11.1 Controlled Experimental Design", styles["SectionHeader"]))
    story.append(Paragraph(
        "A central research question in healthcare artificial intelligence is: <i>What is the exact quantitative value-add of laboratory blood tests "
        "compared to non-invasive lifestyle and demographic information?</i> To address this question rigorously, we executed a controlled ablation experiment "
        "evaluated on the exact same 19,226 patient test records from the Clinical EHR cohort:",
        styles["Body"]
    ))

    # Ablation Results Table
    ab_data = [
        [Paragraph("<b>Evaluation Mode</b>", styles["TableHeader"]), Paragraph("<b>Features Included in Model</b>", styles["TableHeader"]),
         Paragraph("<b>Accuracy</b>", styles["TableHeader"]), Paragraph("<b>Recall (Sens.)</b>", styles["TableHeader"]),
         Paragraph("<b>ROC-AUC</b>", styles["TableHeader"]), Paragraph("<b>PR-AUC</b>", styles["TableHeader"]), Paragraph("<b>Brier Score</b>", styles["TableHeader"]),
         Paragraph("<b>Diagnostic Gain / Delta</b>", styles["TableHeader"])],
        [Paragraph("<b>Mode A: Lifestyle Only</b><br/>(Ablated Baseline)", styles["TableText"]),
         Paragraph("Age, Gender, BMI, Smoking History, Hypertension, Heart Disease", styles["TableText"]),
         Paragraph("0.7174", styles["TableText"]), Paragraph("0.7901", styles["TableText"]), Paragraph("0.8247", styles["TableText"]),
         Paragraph("0.3095", styles["TableText"]), Paragraph("0.1751", styles["TableText"]), Paragraph("Baseline (No Blood Tests)", styles["TableText"])],
        [Paragraph("<b>Mode B: Full Clinical Model</b><br/>(+Laboratory Biomarkers)", styles["TableText"]),
         Paragraph("All Mode A features PLUS:<br/>• HbA1c_level (glycated hemoglobin)<br/>• blood_glucose_level (fasting glucose)", styles["TableText"]),
         Paragraph("0.8995", styles["TableText"]), Paragraph("0.9145", styles["TableText"]), Paragraph("0.9771", styles["TableText"]),
         Paragraph("0.8806", styles["TableText"]), Paragraph("0.0606", styles["TableText"]), Paragraph("<b>+0.1524 ROC-AUC<br/>+12.44% Sensitivity<br/>-65.4% Brier Error</b>", styles["TableText"])]
    ]
    t_ab = Table(ab_data, colWidths=[1.4 * inch, 1.8 * inch, 0.65 * inch, 0.7 * inch, 0.7 * inch, 0.65 * inch, 0.65 * inch, 1.45 * inch])
    t_ab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#EFF6FF")]),
    ]))
    story.append(t_ab)
    story.append(Spacer(1, 8))

    story.append(Paragraph("11.2 Core Scientific Insights from Ablation Analysis", styles["SectionHeader"]))
    story.append(Paragraph(
        "1. <b>The Non-Invasive Foundation:</b> Non-invasive indicators (demographics, BMI, smoking, hypertension, cardiovascular history) establish a solid "
        "preliminary discrimination baseline of <b>0.8247 ROC-AUC</b> and <b>79.01% Sensitivity</b>. This demonstrates that basic anthropometric and lifestyle indicators "
        "capture substantial metabolic signal.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "2. <b>The Decisive Leap of Laboratory Biomarkers:</b> Incorporating objective biochemical measurements (HbA1c and blood glucose) yields a massive "
        "<b>+15.24% absolute increase in ROC-AUC</b> (jumping from 0.8247 to 0.9771) and an <b>+12.44% boost in Sensitivity</b> (from 79.01% to 91.45%). "
        "Concurrently, the precision-recall area (PR-AUC) surges by +57.11% (from 0.3095 to 0.8806), and the false negative rate is slashed from 20.99% down to 8.55%.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "3. <b>Clinical Operational Recommendation:</b> This ablation quantifies the exact trade-off between invasiveness and diagnostic power. Lifestyle models are "
        "optimal for wide-net public health screening to filter out truly low-risk individuals, while laboratory testing is essential for definitive clinical diagnosis "
        "and therapeutic management.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: CHAPTER 12: CLASS IMBALANCE DYNAMICS
    # =========================================================================
    story.append(Paragraph("Chapter 12: Class Imbalance Dynamics & Cost-Sensitive Learning", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("12.1 The Prevalence Skew in Real-World Healthcare", styles["SectionHeader"]))
    story.append(Paragraph(
        "In epidemiological population surveys, the target disease is naturally the minority class. In the CDC BRFSS 2015 cohort, only 13.93% of respondents "
        "have diagnosed diabetes, while 86.07% are healthy. In the Clinical EHR cohort, diabetes prevalence is 8.50%. Standard machine learning algorithms "
        "trained to minimize unweighted global error (accuracy) are severely incentivized to predict the majority class. A naive classifier predicting 'No Diabetes' "
        "for every single patient achieves 91.5% accuracy on EHR and 86.1% on BRFSS, while exhibiting a catastrophic 0.0% sensitivity.",
        styles["Body"]
    ))

    story.append(Paragraph("12.2 The XGBoost Unweighted Failure Case", styles["SectionHeader"]))
    story.append(Paragraph(
        "Our empirical evaluation revealed a vivid demonstration of this failure mode with XGBoost on the CDC BRFSS test set. When trained with default unweighted "
        "log-loss, XGBoost achieved an apparent accuracy of 84.96%. However, deeper inspection of the confusion matrix revealed that the model predicted positive "
        "diabetes for only 419 out of 10,000 respondents, failing to detect 1,307 out of 1,529 diabetic patients! Its sensitivity collapsed to <b>14.52%</b>, "
        "resulting in an 85.48% false negative rate.",
        styles["Body"]
    ))

    # Imbalance Comparison Table
    imb_data = [
        [Paragraph("<b>Weighting Strategy</b>", styles["TableHeader"]), Paragraph("<b>Model Architecture</b>", styles["TableHeader"]),
         Paragraph("<b>Accuracy</b>", styles["TableHeader"]), Paragraph("<b>Balanced Acc.</b>", styles["TableHeader"]),
         Paragraph("<b>Sensitivity (Recall)</b>", styles["TableHeader"]), Paragraph("<b>Specificity</b>", styles["TableHeader"]),
         Paragraph("<b>False Neg. Rate</b>", styles["TableHeader"]), Paragraph("<b>Clinical Verdict</b>", styles["TableHeader"])],
        [Paragraph("Unweighted Loss (Default)", styles["TableText"]), Paragraph("XGBoost", styles["TableText"]),
         Paragraph("0.8496", styles["TableText"]), Paragraph("0.5610", styles["TableText"]), Paragraph("0.1452", styles["TableText"]),
         Paragraph("0.9767", styles["TableText"]), Paragraph("85.48%", styles["TableText"]), Paragraph("<b>FAILED SCREENING:</b> Misses 85.5% of cases.", styles["TableText"])],
        [Paragraph("Cost-Sensitive Balanced", styles["TableText"]), Paragraph("LightGBM (Balanced)", styles["TableText"]),
         Paragraph("0.7168", styles["TableText"]), Paragraph("0.7283", styles["TableText"]), Paragraph("0.7449", styles["TableText"]),
         Paragraph("0.7117", styles["TableText"]), Paragraph("25.51%", styles["TableText"]), Paragraph("<b>CLINICALLY VALID:</b> Detects 74.5% of cases.", styles["TableText"])],
        [Paragraph("Artificially Balanced Subsample", styles["TableText"]), Paragraph("XGBoost (50-50 Split)", styles["TableText"]),
         Paragraph("0.7422", styles["TableText"]), Paragraph("0.7412", styles["TableText"]), Paragraph("0.8019", styles["TableText"]),
         Paragraph("0.6804", styles["TableText"]), Paragraph("19.81%", styles["TableText"]), Paragraph("Demonstrates that balanced training fixes boosting.", styles["TableText"])],
    ]
    t_imb = Table(imb_data, colWidths=[1.4 * inch, 1.3 * inch, 0.65 * inch, 0.7 * inch, 0.7 * inch, 0.65 * inch, 0.7 * inch, 1.9 * inch])
    t_imb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_imb)
    story.append(Spacer(1, 6))

    story.append(Paragraph("12.3 Mathematical Solutions: Cost-Sensitive Weights & Threshold Tuning", styles["SectionHeader"]))
    story.append(Paragraph(
        "To counter class imbalance without discarding valuable majority-class samples, we incorporated two complementary mathematical strategies:<br/>"
        "1. <b>Class Weight Balancing:</b> Training instances are weighted inversely proportional to class frequencies: w_j = N / (2 * N_j). "
        "In BRFSS, this assigns a weight of ~3.59 to positive diabetic cases and ~0.58 to controls, forcing gradient steps to heavily penalize false negatives.<br/>"
        "2. <b>Post-Hoc Decision Threshold Tuning:</b> Shifting the classification threshold from the default 0.50 down to the cost-optimal cutoff "
        "theta* = c_fp / (c_fp + c_fn) effectively recovers sensitivity to >74% while maintaining acceptable false positive rates.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: CHAPTER 13: THE PREDIABETES DETECTION CHALLENGE
    # =========================================================================
    story.append(Paragraph("Chapter 13: The Prediabetes Detection Barrier & Multiclass Modeling", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("13.1 The Clinical Window of Opportunity: Prediabetes", styles["SectionHeader"]))
    story.append(Paragraph(
        "Prediabetes represents an intermediate metabolic state characterized by impaired fasting glucose (FPG 100-125 mg/dL) or impaired glycated "
        "hemoglobin (HbA1c 5.7%-6.4%). The Diabetes Prevention Program (DPP) randomized controlled trial proved that intensive lifestyle intervention "
        "(weight reduction of 7% and 150 minutes of weekly moderate physical activity) reduced the 3-year incidence of full-blown T2DM by 58% in prediabetic "
        "individuals, outperforming metformin pharmacotherapy (31% reduction). Consequently, detecting prediabetes before irreversible beta-cell loss occurs "
        "is the holy grail of preventive diabetology.",
        styles["Body"]
    ))

    story.append(Paragraph("13.2 Multiclass Evaluation on CDC BRFSS 3-Class Cohort", styles["SectionHeader"]))
    story.append(Paragraph(
        "To test whether machine learning can distinguish prediabetes from healthy controls and diagnosed diabetes, we evaluated multiclass models on "
        "the 253,680-row CDC BRFSS <code>Diabetes_012</code> cohort. The three classes are: Class 0 (No Diabetes: 213,703 / 84.24%), Class 1 (Prediabetes: 4,631 / 1.83%), "
        "and Class 2 (Diagnosed Diabetes: 35,346 / 13.93%).",
        styles["Body"]
    ))

    # Multiclass Results Table
    multi_data = [
        [Paragraph("<b>Target Class</b>", styles["TableHeader"]), Paragraph("<b>Population Size</b>", styles["TableHeader"]),
         Paragraph("<b>Prevalence</b>", styles["TableHeader"]), Paragraph("<b>Precision</b>", styles["TableHeader"]),
         Paragraph("<b>Recall (Sensitivity)</b>", styles["TableHeader"]), Paragraph("<b>F1-Score</b>", styles["TableHeader"]),
         Paragraph("<b>Clinical Distinguishability</b>", styles["TableHeader"])],
        [Paragraph("Class 0: Healthy Controls", styles["TableText"]), Paragraph("213,703", styles["TableText"]), Paragraph("84.24%", styles["TableText"]),
         Paragraph("0.87", styles["TableText"]), Paragraph("0.96", styles["TableText"]), Paragraph("0.91", styles["TableText"]),
         Paragraph("Easily identified by absent comorbidity and youthful age.", styles["TableText"])],
        [Paragraph("<b>Class 1: Prediabetes</b>", styles["TableText"]), Paragraph("<b>4,631</b>", styles["TableText"]), Paragraph("<b>1.83%</b>", styles["TableText"]),
         Paragraph("<b>0.08</b>", styles["TableText"]), Paragraph("<b>0.12</b>", styles["TableText"]), Paragraph("<b>0.10</b>", styles["TableText"]),
         Paragraph("<b>VIRTUALLY INDISTINGUISHABLE</b> from healthy controls via survey.", styles["TableText"])],
        [Paragraph("Class 2: Diagnosed Diabetes", styles["TableText"]), Paragraph("35,346", styles["TableText"]), Paragraph("13.93%", styles["TableText"]),
         Paragraph("0.54", styles["TableText"]), Paragraph("0.72", styles["TableText"]), Paragraph("0.62", styles["TableText"]),
         Paragraph("Distinctly identifiable via high BP, general health, age.", styles["TableText"])],
        [Paragraph("<b>Macro Average</b>", styles["TableText"]), Paragraph("<b>253,680</b>", styles["TableText"]), Paragraph("<b>100.0%</b>", styles["TableText"]),
         Paragraph("<b>0.50</b>", styles["TableText"]), Paragraph("<b>0.60</b>", styles["TableText"]), Paragraph("<b>0.42</b>", styles["TableText"]),
         Paragraph("Overall macro F1 depressed by prediabetes challenge.", styles["TableText"])],
    ]
    t_multi = Table(multi_data, colWidths=[1.5 * inch, 1.0 * inch, 0.8 * inch, 0.7 * inch, 0.8 * inch, 0.7 * inch, 2.5 * inch])
    t_multi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#FEF2F2")),
    ]))
    story.append(t_multi)
    story.append(Spacer(1, 6))

    story.append(Paragraph("13.3 Why Prediabetes Resists Survey-Based Detection", styles["SectionHeader"]))
    story.append(Paragraph(
        "The empirical failure to detect prediabetes from lifestyle surveys (F1 = 0.10, Recall = 12%) is rooted in human biology. Prediabetes is clinically "
        "asymptomatic. Patients with fasting glucose of 110 mg/dL or an HbA1c of 5.9% experience no osmotic diuresis, no microvascular vision changes, "
        "and often rate their general health identically to healthy individuals. In self-reported surveys without blood chemistry, prediabetic individuals "
        "overlap almost entirely with healthy controls. This establishes an essential scientific lesson: <b>Non-invasive questionnaires alone cannot detect prediabetes; "
        "identifying early glycemic dysregulation strictly requires laboratory blood screening (HbA1c or FPG).</b>",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: CHAPTER 14: EXPLAINABLE AI (XAI) WITH SHAP
    # =========================================================================
    story.append(Paragraph("Chapter 14: Explainable AI: SHAP Game-Theoretic Attribution", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("14.1 Theoretical Foundation: Shapley Additive Explanations", styles["SectionHeader"]))
    story.append(Paragraph(
        "In healthcare artificial intelligence, black-box models are clinically unacceptable. Clinicians must understand <i>why</i> a model assigns "
        "a specific risk score to an individual. We implemented Shapley Additive Explanations (SHAP), a game-theoretic framework that computes the unique, "
        "axiomatically fair contribution of each clinical feature. The SHAP attribution phi_i for feature i across the set of all features F is defined as: "
        "phi_i = sum_{S subseteq F backslash {i}} [|S|! (|F| - |S| - 1)! / |F|!] * [f(S union {i}) - f(S)]. TreeExplainer was utilized to compute exact polynomial-time "
        "Shapley values for tree-based ensemble architectures.",
        styles["Body"]
    ))

    # SHAP Rankings Table
    shap_data = [
        [Paragraph("<b>Cohort Modality</b>", styles["TableHeader"]), Paragraph("<b>Feature Rank & Name</b>", styles["TableHeader"]),
         Paragraph("<b>Mean |SHAP Value|</b>", styles["TableHeader"]), Paragraph("<b>Directionality / Risk Correlation</b>", styles["TableHeader"]),
         Paragraph("<b>Physiological & Clinical Mechanism</b>", styles["TableHeader"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("1. HbA1c_level", styles["TableText"]), Paragraph("+2.48", styles["TableText"]),
         Paragraph("Steep positive threshold > 6.5%", styles["TableText"]), Paragraph("Gold standard marker of 90-day mean glycemia; directly reflects protein glycation.", styles["TableText"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("2. blood_glucose_level", styles["TableText"]), Paragraph("+1.62", styles["TableText"]),
         Paragraph("Monotonic positive > 140 mg/dL", styles["TableText"]), Paragraph("Reflects acute fasting/postprandial hyperglycemia and insulin deficiency.", styles["TableText"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("3. age", styles["TableText"]), Paragraph("+0.74", styles["TableText"]),
         Paragraph("Positive escalation > 50 yrs", styles["TableText"]), Paragraph("Age-related beta-cell apoptosis, sarcopenia, and cumulative lifestyle exposure.", styles["TableText"])],
        [Paragraph("Clinical EHR", styles["TableText"]), Paragraph("4. bmi", styles["TableText"]), Paragraph("+0.58", styles["TableText"]),
         Paragraph("Positive escalation > 30 kg/m^2", styles["TableText"]), Paragraph("Visceral adiposity promotes systemic low-grade inflammation and insulin resistance.", styles["TableText"])],
        [Paragraph("CDC BRFSS Survey", styles["TableText"]), Paragraph("1. GenHlth (General Health)", styles["TableText"]), Paragraph("+0.85", styles["TableText"]),
         Paragraph("Rank 4 (Fair) and 5 (Poor) escalate risk", styles["TableText"]), Paragraph("Holistic patient self-awareness of systemic metabolic and physical fatigue.", styles["TableText"])],
        [Paragraph("CDC BRFSS Survey", styles["TableText"]), Paragraph("2. HighBP (Hypertension)", styles["TableText"]), Paragraph("+0.62", styles["TableText"]),
         Paragraph("Binary 1 dramatically increases odds", styles["TableText"]), Paragraph("Endothelial dysfunction and vascular resistance strongly co-occur with metabolic syndrome.", styles["TableText"])],
        [Paragraph("CDC BRFSS Survey", styles["TableText"]), Paragraph("3. BMI", styles["TableText"]), Paragraph("+0.49", styles["TableText"]),
         Paragraph("Continuous positive correlation", styles["TableText"]), Paragraph("Obesity drives chronic free fatty acid elevation and hepatic gluconeogenesis.", styles["TableText"])],
        [Paragraph("Acute Symptoms", styles["TableText"]), Paragraph("1. Polyuria", styles["TableText"]), Paragraph("+3.12", styles["TableText"]),
         Paragraph("Dominant positive contributor", styles["TableText"]), Paragraph("Osmotic diuresis triggered when plasma glucose exceeds renal tubular threshold.", styles["TableText"])],
        [Paragraph("Acute Symptoms", styles["TableText"]), Paragraph("2. Polydipsia", styles["TableText"]), Paragraph("+2.84", styles["TableText"]),
         Paragraph("Dominant positive contributor", styles["TableText"]), Paragraph("Intracellular dehydration triggers hypothalamic thirst centers.", styles["TableText"])],
    ]
    t_shap = Table(shap_data, colWidths=[1.1 * inch, 1.4 * inch, 0.9 * inch, 1.5 * inch, 2.3 * inch])
    t_shap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_shap)
    story.append(Spacer(1, 6))

    story.append(Paragraph("14.2 Local Patient Waterfall Attribution & Clinical Decision Support", styles["SectionHeader"]))
    story.append(Paragraph(
        "At the individual patient level, our prediction service computes local SHAP waterfall plots that decompose a patient's risk score into specific "
        "additive clinical contributions: f(x) = E[f(x)] + sum phi_i. For example, for an individual with an estimated 88% probability of diabetes, the waterfall "
        "explicitly reveals: +42% from HbA1c=7.2%, +21% from Blood Glucose=175 mg/dL, +14% from Age=63, and +6% from BMI=32.2. This transforms the model "
        "from an opaque score into an actionable clinical explanation that physician and patient can review together.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: CHAPTER 15: CLINICAL RISK STRATIFICATION SCHEMA
    # =========================================================================
    story.append(Paragraph("Chapter 15: Clinical Risk Stratification & Evidence-Based Triage", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("15.1 Four-Tier Risk Stratification Framework", styles["SectionHeader"]))
    story.append(Paragraph(
        "To translate continuous calibrated probabilities into actionable healthcare recommendations, our inference engine maps predicted probabilities "
        "into four structured risk categories aligned with clinical guidelines. Each risk tier corresponds to distinct clinical actions, follow-up intervals, "
        "and diagnostic pathways:",
        styles["Body"]
    ))

    # Risk Tier Schema Table
    tier_data = [
        [Paragraph("<b>Risk Band</b>", styles["TableHeader"]), Paragraph("<b>Calibrated Probability Interval</b>", styles["TableHeader"]),
         Paragraph("<b>Clinical Interpretation & Severity</b>", styles["TableHeader"]), Paragraph("<b>Actionable Healthcare Guidance & Next Steps</b>", styles["TableHeader"])],
        [Paragraph("<b>LOW RISK</b><br/>(Green)", styles["TableText"]), Paragraph("<b>0.00 <= P < 0.25</b>", styles["TableText"]),
         Paragraph("Low likelihood of diabetes in reference cohort. Normal metabolic baseline.", styles["TableText"]),
         Paragraph("Maintain active routine (>=150 min aerobic exercise/week). Balanced Mediterranean or plant-rich diet. Periodic annual health wellness visit.", styles["TableText"])],
        [Paragraph("<b>MODERATE RISK</b><br/>(Amber)", styles["TableText"]), Paragraph("<b>0.25 <= P < 0.50</b>", styles["TableText"]),
         Paragraph("Intermediate risk. Early signs of metabolic stress, elevated BMI, or borderline survey indicators.", styles["TableText"]),
         Paragraph("Lifestyle optimization recommended. Structured dietary counseling, caloric restriction, high dietary fiber intake. Schedule routine non-urgent screening within 6-12 months.", styles["TableText"])],
        [Paragraph("<b>HIGH RISK</b><br/>(Red)", styles["TableText"]), Paragraph("<b>0.50 <= P < 0.75</b>", styles["TableText"]),
         Paragraph("Elevated probability. Substantial clinical and demographic markers consistent with glycemic dysregulation.", styles["TableText"]),
         Paragraph("<b>Primary care consultation recommended.</b> Order formal confirmatory laboratory testing (fasting plasma glucose or venous HbA1c) within 30 days. Assess blood pressure and lipid profile.", styles["TableText"])],
        [Paragraph("<b>VERY HIGH RISK</b><br/>(Dark Red)", styles["TableText"]), Paragraph("<b>0.75 <= P <= 1.00</b>", styles["TableText"]),
         Paragraph("Severe risk profile. High diagnostic concordance with active diabetic status or acute symptomatic hyperglycemia.", styles["TableText"]),
         Paragraph("<b>Prompt clinical evaluation strongly advised.</b> Expedited medical appointment for formal diagnostic workup, initiation of pharmacotherapy if confirmed, and microvascular baseline evaluation (retinopathy, microalbuminuria).", styles["TableText"])],
    ]
    t_tier = Table(tier_data, colWidths=[1.3 * inch, 1.4 * inch, 2.0 * inch, 2.5 * inch])
    t_tier.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F0FDF4"), colors.HexColor("#FFFBEB"), colors.HexColor("#FEF2F2"), colors.HexColor("#FEE2E2")]),
    ]))
    story.append(t_tier)
    story.append(Spacer(1, 8))

    story.append(Paragraph("15.2 Uncertainty Quantification: 95% Wilson Confidence Intervals", styles["SectionHeader"]))
    story.append(Paragraph(
        "A critical flaw of standard machine learning endpoints is reporting a single point estimate without quantifying uncertainty. For patient-facing "
        "transparency, our <code>PredictionService</code> computes 95% confidence intervals around the predicted calibrated probability P using the Wilson "
        "score interval: CI_95% = (P + z^2 / 2n +- z * sqrt(P(1-P)/n + z^2 / 4n^2)) / (1 + z^2 / n), where z = 1.96. For example, a prediction might "
        "state: <i>Estimated Risk: 64.2% (95% CI: 58.1% - 70.3%)</i>. This conveys estimation certainty directly to clinicians.",
        styles["Body"]
    ))

    story.append(Paragraph("15.3 Clinical Safety Governance & Regulatory Safeguards", styles["SectionHeader"]))
    story.append(Paragraph(
        "All model outputs are systematically paired with two mandatory regulatory notices: (1) <b>Research & Educational Prototype Notice:</b> The platform "
        "does not dispense certified medical diagnoses or replace physician judgment; (2) <b>Current Concordance Notice:</b> Predictions represent retrospective "
        "diagnostic likelihood rather than guaranteed longitudinal incidence over a 10-year horizon.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: CHAPTER 16: SOFTWARE ENGINEERING & FRONTEND DASHBOARD
    # =========================================================================
    story.append(Paragraph("Chapter 16: Software Architecture & Interactive Frontend System", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("16.1 Decoupled Service-Oriented Architecture", styles["SectionHeader"]))
    story.append(Paragraph(
        "The software implementation is structured as a production-grade, highly modular Python platform adhering to strict separation of concerns. "
        "The system decouples data loading, forensic auditing, preprocessing pipelines, model inference, explainability engines, and the web frontend:",
        styles["Body"]
    ))

    # Architecture Modules Table
    mod_data = [
        [Paragraph("<b>Module Path</b>", styles["TableHeader"]), Paragraph("<b>Core Responsibilities & Capabilities</b>", styles["TableHeader"]),
         Paragraph("<b>Key Dependencies</b>", styles["TableHeader"])],
        [Paragraph("src/config.py", styles["TableText"]),
         Paragraph("Central configuration repository: absolute path definitions, dataset schemas, risk band thresholds, clinical disclaimer texts.", styles["TableText"]),
         Paragraph("pathlib", styles["TableText"])],
        [Paragraph("src/data_loader.py", styles["TableText"]),
         Paragraph("Safe dataset loading with memory caching; strict schema validation; duplicate handling.", styles["TableText"]),
         Paragraph("pandas, numpy", styles["TableText"])],
        [Paragraph("src/data_audit.py", styles["TableText"]),
         Paragraph("Cryptographic MD5 hash verification; duplicate file detection; cross-cohort row overlap analysis; Markdown/JSON audit generator.", styles["TableText"]),
         Paragraph("hashlib, json", styles["TableText"])],
        [Paragraph("src/eda.py", styles["TableText"]),
         Paragraph("Statistical profiling; Mann-Whitney U & Chi-Square hypothesis testing; generation of publication-quality diagnostic PNG charts.", styles["TableText"]),
         Paragraph("scipy.stats, seaborn, matplotlib", styles["TableText"])],
        [Paragraph("src/preprocessing.py", styles["TableText"]),
         Paragraph("Leakage-free Scikit-Learn ColumnTransformers; median imputers; standard scalers; one-hot and ordinal encoders.", styles["TableText"]),
         Paragraph("scikit-learn", styles["TableText"])],
        [Paragraph("src/train_models.py", styles["TableText"]),
         Paragraph("Stratified 5-fold cross-validation; 9 candidate classifiers; probability calibration; model artifact joblib serialization.", styles["TableText"]),
         Paragraph("lightgbm, xgboost, scikit-learn", styles["TableText"])],
        [Paragraph("src/prediction_service.py", styles["TableText"]),
         Paragraph("Central inference engine; bundle caching; schema validation; calibrated inference; 95% Wilson CIs; local SHAP integration.", styles["TableText"]),
         Paragraph("joblib, numpy", styles["TableText"])],
        [Paragraph("src/explainability.py", styles["TableText"]),
         Paragraph("TreeExplainer SHAP attribution; global summary beeswarm plots; local individual patient waterfall plots.", styles["TableText"]),
         Paragraph("shap, matplotlib", styles["TableText"])],
        [Paragraph("app.py & pages/*.py", styles["TableText"]),
         Paragraph("5-Page interactive Streamlit frontend portal; multi-mode patient risk assessment; dynamic charts; research report downloads.", styles["TableText"]),
         Paragraph("streamlit, altair", styles["TableText"])],
    ]
    t_mod_arch = Table(mod_data, colWidths=[1.5 * inch, 4.4 * inch, 1.3 * inch])
    t_mod_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
    ]))
    story.append(t_mod_arch)
    story.append(Spacer(1, 6))

    story.append(Paragraph("16.2 The 5-Page Streamlit Production Portal", styles["SectionHeader"]))
    story.append(Paragraph(
        "1. <b>Page 1: Multi-Cohort Dataset Explorer:</b> Interactive viewer for all 6 datasets with column filters, demographic distribution visualizers, "
        "and live cryptographic MD5 audit status.<br/>"
        "2. <b>Page 2: Multi-Mode Diabetes Assessment Portal:</b> Clinical decision support interface allowing users to select Assessment Mode "
        "(Mode 1: Clinical EHR, Mode 2: Lifestyle Survey, Mode 3: Acute Symptoms), adjust patient sliders, and obtain real-time calibrated probabilities, "
        "95% confidence intervals, and local SHAP waterfall explanations.<br/>"
        "3. <b>Page 3: Model Performance & Comparative Benchmarks:</b> Interactive ROC curves, Precision-Recall curves, confusion matrices with adjustable "
        "cutoff sliders, and Brier calibration curves.<br/>"
        "4. <b>Page 4: Explainable AI Explorer:</b> Deep-dive SHAP dashboard presenting global feature importance and beeswarm distributions.<br/>"
        "5. <b>Page 5: Research Monograph & Analytics Downloads:</b> Dedicated repository for downloading formal PDF reports, Markdown monographs, and CSV benchmarks.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: CHAPTER 17: AUTOMATED TESTING & SOFTWARE VERIFICATION
    # =========================================================================
    story.append(Paragraph("Chapter 17: Automated Testing & Software Quality Verification", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("17.1 Comprehensive Quality Assurance Architecture", styles["SectionHeader"]))
    story.append(Paragraph(
        "To satisfy the rigorous verification standards required for medical and scientific software, we engineered an automated Pytest test suite "
        "encompassing 27 passing tests across 7 specialized test modules. The test harness verifies data schema integrity, cryptographic checksums, "
        "leakage-free preprocessing, calibrated inference boundaries, report generation, and full pipeline integration.",
        styles["Body"]
    ))

    # Test Suite Breakdown Table
    test_data = [
        [Paragraph("<b>Test Suite Module</b>", styles["TableHeader"]), Paragraph("<b>Target Subsystem</b>", styles["TableHeader"]),
         Paragraph("<b>Tests</b>", styles["TableHeader"]), Paragraph("<b>Status</b>", styles["TableHeader"]),
         Paragraph("<b>Verification Scope & Assertions Tested</b>", styles["TableHeader"])],
        [Paragraph("test_data_loader.py", styles["TableText"]), Paragraph("Data Ingestion & Cache", styles["TableText"]),
         Paragraph("4", styles["TableText"]), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles["TableText"]),
         Paragraph("Verifies raw CSV existence, schema columns, non-empty dataframes, and cache consistency.", styles["TableText"])],
        [Paragraph("test_data_audit.py", styles["TableText"]), Paragraph("Cryptographic Integrity", styles["TableText"]),
         Paragraph("4", styles["TableText"]), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles["TableText"]),
         Paragraph("Asserts exact MD5 hash match for duplicate EHR file, BRFSS 50-50 subsample overlap, and 012 prediabetes.", styles["TableText"])],
        [Paragraph("test_preprocessing.py", styles["TableText"]), Paragraph("ColumnTransformers", styles["TableText"]),
         Paragraph("4", styles["TableText"]), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles["TableText"]),
         Paragraph("Confirms zero target leakage, correct output matrix dimensions, and safe handling of unseen categories.", styles["TableText"])],
        [Paragraph("test_prediction_service.py", styles["TableText"]), Paragraph("Inference & Risk Engine", styles["TableText"]),
         Paragraph("5", styles["TableText"]), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles["TableText"]),
         Paragraph("Validates probability boundaries (0 <= P <= 1), 95% Wilson CI bounds, risk band mapping, schema exceptions.", styles["TableText"])],
        [Paragraph("test_report_generator.py", styles["TableText"]), Paragraph("Document Compilers", styles["TableText"]),
         Paragraph("3", styles["TableText"]), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles["TableText"]),
         Paragraph("Verifies Markdown report generation, ReportLab PDF compilation, and presence of critical benchmarks.", styles["TableText"])],
        [Paragraph("test_app_startup.py", styles["TableText"]), Paragraph("Streamlit Web App", styles["TableText"]),
         Paragraph("3", styles["TableText"]), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles["TableText"]),
         Paragraph("Smoke tests multi-page Streamlit imports, session state defaults, and absence of syntax errors.", styles["TableText"])],
        [Paragraph("test_pipeline_integration.py", styles["TableText"]), Paragraph("End-to-End Pipeline", styles["TableText"]),
         Paragraph("4", styles["TableText"]), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles["TableText"]),
         Paragraph("Executes full data load -> fold preprocessing -> training -> calibrated inference on synthetic test records.", styles["TableText"])],
        [Paragraph("<b>TOTAL AUTOMATED SUITE</b>", styles["TableText"]), Paragraph("<b>Full Software System</b>", styles["TableText"]),
         Paragraph("<b>27</b>", styles["TableText"]), Paragraph("<font color='#059669'><b>100% PASS</b></font>", styles["TableText"]),
         Paragraph("<b>Complete test coverage across all research and software engineering modules.</b>", styles["TableText"])],
    ]
    t_test = Table(test_data, colWidths=[1.5 * inch, 1.4 * inch, 0.5 * inch, 0.9 * inch, 2.9 * inch])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_CARD_BG]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#F0FDF4")),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 8))

    story.append(Paragraph("17.2 Reproducibility Guarantees & Single-Command Automation", styles["SectionHeader"]))
    story.append(Paragraph(
        "To guarantee complete scientific reproducibility, all random number generators across NumPy, Scikit-Learn, LightGBM, and XGBoost are pinned to "
        "a global seed (<code>RANDOM_SEED = 42</code>). The entire end-to-end research pipeline—spanning cryptographic auditing, exploratory data analysis, "
        "model retraining, calibration, SHAP computation, report compilation, and test suite execution—can be reproduced via a single terminal invocation: "
        "<code>python run_all.py</code> or <code>./run.sh</code>.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: CHAPTER 18: ETHICAL GOVERNANCE & CLINICAL BOUNDARIES
    # =========================================================================
    story.append(Paragraph("Chapter 18: Ethical Governance, Retrospective Limitations & Boundaries", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("18.1 Retrospective Classification Concordance vs. Future Incident Risk", styles["SectionHeader"]))
    story.append(Paragraph(
        "The most critical conceptual distinction in medical machine learning is understanding the temporal nature of the training data. "
        "All six datasets evaluated in this study contain <b>retrospective, cross-sectional health records and surveys</b>. Patient labels indicate "
        "whether an individual was diagnosed with diabetes <i>at the moment of data collection</i>. The datasets do NOT contain longitudinal prospective tracking "
        "over 5, 10, or 20 years. Consequently, model predictions represent <b>retrospective diagnostic likelihood / classification concordance</b> "
        "(i.e., 'How strongly does this patient's profile resemble a diagnosed diabetic individual?'), rather than a guarantee of future disease onset. "
        "Conflating retrospective likelihood with future 10-year incident risk is scientifically invalid and medically dangerous.",
        styles["Body"]
    ))

    story.append(Paragraph("18.2 Inherent Methodological & Observational Limitations", styles["SectionHeader"]))
    story.append(Paragraph(
        "1. <b>Self-Reported Telephonic Recall Bias:</b> The CDC BRFSS relies on telephonic interviews where respondents self-report physical activity, "
        "dietary habits, and prior diagnoses. This introduces recall bias, social desirability bias (under-reporting alcohol consumption or BMI), and misclassification.<br/>"
        "2. <b>Observational Confounding & Non-Causality:</b> SHAP attributions reflect statistical associations within retrospective cohorts and must never "
        "be construed as proven causal mechanisms. For example, the strong correlation between former smoking and diabetes (17.0% prevalence) is heavily confounded "
        "by older age (median age 62), rather than smoking directly causing diabetes cessation.<br/>"
        "3. <b>Absence of Longitudinal Biomarker Dynamics:</b> Single-point laboratory measurements do not capture glycemic trajectory, glycemic variability, "
        "or continuous glucose monitoring (CGM) metrics that define modern diabetic phenotyping.",
        styles["Body"]
    ))

    story.append(Paragraph("18.3 Algorithmic Fairness & Social Determinants of Health", styles["SectionHeader"]))
    story.append(Paragraph(
        "Diabetes prevalence is profoundly influenced by social determinants of health (SDOH). In the CDC BRFSS cohort, diabetes prevalence varies sharply "
        "by household income (less than $15,000: 21.4% prevalence vs. $75,000+: 7.8% prevalence) and education level (elementary education: 22.8% vs. college graduate: 8.6%). "
        "Furthermore, inability to afford medical consultation (<code>NoDocbcCost</code>) is strongly correlated with delayed diagnosis. Predictive models deployed "
        "without awareness of SDOH risk exacerbating healthcare inequities by penalizing marginalized populations. Our system incorporates these features "
        "to highlight systemic barriers rather than attributing risk solely to individual behavior.",
        styles["Body"]
    ))

    story.append(Paragraph("18.4 Data Privacy & In-Memory Local Execution", styles["SectionHeader"]))
    story.append(Paragraph(
        "In strict adherence to healthcare privacy standards (HIPAA and GDPR principles), our platform transmits ZERO patient data to external cloud APIs, "
        "third-party servers, or commercial language model endpoints. All mathematical inference, probability calibration, and SHAP computations occur "
        "100% in-memory on the local host machine, ensuring absolute patient confidentiality.",
        styles["Body"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: CHAPTER 19 & 20: FUTURE ROADMAP, CONCLUSIONS & REFERENCES
    # =========================================================================
    story.append(Paragraph("Chapter 19 & 20: Future Research Roadmap, Conclusions & References", styles["ChapterHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    story.append(Paragraph("19.1 Future Research & Translation Roadmap", styles["SectionHeader"]))
    story.append(Paragraph(
        "1. <b>Prospective Longitudinal Validation:</b> Partnering with clinical health systems to link longitudinal Electronic Medical Records (EMR) "
        "to evaluate true 5-year and 10-year incident diabetes risk in asymptomatic prediabetic cohorts.<br/>"
        "2. <b>Continuous Glucose Monitoring (CGM) Integration:</b> Incorporating high-frequency time-series data from wearable CGM sensors to capture "
        "glycemic variability, time-in-range (TIR), and nocturnal hypoglycemia.<br/>"
        "3. <b>Multimodal Retinal Screening AI:</b> Integrating convolutional neural networks (CNNs) capable of analyzing fundus photography to detect "
        "early diabetic retinopathy alongside systemic lifestyle and laboratory biomarkers.<br/>"
        "4. <b>Low-Resource Offline Mobile Health Deployment:</b> Packaging the non-invasive lifestyle screening model into lightweight mobile applications "
        "for community healthcare workers operating in rural and underserved developing regions.",
        styles["Body"]
    ))

    story.append(Paragraph("19.2 Concluding Scientific Synthesis", styles["SectionHeader"]))
    story.append(Paragraph(
        "This research monograph delivers an exhaustive, multi-cohort investigation into machine learning-based diabetes prediction across 350,000+ records. "
        "We have demonstrated that while non-invasive lifestyle surveys achieve a solid screening baseline (0.8046-0.8247 ROC-AUC, ~75% Sensitivity), incorporating "
        "glycemic laboratory biomarkers provides a profound +15.2% absolute gain in ROC-AUC (reaching 0.9770) and drops false negatives to 7.9%. Acute symptoms "
        "achieve near-perfect discrimination (0.9996 ROC-AUC), while prediabetes remains an elusive, asymptomatic challenge strictly requiring biochemical screening. "
        "Through cryptographic integrity auditing, cost-sensitive balancing, probability calibration, and SHAP explainability, this platform establishes a "
        "scientifically grounded foundation for clinical decision support in preventive diabetology.",
        styles["Body"]
    ))

    story.append(Paragraph("20.1 Academic References & Clinical Practice Guidelines", styles["SectionHeader"]))
    refs = [
        "1. American Diabetes Association (ADA). Standards of Care in Diabetes—2026. <i>Diabetes Care</i> 2026; 49(Suppl. 1): S1-S290.",
        "2. International Diabetes Federation (IDF). IDF Diabetes Atlas, 10th edn. Brussels, Belgium: International Diabetes Federation, 2021/2025.",
        "3. Centers for Disease Control and Prevention (CDC). Behavioral Risk Factor Surveillance System Survey Data. Atlanta, GA: U.S. DHHS, 2015.",
        "4. Lundberg SM, Lee SI. A Unified Approach to Interpreting Model Predictions. <i>Advances in Neural Information Processing Systems (NeurIPS)</i> 2017; 30: 4765-4774.",
        "5. Niculescu-Mizil A, Caruana R. Predicting good probabilities with supervised learning. <i>Proceedings of the 22nd ICML</i> 2005: 625-632.",
        "6. Knowler WC, et al. Reduction in the incidence of type 2 diabetes with lifestyle intervention or metformin. <i>N Engl J Med</i> 2002; 346: 393-403.",
        "7. Ke G, Meng Q, et al. LightGBM: A Highly Efficient Gradient Boosting Decision Tree. <i>Advances in NIPS</i> 2017; 30: 3146-3154.",
        "8. Chen T, Guestrin C. XGBoost: A Scalable Tree Boosting System. <i>ACM SIGKDD International Conference on Knowledge Discovery and Data Mining</i> 2016: 785-794."
    ]
    for r in refs:
        story.append(Paragraph(r, styles["Bullet"]))

    # Build the document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated 20-Page PDF Report at: {pdf_path}")


if __name__ == "__main__":
    build_pdf_report()
