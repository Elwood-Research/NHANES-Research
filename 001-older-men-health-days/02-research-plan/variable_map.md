# Variable Map: Older Men and Physical Health Days Study

## Overview

This document provides a comprehensive mapping of all variables used in the study, including their locations, definitions, and analytical roles.

---

## Outcome Variables

### Primary Outcome

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Physical Health Days | Poor physical health days | HSQ470 | HSQ_B through HSQ_J | 2001-2018 | Number of days in past 30 days when physical health was not good | 0-30 (continuous), 77=Refused, 99=Don't know | Poor Physical Health Days (Past 30 Days) |

### Secondary Outcomes

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Mental Health Days | Poor mental health days | HSQ480 | HSQ_B through HSQ_J | 2001-2018 | Number of days in past 30 days when mental health was not good | 0-30 (continuous), 77=Refused, 99=Don't know | Poor Mental Health Days (Past 30 Days) |
| Activity Limitation Days | Health-related activity limitation | HSQ490 | HSQ_B through HSQ_J | 2001-2018 | Days when poor physical/mental health kept person from usual activities | 0-30 (continuous), 77=Refused, 99=Don't know | Activity Limitation Days (Past 30 Days) |
| General Health Status | Self-rated health | HSD010 | HSQ_B through HSQ_J | 2001-2018 | General health condition rating | 1=Excellent, 2=Very Good, 3=Good, 4=Fair, 5=Poor | General Health Status |

---

## Primary Exposure Variables

### Chronic Conditions

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Diabetes | Diabetes diagnosis | DIQ010 | DIQ_B through DIQ_J | 2001-2018 | Doctor told you have diabetes | 1=Yes, 2=No, 3=Borderline, 7=Refused, 9=Don't know | Diabetes Diagnosis |
| Hypertension | Hypertension diagnosis | BPQ020 | BPQ_B through BPQ_J | 2001-2018 | Ever told you have high blood pressure | 1=Yes, 2=No, 7=Refused, 9=Don't know | Hypertension Diagnosis |
| High Cholesterol | High cholesterol diagnosis | BPQ080 | BPQ_B through BPQ_J | 2001-2018 | Ever told you have high cholesterol | 1=Yes, 2=No, 7=Refused, 9=Don't know | High Cholesterol Diagnosis |
| Cardiovascular Disease | CVD history | CDQ001, CDQ009 | CDQ_B through CDQ_J | 2001-2018 | Chest pain/angina or heart disease history | Derived from multiple items | Cardiovascular Disease History |
| Chronic Condition Count | Multimorbidity burden | Derived | DIQ, BPQ, CDQ | 2001-2018 | Count of diagnosed conditions (0, 1, 2, 3+) | 0, 1, 2, 3+ | Number of Chronic Conditions |

### Chronic Condition Coding Rules

**Diabetes (DIQ010)**:
- 1 (Yes) = Diabetes
- 2 (No), 3 (Borderline) = No diabetes
- 7, 9 = Missing

**Hypertension (BPQ020)**:
- 1 (Yes) = Hypertension
- 2 (No) = No hypertension
- 7, 9 = Missing

**Cardiovascular Disease (derived)**:
- Chest pain/angina (CDQ001 = 1) OR
- Heart disease history (CDQ009 = 1)
- Code as CVD = Yes if either present

**Chronic Condition Count**:
- Sum of: Diabetes + Hypertension + CVD
- Categories: 0 (none), 1 (single), 2 (two), 3+ (multiple)

---

## Demographic Variables

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Age | Chronological age | RIDAGEYR | DEMO_B through DEMO_J | 2001-2018 | Age at screening (years) | 0-150 (continuous) | Age (Years) |
| Sex/Gender | Biological sex | RIAGENDR | DEMO_B through DEMO_J | 2001-2018 | Gender of participant | 1=Male, 2=Female | Sex |
| Race/Ethnicity | Race/Hispanic origin | RIDRETH1 | DEMO_B through DEMO_J | 2001-2018 | Race/ethnicity (recode) | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 5=Other/Multi | Race/Ethnicity |
| Marital Status | Marital status | DMDMARTL | DEMO_B through DEMO_J | 2001-2018 | Marital status | 1=Married, 2=Widowed, 3=Divorced, 4=Separated, 5=Never married, 6=Living with partner | Marital Status |
| Citizenship | US citizenship | DMDCITZN | DEMO_B through DEMO_J | 2001-2018 | Citizenship status | 1=US citizen, 2=Not US citizen | US Citizenship Status |

### Race/Ethnicity Recoding

Original NHANES coding (RIDRETH1):
- 1 = Mexican American
- 2 = Other Hispanic
- 3 = Non-Hispanic White
- 4 = Non-Hispanic Black
- 5 = Other Race - Including Multi-Racial

**Analysis Categories**:
- Mexican American
- Other Hispanic
- Non-Hispanic White (Reference)
- Non-Hispanic Black
- Other/Multi-racial

---

## Socioeconomic Variables

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Education Level | Educational attainment | DMDEDUC2 | DEMO_B through DEMO_J | 2001-2018 | Highest grade or level of education completed | 1=<9th grade, 2=9-11th grade, 3=High school grad, 4=Some college, 5=College grad or above | Education Level |
| Income-to-Poverty Ratio | Poverty status | INDFMPIR | DEMO_B through DEMO_J | 2001-2018 | Ratio of family income to poverty threshold | 0-5+ (continuous) | Income-to-Poverty Ratio |
| Health Insurance | Insurance coverage | HIQ011 | HIQ_B through HIQ_J | 2001-2018 | Covered by health insurance | 1=Yes, 2=No, 7=Refused, 9=Don't know | Health Insurance Coverage |
| Employment Status | Work status | OCD150 | OCQ_B through OCQ_J | 2001-2018 | Work done for pay in past week | 1=Working, 2=Not working | Employment Status |

### Education Recoding

**Original Categories** (DMDEDUC2):
- 1 = Less than 9th grade
- 2 = 9-11th grade (Includes 12th grade with no diploma)
- 3 = High school graduate/GED or equivalent
- 4 = Some college or AA degree
- 5 = College graduate or above
- 7 = Refused
- 9 = Don't know

**Analysis Categories**:
- Less than high school (1-2)
- High school graduate (3)
- Some college (4)
- College graduate or above (5)

### Income-to-Poverty Ratio Categories

- <1.00 (Below poverty)
- 1.00-1.99 (Near poor)
- 2.00-3.99 (Middle income)
- 4.00+ (High income)

---

## Health Behavior Variables

### Physical Activity

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Vigorous Activity | Vigorous work activity | PAQ605 | PAQ_B through PAQ_J | 2001-2018 | Vigorous work activity | 1=Yes, 2=No | Vigorous Work Activity |
| Moderate Activity | Moderate work activity | PAQ620 | PAQ_B through PAQ_J | 2001-2018 | Moderate work activity | 1=Yes, 2=No | Moderate Work Activity |
| Walking/Biking | Active transportation | PAQ635 | PAQ_B through PAQ_J | 2001-2018 | Walk or bicycle for transportation | 1=Yes, 2=No | Active Transportation |
| Recreational Vigorous | Vigorous recreation | PAQ650 | PAQ_B through PAQ_J | 2001-2018 | Vigorous recreational activities | 1=Yes, 2=No | Vigorous Recreational Activity |
| Recreational Moderate | Moderate recreation | PAQ665 | PAQ_B through PAQ_J | 2001-2018 | Moderate recreational activities | 1=Yes, 2=No | Moderate Recreational Activity |
| Physical Activity Level | Derived activity category | Derived from PAQ variables | PAQ | 2001-2018 | Combined activity level | 4 categories | Physical Activity Level |

### Physical Activity Level Derivation

**Inactive**: No moderate or vigorous activity (work or recreation)

**Low Activity**: Only one of: moderate work, walk/bike, or moderate recreation

**Moderate Activity**: Meets minimum activity (≥1 vigorous activity OR ≥2 moderate activities)

**High Activity**: Meets guidelines (vigorous work + recreation OR ≥150 min equivalent)

### Smoking

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Smoking Status | Smoking behavior | SMQ020, SMQ040 | SMQ_B through SMQ_J | 2001-2018 | Ever smoked 100+ cigarettes + current status | Derived 3 categories | Smoking Status |

**Smoking Categories**:
- Never smoker (SMQ020 = 2)
- Former smoker (SMQ020 = 1 AND SMQ040 = 3)
- Current smoker (SMQ020 = 1 AND SMQ040 = 1 or 2)

### Alcohol

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Alcohol Use | Alcohol consumption | ALQ110, ALQ130 | ALQ_B through ALQ_J | 2001-2018 | Ever had alcohol + drinks per occasion | Derived categories | Alcohol Consumption |

---

## Anthropometric Variables

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| BMI | Body mass index | BMXBMI | BMX_B through BMX_J | 2001-2018 | Body mass index (kg/m²) | Continuous | Body Mass Index (kg/m²) |
| BMI Category | Weight status | Derived from BMXBMI | BMX | 2001-2018 | BMI categories | 4 categories | BMI Category |
| Waist Circumference | Abdominal obesity | BMXWAIST | BMX_B through BMX_J | 2001-2018 | Waist circumference (cm) | Continuous | Waist Circumference (cm) |

### BMI Categories

- Underweight: <18.5 kg/m²
- Normal weight: 18.5-24.9 kg/m²
- Overweight: 25.0-29.9 kg/m²
- Obese: ≥30.0 kg/m²

---

## Survey Design Variables

| Variable | Concept | NHANES Variable | Dataset(s) | Years | Description | Values | Final Label |
|----------|---------|-----------------|------------|-------|-------------|--------|-------------|
| Sample Weights | Survey weights | WTMEC2YR | DEMO | 2001-2018 | Full sample 2-year MEC exam weights | Continuous | Sample Weights |
| PSU | Primary sampling unit | SDMVPSU | DEMO | 2001-2018 | Masked variance pseudo-PSU | 1-2 | Primary Sampling Unit |
| Stratum | Stratum identifier | SDMVSTRA | DEMO | 2001-2018 | Masked variance pseudo-stratum | 1-98 | Stratum Identifier |
| Survey Cycle | Data collection cycle | SDDSRVYR | DEMO | 2001-2018 | Release cycle number | 1-10 | Survey Cycle |

---

## Variable Transformation Summary

### Continuous Variables
| Variable | Original Range | Transformed Variable | Transformation Notes |
|----------|---------------|---------------------|---------------------|
| HSQ470 | 0-30 | Physical Health Days | Exclude 77, 99 codes; treat as continuous |
| HSQ480 | 0-30 | Mental Health Days | Exclude 77, 99 codes; treat as continuous |
| HSQ490 | 0-30 | Activity Limitation Days | Exclude 77, 99 codes; treat as continuous |
| RIDAGEYR | 0-150 | Age | Filter to ≥60 years |
| INDFMPIR | 0-5+ | Income-to-Poverty Ratio | Treat as continuous; cap at 5.0 |
| BMXBMI | 0-100+ | BMI | Exclude extreme values (<10 or >80) |

### Categorical Variables
| Variable | Original Categories | Recoded Categories | Recoding Rule |
|----------|--------------------|--------------------|--------------|
| Chronic Condition Count | Derived 0-3 | 0, 1, 2, 3+ | Sum of diabetes + hypertension + CVD |
| Education | 1-5, 7, 9 | 4 categories | Combine <HS; exclude missing |
| Race/Ethnicity | 1-5 | 5 categories | Use as-is |
| Physical Activity | Multiple items | 4 categories | Algorithm based on PAQ items |
| Smoking | Multiple items | 3 categories | Algorithm based on SMQ items |
| BMI Category | Continuous BMI | 4 categories | Standard WHO cutpoints |

### Derived Variables
| Variable Name | Source Variables | Derivation Formula |
|--------------|------------------|-------------------|
| Chronic Condition Count | DIQ010, BPQ020, CDQ001, CDQ009 | Count conditions where (DIQ010=1) + (BPQ020=1) + (CDQ001=1 OR CDQ009=1) |
| Has Any Chronic Condition | Chronic Condition Count | 1 if count ≥1, else 0 |
| Multimorbidity | Chronic Condition Count | 1 if count ≥2, else 0 |
| Poor Physical Health (Binary) | HSQ470 | 1 if HSQ470 ≥14, else 0 |
| Poor Mental Health (Binary) | HSQ480 | 1 if HSQ480 ≥14, else 0 |
| Activity Limitation (Binary) | HSQ490 | 1 if HSQ490 ≥1, else 0 |
| Age Group | RIDAGEYR | 60-69, 70-79, 80+ |

---

## Missing Data Handling

### Missing Data Codes

| Variable Type | Missing Codes | Handling Strategy |
|--------------|---------------|-------------------|
| Outcomes (HSQ470, HSQ480, HSQ490) | 77=Refused, 99=Don't know | Exclude from analysis |
| Binary conditions (DIQ010, BPQ020) | 7=Refused, 9=Don't know | Exclude or impute as "No" |
| Continuous (BMXBMI) | Blank | Exclude extreme outliers |
| Categorical (DMDEDUC2) | 7=Refused, 9=Don't know | Exclude from analysis |

### Missing Data Strategy

1. **Primary Analysis**: Complete case analysis excluding missing values
2. **Sensitivity Analysis**: Multiple imputation for missing covariates
3. **Missingness Assessment**: Compare characteristics of complete vs. incomplete cases

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
| CVD History | CDQ001, CDQ009 | CDQ_B.csv through CDQ_J.csv | CDQ_B_dictionary.csv through CDQ_J_dictionary.csv | 2001-2018 (B-J) | Cardiovascular Disease History |
| Age | RIDAGEYR | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Age (Years) |
| Sex | RIAGENDR | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Sex |
| Race/Ethnicity | RIDRETH1 | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Race/Ethnicity |
| Education Level | DMDEDUC2 | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Education Level |
| Income-to-Poverty Ratio | INDFMPIR | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Income-to-Poverty Ratio |
| Health Insurance | HIQ011 | HIQ_B.csv through HIQ_J.csv | HIQ_B_dictionary.csv through HIQ_J_dictionary.csv | 2001-2018 (B-J) | Health Insurance Coverage |
| Physical Activity | PAQ605, PAQ620, PAQ635, PAQ650, PAQ665 | PAQ_B.csv through PAQ_J.csv | PAQ_B_dictionary.csv through PAQ_J_dictionary.csv | 2001-2018 (B-J) | Physical Activity Level |
| Smoking Status | SMQ020, SMQ040 | SMQ_B.csv through SMQ_J.csv | SMQ_B_dictionary.csv through SMQ_J_dictionary.csv | 2001-2018 (B-J) | Smoking Status |
| Body Mass Index | BMXBMI | BMX_B.csv through BMX_J.csv | BMX_B_dictionary.csv through BMX_J_dictionary.csv | 2001-2018 (B-J) | Body Mass Index (kg/m²) |
| Sample Weights | WTMEC2YR | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Sample Weights |
| PSU | SDMVPSU | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Primary Sampling Unit |
| Stratum | SDMVSTRA | DEMO_B.csv through DEMO_J.csv | DEMO_B_dictionary.csv through DEMO_J_dictionary.csv | 2001-2018 (B-J) | Stratum Identifier |

---

## Data Merge Strategy

### Merge Keys
All datasets merge on **SEQN** (Respondent sequence number), the unique identifier for each NHANES participant.

### Merge Order
1. Start with DEMO (demographics) - contains SEQN and survey weights
2. Merge HSQ (outcomes) - left join to keep only those with health status data
3. Merge DIQ, BPQ, CDQ (chronic conditions) - left join
4. Merge PAQ (physical activity) - left join
5. Merge SMQ (smoking) - left join
6. Merge HIQ (insurance) - left join
7. Merge BMX (body measurements) - left join

### Merge Type
- **Left join** from DEMO to preserve population representativeness
- Include only participants with valid HSQ data
- Filter to males aged 60+ after initial merge

---

*Document Version: 1.0*
*Date: 2026-02-08*
*Study: older-men-health-days-2026-02-08*
