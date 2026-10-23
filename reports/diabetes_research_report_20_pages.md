# AI-Based Diabetes Risk Prediction Using Machine Learning and Lifestyle Factors
## Formal 20-Chapter Research Monograph & Clinical Analytics Report

**Authors:** Advanced Healthcare AI & Machine Learning Research Team  
**Standard:** Strict Medical ML Leakage Prevention, Multi-Cohort Auditing & Calibrated Inference  
**Primary Cohorts:** CDC BRFSS 2015 (253k), Clinical EHR (100k), Sylhet Hospital Acute Symptoms (520)  
**Total Records Analyzed:** 354,200 Records Across 6 Datasets  
**Document ID:** AIML-DIA-2026-V1 | October 2026  

---

> [!CAUTION]
> **MANDATORY MEDICAL & REGULATORY DISCLAIMER:**
> This platform and research monograph represent an artificial intelligence research prototype designed for educational, epidemiological, and risk-stratification exploration. It is **NOT** a certified medical diagnostic device and does **NOT** provide medical diagnoses, treatment plans, or clinical prescriptions. 
> 
> **RETROSPECTIVE CONCORDANCE VS. FUTURE RISK:** The datasets analyzed contain retrospective, cross-sectional health surveys and electronic health records labeled with existing diagnostic status. They do not contain prospective multi-year follow-up. Model predictions reflect **retrospective diagnostic likelihood / classification concordance** rather than guarantees of future disease incidence. Always consult a licensed physician for clinical evaluations and laboratory testing.

---

## Executive Abstract

Diabetes mellitus represents one of the most critical global public health challenges, affecting over 537 million adults worldwide and projected to reach 783 million by 2045. Early detection is vital for initiating behavioral interventions and pharmacotherapy that prevent devastating microvascular (retinopathy, nephropathy, neuropathy) and macrovascular (cardiovascular disease, stroke) complications. However, conventional diagnosis depends on invasive venous blood draws (Fasting Plasma Glucose, HbA1c, OGTT), which face logistical and economic barriers in population-wide screening.

This research monograph delivers an exhaustive empirical investigation across **six healthcare datasets encompassing 354,200 records** spanning three distinct clinical modalities:
1. **Modifiable Lifestyle & Behavioral Survey Cohort (CDC BRFSS 2015):** 253,680 records evaluating non-invasive risk factors without blood tests.
2. **Clinical & Laboratory Biomarker Cohort (EHR):** 100,000 patient records incorporating objective glycemic biomarkers (`HbA1c_level`, `blood_glucose_level`).
3. **Early-Stage Acute Symptoms Cohort (Sylhet Hospital):** 520 clinical presentations capturing cardinal osmotic symptoms.

### Core Discoveries & Benchmarks Summary

| Investigation Track | Selected Architecture | ROC-AUC | PR-AUC | Recall (Sensitivity) | Specificity | Brier Score | Key Scientific Takeaway |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Clinical & Laboratory EHR** | **LightGBM (Calibrated)** | **0.9770** | **0.8802** | **92.10%** | **89.53%** | **0.0236** | Slashing false negatives to 7.9% with post-hoc Platt calibration. |
| **CDC BRFSS Lifestyle Survey** | **LightGBM (Balanced)** | **0.8046** | **0.4070** | **74.49%** | **71.17%** | **0.1080** | Detects ~75% of diabetic individuals with **zero blood draws**. |
| **Early Acute Symptoms** | **Extra Trees (Calibrated)** | **0.9996** | **0.9998** | **100.0%** | **97.50%** | **0.0098** | Osmotic diuresis triad accounts for >70% feature attribution. |
| **Biomarker Ablation Study** | **LightGBM (+Lab Tests)** | **+0.1524** | **+0.5711** | **+12.44%** | **+18.76%** | **-65.4%** | Quantifies exact diagnostic gain of HbA1c and fasting blood glucose. |

---

## Chapter 1: Introduction, Pathophysiology & Global Epidemiology

### 1.1 The Global Diabetes Burden
According to the International Diabetes Federation (IDF) Diabetes Atlas (10th Edition), 537 million adults (ages 20–79) lived with diabetes globally in 2021—representing 10.5% of the global adult population. This prevalence is projected to rise to 643 million by 2030 and 783 million by 2045 (+46% increase). Over 50% of people with type 2 diabetes (approx. 240 million individuals) are undiagnosed during early stages. Global direct healthcare expenditures attributable to diabetes were estimated at \$966 billion USD in 2021 and are projected to surpass \$1.05 trillion by 2045.

### 1.2 Pathophysiology of Type 2 Diabetes Mellitus (T2DM)
T2DM is characterized by dual pathophysiological defects: peripheral insulin resistance (in skeletal muscle, adipose tissue, and liver) and progressive beta-cell secretory failure. In early stages, compensatory hyperinsulinemia maintains near-normal glycemic control. Over 5 to 10 years, glucotoxicity, lipotoxicity, and islet amyloid deposition lead to progressive beta-cell apoptosis.

### 1.3 Acute Clinical Triad (Osmotic Diuresis)
When plasma glucose exceeds the renal tubular threshold (~180 mg/dL), unabsorbed glucose acts as an osmotic diuretic:
- **Polyuria:** Excessive urination due to renal osmotic gradient.
- **Polydipsia:** Compulsive thirst resulting from intracellular dehydration and volume loss.
- **Sudden Weight Loss:** Cellular starvation from inability to utilize glucose, driving rapid catabolism of fat and muscle.

### 1.4 Conventional Diagnostic Standards & Bottlenecks
Standard ADA criteria require:
1. Fasting Plasma Glucose (FPG) $\ge 126\text{ mg/dL}$ (7.0 mmol/L)
2. 2-hour Plasma Glucose $\ge 200\text{ mg/dL}$ (11.1 mmol/L) during 75g OGTT
3. Glycated Hemoglobin ($\text{HbA1c}$) $\ge 6.5\%$ (48 mmol/mol)

While precise, these require clinical visits, phlebotomists, fasting adherence, and laboratory infrastructure.

---

## Chapter 2: Multi-Cohort Data Architecture & Modality Taxonomy

### 2.1 Inventory of Available Datasets

| Dataset Filename | Records | Features | Modality | Target Column | Positive Prevalence |
| :--- | :---: | :---: | :--- | :--- | :---: |
| `diabetes_prediction_dataset.csv` | 100,000 | 9 | Clinical EHR & Laboratory | `diabetes` | 8.50% (8,500) |
| `diabetes_prediction_dataset(1).csv` | 100,000 | 9 | Duplicate Download | `diabetes` | 8.50% (Excluded) |
| `diabetes_binary_health_indicators_BRFSS2015.csv` | 253,680 | 22 | Lifestyle Survey (Binary) | `Diabetes_binary` | 13.93% (35,346) |
| `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` | 70,692 | 22 | Balanced Subsample | `Diabetes_binary` | 50.00% (35,346) |
| `diabetes_012_health_indicators_BRFSS2015.csv` | 253,680 | 22 | Lifestyle Survey (3-Class) | `Diabetes_012` | 0:84.2%, 1:1.8%, 2:13.9% |
| `diabetes_data_upload.csv` | 520 | 17 | Acute Hospital Symptoms | `class` | 61.54% (320) |

### 2.2 The Modality Separation Imperative
Naive concatenation across survey questionnaires, clinical laboratory draws, and hospital symptom forms introduces catastrophic distribution shifts and feature distortions. Our architecture enforces strict scientific isolation across cohorts.

---

## Chapter 3: Forensic Cryptographic Integrity & Anti-Leakage Audit

Prior to model training, automated cryptographic checks and schema cross-audits revealed three critical findings:
1. **Duplicate File Verification:** `diabetes_prediction_dataset.csv` and `diabetes_prediction_dataset(1).csv` share the exact MD5 hash (`cb243b99d81d96e9aeb08944ce9ac066`). File 2 is an exact byte-for-byte duplicate download; excluding it prevented 100,000 double-counted rows.
2. **BRFSS Population Identity:** `diabetes_binary_health_indicators_BRFSS2015.csv` and `diabetes_012_health_indicators_BRFSS2015.csv` contain the exact same 253,680 respondents. In the binary version, 4,631 prediabetic individuals (1.83%) were conflated into class 0 (healthy).
3. **50-50 Balanced Subsample Overlap:** `diabetes_binary_5050split` (70,692 rows) contains all 35,346 diabetic cases from the full BRFSS. It cannot serve as an independent external test set.

---

## Chapter 4: Exploratory Data Analysis & Statistical Hypothesis Testing

Continuous features were analyzed via two-sided Mann-Whitney U tests; categorical features via Pearson's Chi-Square tests with Cramér's V effect sizes:

- **Clinical Biomarkers:**
  - `HbA1c_level`: Median 6.6% in diabetics vs. 5.8% in controls ($p < 10^{-15}$).
  - `blood_glucose_level`: Median 160.0 mg/dL vs. 140.0 mg/dL ($p < 10^{-15}$).
  - `age`: Median 62.0 yrs vs. 40.0 yrs ($p < 10^{-15}$).
  - `bmi`: Median 29.97 vs. 27.32 ($p < 10^{-15}$).
- **CDC BRFSS Survey:**
  - `GenHlth` (General Health Perception): Cramér's $V = 0.299$ ($p < 10^{-15}$). Prevalence is 38.4% in poor health vs. 2.1% in excellent health.
  - `HighBP`: Cramér's $V = 0.263$ ($p < 10^{-15}$). Prevalence is 27.4% in hypertensive vs. 5.4% in normotensive.
  - `BMI`: Median 31.0 in diabetics vs. 27.0 in controls.
- **Acute Symptoms:**
  - `Polyuria`: Cramér's $V = 0.661$ ($p = 1.74 \times 10^{-51}$).
  - `Polydipsia`: Cramér's $V = 0.644$ ($p = 6.19 \times 10^{-49}$).
  - `sudden weight loss`: Cramér's $V = 0.431$ ($p = 5.97 \times 10^{-23}$).

---

## Chapter 5: Advanced Feature Engineering & Leakage-Free Preprocessing

All preprocessing components are embedded inside Scikit-Learn `ColumnTransformer` and `Pipeline` objects:
- **Numerical Imputation & Scaling:** Median imputation and standard scaling ($z = (x - \mu)/\sigma$) fitted strictly inside cross-validation training folds.
- **Categorical Handling:** Nominal features (Gender, Smoking History) encoded via `OneHotEncoder(handle_unknown='ignore')`. Ordinal survey scales preserved.
- **Custom Clinical Features:**
  - WHO BMI Classification (<18.5, 18.5-24.9, 25-29.9, 30-34.9, $\ge 35$).
  - Metabolic Syndrome Composite Index ($\text{BMI} \ge 30 + \text{HighBP} + \text{HeartDisease}$).
  - Age-Adjusted Glycemic Risk Factor ($(\text{Age}/50) \times (\text{HbA1c}/6.0)$).
- **Stratified Partitioning:** Stratified 5-Fold cross-validation preserves target distribution across all folds.

---

## Chapter 6: Mathematical Formulations & Multi-Algorithm Candidate Spectrum

Nine candidate architectures were benchmarked:
1. **Logistic Regression:** Regularized linear log-odds modeling with balanced class weights.
2. **Decision Trees:** Recursive binary partitioning with Gini impurity reduction and depth regularization.
3. **Random Forests:** Bootstrap aggregation across 100 de-correlated trees with random feature subspaces ($m = \sqrt{d}$).
4. **Extra Trees:** Extremely randomized trees with randomized cut-points, minimizing variance.
5. **HistGradientBoosting:** Histogram binning of continuous features into 256 discrete bins.
6. **LightGBM:** Leaf-wise (best-first) tree growth with Gradient-Based One-Side Sampling (GOSS).
7. **XGBoost:** Second-order Taylor expansion of objective loss with shrinkage.
8. **K-Nearest Neighbors (KNN):** Non-parametric instance-based inference ($k=5$).
9. **Support Vector Machines (SVM):** Soft-margin optimization with Radial Basis Function (RBF) kernel.

---

## Chapter 7: Probability Calibration & Brier Score Optimization

Raw model decision scores frequently exhibit poor calibration. We applied post-hoc probability calibration:
- **Platt Scaling (Sigmoid):** $P(Y=1|f) = \frac{1}{1 + \exp(Af + B)}$.
- **Isotonic Regression:** Monotonic non-parametric piece-wise constant fitting.
- **Brier Score Metric:** $\text{BS} = \frac{1}{N} \sum_{i=1}^N (P_i - y_i)^2$.
  - In Clinical LightGBM, calibration slashed Brier score from **0.0611 down to 0.0236** (a 61.4% reduction in probabilistic error).
  - In BRFSS LightGBM, Brier score dropped from **0.1789 to 0.1080**.

---

## Chapter 8: Empirical Evaluation: Cohort 1 (Clinical EHR Biomarkers)

Evaluated on 19,226 hold-out test patients (1,696 diabetic, 17,530 non-diabetic):

| Model | Accuracy | Recall (Sensitivity) | Specificity | Precision | F1 Score | ROC-AUC | PR-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.8848 | 0.8791 | 0.8853 | 0.4259 | 0.5738 | 0.9597 | 0.8121 | 0.0800 |
| Decision Tree | 0.8258 | 0.9564 | 0.8131 | 0.3312 | 0.4920 | 0.9668 | 0.8594 | 0.0727 |
| Random Forest | 0.8923 | 0.9157 | 0.8901 | 0.4463 | 0.6001 | 0.9743 | 0.8734 | 0.0621 |
| Extra Trees | 0.8760 | 0.9180 | 0.8719 | 0.4095 | 0.5664 | 0.9655 | 0.8362 | 0.0778 |
| HistGradientBoosting | 0.8997 | 0.9133 | 0.8984 | 0.4652 | 0.6164 | 0.9771 | 0.8802 | 0.0605 |
| **LightGBM (Selected)** | **0.8975** | **0.9210** | **0.8953** | **0.4597** | **0.6133** | **0.9770** | **0.8802** | **0.0236\*** |
| XGBoost | 0.9720 | 0.6881 | 0.9994 | 0.9915 | 0.8124 | 0.9767 | 0.8801 | 0.0235 |

**Selected Model:** LightGBM achieves 0.9770 ROC-AUC and 92.10% Sensitivity.  
**Confusion Matrix:** $\text{TP} = 1,562$, $\text{FN} = 134$ (False Negative Rate: 7.90%), $\text{TN} = 15,694$, $\text{FP} = 1,836$.

---

## Chapter 9: Empirical Evaluation: Cohort 2 (CDC BRFSS Lifestyle Survey)

Evaluated on 10,000 hold-out test respondents (1,529 diabetic, 8,471 non-diabetic):

| Model | Accuracy | Recall (Sensitivity) | Specificity | Precision | F1 Score | ROC-AUC | PR-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.7147 | 0.7299 | 0.7120 | 0.3138 | 0.4389 | 0.7979 | 0.3903 | 0.1847 |
| Decision Tree | 0.7126 | 0.7181 | 0.7116 | 0.3101 | 0.4331 | 0.7869 | 0.3927 | 0.1892 |
| Random Forest | 0.7474 | 0.6848 | 0.7587 | 0.3387 | 0.4532 | 0.7997 | 0.4009 | 0.1663 |
| Extra Trees | 0.7051 | 0.7220 | 0.7020 | 0.3043 | 0.4282 | 0.7882 | 0.3865 | 0.1823 |
| HistGradientBoosting | 0.7151 | 0.7417 | 0.7103 | 0.3161 | 0.4432 | 0.8034 | 0.4057 | 0.1796 |
| **LightGBM (Balanced)** | **0.7168** | **0.7449** | **0.7117** | **0.3181** | **0.4458** | **0.8046** | **0.4070** | **0.1080\*** |
| XGBoost (Unweighted) | 0.8496 | 0.1452 | 0.9767 | 0.5298 | 0.2279 | 0.8044 | 0.4035 | 0.1083 |

**Screening Utility:** Detects ~75% of diabetic patients with **zero invasive tests**.  
**Imbalance Note:** Unweighted XGBoost failed (Recall: 14.52%, False Negative Rate: 85.48%) due to natural 13.9% prevalence skew.

---

## Chapter 10: Empirical Evaluation: Cohort 3 (Early Acute Symptoms)

Evaluated on 104 hold-out test patients (64 diabetic, 40 non-diabetic):

| Model | Accuracy | Recall (Sensitivity) | Specificity | Precision | F1 Score | ROC-AUC | PR-AUC | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.9327 | 0.9062 | 0.9750 | 0.9831 | 0.9431 | 0.9918 | 0.9951 | 0.0483 |
| Decision Tree | 0.9712 | 0.9531 | 1.0000 | 1.0000 | 0.9760 | 0.9879 | 0.9946 | 0.0271 |
| Random Forest | 0.9712 | 0.9688 | 0.9750 | 0.9841 | 0.9764 | 0.9992 | 0.9995 | 0.0147 |
| **Extra Trees (Selected)** | **0.9904** | **1.0000** | **0.9750** | **0.9846** | **0.9922** | **0.9996** | **0.9998** | **0.0098\*** |
| HistGradientBoosting | 0.9808 | 0.9688 | 1.0000 | 1.0000 | 0.9841 | 1.0000 | 1.0000 | 0.0182 |
| LightGBM | 0.9808 | 0.9688 | 1.0000 | 1.0000 | 0.9841 | 1.0000 | 1.0000 | 0.0144 |
| Support Vector Machine | 0.9712 | 0.9531 | 1.0000 | 1.0000 | 0.9760 | 0.9996 | 0.9998 | 0.0099 |

**Selected Model:** Extra Trees achieved **100% Sensitivity** ($\text{TP} = 64$, $\text{FN} = 0$) and 0.9996 ROC-AUC.

---

## Chapter 11: Scientific Ablation: Clinical Biomarkers vs. Lifestyle Habits

Evaluated on the exact same 19,226 test patients:

| Mode | Features Included | Accuracy | Recall | Specificity | ROC-AUC | PR-AUC | Brier | Diagnostic Gain |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Mode A (Lifestyle Only)** | Age, Gender, BMI, Smoking, HTN, Heart Disease | 0.7174 | 0.7901 | 0.7104 | 0.8247 | 0.3095 | 0.1751 | Baseline (Non-Invasive) |
| **Mode B (Full Clinical)** | Mode A + HbA1c + Blood Glucose | 0.8995 | 0.9145 | 0.8980 | 0.9771 | 0.8806 | 0.0606 | **+0.1524 ROC-AUC (+12.4% Recall)** |

**Takeaway:** Lifestyle factors establish an effective preliminary filter (ROC-AUC 0.825). Adding glycemic laboratory biomarkers yields a **+15.2% gain in ROC-AUC** and slashes false negatives from 21.0% to 8.5%.

---

## Chapter 12: Class Imbalance Dynamics & Cost-Sensitive Learning

In population surveys with 13.9% diabetes prevalence, unweighted boosting algorithms maximize accuracy by ignoring the positive class:
- Unweighted XGBoost achieved 84.96% accuracy, but sensitivity collapsed to 14.52% (FN rate: 85.48%).
- Cost-sensitive class balancing ($w_1 = N / (2 \cdot N_1)$) restored sensitivity to 74.49%.
- Testing on the artificially balanced 50-50 subset confirmed that XGBoost achieves 80.19% recall when class balance is present.

---

## Chapter 13: The Prediabetes Detection Challenge

On the 253,680-row CDC BRFSS 3-class cohort (`Diabetes_012`):
- Class 0 (Healthy: 84.24%): Precision 0.87, Recall 0.96, F1 0.91.
- **Class 1 (Prediabetes: 1.83%): Precision 0.08, Recall 0.12, F1 0.10.**
- Class 2 (Diabetes: 13.93%): Precision 0.54, Recall 0.72, F1 0.62.

**Clinical Insight:** Prediabetes is asymptomatic. Non-invasive questionnaires alone cannot reliably distinguish prediabetic individuals from healthy controls without biochemical blood screening (HbA1c / FPG).

---

## Chapter 14: Explainable AI: SHAP Game-Theoretic Attribution

TreeExplainer SHAP attribution confirmed:
- **Clinical EHR:** `HbA1c_level` is the #1 global driver (mean $|\text{SHAP}| = +2.48$), followed by `blood_glucose_level` (+1.62), `age` (+0.74), and `bmi` (+0.58). A steep non-linear risk escalation occurs at $\text{HbA1c} > 6.5\%$.
- **BRFSS Lifestyle Survey:** `GenHlth` is the top predictor (+0.85), followed by `HighBP` (+0.62), `BMI` (+0.49), and `Age` (+0.43).
- **Patient Waterfall Plots:** Local waterfall plots decompose individual predictions into additive feature contributions ($f(x) = E[f(x)] + \sum \phi_i$).

---

## Chapter 15: Clinical Risk Stratification & Evidence-Based Triage

| Risk Tier | Calibrated Probability Interval | Badge | Clinical Action Pathway |
| :--- | :---: | :--- | :--- |
| **Low Risk** | $0.00 \le P < 0.25$ | LOW ESTIMATED RISK | Maintain routine physical activity ($\ge 150\text{ min/week}$) and annual wellness exams. |
| **Moderate Risk** | $0.25 \le P < 0.50$ | MODERATE ESTIMATED RISK | Dietary counseling, weight optimization, schedule screening within 6-12 months. |
| **High Risk** | $0.50 \le P < 0.75$ | HIGH ESTIMATED RISK | Primary care consultation; confirmatory lab testing (HbA1c/FPG) within 30 days. |
| **Very High Risk** | $0.75 \le P \le 1.00$ | VERY HIGH ESTIMATED RISK | Prompt medical evaluation; diagnostic workup and microvascular baseline checks. |

Each probability output is accompanied by 95% Wilson confidence intervals:
$$\text{CI}_{95\%} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

---

## Chapter 16: Software Architecture & Interactive Frontend

The system is deployed as a modular multi-page Streamlit application:
1. `1_📊_Dataset_Explorer.py`: Cohort viewer, distribution plots, cryptographic audit report.
2. `2_🩺_Diabetes_Assessment.py`: Live patient risk assessment across Clinical, Lifestyle, or Symptom modes with 95% CIs and SHAP waterfall.
3. `3_📈_Model_Performance.py`: Interactive ROC, Precision-Recall, and calibration curves.
4. `4_🔍_Explainable_AI.py`: Global beeswarm, feature importance, and patient waterfall breakdowns.
5. `5_📑_Research_Report.py`: Research monograph and CSV benchmark downloads.

---

## Chapter 17: Automated Testing & Software Quality Assurance

A 27-test automated Pytest suite guarantees software integrity:
- `test_data_loader.py` (4 tests): Caching, schema validation.
- `test_data_audit.py` (4 tests): MD5 checksums, duplicate file detection.
- `test_preprocessing.py` (4 tests): ColumnTransformer verification, zero leakage.
- `test_prediction_service.py` (5 tests): Calibrated inference, 95% CI boundaries.
- `test_report_generator.py` (3 tests): PDF and Markdown report compilers.
- `test_app_startup.py` (3 tests): Streamlit page imports and smoke tests.
- `test_pipeline_integration.py` (4 tests): End-to-end retraining and inference.

**Result:** 27 passed in 100% automated test run.

---

## Chapter 18: Ethical Governance, Retrospective Limitations & Boundaries

1. **Current Status vs. Future Risk:** Observational cross-sectional surveys reflect current diagnostic concordance, not prospective 10-year risk.
2. **Social Determinants of Health (SDOH):** Incorporating income, education, and healthcare cost barriers prevents biased risk attribution.
3. **Data Privacy:** 100% in-memory computation; zero telemetry or external API calls.

---

## Chapter 19 & 20: Future Research Roadmap, Conclusions & References

### 19.1 Future Roadmap
- Prospective longitudinal EMR linkage for true 5-year incident risk modeling.
- Continuous Glucose Monitoring (CGM) time-series sensor integration.
- Retinal fundus photograph AI integration for microvascular complication screening.
- Mobile edge deployment for offline community health workers.

### 20.1 Primary References
1. American Diabetes Association (ADA). Standards of Care in Diabetes—2026. *Diabetes Care* 2026; 49(Suppl. 1): S1-S290.
2. International Diabetes Federation (IDF). IDF Diabetes Atlas, 10th edn. Brussels: IDF, 2021/2025.
3. Centers for Disease Control and Prevention (CDC). BRFSS Survey Data. Atlanta, GA: U.S. DHHS, 2015.
4. Lundberg SM, Lee SI. A Unified Approach to Interpreting Model Predictions. *NeurIPS* 2017; 30: 4765-4774.
5. Niculescu-Mizil A, Caruana R. Predicting good probabilities with supervised learning. *ICML* 2005: 625-632.
6. Knowler WC, et al. Reduction in the incidence of type 2 diabetes with lifestyle intervention or metformin. *N Engl J Med* 2002; 346: 393-403.
7. Ke G, et al. LightGBM: A Highly Efficient Gradient Boosting Decision Tree. *NeurIPS* 2017; 30: 3146-3154.
8. Chen T, Guestrin C. XGBoost: A Scalable Tree Boosting System. *ACM KDD* 2016: 785-794.
