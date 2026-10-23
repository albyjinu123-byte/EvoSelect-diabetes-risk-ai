"""
Script to generate a publication-grade 15-slide PowerPoint Presentation (16:9 Widescreen)
for AI-Based Diabetes Risk Prediction Using Machine Learning and Lifestyle Factors.
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Color Palette Definitions
C_NAVY = RGBColor(15, 23, 42)        # #0F172A
C_SLATE = RGBColor(30, 41, 59)      # #1E293B
C_MUTED = RGBColor(71, 85, 105)     # #475569
C_LIGHT_BG = RGBColor(248, 250, 252)# #F8FAFC
C_WHITE = RGBColor(255, 255, 255)   # #FFFFFF
C_PRIMARY = RGBColor(2, 132, 199)   # #0284C7 (Medical Cyan/Blue)
C_ACCENT = RGBColor(14, 165, 233)   # #0EA5E9
C_SUCCESS = RGBColor(16, 185, 129)  # #10B981 (Emerald)
C_WARNING = RGBColor(245, 158, 11)  # #F59E0B (Amber)
C_DANGER = RGBColor(239, 68, 68)    # #EF4444 (Crimson)
C_CARD_BG = RGBColor(255, 255, 255) # Pure White Cards
C_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 Light Gray Border
C_CARD_SUBTLE = RGBColor(241, 245, 249) # #F1F5F9


def add_header(slide, title_text, category_text, slide_num):
    """Adds a standard header banner with category tracker pill and slide number."""
    # Top banner background line / subtle border
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.9))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Category Tracker
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_PRIMARY
    p_cat.font.name = "Arial"
    
    # Main Slide Title
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = C_NAVY
    p_title.font.name = "Arial"
    p_title.space_before = Pt(3)

    # Slide Number pill on top right
    num_box = slide.shapes.add_textbox(Inches(11.0), Inches(0.4), Inches(1.5), Inches(0.4))
    ntf = num_box.text_frame
    ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
    np = ntf.paragraphs[0]
    np.text = f"SLIDE {slide_num:02d} / 15"
    np.alignment = PP_ALIGN.RIGHT
    np.font.size = Pt(10)
    np.font.bold = True
    np.font.color.rgb = C_MUTED
    np.font.name = "Arial"


def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
    """Draws a card rectangle shape container with subtle border."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card


def set_slide_background(slide, color=C_LIGHT_BG):
    """Sets background color of slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Premium Theme)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, C_NAVY)

    # Subtle top accent bar
    top_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_PRIMARY
    top_bar.line.fill.background()

    # Title & Subtitle Container
    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(10.9), Inches(3.2))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "HEALTHCARE ARTIFICIAL INTELLIGENCE RESEARCH MONOGRAPH"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_ACCENT
    p0.font.name = "Arial"
    p0.space_after = Pt(10)

    p1 = tf1.add_paragraph()
    p1.text = "AI-Based Diabetes Risk Prediction Using Machine Learning & Lifestyle Factors"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.font.name = "Arial"
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "A Multi-Cohort Empirical Evaluation Across 350,000+ Patient Records: Clinical Biomarker Ablation, Population Survey Stratification, Acute Symptom Triad & Explainable AI (SHAP)"
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.font.name = "Arial"

    # 3 Stat Cards on Title Slide
    stats_data = [
        ("350,000+", "Total Patient Records & Surveys", C_PRIMARY),
        ("0.9770", "Peak ROC-AUC (Clinical LightGBM)", C_SUCCESS),
        ("+15.2%", "Diagnostic Value-Add of Biomarkers", C_ACCENT)
    ]
    for i, (val, lbl, col) in enumerate(stats_data):
        c_left = Inches(1.2 + i * 3.75)
        add_card(slide1, c_left, Inches(5.1), Inches(3.5), Inches(1.4), bg_color=C_SLATE, border_color=RGBColor(51, 65, 85))
        sbox = slide1.shapes.add_textbox(c_left + Inches(0.2), Inches(5.2), Inches(3.1), Inches(1.2))
        stf = sbox.text_frame
        stf.word_wrap = True
        sp1 = stf.paragraphs[0]
        sp1.text = val
        sp1.font.size = Pt(24)
        sp1.font.bold = True
        sp1.font.color.rgb = col
        sp1.font.name = "Arial"
        sp2 = stf.add_paragraph()
        sp2.text = lbl
        sp2.font.size = Pt(11)
        sp2.font.color.rgb = RGBColor(226, 232, 240)
        sp2.font.name = "Arial"

    # Footer Metadata
    ft_box = slide1.shapes.add_textbox(Inches(1.2), Inches(6.8), Inches(10.9), Inches(0.4))
    ft_tf = ft_box.text_frame
    ft_p = ft_tf.paragraphs[0]
    ft_p.text = "Standards: Strict Medical Leakage Prevention | Multi-Cohort Auditing | Calibrated Probability Inference"
    ft_p.font.size = Pt(9.5)
    ft_p.font.color.rgb = C_MUTED
    ft_p.font.name = "Arial"

    # =========================================================================
    # SLIDE 2: CLINICAL PROBLEM STATEMENT & EPIDEMIOLOGICAL BURDEN
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, C_LIGHT_BG)
    add_header(slide2, "Clinical Problem Statement & Epidemiological Imperative", "Background & Clinical Motivation", 2)

    # 3 Pillar Cards across the screen
    pills = [
        ("1. The Global Epidemic", [
            "537 Million Adults worldwide live with diabetes mellitus (IDF Atlas).",
            "Projected to exceed 783 million by 2045 (a 46% surge).",
            "Over 50% of people with type 2 diabetes are undiagnosed in early phases.",
            "Annual global healthcare expenditure exceeds $966 Billion USD."
        ], C_DANGER),
        ("2. Asymptomatic Progression", [
            "Silent Pathophysiology: Glycemic dysregulation persists 5-10 years pre-diagnosis.",
            "Microvascular Complications: Diabetic retinopathy, nephropathy, and peripheral neuropathy.",
            "Macrovascular Risk: 2-3x elevated risk of myocardial infarction, stroke, and arterial disease.",
            "Early lifestyle intervention stops 58% of prediabetes progression (DPP Trial)."
        ], C_WARNING),
        ("3. The Screening Dilemma", [
            "Invasive Gold Standards: Fasting plasma glucose, HbA1c, OGTT require venous blood draws.",
            "Logistical Bottlenecks: Laboratory cold chain, trained phlebotomists, patient compliance.",
            "The Machine Learning Opportunity: Can modifiable lifestyle surveys and symptom triage stratify risk accurately without immediate venipuncture?"
        ], C_PRIMARY)
    ]

    for i, (head, bullets, bar_col) in enumerate(pills):
        c_left = Inches(0.8 + i * 4.0)
        c_width = Inches(3.733)
        add_card(slide2, c_left, Inches(1.5), c_width, Inches(5.3))
        
        # Color bar on top of card
        c_bar = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.5), c_width, Inches(0.1))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = bar_col
        c_bar.line.fill.background()

        tbox = slide2.shapes.add_textbox(c_left + Inches(0.25), Inches(1.75), c_width - Inches(0.5), Inches(4.8))
        ttf = tbox.text_frame
        ttf.word_wrap = True
        
        tp0 = ttf.paragraphs[0]
        tp0.text = head
        tp0.font.size = Pt(16)
        tp0.font.bold = True
        tp0.font.color.rgb = C_NAVY
        tp0.font.name = "Arial"
        tp0.space_after = Pt(12)

        for b in bullets:
            bp = ttf.add_paragraph()
            bp.text = f"•  {b}"
            bp.font.size = Pt(11.5)
            bp.font.color.rgb = C_SLATE
            bp.font.name = "Arial"
            bp.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: MULTI-COHORT DATA ARCHITECTURE & MODALITY TAXONOMY
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, C_LIGHT_BG)
    add_header(slide3, "Multi-Cohort Data Architecture Across 350,000+ Records", "Data Architecture & Modalities", 3)

    # Left Column: Table of Datasets
    add_card(slide3, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.3))
    tbox3_left = slide3.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(7.0), Inches(0.6))
    ttf3_l = tbox3_left.text_frame
    p = ttf3_l.paragraphs[0]
    p.text = "Inventory of Analyzed Healthcare Cohorts"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    # Add Table
    rows, cols = 6, 4
    table_shape = slide3.shapes.add_table(rows, cols, Inches(1.0), Inches(2.3), Inches(7.1), Inches(4.2))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.4)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.2)
    tbl.columns[3].width = Inches(2.4)

    headers = ["Cohort Name / File", "Records", "Prevalence", "Modality & Features"]
    data = [
        ("Clinical & Laboratory EHR\n(diabetes_prediction_dataset)", "100,000", "8.5% Diabetic", "HbA1c, Blood Glucose, BMI, Age, Smoking, HTN, Heart Disease"),
        ("CDC BRFSS Survey (Binary)\n(diabetes_binary_health)", "253,680", "13.9% Diabetic", "21 Modifiable Lifestyle, Diet, Physical Activity, General Health"),
        ("CDC BRFSS 50-50 Balanced\n(diabetes_binary_5050split)", "70,692", "50.0% Diabetic", "Artificially balanced subsample for class imbalance research"),
        ("CDC BRFSS 3-Class Cohort\n(diabetes_012_health)", "253,680", "1.8% Prediabetes\n13.9% Diabetes", "Multiclass separation: Healthy (84.2%) vs Prediabetes vs Diabetes"),
        ("Early Symptoms (Sylhet)\n(diabetes_data_upload)", "520", "61.5% Diabetic", "Acute hospital presentation: Polyuria, Polydipsia, Weight Loss")
    ]

    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        cp = cell.text_frame.paragraphs[0]
        cp.text = h
        cp.font.size = Pt(10.5)
        cp.font.bold = True
        cp.font.color.rgb = C_WHITE
        cp.font.name = "Arial"

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE if i % 2 == 0 else C_CARD_SUBTLE
            cp = cell.text_frame.paragraphs[0]
            cp.text = val
            cp.font.size = Pt(9.5)
            cp.font.color.rgb = C_SLATE
            cp.font.name = "Arial"

    # Right Column: Architectural Principles
    add_card(slide3, Inches(8.5), Inches(1.5), Inches(4.033), Inches(5.3))
    tbox3_r = slide3.shapes.add_textbox(Inches(8.75), Inches(1.7), Inches(3.533), Inches(4.8))
    ttf3_r = tbox3_r.text_frame
    ttf3_r.word_wrap = True

    rp0 = ttf3_r.paragraphs[0]
    rp0.text = "Strict Scientific Isolation"
    rp0.font.size = Pt(15)
    rp0.font.bold = True
    rp0.font.color.rgb = C_NAVY
    rp0.space_after = Pt(10)

    rules = [
        ("Zero Naive Concatenation", "Different cohorts represent fundamentally different modalities (telephonic survey vs. EHR lab draw vs. acute hospital triage). Concatenating them would cause catastrophic feature distortion."),
        ("No Target Leakage", "All transformers, imputers, and scalers are fitted exclusively within training cross-validation folds."),
        ("Subsample Recognition", "Recognizing that BRFSS 50-50 is derived from BRFSS full ensures it is never mistakenly used as an independent external validation set.")
    ]
    for r_title, r_desc in rules:
        p_rt = ttf3_r.add_paragraph()
        p_rt.text = f"✔ {r_title}"
        p_rt.font.size = Pt(11.5)
        p_rt.font.bold = True
        p_rt.font.color.rgb = C_PRIMARY
        p_rt.space_after = Pt(2)
        
        p_rd = ttf3_r.add_paragraph()
        p_rd.text = r_desc
        p_rd.font.size = Pt(10)
        p_rd.font.color.rgb = C_SLATE
        p_rd.space_after = Pt(10)

    # =========================================================================
    # SLIDE 4: CRYPTOGRAPHIC AUDIT & DUPLICATE FILE VERIFICATION
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, C_LIGHT_BG)
    add_header(slide4, "Cryptographic Data Integrity Audit & Cohort Deduplication", "Data Hygiene & Forensic Audit", 4)

    # Left: 3 Audit Cards
    audit_findings = [
        ("1. Exact Duplicate File Detection", 
         "MD5 Checksum: cb243b99d81d96e9aeb08944ce9ac066\n"
         "diabetes_prediction_dataset.csv and diabetes_prediction_dataset(1).csv were confirmed to be 100% byte-for-byte identical duplicates.\n"
         "Action: Excluded the duplicate file to prevent 100,000 double-counted rows and false sample size inflation.", C_SUCCESS),
        ("2. CDC BRFSS Cohort Identity",
         "diabetes_binary_health_indicators_BRFSS2015.csv and diabetes_012_health_indicators_BRFSS2015.csv share the exact same 253,680 respondents.\n"
         "Critical Finding: The binary dataset merged 4,631 prediabetic individuals into class 0 (healthy).", C_PRIMARY),
        ("3. 50-50 Balanced Subsample Overlap",
         "diabetes_binary_5050split (70,692 rows) is an undersampled subset containing 100% of diabetic respondents (35,346) and 35,346 balanced controls.\n"
         "Integrity Rule: Must NOT be treated as an external test set for BRFSS models.", C_WARNING)
    ]

    for i, (atitle, adesc, acol) in enumerate(audit_findings):
        c_top = Inches(1.5 + i * 1.8)
        add_card(slide4, Inches(0.8), c_top, Inches(6.8), Inches(1.65))
        
        # Left edge bar
        bar = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), c_top, Inches(0.08), Inches(1.65))
        bar.fill.solid()
        bar.fill.fore_color.rgb = acol
        bar.line.fill.background()

        abox = slide4.shapes.add_textbox(Inches(1.05), c_top + Inches(0.12), Inches(6.4), Inches(1.4))
        atf = abox.text_frame
        atf.word_wrap = True
        ap0 = atf.paragraphs[0]
        ap0.text = atitle
        ap0.font.size = Pt(13)
        ap0.font.bold = True
        ap0.font.color.rgb = C_NAVY
        ap0.space_after = Pt(4)

        ap1 = atf.add_paragraph()
        ap1.text = adesc
        ap1.font.size = Pt(10)
        ap1.font.color.rgb = C_SLATE

    # Right: Embedded Distribution Figure
    add_card(slide4, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.3))
    tbox4_fig = slide4.shapes.add_textbox(Inches(8.05), Inches(1.65), Inches(4.2), Inches(0.4))
    ttf4_f = tbox4_fig.text_frame
    p_fig = ttf4_f.paragraphs[0]
    p_fig.text = "Target Distribution: Clinical EHR Cohort"
    p_fig.font.size = Pt(13)
    p_fig.font.bold = True
    p_fig.font.color.rgb = C_NAVY

    fig_path = FIGURES_DIR / "clinical_target_distribution.png"
    if fig_path.exists():
        slide4.shapes.add_picture(str(fig_path), Inches(8.05), Inches(2.2), width=Inches(4.2))

    # =========================================================================
    # SLIDE 5: EXPLORATORY DATA ANALYSIS & STATISTICAL SIGNIFICANCE
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, C_LIGHT_BG)
    add_header(slide5, "Exploratory Data Analysis & Statistical Significance Testing", "Exploratory Data Analysis", 5)

    # Left: Statistical Findings Card
    add_card(slide5, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.3))
    tbox5_l = slide5.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.5), Inches(4.9))
    ttf5_l = tbox5_l.text_frame
    ttf5_l.word_wrap = True

    p5_0 = ttf5_l.paragraphs[0]
    p5_0.text = "Non-Parametric Statistical Hypothesis Profiling"
    p5_0.font.size = Pt(14)
    p5_0.font.bold = True
    p5_0.font.color.rgb = C_NAVY
    p5_0.space_after = Pt(10)

    stat_bullets = [
        ("Clinical Biomarkers (100k EHR):", [
            "Mann-Whitney U Test: Diabetic HbA1c median is 6.6% vs. 5.8% in controls (p < 1e-15).",
            "Fasting Glucose: Median 160.0 mg/dL vs. 130.0 mg/dL (p < 1e-15).",
            "Age Association: Median age is 62.0 yrs in diabetics vs. 40.0 yrs in controls.",
            "Smoking: Former smokers exhibit highest prevalence (17.0%), driven by age interaction."
        ]),
        ("Lifestyle Habits (253k BRFSS):", [
            "General Health Perception (GenHlth): Strongest categorical association (Cramer's V = 0.299). Poor health = 38.4% prevalence vs. 2.1% in excellent.",
            "High Blood Pressure (HighBP): Cramer's V = 0.263.",
            "Physical Inactivity: Increases prevalence from 11.0% to 23.3%."
        ])
    ]

    for title, b_list in stat_bullets:
        pt = ttf5_l.add_paragraph()
        pt.text = title
        pt.font.size = Pt(11.5)
        pt.font.bold = True
        pt.font.color.rgb = C_PRIMARY
        pt.space_after = Pt(3)
        for b in b_list:
            pb = ttf5_l.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = C_SLATE
            pb.space_after = Pt(4)

    # Right: Embedded Biomarkers Boxplot
    add_card(slide5, Inches(7.0), Inches(1.5), Inches(5.533), Inches(5.3))
    tbox5_r = slide5.shapes.add_textbox(Inches(7.25), Inches(1.65), Inches(5.0), Inches(0.4))
    ttf5_r = tbox5_r.text_frame
    p_fig5 = ttf5_r.paragraphs[0]
    p_fig5.text = "Glycemic Biomarker Distributions by Diabetes Status"
    p_fig5.font.size = Pt(13)
    p_fig5.font.bold = True
    p_fig5.font.color.rgb = C_NAVY

    fig_path5 = FIGURES_DIR / "clinical_biomarkers_boxplot.png"
    if fig_path5.exists():
        slide5.shapes.add_picture(str(fig_path5), Inches(7.2), Inches(2.1), width=Inches(5.1))

    # =========================================================================
    # SLIDE 6: LEAKAGE-FREE PIPELINE & PREPROCESSING
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, C_LIGHT_BG)
    add_header(slide6, "Leakage-Free Machine Learning Pipeline Architecture", "Methodology & Architecture", 6)

    # 4 Architecture Flow Cards
    steps = [
        ("Step 1: Data Isolation", [
            "Strict Modality Partitioning",
            "Survey vs Clinical vs Symptom cohorts isolated into separate pipelines.",
            "Prevent cross-cohort contamination."
        ], C_PRIMARY),
        ("Step 2: Fold-Level Transforms", [
            "Scikit-learn ColumnTransformer",
            "StandardScaler for continuous variables.",
            "OneHotEncoder / OrdinalEncoder for categoricals.",
            "Fitted strictly inside training CV folds."
        ], C_ACCENT),
        ("Step 3: Imbalance Handling", [
            "Cost-Sensitive Loss Formulations",
            "Balanced class weights: w_j = N / (k * N_j).",
            "Calibrated decision threshold tuning to boost sensitivity without sacrificing precision."
        ], C_WARNING),
        ("Step 4: Inference Engine", [
            "Calibrated Probability Engine",
            "Platt Sigmoid / Isotonic probability calibration.",
            "95% Wilson confidence intervals.",
            "SHAP TreeExplainer feature attribution."
        ], C_SUCCESS)
    ]

    for i, (stitle, sbullets, scol) in enumerate(steps):
        c_left = Inches(0.8 + i * 2.95)
        c_width = Inches(2.8)
        add_card(slide6, c_left, Inches(1.5), c_width, Inches(5.3))
        
        c_bar = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.5), c_width, Inches(0.1))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = scol
        c_bar.line.fill.background()

        sbox = slide6.shapes.add_textbox(c_left + Inches(0.15), Inches(1.75), c_width - Inches(0.3), Inches(4.8))
        stf = sbox.text_frame
        stf.word_wrap = True

        sp0 = stf.paragraphs[0]
        sp0.text = stitle
        sp0.font.size = Pt(13)
        sp0.font.bold = True
        sp0.font.color.rgb = C_NAVY
        sp0.space_after = Pt(10)

        for b in sbullets:
            bp = stf.add_paragraph()
            bp.text = f"• {b}"
            bp.font.size = Pt(10.5)
            bp.font.color.rgb = C_SLATE
            bp.space_after = Pt(8)

    # =========================================================================
    # SLIDE 7: MULTI-ALGORITHM BENCHMARK SPECTRUM
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, C_LIGHT_BG)
    add_header(slide7, "Model Spectrum: 9 Machine Learning Architectures Evaluated", "Algorithms & Experimental Setup", 7)

    # Left: Algorithm Categories Card
    add_card(slide7, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.3))
    tbox7_l = slide7.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.3), Inches(4.9))
    ttf7_l = tbox7_l.text_frame
    ttf7_l.word_wrap = True

    p7_0 = ttf7_l.paragraphs[0]
    p7_0.text = "Candidate Model Architectures & Optimization"
    p7_0.font.size = Pt(15)
    p7_0.font.bold = True
    p7_0.font.color.rgb = C_NAVY
    p7_0.space_after = Pt(8)

    algos = [
        ("Parametric Baseline:", "Logistic Regression (L2 regularization, balanced weights) — provides transparent clinical linear odds benchmark."),
        ("Tree Ensembles:", "Decision Trees (max_depth=6), Random Forest (100 trees, bootstrap sampling), Extra Trees (extremely randomized splits)."),
        ("Gradient Boosting:", "HistGradientBoosting (binning-based), LightGBM (leaf-wise growth, GBDT), XGBoost (exact greedy splits)."),
        ("Instance & Kernel:", "K-Nearest Neighbors (k=5, Euclidean distance), Support Vector Machine (RBF kernel, scaled gamma).")
    ]
    for cat_name, cat_desc in algos:
        pt = ttf7_l.add_paragraph()
        pt.text = cat_name
        pt.font.size = Pt(11.5)
        pt.font.bold = True
        pt.font.color.rgb = C_PRIMARY
        pt.space_after = Pt(2)
        pd_ = ttf7_l.add_paragraph()
        pd_.text = cat_desc
        pd_.font.size = Pt(10)
        pd_.font.color.rgb = C_SLATE
        pd_.space_after = Pt(6)

    # Right: Multi-Metric Clinical Evaluation Protocol
    add_card(slide7, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.3))
    tbox7_r = slide7.shapes.add_textbox(Inches(7.05), Inches(1.7), Inches(5.2), Inches(4.9))
    ttf7_r = tbox7_r.text_frame
    ttf7_r.word_wrap = True

    p7_r0 = ttf7_r.paragraphs[0]
    p7_r0.text = "Comprehensive Clinical Evaluation Metrics"
    p7_r0.font.size = Pt(15)
    p7_r0.font.bold = True
    p7_r0.font.color.rgb = C_NAVY
    p7_r0.space_after = Pt(8)

    metrics = [
        ("Sensitivity (Recall):", "Critical in screening. Missing a diabetic patient (False Negative) delays crucial intervention. High sensitivity is strictly prioritized."),
        ("ROC-AUC & PR-AUC:", "Evaluates discrimination threshold-free. PR-AUC is especially vital on imbalanced cohorts (CDC BRFSS: 13.9% prevalence)."),
        ("Brier Score (Probability Calibration):", "Mean squared error between predicted probability and binary outcome. Low Brier score = highly reliable patient probability."),
        ("Specificity & Balanced Accuracy:", "Ensures healthy individuals are not overwhelmed with false alarms and unnecessary clinical referrals.")
    ]
    for m_name, m_desc in metrics:
        pt = ttf7_r.add_paragraph()
        pt.text = m_name
        pt.font.size = Pt(11.5)
        pt.font.bold = True
        pt.font.color.rgb = C_SUCCESS
        pt.space_after = Pt(2)
        pd_ = ttf7_r.add_paragraph()
        pd_.text = m_desc
        pd_.font.size = Pt(10)
        pd_.font.color.rgb = C_SLATE
        pd_.space_after = Pt(6)

    # =========================================================================
    # SLIDE 8: COHORT 1: CLINICAL & LABORATORY EHR BENCHMARK
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, C_LIGHT_BG)
    add_header(slide8, "Cohort 1 Benchmark: Clinical & Laboratory EHR (100,000 Records)", "Empirical Benchmarks: Cohort 1", 8)

    # Left: Results Table
    add_card(slide8, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))
    tbox8_l = slide8.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(6.3), Inches(0.5))
    ttf8_l = tbox8_l.text_frame
    p8_l = ttf8_l.paragraphs[0]
    p8_l.text = "Model Performance on Test Set (19,226 Patients)"
    p8_l.font.size = Pt(14)
    p8_l.font.bold = True
    p8_l.font.color.rgb = C_NAVY

    # Table
    table_shape8 = slide8.shapes.add_table(8, 6, Inches(1.0), Inches(2.3), Inches(6.4), Inches(3.2))
    tbl8 = table_shape8.table
    tbl8.columns[0].width = Inches(2.0)
    tbl8.columns[1].width = Inches(0.85)
    tbl8.columns[2].width = Inches(0.9)
    tbl8.columns[3].width = Inches(0.85)
    tbl8.columns[4].width = Inches(0.9)
    tbl8.columns[5].width = Inches(0.9)

    h8 = ["Model", "Accuracy", "Recall", "ROC-AUC", "PR-AUC", "Brier"]
    d8 = [
        ("Logistic Regression", "0.8848", "87.9%", "0.9597", "0.8121", "0.0800"),
        ("Decision Tree", "0.8258", "95.6%", "0.9668", "0.8594", "0.0727"),
        ("Random Forest", "0.8923", "91.6%", "0.9743", "0.8734", "0.0621"),
        ("Extra Trees", "0.8760", "91.8%", "0.9655", "0.8362", "0.0778"),
        ("HistGradientBoosting", "0.8997", "91.3%", "0.9771", "0.8802", "0.0605"),
        ("LightGBM (Selected)", "0.8975", "92.1%", "0.9770", "0.8802", "0.0236*"),
        ("XGBoost", "0.9720", "68.8%", "0.9767", "0.8801", "0.0235")
    ]
    for j, h in enumerate(h8):
        cell = tbl8.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        cp = cell.text_frame.paragraphs[0]
        cp.text = h
        cp.font.size = Pt(9.5)
        cp.font.bold = True
        cp.font.color.rgb = C_WHITE
    for i, row in enumerate(d8):
        for j, val in enumerate(row):
            cell = tbl8.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(238, 242, 255) if "LightGBM" in row[0] else (C_WHITE if i % 2 == 0 else C_CARD_SUBTLE)
            cp = cell.text_frame.paragraphs[0]
            cp.text = val
            cp.font.size = Pt(9)
            cp.font.bold = True if "LightGBM" in row[0] else False
            cp.font.color.rgb = C_PRIMARY if "LightGBM" in row[0] else C_SLATE

    # Highlight note below table
    h_box8 = slide8.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(6.4), Inches(1.0))
    htf8 = h_box8.text_frame
    htf8.word_wrap = True
    hp8 = htf8.paragraphs[0]
    hp8.text = "*Selected Architecture: LightGBM (Post-Calibration Brier 0.0236). Detects 92.1% of all diabetes cases while maintaining 94.4% specificity. False negative rate dropped to only 7.9%."
    hp8.font.size = Pt(9.5)
    hp8.font.color.rgb = C_MUTED

    # Right: Embedded Diagnostics Figure
    add_card(slide8, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.3))
    fig_path8 = FIGURES_DIR / "clinical_best_diagnostics.png"
    if fig_path8.exists():
        slide8.shapes.add_picture(str(fig_path8), Inches(7.95), Inches(1.65), width=Inches(4.45))

    # =========================================================================
    # SLIDE 9: COHORT 2: CDC BRFSS LIFESTYLE SURVEY BENCHMARK
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, C_LIGHT_BG)
    add_header(slide9, "Cohort 2 Benchmark: CDC BRFSS Lifestyle Survey (253,680 Records)", "Empirical Benchmarks: Cohort 2", 9)

    # Left: Results Table
    add_card(slide9, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))
    tbox9_l = slide9.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(6.3), Inches(0.5))
    ttf9_l = tbox9_l.text_frame
    p9_l = ttf9_l.paragraphs[0]
    p9_l.text = "Modifiable Lifestyle Model Performance (10,000 Test Set)"
    p9_l.font.size = Pt(14)
    p9_l.font.bold = True
    p9_l.font.color.rgb = C_NAVY

    table_shape9 = slide9.shapes.add_table(8, 6, Inches(1.0), Inches(2.3), Inches(6.4), Inches(3.2))
    tbl9 = table_shape9.table
    tbl9.columns[0].width = Inches(2.0)
    tbl9.columns[1].width = Inches(0.85)
    tbl9.columns[2].width = Inches(0.9)
    tbl9.columns[3].width = Inches(0.85)
    tbl9.columns[4].width = Inches(0.9)
    tbl9.columns[5].width = Inches(0.9)

    h9 = ["Model", "Accuracy", "Recall", "ROC-AUC", "PR-AUC", "Brier"]
    d9 = [
        ("Logistic Regression", "0.7147", "73.0%", "0.7979", "0.3903", "0.1847"),
        ("Decision Tree", "0.7126", "71.8%", "0.7869", "0.3927", "0.1892"),
        ("Random Forest", "0.7474", "68.5%", "0.7997", "0.4009", "0.1663"),
        ("Extra Trees", "0.7051", "72.2%", "0.7882", "0.3865", "0.1823"),
        ("HistGradientBoosting", "0.7151", "74.2%", "0.8034", "0.4057", "0.1796"),
        ("LightGBM (Balanced)", "0.7168", "74.5%", "0.8046", "0.4070", "0.1080*"),
        ("XGBoost (Unweighted)", "0.8496", "14.5%", "0.8044", "0.4035", "0.1083")
    ]
    for j, h in enumerate(h9):
        cell = tbl9.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        cp = cell.text_frame.paragraphs[0]
        cp.text = h
        cp.font.size = Pt(9.5)
        cp.font.bold = True
        cp.font.color.rgb = C_WHITE
    for i, row in enumerate(d9):
        for j, val in enumerate(row):
            cell = tbl9.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(238, 242, 255) if "LightGBM" in row[0] else (C_WHITE if i % 2 == 0 else C_CARD_SUBTLE)
            cp = cell.text_frame.paragraphs[0]
            cp.text = val
            cp.font.size = Pt(9)
            cp.font.bold = True if "LightGBM" in row[0] else False
            cp.font.color.rgb = C_PRIMARY if "LightGBM" in row[0] else C_SLATE

    h_box9 = slide9.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(6.4), Inches(1.0))
    htf9 = h_box9.text_frame
    htf9.word_wrap = True
    hp9 = htf9.paragraphs[0]
    hp9.text = "Key Finding: Modifiable lifestyle indicators alone detect ~75% of diabetic patients with ZERO invasive testing or clinical laboratory infrastructure. Unweighted XGBoost failed (14.5% recall) due to natural 13.9% class imbalance."
    hp9.font.size = Pt(9.5)
    hp9.font.color.rgb = C_MUTED

    # Right: Embedded Diagnostics Figure
    add_card(slide9, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.3))
    fig_path9 = FIGURES_DIR / "brfss_lifestyle_best_diagnostics.png"
    if fig_path9.exists():
        slide9.shapes.add_picture(str(fig_path9), Inches(7.95), Inches(1.65), width=Inches(4.45))

    # =========================================================================
    # SLIDE 10: COHORT 3: EARLY-STAGE ACUTE SYMPTOMS BENCHMARK
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, C_LIGHT_BG)
    add_header(slide10, "Cohort 3 Benchmark: Early-Stage Acute Symptoms (520 Records)", "Empirical Benchmarks: Cohort 3", 10)

    # Left: Results Table
    add_card(slide10, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))
    tbox10_l = slide10.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(6.3), Inches(0.5))
    ttf10_l = tbox10_l.text_frame
    p10_l = ttf10_l.paragraphs[0]
    p10_l.text = "Acute Symptom Screening Performance (104 Patients)"
    p10_l.font.size = Pt(14)
    p10_l.font.bold = True
    p10_l.font.color.rgb = C_NAVY

    table_shape10 = slide10.shapes.add_table(8, 6, Inches(1.0), Inches(2.3), Inches(6.4), Inches(3.2))
    tbl10 = table_shape10.table
    tbl10.columns[0].width = Inches(2.0)
    tbl10.columns[1].width = Inches(0.85)
    tbl10.columns[2].width = Inches(0.9)
    tbl10.columns[3].width = Inches(0.85)
    tbl10.columns[4].width = Inches(0.9)
    tbl10.columns[5].width = Inches(0.9)

    h10 = ["Model", "Accuracy", "Recall", "ROC-AUC", "PR-AUC", "Brier"]
    d10 = [
        ("Logistic Regression", "0.9327", "90.6%", "0.9918", "0.9951", "0.0483"),
        ("Decision Tree", "0.9712", "95.3%", "0.9879", "0.9946", "0.0271"),
        ("Random Forest", "0.9712", "96.9%", "0.9992", "0.9995", "0.0147"),
        ("Extra Trees (Selected)", "0.9904", "100.0%", "0.9996", "0.9998", "0.0098*"),
        ("HistGradientBoosting", "0.9808", "96.9%", "1.0000", "1.0000", "0.0182"),
        ("LightGBM", "0.9808", "96.9%", "1.0000", "1.0000", "0.0144"),
        ("Support Vector Machine", "0.9712", "95.3%", "0.9996", "0.9998", "0.0099")
    ]
    for j, h in enumerate(h10):
        cell = tbl10.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        cp = cell.text_frame.paragraphs[0]
        cp.text = h
        cp.font.size = Pt(9.5)
        cp.font.bold = True
        cp.font.color.rgb = C_WHITE
    for i, row in enumerate(d10):
        for j, val in enumerate(row):
            cell = tbl10.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(238, 242, 255) if "Extra Trees" in row[0] else (C_WHITE if i % 2 == 0 else C_CARD_SUBTLE)
            cp = cell.text_frame.paragraphs[0]
            cp.text = val
            cp.font.size = Pt(9)
            cp.font.bold = True if "Extra Trees" in row[0] else False
            cp.font.color.rgb = C_PRIMARY if "Extra Trees" in row[0] else C_SLATE

    h_box10 = slide10.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(6.4), Inches(1.0))
    htf10 = h_box10.text_frame
    htf10.word_wrap = True
    hp10 = htf10.paragraphs[0]
    hp10.text = "Selected Model: Extra Trees Classifier (100% Sensitivity, 0.9996 ROC-AUC, 0.0098 Brier). The osmotic diuresis triad (Polyuria, Polydipsia, sudden weight loss) accounts for >70% of feature attribution."
    hp10.font.size = Pt(9.5)
    hp10.font.color.rgb = C_MUTED

    # Right: Embedded Diagnostics Figure
    add_card(slide10, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.3))
    fig_path10 = FIGURES_DIR / "early_symptoms_best_diagnostics.png"
    if fig_path10.exists():
        slide10.shapes.add_picture(str(fig_path10), Inches(7.95), Inches(1.65), width=Inches(4.45))

    # =========================================================================
    # SLIDE 11: SCIENTIFIC ABLATION STUDY
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, C_LIGHT_BG)
    add_header(slide11, "Scientific Ablation: Clinical Biomarkers vs. Lifestyle Habits", "Controlled Ablation Experiment", 11)

    # Top: Side by Side Comparison Card
    add_card(slide11, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))
    tbox11_l = slide11.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(6.3), Inches(4.9))
    ttf11_l = tbox11_l.text_frame
    ttf11_l.word_wrap = True

    p11_0 = ttf11_l.paragraphs[0]
    p11_0.text = "Controlled Experiment on Identical 19,226 Patients"
    p11_0.font.size = Pt(15)
    p11_0.font.bold = True
    p11_0.font.color.rgb = C_NAVY
    p11_0.space_after = Pt(10)

    # 2 Comparison Blocks
    c1 = [
        ("Mode A: Non-Invasive Lifestyle Only", 
         "Features: Age, Gender, BMI, Smoking History, Hypertension, Heart Disease.\n"
         "• Accuracy: 71.74% | Balanced Accuracy: 75.02%\n"
         "• Recall (Sensitivity): 79.01% (Misses 21.0% of cases)\n"
         "• ROC-AUC: 0.8247 | PR-AUC: 0.3095\n"
         "• Brier Score: 0.1751", C_MUTED),
        ("Mode B: Full Clinical Model (+HbA1c & Glucose)",
         "Features: Above + HbA1c Level + Fasting Blood Glucose Level.\n"
         "• Accuracy: 89.95% | Balanced Accuracy: 90.63%\n"
         "• Recall (Sensitivity): 91.45% (Misses only 8.5% of cases)\n"
         "• ROC-AUC: 0.9771 | PR-AUC: 0.8806\n"
         "• Brier Score: 0.0606", C_SUCCESS)
    ]
    for m_head, m_body, col in c1:
        pt = ttf11_l.add_paragraph()
        pt.text = m_head
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = col
        pt.space_after = Pt(2)
        pb = ttf11_l.add_paragraph()
        pb.text = m_body
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = C_SLATE
        pb.space_after = Pt(8)

    # Quantified Diagnostic Gain Callout
    gain_p = ttf11_l.add_paragraph()
    gain_p.text = "DIAGNOSTIC VALUE-ADD OF CLINICAL BIOMARKERS:"
    gain_p.font.size = Pt(11)
    gain_p.font.bold = True
    gain_p.font.color.rgb = C_PRIMARY
    gain_p.space_after = Pt(2)

    gain_desc = ttf11_l.add_paragraph()
    gain_desc.text = "+15.2% Absolute Gain in ROC-AUC (0.825 -> 0.977)\n+12.4% Absolute Gain in Recall Sensitivity (79.0% -> 91.5%)\n-65.4% Relative Error Reduction in Brier Score"
    gain_desc.font.size = Pt(10)
    gain_desc.font.bold = True
    gain_desc.font.color.rgb = C_NAVY

    # Right: Embedded Scatter / Figure
    add_card(slide11, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.3))
    fig_path11 = FIGURES_DIR / "clinical_hba1c_glucose_scatter.png"
    if fig_path11.exists():
        slide11.shapes.add_picture(str(fig_path11), Inches(7.95), Inches(1.65), width=Inches(4.45))

    # =========================================================================
    # SLIDE 12: CLASS IMBALANCE & PREDIABETES DETECTION CHALLENGE
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, C_LIGHT_BG)
    add_header(slide12, "Class Imbalance Dynamics & The Prediabetes Detection Barrier", "Specialized Research Findings", 12)

    # Left: Imbalance Breakdown Card
    add_card(slide12, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.3))
    tbox12_l = slide12.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.3), Inches(4.9))
    ttf12_l = tbox12_l.text_frame
    ttf12_l.word_wrap = True

    p12_0 = ttf12_l.paragraphs[0]
    p12_0.text = "1. Class Imbalance in Population Surveys"
    p12_0.font.size = Pt(14)
    p12_0.font.bold = True
    p12_0.font.color.rgb = C_NAVY
    p12_0.space_after = Pt(6)

    imb_desc = [
        "Natural Prevalence Distortion: CDC BRFSS has 13.9% diabetes prevalence (86.1% healthy).",
        "The XGBoost Collapse: Default unweighted objective converged to 84.96% accuracy by predicting majority class, yielding an abysmal 14.5% Sensitivity and 85.5% False Negative Rate!",
        "Cost-Sensitive Recovery: Applying balanced class weights restored Sensitivity to 74.5% with 72.8% balanced accuracy."
    ]
    for b in imb_desc:
        bp = ttf12_l.add_paragraph()
        bp.text = f"• {b}"
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_SLATE
        bp.space_after = Pt(4)

    p12_1 = ttf12_l.add_paragraph()
    p12_1.text = "2. The Prediabetes Distinguishability Challenge"
    p12_1.font.size = Pt(14)
    p12_1.font.bold = True
    p12_1.font.color.rgb = C_DANGER
    p12_1.space_before = Pt(8)
    p12_1.space_after = Pt(6)

    pred_desc = [
        "In 3-Class CDC BRFSS (Diabetes_012), prediabetes accounts for only 1.8% of the population.",
        "Prediabetes was virtually indistinguishable from healthy controls based on lifestyle questionnaires alone (Macro F1 ~0.42).",
        "Clinical Lesson: Prediabetic glycemic dysregulation is asymptomatic. Non-invasive questionnaires alone cannot reliably detect early prediabetes without laboratory blood draws."
    ]
    for b in pred_desc:
        bp = ttf12_l.add_paragraph()
        bp.text = f"• {b}"
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_SLATE
        bp.space_after = Pt(4)

    # Right: Embedded Balanced Diagnostics Figure
    add_card(slide12, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.3))
    fig_path12 = FIGURES_DIR / "brfss_5050_balanced_best_diagnostics.png"
    if fig_path12.exists():
        slide12.shapes.add_picture(str(fig_path12), Inches(7.05), Inches(1.65), width=Inches(5.2))

    # =========================================================================
    # SLIDE 13: EXPLAINABLE AI & SHAP ATTRIBUTION
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, C_LIGHT_BG)
    add_header(slide13, "Explainable AI (XAI): SHAP Game-Theoretic Feature Attribution", "Explainability & Interpretability", 13)

    # Left: SHAP Findings
    add_card(slide13, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.3))
    tbox13_l = slide13.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.3), Inches(4.9))
    ttf13_l = tbox13_l.text_frame
    ttf13_l.word_wrap = True

    p13_0 = ttf13_l.paragraphs[0]
    p13_0.text = "TreeExplainer SHAP Attribution Across Modalities"
    p13_0.font.size = Pt(14)
    p13_0.font.bold = True
    p13_0.font.color.rgb = C_NAVY
    p13_0.space_after = Pt(8)

    shap_sections = [
        ("Clinical Biomarkers Cohort:", [
            "HbA1c_level is the #1 global driver by an overwhelming margin.",
            "SHAP shows steep non-linear risk escalation above HbA1c 6.5%.",
            "blood_glucose_level is secondary driver, followed by Age and BMI."
        ]),
        ("CDC BRFSS Lifestyle Survey:", [
            "GenHlth (General Health Perception) is the strongest non-invasive predictor.",
            "HighBP (Hypertension) and BMI represent major secondary contributors.",
            "PhysActivity (sedentary lifestyle) demonstrates consistent positive risk attribution."
        ]),
        ("Clinical Safety Disclaimer:", [
            "SHAP attributions represent statistical associations within retrospective cohorts and do NOT establish proven medical causation."
        ])
    ]
    for stitle, slist in shap_sections:
        pt = ttf13_l.add_paragraph()
        pt.text = stitle
        pt.font.size = Pt(11.5)
        pt.font.bold = True
        pt.font.color.rgb = C_PRIMARY
        pt.space_after = Pt(2)
        for b in slist:
            pb = ttf13_l.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = C_SLATE
            pb.space_after = Pt(4)

    # Right: Embedded SHAP Summary Figure
    add_card(slide13, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.3))
    fig_path13 = FIGURES_DIR / "clinical_shap_summary.png"
    if fig_path13.exists():
        slide13.shapes.add_picture(str(fig_path13), Inches(7.05), Inches(1.65), width=Inches(5.2))

    # =========================================================================
    # SLIDE 14: INTERACTIVE WEB DASHBOARD & CLINICAL DECISION SUPPORT
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, C_LIGHT_BG)
    add_header(slide14, "Interactive Web Dashboard & Clinical Decision Support System", "Software Engineering & Deployment", 14)

    # 4 Portal Module Cards
    modules = [
        ("1. Multi-Cohort Explorer", [
            "Interactive dataset viewer across 6 cohorts.",
            "Feature distribution plots & correlation matrices.",
            "Cryptographic MD5 hash verification panel."
        ], C_PRIMARY),
        ("2. Multi-Mode Risk Portal", [
            "Live Patient Risk Assessment.",
            "Mode 1: Clinical laboratory input.",
            "Mode 2: BRFSS Lifestyle survey input.",
            "Mode 3: Acute symptom triage.",
            "Outputs calibrated probabilities & 95% CIs."
        ], C_ACCENT),
        ("3. Model Benchmarks", [
            "Interactive ROC & Precision-Recall curves.",
            "Confusion matrices with cutoff threshold sliders.",
            "Calibration curve reliability visualizer."
        ], C_WARNING),
        ("4. Explainable AI & Monograph", [
            "Patient-level local waterfall attribution.",
            "Global beeswarm & feature importance.",
            "Direct PDF & CSV research report downloads."
        ], C_SUCCESS)
    ]

    for i, (mtitle, mbullets, mcol) in enumerate(modules):
        c_left = Inches(0.8 + i * 2.95)
        c_width = Inches(2.8)
        add_card(slide14, c_left, Inches(1.5), c_width, Inches(5.3))
        
        c_bar = slide14.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.5), c_width, Inches(0.1))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = mcol
        c_bar.line.fill.background()

        mbox = slide14.shapes.add_textbox(c_left + Inches(0.15), Inches(1.75), c_width - Inches(0.3), Inches(4.8))
        mtf = mbox.text_frame
        mtf.word_wrap = True

        mp0 = mtf.paragraphs[0]
        mp0.text = mtitle
        mp0.font.size = Pt(13)
        mp0.font.bold = True
        mp0.font.color.rgb = C_NAVY
        mp0.space_after = Pt(10)

        for b in mbullets:
            bp = mtf.add_paragraph()
            bp.text = f"• {b}"
            bp.font.size = Pt(10.5)
            bp.font.color.rgb = C_SLATE
            bp.space_after = Pt(8)

    # =========================================================================
    # SLIDE 15: CLINICAL GOVERNANCE, LIMITATIONS & FUTURE ROADMAP
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, C_NAVY)

    # Header in White/Cyan
    top_bar15 = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar15.fill.solid()
    top_bar15.fill.fore_color.rgb = C_PRIMARY
    top_bar15.line.fill.background()

    hdr15 = slide15.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.9))
    htf15 = hdr15.text_frame
    hp15_0 = htf15.paragraphs[0]
    hp15_0.text = "CLINICAL GOVERNANCE & FUTURE ROADMAP"
    hp15_0.font.size = Pt(10)
    hp15_0.font.bold = True
    hp15_0.font.color.rgb = C_ACCENT
    hp15_1 = htf15.add_paragraph()
    hp15_1.text = "Clinical Governance, Scientific Limitations & Future Research"
    hp15_1.font.size = Pt(22)
    hp15_1.font.bold = True
    hp15_1.font.color.rgb = C_WHITE

    # 3 Dark Cards
    cols15 = [
        ("1. Critical Medical Limitations", [
            "Retrospective vs. Future Risk: Models predict retrospective classification concordance, NOT prospective future disease incidence.",
            "Cross-Sectional Observational Data: Lacks multi-year longitudinal follow-up.",
            "Self-Report Bias: CDC BRFSS relies on telephonic surveys, subject to recall bias."
        ], C_WARNING),
        ("2. Ethical Framework & Privacy", [
            "Research Prototype Only: NOT a certified medical diagnostic device.",
            "Zero Automated Diagnosis: Serves solely as an educational risk stratification aid.",
            "Data Privacy: Zero patient information transmitted to cloud or external APIs; all computation executed locally."
        ], C_PRIMARY),
        ("3. Future Research Directions", [
            "Prospective Longitudinal Cohort Tracking: Evaluating 5-year incident risk.",
            "Continuous Glucose Monitoring (CGM): Integration of continuous glycemic time-series.",
            "Edge & Mobile Health Deployment: Offline mobile screening apps for low-resource settings."
        ], C_SUCCESS)
    ]

    for i, (ctitle, cbullets, ccol) in enumerate(cols15):
        c_left = Inches(0.8 + i * 4.0)
        c_width = Inches(3.733)
        add_card(slide15, c_left, Inches(1.5), c_width, Inches(5.3), bg_color=C_SLATE, border_color=RGBColor(51, 65, 85))
        
        c_bar = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.5), c_width, Inches(0.1))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = ccol
        c_bar.line.fill.background()

        cbox = slide15.shapes.add_textbox(c_left + Inches(0.2), Inches(1.75), c_width - Inches(0.4), Inches(4.8))
        ctf = cbox.text_frame
        ctf.word_wrap = True

        cp0 = ctf.paragraphs[0]
        cp0.text = ctitle
        cp0.font.size = Pt(14)
        cp0.font.bold = True
        cp0.font.color.rgb = C_WHITE
        cp0.space_after = Pt(10)

        for b in cbullets:
            bp = ctf.add_paragraph()
            bp.text = f"• {b}"
            bp.font.size = Pt(11)
            bp.font.color.rgb = RGBColor(203, 213, 225)
            bp.space_after = Pt(10)

    # Save presentation
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    out_file1 = OUTPUT_DIR / "diabetes_risk_prediction_15_slides.pptx"
    out_file2 = REPORTS_DIR / "diabetes_risk_prediction_15_slides.pptx"
    
    prs.save(str(out_file1))
    prs.save(str(out_file2))
    print(f"Successfully generated 15-slide PowerPoint Presentation:")
    print(f"  -> {out_file1}")
    print(f"  -> {out_file2}")


if __name__ == "__main__":
    build_presentation()
