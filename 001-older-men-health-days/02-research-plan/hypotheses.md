# Study Hypotheses: Factors Associated with Poor Physical Health Days Among Older Men

## Overview

This document presents the formal hypotheses for the NHANES study examining factors associated with poor physical health days among U.S. men aged 60 years and older. Each hypothesis includes the theoretical rationale, specific prediction, expected direction of association, and proposed analytical approach.

---

## Primary Hypothesis (H1)

### Statement
**Older men (60+) with chronic conditions (diabetes, hypertension, cardiovascular disease) will report significantly more poor physical health days compared to those without chronic conditions, after adjusting for age, race/ethnicity, and socioeconomic status.**

### Theoretical Rationale
The Chronic Care Model posits that chronic diseases impose substantial burden on daily functioning and health-related quality of life. Physical health days capture this burden by quantifying days when physical health is "not good" due to illness or injury. The literature consistently demonstrates that chronic disease burden is the strongest predictor of health-related quality of life measures in older adults. Multimorbidity creates compounding effects through disease interactions, treatment burden, and complexity of care.

### Specific Predictions

**H1a**: Men with any chronic condition (diabetes, hypertension, or CVD) will report on average 3-5 additional poor physical health days per month compared to men without any chronic conditions.

**H1b**: The association will demonstrate a dose-response relationship:
- 1 chronic condition: +2 to +3 days
- 2 chronic conditions: +4 to +6 days
- 3+ chronic conditions: +7 to +10 days

**H1c**: Diabetes will have the strongest individual association with poor physical health days among the three conditions, followed by cardiovascular disease, then hypertension.

### Operationalization

| Component | Specification |
|-----------|--------------|
| **Exposure** | Chronic condition count (0, 1, 2, 3+) and individual conditions (binary) |
| **Outcome** | HSQ470: Physical health days not good (0-30 days) |
| **Covariates** | Age (continuous), race/ethnicity (categorical), education (categorical), income-to-poverty ratio (continuous), insurance status (binary) |
| **Analysis** | Multiple linear regression with survey weights; negative binomial regression as sensitivity analysis |
| **Effect Measure** | Beta coefficient (difference in mean days) with 95% CI |
| **Expected Effect** | Positive association (chronic conditions → more poor health days) |

### Alternative Hypotheses
- **Null Hypothesis (H0)**: There is no association between chronic condition status and poor physical health days among older men (β = 0).
- **Alternative Hypothesis (H1)**: Chronic condition status is positively associated with poor physical health days (β > 0).

### Interpretation Criteria
| Result | Interpretation |
|--------|----------------|
| β > 0, p < 0.05, 95% CI excludes 0 | Hypothesis supported - chronic conditions associated with more poor health days |
| β ≈ 0, p > 0.05 | Hypothesis not supported - no significant association |
| β < 0, p < 0.05 | Contradicts hypothesis - unexpected protective effect |

---

## Secondary Hypotheses

### H2: Mental Health Days and Physical Health Days

#### Statement
**Among older men (60+), mental health days will be positively associated with physical health days, such that men reporting more poor mental health days will also report more poor physical health days, independent of chronic disease burden.**

#### Theoretical Rationale
The mind-body connection in health is well-established. Mental health problems (stress, depression, emotional problems) and physical health problems are bidirectionally related:
- Physical illness increases risk of depression and anxiety
- Mental health problems amplify physical symptom perception and reduce coping capacity
- Shared biological pathways include inflammation, HPA axis dysregulation, and neuroimmune interactions
- The CDC Healthy Days module captures this interrelationship through parallel measurement

#### Specific Predictions

**H2a**: Each additional poor mental health day will be associated with 0.5 to 0.8 additional poor physical health days.

**H2b**: The association will remain significant after adjusting for chronic conditions, suggesting mental health contributes to poor physical health days beyond disease burden.

**H2c**: Men with concurrent poor mental health (14+ days) will report approximately 10-15 additional poor physical health days compared to those with good mental health (0 days).

#### Operationalization

| Component | Specification |
|-----------|--------------|
| **Exposure** | HSQ480: Mental health days not good (0-30 days) |
| **Outcome** | HSQ470: Physical health days not good (0-30 days) |
| **Covariates** | All H1 covariates + chronic condition count |
| **Analysis** | Linear regression; correlation analysis; categorize mental health days (0, 1-7, 8-14, 15+) |
| **Effect Measure** | Beta coefficient, Pearson correlation coefficient |
| **Expected Effect** | Positive association (r = 0.4 to 0.6) |

#### Clinical Significance
If supported, findings would suggest that addressing mental health could yield physical health benefits, supporting integrated care approaches for older men with chronic conditions.

---

### H3: Socioeconomic Status and Physical Health Days

#### Statement
**Higher socioeconomic status, as measured by education and income, will be inversely associated with poor physical health days among older men (60+), and this association will persist after adjustment for chronic disease burden and healthcare access.**

#### Theoretical Rationale
The Social Gradient in Health framework demonstrates that socioeconomic position shapes health outcomes through multiple pathways:
- **Material resources**: Ability to afford healthy food, safe housing, medical care
- **Psychosocial factors**: Control over life circumstances, social support, stress exposure
- **Behavioral factors**: Health literacy, health-promoting behaviors
- **Healthcare access**: Insurance coverage, quality of care
- **Environmental exposures**: Neighborhood conditions, occupational hazards

Even among older adults with universal Medicare access, SES gradients persist through these pathways.

#### Specific Predictions

**H3a**: Men with less than high school education will report 3-5 more poor physical health days compared to college graduates.

**H3b**: Men below the poverty line will report 5-7 more poor physical health days compared to those with incomes ≥400% of poverty.

**H3c**: The SES gradient will be partially mediated by chronic disease burden but will remain significant after adjustment, indicating independent effects of SES on health-related quality of life.

**H3d**: Education will have a stronger association than income in this older population, reflecting cumulative advantage over the life course.

#### Operationalization

| Component | Specification |
|-----------|--------------|
| **Exposures** | Education (4 categories: <HS, HS, some college, college+); Income-to-poverty ratio (continuous or quintiles) |
| **Outcome** | HSQ470: Physical health days not good |
| **Covariates** | Age, race/ethnicity, insurance, chronic conditions |
| **Analysis** | Linear regression; test for trend across SES categories; mediation analysis |
| **Effect Measure** | Beta coefficient per education category, per unit income |
| **Expected Effect** | Inverse association (higher SES → fewer poor health days) |

#### Policy Implications
Support for policies addressing social determinants of health beyond medical care, including income support, education initiatives, and community development.

---

### H4: Racial/Ethnic Disparities in Physical Health Days

#### Statement
**Racial and ethnic minority older men (60+) will report more poor physical health days compared to non-Hispanic White men, and these disparities will persist after comprehensive adjustment for socioeconomic factors and chronic disease burden.**

#### Theoretical Rationale
Health disparities research demonstrates persistent inequities across racial/ethnic groups, even after controlling for SES. Potential explanatory mechanisms include:
- **Structural racism**: Discrimination in housing, employment, healthcare
- **Healthcare quality**: Differential treatment, implicit bias, cultural competence
- **Chronic stress**: Weathering hypothesis regarding cumulative physiological wear from discrimination
- **Neighborhood context**: Residential segregation and concentrated disadvantage
- **Cultural factors**: Health beliefs, social support patterns, coping resources

#### Specific Predictions

**H4a**: Non-Hispanic Black men will report 4-6 more poor physical health days compared to non-Hispanic White men in unadjusted analyses.

**H4b**: Hispanic men will report 3-5 more poor physical health days compared to non-Hispanic White men.

**H4c**: Racial/ethnic disparities will attenuate but persist after adjustment for SES (education, income), suggesting both SES and non-SES mechanisms.

**H4d**: Disparities will be largest among men with multiple chronic conditions, indicating differential vulnerability to multimorbidity burden.

#### Operationalization

| Component | Specification |
|-----------|--------------|
| **Exposure** | Race/ethnicity (5 categories: Mexican American, Other Hispanic, Non-Hispanic White, Non-Hispanic Black, Other/Multi) |
| **Outcome** | HSQ470: Physical health days not good |
| **Covariates** | Sequential adjustment: (1) demographic, (2) +SES, (3) +chronic conditions, (4) +health behaviors |
| **Analysis** | Linear regression with sequential models; Blinder-Oaxaca decomposition |
| **Effect Measure** | Beta coefficient (reference: Non-Hispanic White) |
| **Expected Effect** | Positive coefficients for minority groups (more poor health days) |

#### Disparity Metrics
- **Unadjusted disparity**: Raw difference between groups
- **SES-adjusted disparity**: Remaining difference after accounting for education/income
- **Fully-adjusted disparity**: Residual difference unexplained by measured factors
- **Proportion explained**: Percentage of disparity attributable to measured covariates

---

### H5: Physical Activity and Physical Health Days

#### Statement
**Higher levels of physical activity will be inversely associated with poor physical health days among older men (60+), and this protective effect will be present even among men with chronic conditions.**

#### Theoretical Rationale
Physical activity is a well-established determinant of health-related quality of life:
- **Direct effects**: Improved cardiovascular fitness, muscular strength, functional capacity
- **Disease management**: Better glycemic control, blood pressure regulation, weight management
- **Mental health benefits**: Reduced depression, anxiety, stress through endorphin release and behavioral activation
- **Functional preservation**: Maintenance of mobility, independence, activities of daily living
- **Mechanism independence**: Benefits occur even in presence of chronic disease

Evidence supports dose-response relationships where higher activity yields greater benefits.

#### Specific Predictions

**H5a**: Men meeting physical activity guidelines (150+ minutes/week moderate activity) will report 5-8 fewer poor physical health days compared to inactive men.

**H5b**: A dose-response relationship will exist across activity categories:
- Inactive (reference): 0 days reduction
- Low activity: -2 to -3 days
- Moderate activity: -4 to -6 days
- High activity: -7 to -10 days

**H5c**: The protective effect will be stronger among men with chronic conditions (disease-modifying effect) compared to those without.

**H5d**: Physical activity will partially mediate the association between SES and physical health days.

#### Operationalization

| Component | Specification |
|-----------|--------------|
| **Exposure** | Physical activity level derived from PAQ questions (4 categories: Inactive, Low, Moderate, High) |
| **Outcome** | HSQ470: Physical health days not good |
| **Covariates** | Age, race/ethnicity, SES, chronic conditions, BMI, smoking |
| **Analysis** | Linear regression; test for trend; stratified by chronic condition status; interaction testing |
| **Effect Measure** | Beta coefficient per activity category |
| **Expected Effect** | Inverse association (higher activity → fewer poor health days) |

#### Behavioral Change Implications
Quantifying the specific benefit of physical activity (days of improved health) provides a concrete, meaningful metric for motivating behavior change in clinical settings.

---

## Additional Exploratory Hypotheses

### H6: Activity Limitation Days as Alternative Outcome

**Statement**: The associations observed with physical health days will be stronger when using activity limitation days (HSQ490) as the outcome, as this measure captures functional impairment more directly.

**Rationale**: Activity limitation days may be more sensitive to chronic disease burden than general physical health days.

**Analysis**: Replicate primary analyses using HSQ490 as outcome; compare effect sizes.

---

### H7: Smoking Status Interaction

**Statement**: The association between chronic conditions and physical health days will be stronger among current smokers compared to never smokers, indicating synergistic effects of multimorbidity and smoking.

**Rationale**: Smoking exacerbates chronic disease severity and progression, potentially amplifying health-related quality of life impairment.

**Analysis**: Test chronic condition count × smoking status interaction in regression models.

---

### H8: Age as Effect Modifier

**Statement**: The association between chronic conditions and physical health days will be stronger among men aged 60-69 compared to those aged 70+, reflecting survivor bias and adaptation to illness in older age groups.

**Rationale**: Older survivors may have better coping mechanisms or represent a healthier subset of their birth cohort.

**Analysis**: Stratify analyses by age group (60-69, 70-79, 80+); test for interaction.

---

## Hypothesis Testing Summary Table

| Hypothesis | Exposure | Outcome | Expected Direction | Key Covariates | Primary Test |
|------------|----------|---------|-------------------|----------------|--------------|
| H1 | Chronic conditions | Physical health days | Positive (+) | Age, race, SES | Linear regression |
| H2 | Mental health days | Physical health days | Positive (+) | All H1 covariates | Correlation, regression |
| H3 | SES (education, income) | Physical health days | Negative (-) | Age, race, conditions | Linear regression |
| H4 | Race/ethnicity | Physical health days | Positive for minorities | Sequential adjustment | Sequential models |
| H5 | Physical activity | Physical health days | Negative (-) | All H1 covariates | Linear regression |
| H6 | Chronic conditions | Activity limitation days | Positive (+) | Same as H1 | Linear regression |
| H7 | Chronic conditions × Smoking | Physical health days | Stronger in smokers | Full covariates | Interaction test |
| H8 | Chronic conditions × Age group | Physical health days | Stronger in younger | Full covariates | Interaction test |

---

## Decision Rules for Hypothesis Evaluation

### Primary Hypothesis (H1)
- **Supported**: β > 2.0 days per condition, p < 0.05, dose-response pattern observed
- **Partially Supported**: Significant association but smaller effect size or inconsistent dose-response
- **Not Supported**: Non-significant association (p ≥ 0.05) or negative coefficient

### Secondary Hypotheses (H2-H5)
- **Supported**: p < 0.05 with effect in hypothesized direction
- **Not Supported**: p ≥ 0.05 or effect in opposite direction

### Exploratory Hypotheses (H6-H8)
- **Supported**: p < 0.05 with effect in hypothesized direction
- **Not Supported**: p ≥ 0.05 or effect in opposite direction
- **Note**: Exploratory findings require cautious interpretation and replication

---

## Multiple Comparisons Consideration

Given 8 formal hypotheses, the risk of Type I error (false positives) is elevated. To address this:

1. **Family-wise error control**: Apply Bonferroni correction (α = 0.05/8 = 0.006) for declaring definitive significance
2. **Primary vs. secondary distinction**: H1 has priority; H2-H5 are secondary; H6-H8 are exploratory
3. **Confidence interval emphasis**: Focus on confidence intervals and effect sizes rather than binary significance
4. **Pattern consistency**: Look for coherent patterns across related hypotheses
5. **Replication necessity**: Exploratory findings require independent replication

---

## Hypothesis Refinement Protocol

In the event of unexpected findings, the following refinement options are available:

1. **Non-linear associations**: Test quadratic terms if linear associations are non-significant
2. **Categorization**: Convert continuous exposures to categories if assumptions violated
3. **Stratification**: Conduct subgroup analyses if overall effects are heterogeneous
4. **Alternative outcomes**: Use general health status (HSD010) if count models fail
5. **Sensitivity analyses**: Modify exclusion criteria or covariate specifications

Any substantive hypothesis modifications will be documented as deviations from the pre-specified plan.

---

*Document Version: 1.0*
*Date: 2026-02-08*
*Study: older-men-health-days-2026-02-08*
