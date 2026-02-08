# Research Plan: Factors Associated with Poor Physical Health Days Among Older Men (60+) in the United States

## Study Overview

This study examines factors associated with poor physical health days among older men (age 60+) using the National Health and Nutrition Examination Survey (NHANES). The CDC Healthy Days measure provides a validated, population-level indicator of health-related quality of life that captures the burden of physical health problems on daily functioning.

---

## 1. Study Objectives

### Primary Objective
To identify and quantify the association between chronic disease burden and poor physical health days among U.S. men aged 60 years and older.

### Secondary Objectives
1. To examine the relationship between mental health days and physical health days in older men
2. To assess socioeconomic disparities in physical health days after adjusting for chronic conditions
3. To evaluate racial/ethnic differences in physical health days
4. To determine the protective effect of physical activity on physical health days
5. To characterize the multimorbidity patterns associated with activity limitation days

### Specific Aims

**Aim 1**: Determine the association between chronic condition count (diabetes, hypertension, cardiovascular disease) and poor physical health days among older men.

**Aim 2**: Examine whether mental health days mediate or moderate the relationship between chronic conditions and physical health days.

**Aim 3**: Assess the independent effects of socioeconomic status (education, income, insurance) on physical health days after controlling for chronic disease burden.

**Aim 4**: Evaluate racial/ethnic disparities in physical health days and test whether these disparities persist after comprehensive adjustment for socioeconomic and clinical factors.

**Aim 5**: Quantify the dose-response relationship between physical activity levels and reduced physical health days.

---

## 2. Conceptual Framework

### Theoretical Model

This study applies an adapted version of the **Social Determinants of Health Framework** combined with the **Chronic Care Model** to understand physical health days in older men:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CONCEPTUAL FRAMEWORK                                  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  SOCIAL &       │────▶│  HEALTHCARE      │────▶│  CHRONIC            │
│  DEMOGRAPHIC    │     │  ACCESS          │     │  DISEASE            │
│  FACTORS        │     │  (Insurance)     │     │  BURDEN             │
│                 │     │                  │     │                     │
│ • Age           │     │                  │     │ • Diabetes          │
│ • Race/Ethnicity│     │                  │     │ • Hypertension      │
│ • Education     │     │                  │     │ • CVD               │
│ • Income        │     │                  │     │ • Multimorbidity    │
│ • Marital Status│     │                  │     │                     │
└─────────────────┘     └──────────────────┘     └─────────────────────┘
         │                      │                        │
         │                      │                        │
         └──────────────────────┴────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │      MODIFIABLE RISK FACTORS           │
         │                                        │
         │  • Physical Activity  • Smoking        │
         │  • BMI/Obesity        • Alcohol Use    │
         │                                        │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │         PRIMARY OUTCOME                │
         │                                        │
         │   Poor Physical Health Days (HSQ470)   │
         │                                        │
         └────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   SECONDARY     │  │   SECONDARY     │  │   SECONDARY     │
│   OUTCOME 1     │  │   OUTCOME 2     │  │   OUTCOME 3     │
│                 │  │                 │  │                 │
│ Mental Health   │  │ Activity        │  │ General Health  │
│ Days (HSQ480)   │  │ Limitation Days │  │ Status (HSD010) │
│                 │  │ (HSQ490)        │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Key Constructs

#### Exposure Variables
- **Chronic Disease Burden**: Count of diagnosed conditions (0, 1, 2, 3+)
- **Individual Chronic Conditions**: Diabetes, hypertension, cardiovascular disease (binary)
- **Multimorbidity Patterns**: Specific combinations of conditions

#### Outcome Variables
- **Primary**: Poor physical health days (HSQ470) - continuous 0-30 scale
- **Secondary 1**: Mental health days (HSQ480) - continuous 0-30 scale
- **Secondary 2**: Activity limitation days (HSQ490) - continuous 0-30 scale
- **Secondary 3**: General health status (HSD010) - categorical excellent to poor

#### Confounding Variables
- **Demographic**: Age (continuous), race/ethnicity (categorical), marital status
- **Socioeconomic**: Education level, income-to-poverty ratio, health insurance status
- **Clinical**: BMI category, smoking status
- **Behavioral**: Physical activity level, alcohol consumption

#### Effect Modifiers (to be tested)
- Race/ethnicity (for chronic condition associations)
- Age group (60-69, 70-79, 80+)
- Education level (for SES gradients)

---

## 3. Study Design Rationale

### Design Selection: Cross-Sectional Analysis

A cross-sectional design is appropriate for this research because:

1. **Research Question**: The study aims to describe associations and prevalence patterns rather than establish causation or temporal sequences.

2. **Healthy Days Measure**: The CDC Healthy Days questions capture recent (past 30 days) health status, making them inherently cross-sectional in nature.

3. **Chronic Conditions**: The conditions of interest (diabetes, hypertension, CVD) are chronic and persistent, making the timing of assessment less critical than for acute conditions.

4. **Population Surveillance**: NHANES is designed for population-level surveillance, which aligns with describing health status distributions across demographic subgroups.

5. **Resource Efficiency**: Cross-sectional analysis allows for efficient use of the large, nationally representative NHANES sample.

### Limitations Acknowledged
- Cannot establish temporal precedence (conditions may predate or follow poor health days)
- Survivorship bias (sicker individuals may not survive to older ages)
- Selection bias (healthier individuals may participate more readily)

### Mitigation Strategies
- Focus on interpretation as "factors associated with" rather than "predictors of"
- Use consistent time windows (past 30 days for outcomes, current status for conditions)
- Apply appropriate survey weights for population representativeness
- Conduct sensitivity analyses excluding those with very poor general health

---

## 4. Data Source and Study Population

### NHANES Cycles

**Primary Analysis Cycles**: 2001-2018 (Cycles B through J)
- B: 2001-2002
- C: 2003-2004
- D: 2005-2006
- E: 2007-2008
- F: 2009-2010
- G: 2011-2012
- H: 2013-2014
- I: 2015-2016
- J: 2017-2018

**Rationale for Cycle Selection**:
- HSQ (Health Status Questionnaire) with Healthy Days measures available in all cycles
- DEMO (Demographics) available for cycles B-J
- Sufficient sample size for subgroup analyses
- Consistent variable definitions across cycles
- Balanced representation across study period

### Inclusion Criteria
1. Males only
2. Age 60 years or older at time of examination
3. Completed the HSQ questionnaire module
4. Valid response for physical health days (HSQ470)
5. Valid survey weights available

### Exclusion Criteria
1. Missing physical health days data (HSQ470)
2. Refused or don't know responses to primary outcome
3. Pregnant individuals (if applicable, though rare in this age group)

### Expected Sample Size
Based on NHANES sampling patterns:
- Approximately 1,200-1,500 older men across pooled cycles
- Estimated 150-200 participants per cycle
- Adequate power to detect moderate effect sizes (Cohen's d = 0.3) with 80% power

---

## 5. Analysis Approach Overview

### Descriptive Analysis

**Unweighted Statistics**:
- Means, standard deviations for continuous variables
- Frequencies, percentages for categorical variables
- Histograms and density plots for outcome distributions

**Weighted Statistics**:
- Population-weighted means and proportions
- 95% confidence intervals using Taylor series linearization
- Stratified by chronic condition status

### Primary Analysis

**Linear Regression Models**:

Model 1 (Crude): Physical Health Days ~ Chronic Condition Burden

Model 2 (Adjusted for Demographics): Physical Health Days ~ Chronic Condition Burden + Age + Race/Ethnicity

Model 3 (Fully Adjusted): Physical Health Days ~ Chronic Condition Burden + Age + Race/Ethnicity + Education + Income + Insurance + Smoking + BMI

**Outcomes**: Beta coefficients with 95% CIs, p-values

### Secondary Analyses

**Multimorbidity Analysis**:
- Compare physical health days across multimorbidity categories:
  - No chronic conditions (reference)
  - Single condition (diabetes only, hypertension only, CVD only)
  - Two conditions
  - Three or more conditions

**Mental Health Mediation**:
- Test whether mental health days mediate the chronic condition → physical health days relationship using Baron & Kenny approach or structural equation modeling

**Racial/Ethnic Disparities**:
- Sequential models showing attenuation of racial/ethnic coefficients with progressive adjustment
- Blinder-Oaxaca decomposition to quantify explained vs. unexplained disparities

**Physical Activity Dose-Response**:
- Categories: None, Low, Moderate, High activity levels
- Test for linear trend across categories
- Interaction with chronic condition status

**Outcome Distribution Analysis**:
- Given the expected zero-inflated distribution, consider:
  - Negative binomial regression (for count data)
  - Zero-inflated models (separate processes for zero vs. non-zero days)
  - Ordinal categorization (0, 1-7, 8-14, 15-30 days)

### Sensitivity Analyses

1. **Exclusion of Outliers**: Remove observations with |z-score| > 4 for continuous variables
2. **Complete Case Analysis**: Compare with multiple imputation for missing covariates
3. **Cycle-Specific Analyses**: Test for temporal trends across study period
4. **Age Stratification**: Separate analyses for 60-69, 70-79, and 80+ age groups
5. **Mental Health Exclusion**: Exclude those with extreme mental health days to test robustness

### Interaction Testing

Planned interaction tests:
- Chronic conditions × Race/Ethnicity
- Chronic conditions × Age group
- Physical activity × Chronic conditions
- Education × Income (SES gradient)

### Software and Packages

- **Python** (primary analysis language)
- pandas, numpy for data manipulation
- statsmodels for survey-weighted regression
- scipy for statistical tests
- matplotlib, seaborn for visualization

### Significance Level
- Two-tailed alpha = 0.05
- Bonferroni correction for multiple comparisons where appropriate
- Focus on confidence intervals rather than sole reliance on p-values

---

## 6. Variables Summary

| Domain | Variable(s) | Dataset | Type | Role |
|--------|-------------|---------|------|------|
| **Primary Outcome** | HSQ470 (Physical Health Days) | HSQ | Continuous (0-30) | Outcome |
| **Secondary Outcomes** | HSQ480 (Mental Health Days) | HSQ | Continuous (0-30) | Outcome |
| | HSQ490 (Activity Limitation Days) | HSQ | Continuous (0-30) | Outcome |
| | HSD010 (General Health Status) | HSQ | Categorical (1-5) | Outcome |
| **Primary Exposure** | Chronic Condition Count | DIQ, BPQ, CDQ | Categorical (0,1,2,3+) | Primary Predictor |
| **Chronic Conditions** | Diabetes (DIQ010) | DIQ | Binary | Predictor |
| | Hypertension (BPQ020) | BPQ | Binary | Predictor |
| | CVD History (CDQ001-CDQ009) | CDQ | Binary | Predictor |
| **Demographics** | Age (RIDAGEYR) | DEMO | Continuous | Confounder |
| | Sex (RIAGENDR) | DEMO | Binary (Male only) | Inclusion |
| | Race/Ethnicity (RIDRETH1) | DEMO | Categorical | Confounder |
| | Marital Status (DMDMARTL) | DEMO | Categorical | Confounder |
| **Socioeconomic** | Education (DMDEDUC2) | DEMO | Categorical | Confounder |
| | Income-to-Poverty Ratio | DEMO | Continuous | Confounder |
| | Insurance Status (HIQ011) | HIQ | Binary | Confounder |
| **Health Behaviors** | Physical Activity (PAQ605-PAQ650) | PAQ | Categorical | Predictor/Confounder |
| | Smoking Status (SMQ020) | SMQ | Binary | Confounder |
| | BMI Category (BMXBMI) | BMX | Categorical | Confounder |
| **Survey Design** | Sample Weights (WTMEC2YR) | DEMO | Sampling weights | Adjustment |
| | PSU, Stratum | DEMO | Clustering | Adjustment |

---

## 7. Expected Contributions

### Scientific Contributions
1. First comprehensive examination of Healthy Days specifically among older men using NHANES
2. Quantification of multimorbidity effects on health-related quality of life
3. Evidence on modifiable risk factors for poor physical health days
4. Documentation of persistent racial/ethnic and socioeconomic disparities

### Public Health Relevance
1. Identifies high-risk subgroups requiring targeted interventions
2. Informs chronic disease management strategies
3. Supports healthy aging initiatives
4. Provides baseline for monitoring health trends in older men

### Clinical Implications
1. Highlights importance of addressing mental health alongside physical health
2. Supports integration of physical activity counseling in chronic disease care
3. Emphasizes need for comprehensive, multidisciplinary care for multimorbidity

---

## 8. Timeline

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| Phase 1: Literature Review | Completed | Systematic review, reference compilation |
| **Phase 2: Research Planning** | **Current** | **Hypothesis development, variable specification** |
| Phase 3: Methods Development | Week 1-2 | Statistical analysis plan, IRB documentation |
| Phase 4: Data Analysis | Week 3-6 | Data extraction, cleaning, statistical modeling |
| Phase 5: Results Interpretation | Week 7-8 | Synthesis, sensitivity analyses |
| Phase 6: Manuscript Preparation | Week 9-12 | Drafting, revisions, submission preparation |

---

## 9. Ethical Considerations

1. **Data Use**: De-identified public-use NHANES data; no direct human subjects involvement
2. **Population Representativeness**: Use of survey weights ensures findings generalize to U.S. older men
3. **Health Disparities**: Findings may reveal disparities requiring sensitive interpretation
4. **Scientific Rigor**: Pre-specified analysis plan to reduce selective reporting

---

*Document Version: 1.0*
*Date: 2026-02-08*
*Study: older-men-health-days-2026-02-08*
