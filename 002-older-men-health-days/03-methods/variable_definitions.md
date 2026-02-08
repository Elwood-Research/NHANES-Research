# Variable Definitions and Coding: Older Men and Physical Health Days

## Overview

This document provides comprehensive documentation of all variables used in the study "Factors Associated with Poor Physical Health Days Among Older Men: NHANES 2001-2018." It includes NHANES variable names, human-readable labels, coding schemes, reference categories, and missing value handling procedures.

## Variable Naming Convention

### Raw NHANES Variables
All NHANES variables retain their original variable names as provided in the public use files (e.g., HSQ470, RIDAGEYR, DIQ010).

### Analytical Variables
Derived variables created for analysis use descriptive names following snake_case convention:
- `physical_health_days` (mapped from HSQ470)
- `chronic_condition_count` (derived)
- `age_centered` (derived from RIDAGEYR)

### Manuscript Labels
All variables will be presented in manuscripts using clear, human-readable labels without NHANES codes (e.g., "Physical Health Days" not "HSQ470").

---

## Primary Outcome Variables

### Physical Health Days Not Good

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | HSQ470 |
| **Analytical Variable** | `physical_health_days` |
| **Manuscript Label** | Physical Health Days Not Good |
| **Description** | Number of days in the past 30 days when physical health was not good |
| **Question Text** | "Thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good?" |
| **Scale** | Count variable (0-30 days) |
| **Type** | Discrete numeric |

#### Valid Values
| Value | Meaning | Manuscript Label |
|-------|---------|------------------|
| 0-30 | Number of days | [Value] days |
| 77 | Refused | Excluded |
| 99 | Don't know | Excluded |
| . | Missing | Excluded |

#### Handling Instructions
- **Valid range**: 0-30
- **Exclusions**: 77, 99, missing
- **Outlier screening**: Remove |z| > 4
- **Distribution**: Expected zero-inflation and right skew

---

### Mental Health Days Not Good

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | HSQ480 |
| **Analytical Variable** | `mental_health_days` |
| **Manuscript Label** | Mental Health Days Not Good |
| **Description** | Number of days in the past 30 days when mental health was not good |
| **Scale** | Count variable (0-30 days) |
| **Type** | Discrete numeric |

#### Valid Values
| Value | Meaning | Handling |
|-------|---------|----------|
| 0-30 | Number of days | Include |
| 77 | Refused | Exclude |
| 99 | Don't know | Exclude |
| . | Missing | Exclude |

#### Handling Instructions
- **Confounder**: Include in adjusted models
- **Potential mediator**: Assess in sensitivity analysis
- **Categorization**: Can be analyzed as continuous or categorized (0, 1-7, 8-14, 15-30)

---

### Activity Limitation Days

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | HSQ490 |
| **Analytical Variable** | `activity_limitation_days` |
| **Manuscript Label** | Activity Limitation Days |
| **Description** | Number of days when poor health kept respondent from usual activities |
| **Scale** | Count variable (0-30 days) |
| **Type** | Discrete numeric |

#### Valid Values
| Value | Meaning | Handling |
|-------|---------|----------|
| 0-30 | Number of days | Include |
| 77 | Refused | Exclude |
| 99 | Don't know | Exclude |
| . | Missing | Exclude |

---

## Primary Exposure: Chronic Condition Count

### Overview
The chronic condition count is a derived composite variable summing confirmed diagnoses of major chronic diseases.

| Attribute | Specification |
|-----------|---------------|
| **Analytical Variable** | `chronic_condition_count` |
| **Manuscript Label** | Chronic Condition Count |
| **Description** | Sum of confirmed chronic disease diagnoses |
| **Range** | 0-4+ (collapsed to 0, 1, 2, 3+) |
| **Type** | Ordinal categorical |

### Component Conditions

#### 1. Diabetes

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | DIQ010 |
| **Question** | "Other than during pregnancy, have you ever been told by a doctor or health professional that you have diabetes or sugar diabetes?" |

| Value | Meaning | Counts As |
|-------|---------|-----------|
| 1 | Yes | 1 condition |
| 2 | No | 0 conditions |
| 3 | Borderline | 0 conditions |
| 7 | Refused | Missing |
| 9 | Don't know | Missing |
| . | Missing | Missing |

**Notes**:
- Borderline cases excluded from count
- Gestational diabetes only excluded
- Requires doctor diagnosis

---

#### 2. Hypertension

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | BPQ020 |
| **Question** | "Have you ever been told by a doctor or other health professional that you had hypertension, also called high blood pressure?" |

| Value | Meaning | Counts As |
|-------|---------|-----------|
| 1 | Yes | 1 condition |
| 2 | No | 0 conditions |
| 7 | Refused | Missing |
| 9 | Don't know | Missing |
| . | Missing | Missing |

**Notes**:
- Based on physician diagnosis only
- Current medication status not required

---

#### 3. Cardiovascular Disease

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variables** | CDQ001, CDQ010, CDQ020 (varies by cycle) |
| **Question** | "Have you ever had any pain or discomfort in your chest?" / "Do you get chest pain or discomfort when you walk uphill or hurry?" |

| Variable | Value | Meaning | Counts As |
|----------|-------|---------|-----------|
| CDQ001 | 1 | Yes | CVD indicator |
| CDQ001 | 2 | No | Not CVD |
| CDQ010 | 1 | Yes | CVD indicator |
| CDQ020 | 1 | Yes | Angina indicator |

**Derivation Rule**:
```python
cvd = 1 if (CDQ001 == 1 or CDQ010 == 1 or CDQ020 == 1) else 0
```

**Notes**:
- Variable availability varies by cycle
- Uses self-reported chest pain/angina history
- Proxy for coronary heart disease

---

### Chronic Condition Count Derivation

```python
def calculate_chronic_count(row):
    """
    Calculate chronic condition count from component conditions
    """
    conditions = [
        row['diabetes'],      # DIQ010 == 1
        row['hypertension'],  # BPQ020 == 1
        row['cvd']            # CDQ-derived
    ]
    
    # Sum valid conditions (excluding missing)
    valid_conditions = [c for c in conditions if pd.notna(c)]
    count = sum(valid_conditions)
    
    return count
```

### Final Categories

| Category | Count Range | Manuscript Label | Reference |
|----------|-------------|------------------|-----------|
| 0 | 0 conditions | No chronic conditions | ✓ Reference |
| 1 | 1 condition | One chronic condition | |
| 2 | 2 conditions | Two chronic conditions | |
| 3+ | 3+ conditions | Three or more chronic conditions | |

---

## Demographic Variables

### Age

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | RIDAGEYR |
| **Analytical Variables** | `age`, `age_centered`, `age_squared` |
| **Manuscript Label** | Age (years) |
| **Description** | Age at screening adjudicated |
| **Scale** | Continuous (years) |
| **Range** | 60-85 (top-coded at 85) |

#### Valid Values
| Value | Meaning | Handling |
|-------|---------|----------|
| 60-84 | Exact age | Include |
| 85 | 85 or older | Include (top-coded) |
| <60 | Younger than 60 | Exclude (study population) |
| . | Missing | Exclude |

#### Derived Variables

**Age Centered**:
```python
age_centered = RIDAGEYR - 70  # Centered at 70 years
```

**Age Squared**:
```python
age_squared = age_centered ** 2
```

**Age Categories**:
| Category | Range | Manuscript Label |
|----------|-------|------------------|
| 1 | 60-69 years | Young-old |
| 2 | 70-79 years | Middle-old |
| 3 | 80+ years | Oldest-old |

---

### Sex/Gender

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | RIAGENDR |
| **Analytical Variable** | `sex` |
| **Manuscript Label** | Sex |
| **Description** | Biological sex |

#### Valid Values
| Value | Meaning | Study Inclusion |
|-------|---------|-----------------|
| 1 | Male | ✓ Include |
| 2 | Female | ✗ Exclude |
| . | Missing | Exclude |

**Note**: This study includes only males (RIAGENDR = 1).

---

### Race/Ethnicity

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | RIDRETH1 |
| **Analytical Variable** | `race_ethnicity` |
| **Manuscript Label** | Race/Ethnicity |
| **Description** | Recode of reported race and ethnicity |
| **Type** | Categorical |

#### Categories
| Value | NHANES Label | Analytical Code | Manuscript Label | Dummy Variables |
|-------|--------------|-----------------|------------------|-----------------|
| 1 | Mexican American | 1 | Mexican American | race_mex |
| 2 | Other Hispanic | 2 | Other Hispanic | race_hispother |
| 3 | Non-Hispanic White | 3 (ref) | Non-Hispanic White | — |
| 4 | Non-Hispanic Black | 4 | Non-Hispanic Black | race_black |
| 5 | Other Race | 5 | Other/Multiracial | race_other |
| . | Missing | — | — | Exclude |

#### Dummy Variable Coding
```python
# Reference: Non-Hispanic White (value = 3)
race_mex = 1 if RIDRETH1 == 1 else 0
race_hispother = 1 if RIDRETH1 == 2 else 0
race_black = 1 if RIDRETH1 == 4 else 0
race_other = 1 if RIDRETH1 == 5 else 0
```

---

## Socioeconomic Status Variables

### Education

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | DMDEDUC2 |
| **Analytical Variable** | `education` |
| **Manuscript Label** | Educational Attainment |
| **Description** | Highest grade or level of education completed |
| **Type** | Categorical |

#### Original Categories
| Value | Meaning |
|-------|---------|
| 1 | Less than 9th grade |
| 2 | 9-11th grade (includes 12th grade with no diploma) |
| 3 | High school graduate/GED or equivalent |
| 4 | Some college or AA degree |
| 5 | College graduate or above |
| 7 | Refused |
| 9 | Don't know |
| . | Missing |

#### Harmonized Categories
| Category | Original Values | Analytical Code | Manuscript Label | Dummy Variable |
|----------|-----------------|-----------------|------------------|----------------|
| < High School | 1, 2 | 1 | Less than High School | edu_lt_hs |
| High School/GED | 3 | 2 | High School Graduate/GED | edu_hs |
| Some College | 4 | 3 | Some College/AA Degree | edu_somecoll |
| College+ | 5 | 4 (ref) | College Graduate or Higher | — |
| Missing | 7, 9, . | — | — | Exclude |

#### Dummy Variable Coding
```python
# Reference: College Graduate or Higher (value = 4)
edu_lt_hs = 1 if DMDEDUC2 in [1, 2] else 0
edu_hs = 1 if DMDEDUC2 == 3 else 0
edu_somecoll = 1 if DMDEDUC2 == 4 else 0
```

---

### Income-to-Poverty Ratio

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | INDFMPIR |
| **Analytical Variable** | `pir` |
| **Manuscript Label** | Income-to-Poverty Ratio |
| **Description** | Ratio of family income to federal poverty threshold |
| **Scale** | Continuous |
| **Range** | 0-5 (top-coded at 5.0) |

#### Valid Values
| Value | Meaning | Handling |
|-------|---------|----------|
| 0-5 | Ratio value | Include |
| 5 | ≥5 (top-coded) | Include |
| . | Missing | Exclude if no imputation |

#### Interpretation
| Range | Category |
|-------|----------|
| 0 to <1 | Below poverty |
| 1 to <2 | 100-199% of poverty |
| 2 to <3 | 200-299% of poverty |
| 3 to <5 | 300-499% of poverty |
| 5 | 500%+ of poverty |

**Notes**:
- Higher values indicate higher socioeconomic status
- Top-coded at 5.0 across all cycles
- Missing for approximately 5-10% of respondents

---

### Marital Status

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | DMDMARTL |
| **Analytical Variable** | `marital_status` |
| **Manuscript Label** | Marital Status |
| **Type** | Categorical |

#### Harmonized Categories (may vary slightly by cycle)
| Category | Typical Values | Analytical Code | Manuscript Label | Dummy Variable |
|----------|----------------|-----------------|------------------|----------------|
| Married/Partner | 1 | 1 (ref) | Married or Living with Partner | — |
| Widowed | 2 | 2 | Widowed | marital_widowed |
| Divorced/Separated | 3, 4, 5 | 3 | Divorced or Separated | marital_divorced |
| Never Married | 6 | 4 | Never Married | marital_never |
| Missing | 77, 99, . | — | — | Exclude |

#### Dummy Variable Coding
```python
# Reference: Married or Living with Partner
marital_widowed = 1 if DMDMARTL == 2 else 0
marital_divorced = 1 if DMDMARTL in [3, 4, 5] else 0
marital_never = 1 if DMDMARTL == 6 else 0
```

---

## Health-Related Variables

### Health Insurance

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | HIQ011 |
| **Analytical Variable** | `insurance` |
| **Manuscript Label** | Health Insurance Coverage |
| **Type** | Binary |

| Value | Meaning | Analytical Code | Handling |
|-------|---------|-----------------|----------|
| 1 | Yes, covered by insurance | 1 (ref) | Include |
| 2 | No, not covered | 0 | Include |
| 7 | Refused | — | Exclude |
| 9 | Don't know | — | Exclude |
| . | Missing | — | Exclude |

#### Reference Category
- **Insured** (coded as 1) = Reference category
- **Uninsured** (coded as 0) = Comparison group

---

### Smoking Status

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variables** | SMQ020, SMQ040 |
| **Analytical Variable** | `smoking_status` |
| **Manuscript Label** | Smoking Status |
| **Type** | Categorical |

#### Derivation Logic
```python
def derive_smoking_status(row):
    ever_smoked = row['SMQ020'] == 1
    current_smoking = row['SMQ040'] in [1, 2]  # Every day or some days
    
    if not ever_smoked:
        return 'never'  # Never smoker
    elif ever_smoked and not current_smoking:
        return 'former'  # Former smoker
    elif ever_smoked and current_smoking:
        return 'current'  # Current smoker
    else:
        return None  # Missing
```

#### Categories
| Category | SMQ020 | SMQ040 | Analytical Code | Manuscript Label | Dummy Variable |
|----------|--------|--------|-----------------|------------------|----------------|
| Never | 2 | N/A | 1 (ref) | Never Smoker | — |
| Former | 1 | 3 | 2 | Former Smoker | smoke_former |
| Current | 1 | 1 or 2 | 3 | Current Smoker | smoke_current |
| Missing | 7, 9, . | 7, 9, . | — | — | Exclude |

---

### Body Mass Index

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | BMXBMI |
| **Analytical Variable** | `bmi`, `bmi_category` |
| **Manuscript Label** | Body Mass Index (kg/m²) |
| **Scale** | Continuous |
| **Range** | Valid range: 10-70 |

#### Valid Values
| Value | Meaning | Handling |
|-------|---------|----------|
| 10-70 | BMI value | Include |
| <10 or >70 | Implausible | Exclude as outlier |
| . | Missing | Exclude |

#### Categorization
| Category | BMI Range | Analytical Code | Manuscript Label | Dummy Variable |
|----------|-----------|-----------------|------------------|----------------|
| Normal | 18.5-24.9 | 1 (ref) | Normal Weight | — |
| Overweight | 25.0-29.9 | 2 | Overweight | bmi_over |
| Obese | ≥30.0 | 3 | Obese | bmi_obese |
| Underweight | <18.5 | — | — | Exclude (insufficient n) |

```python
# Derivation
def categorize_bmi(bmi):
    if pd.isna(bmi):
        return None
    elif bmi < 18.5:
        return 'underweight'  # May exclude
    elif bmi < 25:
        return 'normal'  # Reference
    elif bmi < 30:
        return 'overweight'
    else:
        return 'obese'

bmi_over = 1 if bmi_category == 'overweight' else 0
bmi_obese = 1 if bmi_category == 'obese' else 0
```

---

### Physical Activity

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variables** | PAQ650, PAQ665, PAQ620, PAQ605 (varies by cycle) |
| **Analytical Variable** | `physical_activity` |
| **Manuscript Label** | Physical Activity Level |
| **Type** | Categorical |
| **Note** | Variable definitions vary across cycles |

#### Cycle-Specific Harmonization

**Cycles B-D (2001-2006)**:
- Used PAQIAF (detailed physical activity questionnaire)
- Variables: PADACTIV, PADDURAT, PADMETS

**Cycles E-J (2007-2018)**:
- Used PAQ (standard questionnaire)
- Variables: PAQ650 (vigorous), PAQ665 (moderate)

#### Harmonized Categories
```python
def derive_physical_activity(row, cycle):
    """
    Harmonize physical activity across cycles
    """
    if cycle in ['B', 'C', 'D']:
        # Use PAQIAF if available, else questionnaire
        vigorous = row.get('vigorous_activity_indicator', 0)
        moderate = row.get('moderate_activity_indicator', 0)
    else:
        # Use standard PAQ
        vigorous = row.get('PAQ650') == 1
        moderate = row.get('PAQ665') == 1
    
    if vigorous:
        return 'vigorous'  # Reference
    elif moderate:
        return 'moderate'
    else:
        return 'inactive'
```

#### Categories
| Category | Definition | Analytical Code | Manuscript Label | Dummy Variable |
|----------|------------|-----------------|------------------|----------------|
| Vigorous | Any vigorous activity | 1 (ref) | Vigorous Activity | — |
| Moderate | Moderate but no vigorous | 2 | Moderate Activity Only | pa_moderate |
| Inactive | No moderate or vigorous | 3 | Inactive | pa_inactive |
| Missing | — | — | — | Exclude |

---

## Survey Design Variables

### Primary Sampling Unit (PSU)

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | SDMVPSU |
| **Analytical Variable** | `psu` |
| **Manuscript Label** | Masked Variance Unit PSU |
| **Description** | Pseudo-PSU for variance estimation |
| **Type** | Cluster identifier |
| **Required** | Yes - all analyses |

**Usage**: Specify as clustering variable in survey design

---

### Strata

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | SDMVSTRA |
| **Analytical Variable** | `strata` |
| **Manuscript Label** | Masked Variance Unit Stratum |
| **Description** | Pseudo-stratum for variance estimation |
| **Type** | Stratification identifier |
| **Required** | Yes - all analyses |

**Usage**: Specify as stratification variable in survey design

---

### Sample Weight

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | WTMEC2YR |
| **Analytical Variable** | `weight` |
| **Manuscript Label** | 2-Year MEC Examination Weight |
| **Description** | Full sample 2-year MEC examination weight |
| **Type** | Sampling weight |
| **Required** | Yes - all analyses |

#### Weight Adjustment for Pooling
```python
# For 9-cycle pooled analysis
data['weight_adjusted'] = data['WTMEC2YR'] / 9
```

**Rationale**: Dividing by number of cycles ensures weighted estimates represent average population size across study period rather than cumulative population.

---

## Auxiliary Variables

### General Health Status

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | HSD010 |
| **Analytical Variable** | `general_health` |
| **Manuscript Label** | Self-Rated General Health |
| **Type** | Ordinal |

| Value | Meaning | Category |
|-------|---------|----------|
| 1 | Excellent | Very Good/Excellent |
| 2 | Very Good | Very Good/Excellent |
| 3 | Good | Good |
| 4 | Fair | Fair/Poor |
| 5 | Poor | Fair/Poor |
| 7 | Refused | Exclude |
| 9 | Don't know | Exclude |

**Usage**: Potential stratification variable, descriptive analyses

---

### Survey Cycle Indicator

| Attribute | Specification |
|-----------|---------------|
| **Derived Variable** | SDDSRVYR |
| **Analytical Variable** | `cycle` |
| **Manuscript Label** | NHANES Survey Cycle |

| Value | Years | Analytical Code |
|-------|-------|-----------------|
| 2 | 2001-2002 | B |
| 3 | 2003-2004 | C |
| 4 | 2005-2006 | D |
| 5 | 2007-2008 | E |
| 6 | 2009-2010 | F |
| 7 | 2011-2012 | G |
| 8 | 2013-2014 | H |
| 9 | 2015-2016 | I |
| 10 | 2017-2018 | J |

**Usage**: Temporal trend analysis, cycle-stratified analyses

---

## Missing Value Handling Summary

### Missing Value Codes
NHANES uses standardized missing value codes:
- **7 or 77 or 777...**: Refused
- **9 or 99 or 999...**: Don't know
- **.** (dot): System missing

### Handling Strategy by Variable Type

| Variable Type | Strategy |
|--------------|----------|
| **Primary Outcome** | Exclude if missing (listwise deletion) |
| **Primary Exposure** | Exclude if missing |
| **Key Confounders** | Exclude if missing (complete case) |
| **Secondary Variables** | Exclude if missing |
| **Survey Design Vars** | Exclude if missing (required) |

### Missing Data Reporting
All analyses will report:
1. Number and percentage missing for each variable
2. Comparison of missing vs. non-missing on key characteristics
3. Missing data patterns (MCAR, MAR assessment)
4. Sensitivity analysis with multiple imputation

---

## Variable Mapping Quick Reference

### For Manuscript Preparation

| NHANES Code | Human-Readable Label | Variable Type |
|-------------|---------------------|---------------|
| HSQ470 | Physical Health Days Not Good | Outcome (count) |
| HSQ480 | Mental Health Days Not Good | Confounder (count) |
| HSQ490 | Activity Limitation Days | Secondary outcome |
| DIQ010 | Diabetes Diagnosis | Chronic condition |
| BPQ020 | Hypertension Diagnosis | Chronic condition |
| CDQ001/CDQ010 | Cardiovascular Disease | Chronic condition |
| RIDAGEYR | Age (years) | Confounder (continuous) |
| RIDRETH1 | Race/Ethnicity | Confounder (categorical) |
| DMDEDUC2 | Educational Attainment | Confounder (categorical) |
| INDFMPIR | Income-to-Poverty Ratio | Confounder (continuous) |
| DMDMARTL | Marital Status | Confounder (categorical) |
| HIQ011 | Health Insurance Coverage | Confounder (binary) |
| SMQ020/SMQ040 | Smoking Status | Confounder (categorical) |
| BMXBMI | Body Mass Index | Confounder (continuous) |
| PAQ650/PAQ665 | Physical Activity Level | Exposure/Confounder |
| SDMVPSU | Primary Sampling Unit | Survey design |
| SDMVSTRA | Stratum | Survey design |
| WTMEC2YR | MEC Examination Weight | Survey design |

---

## Data Dictionary Summary Table

| Variable Name | Type | Role | Valid Range | Missing Values |
|--------------|------|------|-------------|----------------|
| physical_health_days | Count | Outcome | 0-30 | Exclude 77, 99, . |
| mental_health_days | Count | Confounder | 0-30 | Exclude 77, 99, . |
| chronic_condition_count | Ordinal | Primary Exposure | 0-3+ | Exclude if missing |
| age | Continuous | Confounder | 60-85 | Exclude <60, . |
| race_ethnicity | Categorical | Confounder | 1-5 | Exclude . |
| education | Categorical | Confounder | 1-4 | Exclude 7, 9, . |
| pir | Continuous | Confounder | 0-5 | Exclude . |
| marital_status | Categorical | Confounder | 1-4 | Exclude 77, 99, . |
| insurance | Binary | Confounder | 0-1 | Exclude 7, 9, . |
| smoking_status | Categorical | Confounder | 1-3 | Exclude missing |
| bmi_category | Categorical | Confounder | 1-3 | Exclude . |
| physical_activity | Categorical | Exposure | 1-3 | Exclude missing |

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-08  
**Maintained By**: Methods Definition Agent  
**Review Cycle**: Updated as variables added/modified
