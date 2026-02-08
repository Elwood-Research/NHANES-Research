# Statistical Methods: Older Men and Physical Health Days

## Study Design and Population

### Design
This study employs a cross-sectional analysis using pooled data from nine consecutive cycles of the National Health and Nutrition Examination Survey (NHANES) conducted between 2001 and 2018. The analysis follows the STROBE (Strengthening the Reporting of Observational Studies in Epidemiology) guidelines for cross-sectional studies.

### Study Population
The target population consists of civilian, non-institutionalized males aged 60 years and older residing in the United States. Inclusion criteria are:

1. **Age**: 60 years or older at the time of screening
2. **Sex**: Male (identified as biological sex)
3. **Survey Participation**: Completed both the household interview and Mobile Examination Center (MEC) examination
4. **Data Availability**: Complete data for the primary outcome variable (Physical Health Days Not Good)
5. **Weight Availability**: Valid examination sample weights (WTMEC2YR)

Exclusion criteria include:
- Missing primary outcome data (HSQ470)
- Missing survey design variables (strata or PSU)
- Zero or invalid sample weights
- Extreme outliers (see Data Cleaning section)

### Data Source and Years

#### NHANES Cycles Included
| Cycle Code | Years        | Data Release |
|------------|--------------|--------------|
| B          | 2001-2002    | 2            |
| C          | 2003-2004    | 2            |
| D          | 2005-2006    | 3            |
| E          | 2007-2008    | 4            |
| F          | 2009-2010    | 5            |
| G          | 2011-2012    | 6            |
| H          | 2013-2014    | 7            |
| I          | 2015-2016    | 8            |
| J          | 2017-2018    | 9            |

Total study period: 18 years (2001-2018)

#### Dataset Components Merged
1. **DEMO** - Demographic variables and sample weights
2. **HSQ** - Current Health Status questionnaire (primary outcomes)
3. **DIQ** - Diabetes questionnaire
4. **BPQ** - Blood pressure and hypertension questionnaire
5. **CDQ** - Cardiovascular disease questionnaire
6. **PAQ** - Physical activity questionnaire
7. **SMQ** - Smoking questionnaire
8. **BMX** - Body measures (examination component)
9. **HIQ** - Health insurance questionnaire

### Data Harmonization Across Cycles

Multi-cycle pooling requires careful harmonization of variables that may have changed across survey cycles:

1. **Variable Name Changes**: Some NHANES variables were renamed across cycles. All variables are mapped to a consistent naming convention using the most recent cycle's variable names.

2. **Category Harmonization**: Response categories are harmonized across cycles:
   - Education: Recoded to consistent 4-level classification
   - Income: PIR used as continuous measure where available
   - Race/Ethnicity: 5-level NHANES standard maintained across all cycles

3. **Missing Value Codes**: Consistent handling of NHANES missing value codes (7=Refused, 9=Don't Know, .=Missing)

4. **Sampling Design Variables**: SDMVSTRA (strata) and SDMVPSU (PSU) are used consistently across all cycles

5. **Weight Adjustment**: For pooled analyses, weights are divided by the number of cycles (9) to ensure appropriate population representation

## Variable Definitions and Coding

### Primary Outcome Variable

#### Physical Health Days Not Good (HSQ470)
- **Description**: Number of days in past 30 days when physical health was not good
- **Question**: "Thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good?"
- **Scale**: Count variable (0-30 days)
- **Distribution Characteristics**:
  - Expected zero-inflation (many respondents report 0 days)
  - Right-skewed distribution
  - Ceiling effect at 30 days

### Secondary Outcome Variables

#### Mental Health Days Not Good (HSQ480)
- **Description**: Number of days in past 30 days when mental health was not good
- **Question**: "Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good?"
- **Scale**: Count variable (0-30 days)
- **Role**: Both confounder and secondary outcome

#### Activity Limitation Days (HSQ490)
- **Description**: Number of days when poor physical or mental health kept respondent from usual activities
- **Question**: "During the past 30 days, for about how many days did poor physical or mental health keep you from doing your usual activities, such as self-care, work, or recreation?"
- **Scale**: Count variable (0-30 days)
- **Role**: Secondary outcome

### Primary Exposure: Chronic Condition Count

The chronic condition count is constructed as a composite variable summing confirmed diagnoses:

#### Component Conditions

1. **Diabetes (DIQ010)**
   - Coded as present (1) if: "Doctor told you have diabetes" = Yes
   - Excludes: Borderline cases, gestational diabetes only
   - Variable: DIQ010 = 1

2. **Hypertension (BPQ020)**
   - Coded as present (1) if: "Ever told you had high blood pressure" = Yes
   - Variable: BPQ020 = 1

3. **Cardiovascular Disease (CDQ001, CDQ010)**
   - Coded as present (1) if ANY of the following:
     - CDQ001: Chest pain ever = Yes
     - CDQ010: Shortness of breath walking up hills = Yes (in some cycles)
   - Alternative: CDQ020 (angina) = Yes where available

4. **Additional Chronic Conditions** (where available):
   - Congestive heart failure (MCQ160B) where available
   - Stroke (MCQ160F) where available
   - Chronic obstructive pulmonary disease indicators

#### Chronic Condition Count Categories
- **0 conditions**: No diagnosed chronic conditions
- **1 condition**: Single chronic condition
- **2 conditions**: Two chronic conditions
- **3+ conditions**: Three or more chronic conditions

### Demographic Variables

#### Age (RIDAGEYR)
- **Description**: Age at screening adjudicated
- **Scale**: Continuous (years)
- **Range**: 60-85 years (top-coded at 85)
- **Centering**: Age will be centered at 70 years for regression models
- **Transformation**: Age squared included for non-linearity assessment

#### Race/Ethnicity (RIDRETH1)
- **Categories**:
  1. Mexican American
  2. Other Hispanic
  3. Non-Hispanic White (reference category)
  4. Non-Hispanic Black
  5. Other Race - Including Multi-Racial
- **Coding**: Dummy variables with Non-Hispanic White as reference

### Socioeconomic Status Variables

#### Education (DMDEDUC2)
- **Categories**:
  1. Less than High School (DMDEDUC2 = 1, 2)
  2. High School Graduate/GED (DMDEDUC2 = 3)
  3. Some College/AA Degree (DMDEDUC2 = 4)
  4. College Graduate or Higher (DMDEDUC2 = 5, reference)
- **Harmonization**: Consistent across all cycles

#### Income-to-Poverty Ratio (INDFMPIR)
- **Description**: Ratio of family income to federal poverty threshold
- **Scale**: Continuous
- **Range**: 0-5 (top-coded at 5.0 in NHANES)
- **Missing handling**: Imputed where possible; excluded if missing
- **Interpretation**: Values <1 indicate income below poverty line

#### Marital Status (DMDMARTL)
- **Categories** (harmonized):
  1. Married/Living with partner (reference)
  2. Widowed
  3. Divorced/Separated
  4. Never married

### Health-Related Variables

#### Health Insurance (HIQ011)
- **Description**: Coverage by health insurance
- **Categories**: 
  - Insured (HIQ011 = 1)
  - Uninsured (HIQ011 = 2)
- **Reference**: Insured

#### Smoking Status (SMQ020, SMQ040)
- **Categories**:
  1. Never smoker: SMQ020 = 2
  2. Former smoker: SMQ020 = 1 AND SMQ040 = 3
  3. Current smoker: SMQ020 = 1 AND (SMQ040 = 1 OR 2)
- **Reference**: Never smoker

#### Body Mass Index (BMXBMI)
- **Description**: Body mass index (kg/m²)
- **Categories**:
  - Normal: 18.5-24.9
  - Overweight: 25.0-29.9
  - Obese: ≥30.0
- **Reference**: Normal weight

#### Physical Activity (PAQ650, PAQ665)

**Vigorous Activity (PAQ650)**
- Question: "In a typical week, do you do any vigorous-intensity sports, fitness or recreational activities?"
- Binary: Yes/No

**Moderate Activity (PAQ665)**
- Question: "In a typical week, do you do any moderate-intensity sports, fitness or recreational activities?"
- Binary: Yes/No

**Physical Activity Categories**:
1. Inactive: No moderate or vigorous activity
2. Moderate only: Moderate but no vigorous activity
3. Vigorous: Any vigorous activity (reference)

*Note: Physical activity variable definitions vary across cycles and will be harmonized based on available measures*

## Survey Design Considerations

### Complex Sampling Design
NHANES employs a complex, multistage probability sampling design requiring special statistical procedures:

#### Primary Sampling Units (PSU)
- Variable: SDMVPSU
- Description: Masked variance unit pseudo-PSU
- Purpose: Accounts for clustering in the sampling design

#### Stratification
- Variable: SDMVSTRA
- Description: Masked variance unit pseudo-stratum
- Purpose: Accounts for stratification in the sampling design

#### Sample Weights
- **Primary Weight**: WTMEC2YR (2-year MEC examination weight)
- **Weight Adjustment for Pooled Analyses**: 
  - Each cycle's weight divided by 9 (number of cycles)
  - Ensures sum of weights represents average population across study period
- **Rationale**: WTMEC2YR selected because:
  - Primary outcome comes from MEC examination questionnaire
  - Accounts for differential non-response to examination
  - Recommended by NCHS for analyses using examination data

### Variance Estimation
- **Method**: Taylor series linearization
- **Software**: Survey package in Python (statsmodels or survey python package)
- **Degrees of Freedom**: Based on number of PSUs minus number of strata

### Finite Population Correction
NHANES public use files do not include finite population correction factors. Standard errors may be slightly conservative (overestimated) for large estimates.

## Statistical Analysis Plan

### Analysis Overview
The analysis proceeds in sequential stages addressing each hypothesis:

| Stage | Analysis | Hypothesis | Model |
|-------|----------|------------|-------|
| 1 | Descriptive | N/A | Weighted means/proportions |
| 2 | Bivariate | All H1-H8 | Survey-weighted regressions |
| 3 | Multivariable | H1-H5 | Negative binomial regression |
| 4 | Interactions | H6-H8 | Stratified analyses |
| 5 | Sensitivity | All | Multiple robustness checks |

### Primary Statistical Model

Given the count nature of the outcome variable (Physical Health Days: 0-30) with expected zero-inflation and overdispersion, the primary analysis will use **Negative Binomial Regression** with survey design adjustment.

#### Model Specification

```
log(μ_i) = β₀ + β₁(ChronicConditions_i) + β₂(MentalHealthDays_i) + β₃(PIR_i) 
           + β₄(Race/Ethnicity_i) + β₅(PhysicalActivity_i) + β₆(Age_i) 
           + β₇(Education_i) + β₈(MaritalStatus_i) + β₉(Insurance_i)
           + β₁₀(Smoking_i) + β₁₁(BMI_i)
```

Where:
- μ_i = Expected count of physical health days for individual i
- β₀ = Intercept
- β₁-β₁₁ = Regression coefficients

#### Survey-Adjusted Model Implementation

The survey-adjusted negative binomial regression will account for:
1. Stratification (SDMVSTRA)
2. Clustering (SDMVPSU)
3. Weighting (WTMEC2YR/9)

#### Variance-Covariance Matrix
- Estimation: Taylor series linearization
- Confidence intervals: 95% Wald-type intervals
- Hypothesis tests: Design-adjusted F-tests

### Alternative Model Considerations

#### Zero-Inflated Negative Binomial (ZINB)
If exploratory analysis reveals substantial zero-inflation (excess zeros beyond what negative binomial predicts):

```
Model: Pr(Y=y) = π·I(y=0) + (1-π)·NB(μ, α)

Where:
- π = Probability of structural zero (logit model)
- I(y=0) = Indicator for zero count
- NB = Negative binomial distribution
```

**Zero-inflation model** will include:
- Chronic condition count (higher conditions → lower probability of zero)
- Age (older → lower probability of zero)
- General health status (HSD010)

#### Model Selection Criteria
- **Vuong Test**: Compares zero-inflated vs. standard negative binomial
- **AIC/BIC**: Information criteria for model fit comparison
- **Residual Analysis**: Pearson residuals, deviance residuals
- **Overdispersion Test**: Cameron-Trivedi test

### Confounding Strategy

#### Confounder Selection
Variables included in the multivariable model based on:
1. **Directed Acyclic Graphs (DAGs)**: Theoretical causal relationships
2. **Change-in-Estimate**: >10% change in primary exposure coefficient
3. **Literature Review**: Established confounders in prior research

#### Confounders Included
- **Age**: Continuous, non-linear (squared term)
- **Race/Ethnicity**: 4 dummy variables
- **Education**: 3 dummy variables
- **Income-to-Poverty Ratio**: Continuous
- **Marital Status**: 3 dummy variables
- **Health Insurance**: Binary
- **Smoking Status**: 2 dummy variables
- **BMI Categories**: 2 dummy variables
- **Mental Health Days**: Continuous (potential mediator/confounder)

#### Potential Mediators
- Mental health days (H2 hypothesis testing)
- Physical activity (H5 hypothesis testing)

*Analysis will include models with and without potential mediators to assess direct vs. indirect effects*

### Effect Modification Analysis

#### Age Group Stratification
Three age groups will be analyzed separately:
1. Young-old: 60-69 years
2. Middle-old: 70-79 years
3. Oldest-old: 80+ years

#### Race/Ethnicity Interactions
Tests for differential effects by race/ethnicity:
- Chronic conditions × Race/Ethnicity
- SES variables × Race/Ethnicity
- Physical activity × Race/Ethnicity

#### Testing Procedure
1. Fit full model with interaction terms
2. Design-adjusted Wald F-test for interaction
3. Report stratified estimates if p-interaction < 0.10

## Data Cleaning and Quality Control

### Outlier Screening

#### Continuous Variables
For all continuous variables (age, PIR, health days measures), observations with |z-score| > 4 will be flagged and removed:

```
z_i = (x_i - x̄) / s

Where:
- x̄ = Survey-weighted mean
- s = Survey-weighted standard deviation
```

**Variables screened**:
- Physical health days (HSQ470)
- Mental health days (HSQ480)
- Activity limitation days (HSQ490)
- Age (RIDAGEYR)
- Income-to-Poverty Ratio (INDFMPIR)
- BMI (BMXBMI)

#### Categorical Variables
Categories with <5% membership will be examined for:
- Collapsing into larger categories
- Exclusion if uninformative
- Impact on model convergence

### Missing Data Handling

#### Missing Data Patterns
1. **Listwise Deletion**: Primary analysis excludes observations with missing data on any analysis variable
2. **Missingness Assessment**: Report missing data patterns and percentages
3. **Missing Data Mechanism**: Assess whether data are Missing Completely at Random (MCAR), Missing at Random (MAR), or Missing Not at Random (MNAR)

#### Variables with High Missingness
- Report proportion missing for all variables
- Exclude variables with >20% missing unless clinically essential
- Consider multiple imputation for sensitivity analysis

### Data Quality Checks

1. **Range Checks**: Verify all values within valid ranges
2. **Logical Consistency**: 
   - Age ≥ 60 for all included participants
   - Health days 0-30 for valid responses
   - BMI within biologically plausible range (15-60)
3. **Cross-Variable Validation**:
   - Chronic conditions consistent with medications (where available)
   - Education consistent with age

## Sensitivity Analyses

### Analysis 1: Alternative Outcome Specifications
1. **Dichotomized Outcome**: 
   - 0 days vs. 1+ days (any poor physical health)
   - 0-13 days vs. 14+ days (half the month or more)
   - **Model**: Survey-adjusted logistic regression

2. **Categorized Outcome**:
   - 0 days, 1-7 days, 8-14 days, 15-30 days
   - **Model**: Survey-adjusted multinomial logistic regression

3. **Top-coded Outcome**:
   - Create binary indicator for 30 days (maximum)
   - **Model**: Survey-adjusted logistic regression

### Analysis 2: Zero-Inflated Models
If primary negative binomial shows poor fit:
- Zero-inflated Poisson (ZIP)
- Zero-inflated negative binomial (ZINB)
- Hurdle models

### Analysis 3: Different Weight Specifications
1. **2-year weights only**: Analyze each cycle separately, then meta-analyze
2. **Day 1 weights**: WTMEC2YR_D1 (subsample weights)
3. **Dietary day weights**: For analyses incorporating dietary variables

### Analysis 4: Confounder Adjustments
1. **Minimal model**: Age + Race/Ethnicity only
2. **Full model**: All confounders
3. **Parsimonious model**: Only confounders changing estimate >10%
4. **Extended model**: Additional potential confounders (occupation, region, urbanicity where available)

### Analysis 5: Stratified Analyses
1. **By Survey Cycle**: Analyze each 2-year cycle separately, test for temporal trends
2. **By Age Group**: 60-69, 70-79, 80+
3. **By General Health Status**: Excellent/Very Good/Good vs. Fair/Poor baseline health
4. **By Specific Chronic Conditions**: Diabetes only, Hypertension only, etc.

### Analysis 6: Multiple Imputation
For missing data sensitivity:
1. **Imputation Model**: Include all analysis variables and auxiliary variables
2. **Number of Imputations**: m = 20
3. **Method**: Predictive mean matching for continuous, logistic for binary
4. **Software**: statsmodels or sklearn IterativeImputer

### Analysis 7: Trimmed Estimates
To assess impact of extreme values:
1. Trim top and bottom 1% of continuous variables
2. Trim top and bottom 5% of continuous variables
3. Winsorize at 95th percentile

### Analysis 8: Subpopulation Analyses
Restrict to specific subgroups:
1. Medicare-eligible only (age 65+)
2. Non-institutionalized confirmed (no long-term care indicators)
3. English/Spanish speakers only (excludes other languages)

## Model Assumptions and Diagnostics

### Negative Binomial Assumptions
1. **Linearity**: Log-linear relationship between predictors and outcome
2. **Overdispersion**: Variance > mean (assumed, tested)
3. **Independence**: Conditional independence given covariates (addressed by survey design)

### Diagnostic Procedures

#### 1. Linearity Assessment
- Partial residual plots for continuous predictors
- Box-Tidwell test for non-linearity
- Fractional polynomial modeling if non-linearity detected

#### 2. Overdispersion Test
- Cameron-Trivedi test
- Pearson chi-square divided by degrees of freedom
- If overdispersion mild, quasi-Poisson as alternative

#### 3. Outlier Detection
- Pearson residuals > |3|
- Deviance residuals > |3|
- Cook's distance for survey-weighted models
- Influence plots

#### 4. Multicollinearity
- Variance Inflation Factors (VIF) for survey-weighted models
- Tolerance statistics
- Action: Remove or combine variables if VIF > 10

#### 5. Model Fit Assessment
- Hosmer-Lemeshow-type test for count models
- Visual inspection of observed vs. predicted
- Deviance and Pearson goodness-of-fit tests

### Handling Model Violations

| Violation | Diagnostic | Solution |
|-----------|------------|----------|
| Non-linearity | Partial residual plots | Polynomial terms, splines, or transformation |
| Overdispersion | Pearson χ²/df | Negative binomial instead of Poisson |
| Zero-inflation | Vuong test | Zero-inflated models |
| Influential points | Cook's distance | Sensitivity analysis with/without |
| Multicollinearity | VIF > 10 | Remove or combine variables |
| Poor fit | Residual plots | Alternative model specification |

## STROBE Flow Diagram

A STROBE flow diagram will be constructed detailing:

1. **Initial Sample**: All NHANES participants cycles B-J
2. **Gender Exclusion**: Females excluded
3. **Age Exclusion**: Males <60 excluded
4. **Missing Outcome**: Missing HSQ470 excluded
5. **Missing Design Variables**: Missing strata/PSU/weights excluded
6. **Outlier Exclusion**: Extreme outliers removed (|z| > 4)
7. **Missing Covariates**: Missing confounders excluded (listwise)
8. **Final Analytic Sample**: Count and weighted population estimate

Each exclusion step will report:
- Number excluded
- Weighted population estimate excluded
- Percentage of eligible population

## Software and Computational Environment

### Primary Software
- **Python 3.9+**: Primary analysis language
- **Environment**: nhanes-analysis-vault Docker container

### Required Python Packages
```
pandas>=1.5.0
numpy>=1.21.0
statsmodels>=0.13.0
scipy>=1.9.0
scikit-learn>=1.1.0
survey>=0.1.0  # Survey design analysis
matplotlib>=3.5.0
seaborn>=0.12.0
```

### Analysis Pipeline Structure
1. **Data Preparation** (`01_data_prep.py`):
   - Load and merge datasets
   - Create derived variables
   - Apply exclusion criteria
   - Quality control checks

2. **Descriptive Analysis** (`02_descriptive.py`):
   - Weighted means and proportions
   - Missing data patterns
   - Outlier screening

3. **Model Fitting** (`03_regression.py`):
   - Primary negative binomial models
   - Model diagnostics
   - Hypothesis testing

4. **Sensitivity Analyses** (`04_sensitivity.py`):
   - Alternative models
   - Stratified analyses
   - Robustness checks

5. **Output Generation** (`05_outputs.py`):
   - Tables
   - Figures
   - Results summary

### Reproducibility
- Random seeds set for any stochastic procedures
- Version control of all software dependencies
- Complete code documentation
- Audit trail of all data transformations

## Ethical Considerations

### Data Use Agreement
This research uses publicly available NHANES de-identified data. No individual participant data will be reported in any publication or presentation.

### Ethical Review
As this research uses publicly available, de-identified data, it is exempt from IRB review under 45 CFR 46.104(d)(4).

### Reporting Standards
All analyses will follow:
- STROBE guidelines for cross-sectional studies
- American Statistical Association (ASA) ethical guidelines
- NHANES data release guidelines from NCHS

## Limitations and Considerations

### Study Design Limitations
1. **Cross-sectional**: Cannot establish temporal ordering or causality
2. **Self-reported outcomes**: Physical health days subject to recall bias
3. **Self-reported conditions**: Chronic conditions based on diagnosis recall
4. **Survivorship bias**: Population limited to survivors to age 60+

### Statistical Limitations
1. **Complex survey adjustments**: Some advanced models may not have survey-adjusted implementations
2. **Small cell sizes**: Rare combinations may have unstable estimates
3. **Multiple comparisons**: Type I error inflation across hypothesis tests
4. **Model misspecification**: True data-generating process unknown

### Generalizability Limitations
1. **Non-institutionalized**: Excludes nursing home residents
2. **U.S. only**: Results may not generalize to other countries
3. **Time period**: 2001-2018 may not reflect current health patterns
4. **Males only**: Results not generalizable to females or both sexes

## References

1. Centers for Disease Control and Prevention (CDC). National Health and Nutrition Examination Survey (NHANES): Analytic Guidelines, 2011-2014 and 2015-2016. 2017.

2. Johnson CL, Paulose-Ram R, Ogden CL, et al. National Health and Nutrition Examination Survey: Analytic guidelines, 1999-2010. Vital Health Stat 2. 2013;(161):1-24.

3. Von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. Ann Intern Med. 2007;147(8):573-577.

4. Hilbe JM. Negative Binomial Regression. 2nd ed. Cambridge University Press; 2011.

5. Lumley T. Complex Surveys: A Guide to Analysis Using R. John Wiley & Sons; 2010.

6. Ridout M, Demétrio CGB, Hinde J. Models for count data with many zeros. International Biometric Conference. 1998.

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-08  
**Next Review**: Upon completion of analysis phase
