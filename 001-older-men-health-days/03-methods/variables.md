# Variables Documentation

## Study: Factors Associated with Poor Physical Health Days Among Older Men (60+)

This document provides detailed documentation of all variables used in the analysis, including variable definitions, coding schemes, and analytical specifications.

---

## Variable Evidence Table

| Variable Concept | NHANES Variable(s) | Dataset File(s) | Doc File(s) | Year Coverage | Final Human-Readable Label |
|------------------|-------------------|-----------------|-------------|---------------|---------------------------|
| Poor Physical Health Days | HSQ470 | HSQ_B.csv through HSQ_J.csv | HSQ_B_dictionary.csv through HSQ_J_dictionary.csv | 2001-2018 (B-J) | Poor Physical Health Days (Past 30 Days) |
| Poor Mental Health Days | HSQ480 | HSQ_B.csv through HSQ_J.csv | HSQ_B_dictionary.csv through HSQ_J_dictionary.csv | 2001-2018 (B-J) | Poor Mental Health Days (Past 30 Days) |
| Activity Limitation Days | HSQ490 | HSQ_B.csv through HSQ_J.csv | HSQ_B_dictionary.csv through HSQ_J_dictionary.csv | 2001-2018 (B-J) | Activity Limitation Days (Past 30 Days) |
| General Health Status | HSD010 | HSQ_B.csv through HSQ_J.csv | HSQ_B_dictionary.csv through HSQ_J_dictionary.csv | 2001-2018 (B-J) | General Health Status |
| Diabetes Diagnosis | DIQ010 | DIQ_B.csv through DIQ_J.csv | DIQ_B_dictionary.csv through DIQ_J_dictionary.csv | 2001-2018 (B-J) | Diabetes Diagnosis |
| Hypertension Diagnosis | BPQ020 | BPQ_B.csv through BPQ_J.csv | BPQ_B_dictionary.csv through BPQ_J_dictionary.csv | 2001-2018 (B-J) | Hypertension Diagnosis |
| Cardiovascular Disease History | CDQ001, CDQ009 | CDQ_B.csv through CDQ_J.csv | CDQ_B_dictionary.csv through CDQ_J_dictionary.csv | 2001-2018 (B-J) | Cardiovascular Disease History |
| High Cholesterol Diagnosis | BPQ080 | BPQ_B.csv through BPQ_J.csv | BPQ_B_dictionary.csv through BPQ_J_dictionary.csv | 2001-2018 (B-J) | High Cholesterol Diagnosis |
| Age | RIDAGEYR | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Age (Years) |
| Sex | RIAGENDR | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Sex |
| Race/Ethnicity | RIDRETH1 | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Race/Ethnicity |
| Marital Status | DMDMARTL | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Marital Status |
| Education Level | DMDEDUC2 | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Education Level |
| Income-to-Poverty Ratio | INDFMPIR | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Income-to-Poverty Ratio |
| Health Insurance Coverage | HIQ011 | HIQ_B.csv through HIQ_J.csv | HIQ_B_dictionary.csv through HIQ_J_dictionary.csv | 2001-2018 (B-J) | Health Insurance Coverage |
| Vigorous Work Activity | PAQ605 | PAQ_B.csv through PAQ_J.csv | PAQ_B_dictionary.csv through PAQ_J_dictionary.csv | 2001-2018 (B-J) | Vigorous Work Activity |
| Moderate Work Activity | PAQ620 | PAQ_B.csv through PAQ_J.csv | PAQ_B_dictionary.csv through PAQ_J_dictionary.csv | 2001-2018 (B-J) | Moderate Work Activity |
| Active Transportation | PAQ635 | PAQ_B.csv through PAQ_J.csv | PAQ_B_dictionary.csv through PAQ_J_dictionary.csv | 2001-2018 (B-J) | Active Transportation |
| Vigorous Recreational Activity | PAQ650 | PAQ_B.csv through PAQ_J.csv | PAQ_B_dictionary.csv through PAQ_J_dictionary.csv | 2001-2018 (B-J) | Vigorous Recreational Activity |
| Moderate Recreational Activity | PAQ665 | PAQ_B.csv through PAQ_J.csv | PAQ_B_dictionary.csv through PAQ_J_dictionary.csv | 2001-2018 (B-J) | Moderate Recreational Activity |
| Smoking Status | SMQ020, SMQ040 | SMQ_B.csv through SMQ_J.csv | SMQ_B_dictionary.csv through SMQ_J_dictionary.csv | 2001-2018 (B-J) | Smoking Status |
| Body Mass Index | BMXBMI | BMX_B.csv through BMX_J.csv | BMX_B_dictionary.csv through BMX_J_dictionary.csv | 2001-2018 (B-J) | Body Mass Index (kg/m²) |
| Waist Circumference | BMXWAIST | BMX_B.csv through BMX_J.csv | BMX_B_dictionary.csv through BMX_J_dictionary.csv | 2001-2018 (B-J) | Waist Circumference (cm) |
| Sample Weights | WTMEC2YR | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Sample Weights |
| Primary Sampling Unit | SDMVPSU | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Primary Sampling Unit |
| Stratum Identifier | SDMVSTRA | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Stratum Identifier |

---

## Outcome Variables

### Primary Outcome: Poor Physical Health Days

| Attribute | Specification |
|-----------|--------------|
| **NHANES Variable** | HSQ470 |
| **Question Text** | "Thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good?" |
| **Response Range** | 0-30 days |
| **Special Codes** | 77 = Refused, 99 = Don't know |
| **Variable Type** | Continuous (count) |
| **Distribution Expected** | Right-skewed, zero-inflated |
| **Analytical Approach** | Linear regression (primary), Negative binomial (sensitivity) |
| **Label** | Poor Physical Health Days (Past 30 Days) |

**Handling Notes**:
- Exclude observations with values 77 or 99
- Treat as continuous variable (0-30)
- Consider log transformation if highly skewed
- Alternative categorization: 0, 1-7, 8-14, 15-30 days

### Secondary Outcome: Poor Mental Health Days

| Attribute | Specification |
|-----------|--------------|
| **NHANES Variable** | HSQ480 |
| **Question Text** | "Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good?" |
| **Response Range** | 0-30 days |
| **Special Codes** | 77 = Refused, 99 = Don't know |
| **Variable Type** | Continuous (count) |
| **Analytical Role** | Secondary outcome; mediator/exposure in H2 |
| **Label** | Poor Mental Health Days (Past 30 Days) |

### Secondary Outcome: Activity Limitation Days

| Attribute | Specification |
|-----------|--------------|
| **NHANES Variable** | HSQ490 |
| **Question Text** | "During the past 30 days, for about how many days did poor physical or mental health keep you from doing your usual activities, such as self-care, work, school or recreation?" |
| **Response Range** | 0-30 days |
| **Special Codes** | 77 = Refused, 99 = Don't know |
| **Variable Type** | Continuous (count) |
| **Analytical Role** | Secondary outcome (H6) |
| **Label** | Activity Limitation Days (Past 30 Days) |

### Secondary Outcome: General Health Status

| Attribute | Specification |
|-----------|--------------|
| **NHANES Variable** | HSD010 |
| **Question Text** | "Would you say your health in general is..." |
| **Response Options** | 1=Excellent, 2=Very Good, 3=Good, 4=Fair, 5=Poor |
| **Special Codes** | 7 = Refused, 9 = Don't know |
| **Variable Type** | Ordinal categorical |
| **Analytical Role** | Descriptive; validation of physical health days |
| **Label** | General Health Status |

---

## Primary Exposure Variables

### Chronic Condition Variables

#### Diabetes Diagnosis (DIQ010)

| Attribute | Specification |
|-----------|--------------|
| **Question** | "The next questions are about specific medical conditions. Has a doctor or other health professional ever told you that you have diabetes or sugar diabetes?" |
| **Response Options** | 1=Yes, 2=No, 3=Borderline, 7=Refused, 9=Don't know |
| **Analytical Coding** | 1=Yes (includes borderline), 0=No |
| **Missing Handling** | Exclude 7, 9; or impute as No |
| **Label** | Diabetes Diagnosis |

#### Hypertension Diagnosis (BPQ020)

| Attribute | Specification |
|-----------|--------------|
| **Question** | "Has a doctor or other health professional ever told you that you had hypertension, also called high blood pressure?" |
| **Response Options** | 1=Yes, 2=No, 7=Refused, 9=Don't know |
| **Analytical Coding** | 1=Yes, 0=No |
| **Missing Handling** | Exclude 7, 9; or impute as No |
| **Label** | Hypertension Diagnosis |

#### Cardiovascular Disease History

Derived from multiple CDQ variables:

| Component Variable | Question |
|-------------------|----------|
| CDQ001 | "Have you ever had any pain or discomfort in your chest?" |
| CDQ009 | "Have you ever had severe chest pain lasting more than half an hour?" |

**Derivation Rule**:
```
CVD = 1 if (CDQ001 = 1) OR (CDQ009 = 1)
CVD = 0 otherwise
```

| Attribute | Specification |
|-----------|--------------|
| **Variable Type** | Binary (derived) |
| **Analytical Coding** | 1=CVD history, 0=No CVD history |
| **Label** | Cardiovascular Disease History |

#### Chronic Condition Count (Derived)

| Attribute | Specification |
|-----------|--------------|
| **Derivation** | Sum of: Diabetes + Hypertension + CVD |
| **Range** | 0 to 3+ |
| **Categories** | 0 (none), 1 (single), 2 (two), 3+ (multiple) |
| **Variable Type** | Categorical |
| **Reference Category** | 0 (no chronic conditions) |
| **Label** | Number of Chronic Conditions |

---

## Demographic Variables

### Age (RIDAGEYR)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Age at screening in years |
| **Range** | 0-150 years |
| **Study Population** | ≥60 years |
| **Variable Type** | Continuous |
| **Centering** | Consider centering at 60 or 70 for interpretation |
| **Categories for Stratification** | 60-69, 70-79, 80+ |
| **Label** | Age (Years) |

### Sex (RIAGENDR)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Gender of participant |
| **Values** | 1=Male, 2=Female |
| **Study Population** | Males only (RIAGENDR = 1) |
| **Analytical Role** | Inclusion criterion only |
| **Label** | Sex |

### Race/Ethnicity (RIDRETH1)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Race/Hispanic origin recode |
| **Original Values** | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 5=Other/Multi-racial |
| **Categories** | Mexican American, Other Hispanic, Non-Hispanic White (Ref), Non-Hispanic Black, Other/Multi-racial |
| **Variable Type** | Categorical |
| **Reference** | Non-Hispanic White |
| **Label** | Race/Ethnicity |

### Marital Status (DMDMARTL)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Marital status |
| **Values** | 1=Married, 2=Widowed, 3=Divorced, 4=Separated, 5=Never married, 6=Living with partner |
| **Recoding for Analysis** | Married (1,6), Widowed (2), Divorced/Separated (3,4), Never married (5) |
| **Variable Type** | Categorical |
| **Label** | Marital Status |

---

## Socioeconomic Variables

### Education Level (DMDEDUC2)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Highest grade or level of education completed |
| **Original Values** | 1=<9th grade, 2=9-11th grade, 3=High school grad, 4=Some college, 5=College grad or above, 7=Refused, 9=Don't know |
| **Analytical Categories** | Less than HS (1-2), High school grad (3), Some college (4), College grad+ (5) |
| **Variable Type** | Categorical |
| **Reference** | College graduate or above |
| **Missing** | Exclude 7, 9 |
| **Label** | Education Level |

### Income-to-Poverty Ratio (INDFMPIR)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Ratio of family income to poverty threshold |
| **Range** | 0 to 5+ (capped at 5.0) |
| **Variable Type** | Continuous |
| **Categories** | <1.0 (poor), 1.0-1.99 (near poor), 2.0-3.99 (middle), 4.0+ (high) |
| **Label** | Income-to-Poverty Ratio |

### Health Insurance Coverage (HIQ011)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Covered by health insurance |
| **Values** | 1=Yes, 2=No, 7=Refused, 9=Don't know |
| **Analytical Coding** | 1=Insured, 0=Uninsured |
| **Missing Handling** | Exclude 7, 9 |
| **Label** | Health Insurance Coverage |

---

## Health Behavior Variables

### Physical Activity Level (Derived)

Derived from multiple PAQ variables:

| Source Variable | Description |
|-----------------|-------------|
| PAQ605 | Vigorous work activity |
| PAQ620 | Moderate work activity |
| PAQ635 | Walk or bicycle for transportation |
| PAQ650 | Vigorous recreational activities |
| PAQ665 | Moderate recreational activities |

**Derivation Algorithm**:

```
IF (PAQ605 = 1) OR (PAQ650 = 1) THEN High Activity
ELSE IF (PAQ620 = 1 AND PAQ665 = 1) THEN Moderate Activity
ELSE IF (PAQ620 = 1 OR PAQ635 = 1 OR PAQ665 = 1) THEN Low Activity
ELSE Inactive
```

| Attribute | Specification |
|-----------|--------------|
| **Categories** | Inactive, Low, Moderate, High |
| **Variable Type** | Ordinal categorical |
| **Reference** | Inactive |
| **Label** | Physical Activity Level |

### Smoking Status (Derived)

Derived from SMQ020 and SMQ040:

| Source Variable | Description |
|-----------------|-------------|
| SMQ020 | Smoked at least 100 cigarettes in life |
| SMQ040 | Do you now smoke cigarettes? |

**Derivation Algorithm**:

```
IF SMQ020 = 2 THEN Never Smoker
ELSE IF SMQ040 = 3 THEN Former Smoker
ELSE IF SMQ040 IN (1, 2) THEN Current Smoker
```

| Attribute | Specification |
|-----------|--------------|
| **Categories** | Never, Former, Current |
| **Variable Type** | Categorical |
| **Reference** | Never smoker |
| **Label** | Smoking Status |

---

## Anthropometric Variables

### Body Mass Index (BMXBMI)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Body mass index (kg/m²) |
| **Calculation** | Weight (kg) / Height (m)² |
| **Range** | Typically 10-80 |
| **Categories** | <18.5 (Underweight), 18.5-24.9 (Normal), 25.0-29.9 (Overweight), ≥30.0 (Obese) |
| **Variable Type** | Continuous (or categorical) |
| **Outlier Handling** | Exclude <10 or >80 |
| **Label** | Body Mass Index (kg/m²) |

### Waist Circumference (BMXWAIST)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Waist circumference in cm |
| **Range** | Typically 40-200 cm |
| **Variable Type** | Continuous |
| **Outlier Handling** | Exclude <40 or >200 |
| **Label** | Waist Circumference (cm) |

---

## Survey Design Variables

### Sample Weights (WTMEC2YR)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Full sample 2-year MEC exam weights |
| **Usage** | All analyses must use weights |
| **Adjustment** | Divide by number of cycles when pooling (2-year weights) |
| **Label** | Sample Weights |

### Primary Sampling Unit (SDMVPSU)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Masked variance pseudo-PSU |
| **Values** | 1-2 per stratum |
| **Usage** | Required for variance estimation |
| **Label** | Primary Sampling Unit |

### Stratum Identifier (SDMVSTRA)

| Attribute | Specification |
|-----------|--------------|
| **Description** | Masked variance pseudo-stratum |
| **Values** | 1-98 |
| **Usage** | Required for variance estimation |
| **Label** | Stratum Identifier |

---

## Variable Transformations and Derived Measures

### Binary Indicators for Analysis

| Derived Variable | Base Variable | Threshold | Interpretation |
|-----------------|--------------|-----------|----------------|
| Poor Physical Health | HSQ470 | ≥14 days | Frequent poor physical health |
| Poor Mental Health | HSQ480 | ≥14 days | Frequent poor mental health |
| Activity Limitation | HSQ490 | ≥1 day | Any activity limitation |
| Has Any Chronic Condition | Condition Count | ≥1 | Presence of chronic disease |
| Multimorbidity | Condition Count | ≥2 | Multiple chronic conditions |
| Obesity | BMXBMI | ≥30 kg/m² | Obese status |
| Low Income | INDFMPIR | <1.0 | Below poverty line |

### Continuous Variable Standardization

| Variable | Standardization Approach |
|----------|-------------------------|
| Age | Center at 60 years; optional: standardize to z-scores |
| Income-to-Poverty Ratio | Cap at 5.0; consider log transformation |
| BMI | Center at 25 kg/m²; consider categorization |
| Physical Health Days | Consider log(x+1) transformation if skewed |

---

## Missing Data Specifications

### Variable-Specific Missing Data Handling

| Variable | Missing Codes | Handling Strategy |
|----------|--------------|---------------------|
| HSQ470, HSQ480, HSQ490 | 77, 99 | Exclude from analysis (listwise deletion) |
| DIQ010 | 7, 9 | Exclude or code as No |
| BPQ020 | 7, 9 | Exclude or code as No |
| DMDEDUC2 | 7, 9 | Exclude from analysis |
| INDFMPIR | Blank/missing | Exclude from analysis |
| HIQ011 | 7, 9 | Exclude from analysis |
| BMXBMI | Blank | Exclude from analysis |

### Missing Data Assessment

1. Calculate missing data proportions for each variable
2. Compare characteristics of complete vs. incomplete cases
3. Conduct sensitivity analyses with multiple imputation if >5% missing
4. Document exclusions in STROBE flow diagram

---

## Variable Groupings for Analysis

### Model 1: Crude Model
- **Outcome**: HSQ470
- **Exposure**: Chronic condition count
- **No covariates**

### Model 2: Demographic-Adjusted
- **Outcome**: HSQ470
- **Exposure**: Chronic condition count
- **Covariates**: Age, race/ethnicity

### Model 3: Fully Adjusted
- **Outcome**: HSQ470
- **Exposure**: Chronic condition count
- **Covariates**: 
  - Demographic: Age, race/ethnicity, marital status
  - Socioeconomic: Education, income-to-poverty ratio, insurance
  - Clinical: BMI, smoking status
  - Behavioral: Physical activity level

### Secondary Analyses
- Same model structures with HSQ480, HSQ490 as outcomes
- Stratified analyses by age group, race/ethnicity
- Interaction models (chronic conditions × physical activity, etc.)

---

*Document Version: 1.0*
*Date: 2026-02-08*
*Study: older-men-health-days-2026-02-08*
