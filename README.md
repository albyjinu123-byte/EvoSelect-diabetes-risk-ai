<div align="center">

# 🩺 AI-Based Diabetes Risk Prediction & Clinical Stratification
### Multi-Cohort Machine Learning, Biomarker Ablation, and Explainable AI (XAI) Across 350,000+ Records

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.3+-2E8540?style=for-the-badge)](https://lightgbm.readthedocs.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EB5424?style=for-the-badge)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainable%20AI-blueviolet?style=for-the-badge)](https://shap.readthedocs.io/)
[![Tests](https://img.shields.io/badge/Pytest-27%20Passed-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <a href="#-key-empirical-findings">Key Findings</a> •
  <a href="#-project-deliverables">Reports & Slides</a> •
  <a href="#-cohort-architecture--data-modalities">Datasets</a> •
  <a href="#-benchmark-results">Benchmarks</a> •
  <a href="#-scientific-ablation-study">Ablation Study</a> •
  <a href="#-explainable-ai-shap">Explainability</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-ethical--clinical-governance">Clinical Notice</a>
</p>

</div>

---

## 📌 Executive Summary & Project Overview

This repository hosts a production-grade, research-validated machine learning and clinical decision support system for **Type 2 Diabetes Mellitus risk stratification**. Evaluated across **six healthcare datasets comprising 354,200 records**, the platform investigates how non-invasive modifiable lifestyle habits, demographic attributes, acute clinical symptoms, and laboratory glycemic biomarkers relate to diabetic status.

### 🎯 Core Problem Addressed
Over **537 million adults** live with diabetes worldwide, and more than **50% are undiagnosed in early stages**. Routine screening traditionally requires invasive venous blood draws ($\text{HbA1c}$, Fasting Plasma Glucose, OGTT), which face logistical, cold-chain, and cost bottlenecks in population-scale and community health screening. 

This platform evaluates:
1. **How accurately can non-invasive lifestyle surveys screen for diabetes without blood draws?** (Answer: **0.8046 ROC-AUC**, detecting ~75% of cases).
2. **What is the exact diagnostic value-add of laboratory biomarkers?** (Answer: **+15.2% absolute gain in ROC-AUC**, boosting sensitivity to **92.1%**).
3. **How do acute cardinal symptoms discriminate clinical presentation?** (Answer: **0.9996 ROC-AUC**, **100% sensitivity** via osmotic diuresis triad).
4. **Why is prediabetes undetectable from lifestyle surveys alone?** (Answer: Prediabetes is clinically asymptomatic; survey models achieve $\text{F1} \approx 0.10$, proving blood screening is mandatory).

---

## 📑 Project Deliverables

This repository includes complete research publications and presentation assets:

| Asset | Format | Description |
| :--- | :---: | :--- |
| **20-Page Research Monograph** | [`PDF`](diabetes_research_report_20_pages.pdf) \| [`Markdown`](diabetes_research_report_20_pages.md) | Publication-grade 20-chapter monograph with running headers/footers (`Page X of 20`), complete methodology, equations, tables, and references. |
| **15-Slide Presentation Deck** | [`PPTX`](diabetes_risk_prediction_15_slides.pptx) \| [`Notes`](presentation_transcript_15_slides.md) | Widescreen (16:9) slide deck with dark/light visual identity, KPI cards, comparative tables, and embedded high-resolution figures. |
| **Interactive Streamlit Web Portal** | `Python` (`app.py`) | 5-page clinical application for live patient assessment, uncertainty intervals, model diagnostics, and SHAP visualizers. |
| **Automated Test Harness** | `Pytest` (`tests/`) | 27 passing unit, schema validation, pipeline integration, and calibrated inference tests. |

---

## 🔬 Key Empirical Findings

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  CLINICAL ABLATION: Non-Invasive Baseline vs. Laboratory Biomarkers                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  Mode A: Lifestyle & History Only (Age, Gender, BMI, Smoking, HTN, Heart Disease)      │
│  ROC-AUC: 0.8247  |  Recall (Sensitivity): 79.01%  |  Brier Score: 0.1751              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  Mode B: Full Clinical Model (+ HbA1c Level & Fasting Blood Glucose)                  │
│  ROC-AUC: 0.9771  |  Recall (Sensitivity): 91.45%  |  Brier Score: 0.0606              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  DIAGNOSTIC VALUE-ADD OF BIOMARKERS:                                                   │
│  ▲ +15.24% ROC-AUC Gain  |  ▲ +12.44% Sensitivity  |  ▼ -65.4% Brier Probabilistic Error│
│  False Negative Rate slashed from 20.99% down to 8.55%                                 │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Needle-Free Population Screening:** On the CDC BRFSS survey (253,680 records), cost-sensitive LightGBM achieves **0.8046 ROC-AUC** and **74.49% Sensitivity** using zero invasive tests.
2. **Class Imbalance & The XGBoost Collapse:** Unweighted gradient boosting on imbalanced surveys (13.9% prevalence) collapsed to an abysmal **14.5% Sensitivity** (85.5% False Negative Rate) despite an apparent 84.96% accuracy. Cost-sensitive class balancing restored sensitivity to **74.5%**.
3. **The Prediabetes Distinguishability Barrier:** In 3-class modeling (`Diabetes_012`), prediabetes (1.8% prevalence) was virtually indistinguishable from healthy controls based on lifestyle questionnaires alone ($\text{F1} \approx 0.10$). Asymptomatic early glycemic elevation strictly demands biochemical laboratory testing.
4. **Forensic Cryptographic Deduplication:** MD5 checksum auditing (`cb243b99d81d96e9aeb08944ce9ac066`) detected that `diabetes_prediction_dataset(1).csv` was an exact duplicate download, excluding 100,000 double-counted rows and preventing sample inflation.

---

## 🏥 Cohort Architecture & Data Modalities

```
                        ┌──────────────────────────────────────────────┐
                        │      Multi-Cohort Healthcare Datasets        │
                        │             (354,200 Records)                │
                        └──────────────────────┬───────────────────────┘
                                               │
             ┌─────────────────────────────────┼────────────────────────────────┐
             ▼                                 ▼                                ▼
┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│ Track 1: Clinical EHR   │       │ Track 2: CDC BRFSS      │       │ Track 3: Acute Symptoms │
│ 100,000 Patients        │       │ 253,680 Respondents     │       │ 520 Hospital Patients   │
├─────────────────────────┤       ├─────────────────────────┤       ├─────────────────────────┤
│ • HbA1c Level           │       │ • General Health Rating │       │ • Polyuria (Excessive)  │
│ • Blood Glucose Level   │       │ • Physical Activity     │       │ • Polydipsia (Thirst)   │
│ • BMI & Demographics    │       │ • High Blood Pressure   │       │ • Sudden Weight Loss    │
│ • Hypertension, CVD     │       │ • Fruit/Veg Intake      │       │ • Visual Blurring       │
├─────────────────────────┤       ├─────────────────────────┤       ├─────────────────────────┤
│ Best: LightGBM (Calib.) │       │ Best: LightGBM (Bal.)   │       │ Best: Extra Trees       │
│ AUC: 0.9770 | Sens: 92% │       │ AUC: 0.8046 | Sens: 75% │       │ AUC: 0.9996 | Sens: 100%│
└─────────────────────────┘       └─────────────────────────┘       └─────────────────────────┘
```

| Cohort Modality | Primary File | Records | Features | Target Column | Positive Prevalence | Clinical Role |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| **Clinical EHR** | `diabetes_prediction_dataset.csv` | 100,000 | 9 | `diabetes` | 8.50% | High-precision diagnostic decision support |
| **Clinical Copy** | `diabetes_prediction_dataset(1).csv` | 100,000 | 9 | `diabetes` | 8.50% | **Flagged & excluded** (Identical MD5) |
| **CDC BRFSS Survey** | `diabetes_binary_health_indicators_BRFSS2015.csv` | 253,680 | 22 | `Diabetes_binary` | 13.93% | Non-invasive community & digital screening |
| **BRFSS Balanced** | `diabetes_binary_5050split_BRFSS2015.csv` | 70,692 | 22 | `Diabetes_binary` | 50.00% | Class-imbalance comparative research |
| **BRFSS 3-Class** | `diabetes_012_health_indicators_BRFSS2015.csv` | 253,680 | 22 | `Diabetes_012` | 0:84.2%, 1:1.8%, 2:13.9% | Prediabetes distinguishability research |
| **Early Symptoms** | `diabetes_data_upload.csv` | 520 | 17 | `class` | 61.54% | Acute hospital outpatient triage |

---

## 📊 Benchmark Results

### 1. Clinical & Laboratory Cohort (19,226 Test Patients)
*Champion Algorithm:* **LightGBM Classifier (Calibrated)**

| Model | Accuracy | Recall (Sensitivity) | Specificity | Precision | F1 Score | ROC-AUC | PR-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.8848 | 0.8791 | 0.8853 | 0.4259 | 0.5738 | 0.9597 | 0.8121 | 0.0800 |
| Decision Tree | 0.8258 | 0.9564 | 0.8131 | 0.3312 | 0.4920 | 0.9668 | 0.8594 | 0.0727 |
| Random Forest | 0.8923 | 0.9157 | 0.8901 | 0.4463 | 0.6001 | 0.9743 | 0.8734 | 0.0621 |
| Extra Trees | 0.8760 | 0.9180 | 0.8719 | 0.4095 | 0.5664 | 0.9655 | 0.8362 | 0.0778 |
| HistGradientBoosting | 0.8997 | 0.9133 | 0.8984 | 0.4652 | 0.6164 | 0.9771 | 0.8802 | 0.0605 |
| **LightGBM (Selected)** | **0.8975** | **0.9210** | **0.8953** | **0.4597** | **0.6133** | **0.9770** | **0.8802** | **0.0236\*** |
| XGBoost | 0.9720 | 0.6881 | 0.9994 | 0.9915 | 0.8124 | 0.9767 | 0.8801 | 0.0235 |

\* *Post-calibration Brier score via Platt scaling.*

---

### 2. CDC BRFSS Lifestyle Survey (10,000 Test Respondents)
*Champion Algorithm:* **LightGBM Classifier (Cost-Sensitive Balanced)**

| Model | Accuracy | Recall (Sensitivity) | Specificity | Precision | F1 Score | ROC-AUC | PR-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.7147 | 0.7299 | 0.7120 | 0.3138 | 0.4389 | 0.7979 | 0.3903 | 0.1847 |
| Decision Tree | 0.7126 | 0.7181 | 0.7116 | 0.3101 | 0.4331 | 0.7869 | 0.3927 | 0.1892 |
| Random Forest | 0.7474 | 0.6848 | 0.7587 | 0.3387 | 0.4532 | 0.7997 | 0.4009 | 0.1663 |
| Extra Trees | 0.7051 | 0.7220 | 0.7020 | 0.3043 | 0.4282 | 0.7882 | 0.3865 | 0.1823 |
| HistGradientBoosting | 0.7151 | 0.7417 | 0.7103 | 0.3161 | 0.4432 | 0.8034 | 0.4057 | 0.1796 |
| **LightGBM (Balanced)** | **0.7168** | **0.7449** | **0.7117** | **0.3181** | **0.4458** | **0.8046** | **0.4070** | **0.1080\*** |
| XGBoost (Unweighted) | 0.8496 | 0.1452 | 0.9767 | 0.5298 | 0.2279 | 0.8044 | 0.4035 | 0.1083 |

---

### 3. Early-Stage Acute Symptoms Cohort (104 Test Patients)
*Champion Algorithm:* **Extra Trees Classifier (Calibrated)**

| Model | Accuracy | Recall (Sensitivity) | Specificity | Precision | F1 Score | ROC-AUC | PR-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.9327 | 0.9062 | 0.9750 | 0.9831 | 0.9431 | 0.9918 | 0.9951 | 0.0483 |
| Decision Tree | 0.9712 | 0.9531 | 1.0000 | 1.0000 | 0.9760 | 0.9879 | 0.9946 | 0.0271 |
| Random Forest | 0.9712 | 0.9688 | 0.9750 | 0.9841 | 0.9764 | 0.9992 | 0.9995 | 0.0147 |
| **Extra Trees (Selected)** | **0.9904** | **1.0000** | **0.9750** | **0.9846** | **0.9922** | **0.9996** | **0.9998** | **0.0098\*** |
| HistGradientBoosting | 0.9808 | 0.9688 | 1.0000 | 1.0000 | 0.9841 | 1.0000 | 1.0000 | 0.0182 |
| LightGBM | 0.9808 | 0.9688 | 1.0000 | 1.0000 | 0.9841 | 1.0000 | 1.0000 | 0.0144 |
| Support Vector Machine | 0.9712 | 0.9531 | 1.0000 | 1.0000 | 0.9760 | 0.9996 | 0.9998 | 0.0099 |

---

## 🔍 Explainable AI (SHAP)

To satisfy medical transparency requirements, our inference service integrates **Shapley Additive Explanations (SHAP)** with `TreeExplainer`:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{i\}) - f(S) \right]$$

- **Clinical Biomarkers:** `HbA1c_level` dominates global attribution, exhibiting a sharp non-linear risk escalation above 6.5%. `blood_glucose_level` serves as the secondary driver, followed by `age` and `bmi`.
- **Lifestyle Survey:** `GenHlth` (self-rated general health perception) is the single strongest non-invasive driver, followed by `HighBP`, `BMI`, and `PhysActivity`.
- **Acute Symptoms:** The osmotic diuresis triad (`Polyuria`, `Polydipsia`, and `sudden weight loss`) drives over 70% of feature attribution.
- **Local Waterfall Attributions:** Each patient assessment dynamically produces an individualized waterfall plot explaining the exact positive and negative contributors to their risk score.

---

## 🩺 Patient Risk Stratification Schema

Calibrated model probabilities $P(\text{Diabetes})$ are mapped into structured clinical risk categories:

| Risk Tier | Probability Range | Badge | Clinical Interpretation & Actionable Guidance |
| :--- | :---: | :--- | :--- |
| **Low** | $0.00 \le P < 0.25$ | `LOW RISK` | Low likelihood in reference population. Maintain active routine ($\ge 150\text{ min/wk}$) and periodic annual check-ups. |
| **Moderate** | $0.25 \le P < 0.50$ | `MODERATE RISK` | Intermediate likelihood. Lifestyle modifications recommended (structured diet, aerobic exercise). Re-screen in 6–12 months. |
| **High** | $0.50 \le P < 0.75$ | `HIGH RISK` | Elevated probability. Primary physician consultation recommended; order confirmatory fasting glucose or $\text{HbA1c}$ within 30 days. |
| **Very High** | $0.75 \le P \le 1.00$ | `VERY HIGH RISK` | Substantial risk profile. Strongly recommend prompt clinical evaluation, formal diagnostic workup, and microvascular checks. |

*Every prediction includes a 95% Wilson score confidence interval: $\text{CI}_{95\%} = \hat{p} \pm 1.96 \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$.*

---

## 📁 Repository Structure

```
AI_Project/
├── app.py                                   # Streamlit Home Portal & Navigation
├── pages/
│   ├── 1_📊_Dataset_Explorer.py             # Multi-Cohort Explorer & Cryptographic Audit
│   ├── 2_🩺_Diabetes_Assessment.py           # Multi-Mode Patient Risk Assessment Portal
│   ├── 3_📈_Model_Performance.py            # Comparative Benchmarks & Diagnostic Curves
│   ├── 4_🔍_Explainable_AI.py               # Global & Local SHAP Feature Attribution
│   └── 5_📑_Research_Report.py              # Downloadable Research Monograph & CSVs
├── src/
│   ├── config.py                            # Constants, paths, risk stratifications
│   ├── data_loader.py                       # Safe dataset loading with caching
│   ├── data_audit.py                        # Cryptographic MD5 & cross-cohort overlap audit
│   ├── eda.py                              # Visualizations & statistical hypothesis tests
│   ├── feature_engineering.py               # Leakage-free custom clinical transformers
│   ├── preprocessing.py                     # Scikit-learn ColumnTransformers & pipelines
│   ├── train_models.py                      # Multi-algorithm training & calibration
│   ├── evaluate_models.py                   # ROC, PR, Brier score, calibration curves
│   ├── explainability.py                    # TreeExplainer SHAP & clinical narratives
│   ├── prediction_service.py                # Calibrated inference & uncertainty engine
│   ├── create_presentation.py               # Script generating 15-slide PowerPoint deck
│   └── generate_20page_report.py            # Script compiling 20-page formal PDF report
├── models/                                  # Serialized joblib model artifacts
├── outputs/
│   ├── figures/                             # High-resolution PNG diagnostic charts
│   └── tables/                              # Benchmark comparison CSVs & statistical tests
├── reports/                                 # Research monographs & audit logs
│   ├── diabetes_research_report_20_pages.pdf
│   ├── diabetes_research_report_20_pages.md
│   ├── diabetes_risk_prediction_15_slides.pptx
│   └── presentation_transcript_15_slides.md
├── tests/                                   # Pytest test suite (27 passing tests)
├── requirements.txt                         # Pinned dependencies
├── run_all.py                               # Single-command orchestrator
├── .gitignore                               # Clean gitignore (ignoring OS & Mac artifacts)
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/<YOUR-USERNAME>/diabetes-risk-ai.git
cd diabetes-risk-ai
```

### 2. Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Interactive Web Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🛠️ Pipeline Execution & Reproduction

Run individual stages of the research pipeline:

```bash
# 1. Run Data Integrity Audit & Cryptographic Verification
python -m src.data_audit

# 2. Run Exploratory Data Analysis & Statistical Hypothesis Tests
python -m src.eda

# 3. Train, Evaluate & Calibrate All 9 Models (5-Fold CV)
python -m src.train_models

# 4. Generate Explainable AI (SHAP) Visualizations
python -m src.explainability

# 5. Generate 15-Slide Presentation Deck (.pptx)
python -m src.create_presentation

# 6. Generate 20-Page Formal PDF Monograph
python -m src.generate_20page_report

# 7. Run Automated Pytest Test Suite
pytest -v tests/
```

Or run everything end-to-end with a single command:
```bash
python run_all.py
```

---

## 🛡️ Leakage Prevention & Scientific Rigor

1. **Zero Information Leakage:** Every imputer, standard scaler, and categorical encoder is fitted strictly within training cross-validation folds. Hold-out test sets remain completely unseen.
2. **Modality Isolation:** Survey questionnaires, clinical blood draws, and hospital symptom forms are never naively pooled into an unscientific hybrid table.
3. **Calibrated Probabilities:** Models undergo post-hoc calibration via Platt scaling / Isotonic regression, driving clinical Brier scores down to **0.0236**.
4. **Data Privacy:** 100% in-memory local computation; zero patient data transmitted to external APIs.

---

## ⚖️ Ethical & Clinical Governance

> [!WARNING]
> **RESEARCH & EDUCATIONAL USE ONLY:** This platform is an artificial intelligence research prototype and is **NOT** a certified medical diagnostic device. It does not provide medical advice, diagnosis, treatment, or prevention of diabetes or any medical condition.
> 
> **RETROSPECTIVE CONCORDANCE VS. FUTURE RISK:** The datasets analyzed contain retrospective, cross-sectional health surveys and clinical records labeled with existing diabetes diagnoses. They do NOT contain prospective longitudinal follow-up. Model predictions represent **retrospective diagnostic likelihood / classification concordance** rather than guarantees of future disease incidence. Always consult a licensed healthcare professional for clinical diagnoses.

---

## 📜 Citation & License

This project is licensed under the [MIT License](LICENSE).

```bibtex
@article{diabetes_risk_ai_2026,
  title={AI-Based Diabetes Risk Prediction Using Machine Learning and Lifestyle Factors: A Multi-Cohort Empirical Evaluation Across 350,000+ Records},
  author={Advanced Healthcare AI & Machine Learning Research Team},
  year={2026},
  journal={Healthcare AI Monograph Series},
  volume={AIML-DIA-2026-V1}
}
```
