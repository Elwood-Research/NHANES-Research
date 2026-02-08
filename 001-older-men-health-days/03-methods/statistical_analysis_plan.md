# Statistical Analysis Plan: Older Men and Physical Health Days

## Executive Summary

This document provides detailed specifications for all statistical analyses to be conducted for the study "Factors Associated with Poor Physical Health Days Among Older Men: NHANES 2001-2018." The analysis plan operationalizes the hypotheses developed in Phase 2 and implements the methodological framework outlined in `methods.md`.

## 1. Hypothesis Testing Framework

### Primary Hypothesis (H1)
**Chronic conditions are positively associated with the number of poor physical health days among older men.**

#### Statistical Specification
- **Outcome (Y)**: Physical Health Days Not Good (HSQ470) - count variable (0-30)
- **Primary Exposure (X₁)**: Chronic condition count (0, 1, 2, 3+ categories)
- **Model**: Survey-adjusted negative binomial regression
- **Effect Measure**: Incidence Rate Ratio (IRR) with 95% CI
- **Null Hypothesis**: IRR = 1 for all chronic condition categories vs. reference
- **Alternative Hypothesis**: IRR ≠ 1 for at least one category
- **Alpha**: 0.05 (two-tailed)

#### Contrast Matrix
| Comparison | Reference | Test | Expected Direction |
|------------|-----------|------|-------------------|
| 1 condition vs. 0 | 0 conditions | β₁ | IRR > 1 |
| 2 conditions vs. 0 | 0 conditions | β₂ | IRR > 1 |
| 3+ conditions vs. 0 | 0 conditions | β₃ | IRR > 1 |
| Trend test | Linear trend | β_trend | β > 0 |

#### Success Criteria
- H1 supported if: IRR for 3+ conditions vs. 0 > 1.5 AND p < 0.05
- Partial support if: Any category IRR > 1.2 AND p < 0.05

---

### Hypothesis 2 (H2)
**Poor mental health days are positively associated with poor physical health days.**

#### Statistical Specification
- **Outcome (Y)**: Physical Health Days Not Good
- **Exposure (X)**: Mental Health Days Not Good (HSQ480) - continuous or categorized
- **Model**: Survey-adjusted negative binomial regression
- **Effect Measure**: IRR per 1-day increase or category IRRs
- **Confounding Strategy**: Adjusted for H1 confounders plus chronic conditions

#### Analysis Specifications
1. **Continuous Form**: IRR per 1-day increase in mental health days
2. **Categorized Form**:
   - 0 days (reference)
   - 1-7 days
   - 8-14 days
   - 15-30 days
3. **Potential Mediation**: Assess whether mental health days mediate chronic condition effects

---

### Hypothesis 3 (H3)
**Socioeconomic status is inversely associated with poor physical health days.**

#### Statistical Specification
- **Outcome (Y)**: Physical Health Days Not Good
- **Exposures (X)**:
  - Income-to-Poverty Ratio (PIR): continuous
  - Education: 4-level categorical
- **Model**: Survey-adjusted negative binomial regression
- **Effect Measures**:
  - PIR: IRR per 1-unit increase
  - Education: IRR for each level vs. College+

#### Education Contrasts
| Level | Comparison | Expected IRR |
|-------|------------|--------------|
| < High School | vs. College+ | > 1.0 |
| High School/GED | vs. College+ | > 1.0 |
| Some College | vs. College+ | > 1.0 (but smaller) |

---

### Hypothesis 4 (H4)
**Racial/ethnic disparities persist after adjustment for SES and health factors.**

#### Statistical Specification
- **Outcome (Y)**: Physical Health Days Not Good
- **Exposure (X)**: Race/Ethnicity (5 categories)
- **Models**:
  - Model 1: Unadjusted (crude)
  - Model 2: Adjusted for age only
  - Model 3: Adjusted for age + SES (education + PIR)
  - Model 4: Fully adjusted (all confounders)
- **Effect Measure**: IRR at each adjustment level

#### Disparity Assessment
Disparities considered "persistent" if:
- IRR for Non-Hispanic Black vs. Non-Hispanic White remains > 1.1 in Model 4
- IRR for Mexican American vs. Non-Hispanic White remains > 1.1 in Model 4
- AND p < 0.05 in fully adjusted model

---

### Hypothesis 5 (H5)
**Physical activity is inversely associated with poor physical health days.**

#### Statistical Specification
- **Outcome (Y)**: Physical Health Days Not Good
- **Exposure (X)**: Physical activity level
- **Categories**:
  - Inactive (reference)
  - Moderate activity only
  - Vigorous activity (any)
- **Model**: Survey-adjusted negative binomial regression
- **Expected**: IRR < 1 for active vs. inactive

---

### Hypothesis 6-8: Interaction Hypotheses

#### H6: Chronic Conditions × Age Group
**Test**: Does the effect of chronic conditions vary by age group?

**Specification**:
- Model with chronic conditions × age group interaction
- Age groups: 60-69, 70-79, 80+
- Test: Design-adjusted F-test for interaction term
- Interpretation: If p-interaction < 0.10, report stratified estimates

#### H7: Chronic Conditions × Race/Ethnicity
**Test**: Do racial/ethnic disparities in chronic condition effects exist?

**Specification**:
- Model with chronic conditions × race/ethnicity interaction
- Test: Design-adjusted F-test
- Stratified analyses by race/ethnicity if interaction significant

#### H8: Physical Activity × Chronic Conditions
**Test**: Does physical activity buffer the effect of chronic conditions?

**Specification**:
- Model with physical activity × chronic conditions interaction
- Test: Design-adjusted F-test
- Interpretation: If interaction significant, activity may moderate condition impact

## 2. Model Building Strategy

### Step 1: Unadjusted (Crude) Models
For each exposure-outcome pair:
```python
# Pseudo-code for crude model
model_crude = SurveyNegativeBinomial(
    y = physical_health_days,
    x = exposure,
    weights = WTMEC2YR / 9,
    strata = SDMVSTRA,
    psu = SDMVPSU
)
```

### Step 2: Demographic Adjustment
Add demographic confounders:
- Age (continuous, centered at 70)
- Age² (to allow non-linearity)
- Race/Ethnicity (dummy variables)

### Step 3: SES Adjustment
Add socioeconomic confounders:
- Education (dummy variables)
- Income-to-Poverty Ratio (continuous)
- Marital status (dummy variables)

### Step 4: Full Adjustment
Add remaining confounders:
- Health insurance (binary)
- Smoking status (dummy variables)
- BMI category (dummy variables)
- Mental health days (continuous or categorical)

### Step 5: Mediators
Conditional on primary hypothesis, add potential mediators:
- Physical activity (for H5 analysis)

## 3. Detailed Model Specifications

### Primary Model (H1)

```
log(μ) = β₀ + β₁(Chronic1) + β₂(Chronic2) + β₃(Chronic3plus)
       + β₄(Age_c) + β₅(Age_c²)
       + β₆(Black) + β₇(HispanicMex) + β₈(HispanicOther) + β₉(RaceOther)
       + β₁₀(EduHS) + β₁₁(EduSomeColl) + β₁₂(EduCollPlus)
       + β₁₃(PIR) + β₁₄(Married) + β₁₅(Widowed) + β₁₆(Divorced)
       + β₁₇(Insured) + β₁₈(SmokeFormer) + β₁₉(SmokeCurrent)
       + β₂₀(BMIOver) + β₂₁(BMIObese)
       + β₂₂(MentalHealthDays)
```

Where:
- **β₁-β₃**: Primary coefficients of interest (chronic conditions)
- Chronic1: 1 condition vs. 0 (reference)
- Chronic2: 2 conditions vs. 0
- Chronic3plus: 3+ conditions vs. 0

### Interpretation Guide

| Coefficient | Interpretation |
|-------------|----------------|
| exp(β₁) | IRR comparing 1 condition vs. 0 conditions |
| exp(β₂) | IRR comparing 2 conditions vs. 0 conditions |
| exp(β₃) | IRR comparing 3+ conditions vs. 0 conditions |
| exp(β₁₃) | IRR per 1-unit increase in PIR |

### Contrast Estimation

Linear combinations for specific contrasts:

**1 vs. 2 conditions**:
```
log(IRR) = β₂ - β₁
SE = sqrt(Var(β₂) + Var(β₁) - 2*Cov(β₂,β₁))
```

**Trend test across chronic condition categories**:
```
Score: 0*β₀ + 1*β₁ + 2*β₂ + 3*β₃
Test: Score / SE(Score) ~ N(0,1)
```

## 4. Assumption Testing Protocol

### 4.1 Overdispersion Test

**Cameron-Trividi Test**:
```
H₀: Var(Y) = μ (equidispersion)
H₁: Var(Y) = μ + α·μ² (overdispersion)

Test statistic: z = α̂ / SE(α̂)
```

**Decision Rule**:
- If p < 0.05: Reject equidispersion, use negative binomial
- If p ≥ 0.05: Poisson may be adequate

### 4.2 Zero-Inflation Assessment

**Vuong Test**:
Compares zero-inflated negative binomial (ZINB) vs. negative binomial (NB)

```
H₀: NB is preferred
H₁: ZINB is preferred

V = [Σ(log(P_ZINB(yᵢ)) - log(P_NB(yᵢ)))] / (σ·sqrt(n))
```

**Decision Rule**:
- |V| > 1.96: Significant difference, choose model with better fit
- Compare AIC/BIC as secondary criteria

### 4.3 Linearity Assessment

For continuous predictors (age, PIR, mental health days):

**Box-Tidwell Test**:
```
Add x·log(x) term to model
If coefficient significant: Non-linearity present
```

**Fractional Polynomial Approach**:
```
Test powers: -2, -1, -0.5, 0 (log), 0.5, 1, 2, 3
Select best-fitting power transformation using deviance
```

### 4.4 Influential Observations

**Survey-Adjusted Diagnostics**:

1. **Pearson Residuals**:
   ```
   rᵢ = (yᵢ - μ̂ᵢ) / sqrt(μ̂ᵢ + α·μ̂ᵢ²)
   ```
   Flag if |rᵢ| > 3

2. **Cook's Distance** (survey-adjusted):
   ```
   Dᵢ = (β̂ - β̂₍ᵢ₎)' · Var(β̂)⁻¹ · (β̂ - β̂₍ᵢ₎) / k
   ```
   Flag if Dᵢ > 4/n

3. **DFBETA**:
   Standardized change in each coefficient when observation removed
   Flag if |DFBETA| > 2/sqrt(n)

**Handling Strategy**:
- Report all flagged observations
- Conduct sensitivity analysis with/without influential points
- Do not automatically remove unless data error confirmed

### 4.5 Multicollinearity Assessment

**Variance Inflation Factor (VIF)**:
```
VIFⱼ = 1 / (1 - Rⱼ²)

Where Rⱼ² is from regressing predictor j on all other predictors
```

**Decision Rule**:
- VIF < 5: No multicollinearity concern
- 5 ≤ VIF < 10: Moderate concern
- VIF ≥ 10: Severe concern - consider removing/combining variables

## 5. Sample Size and Power Considerations

### Expected Sample Size
Based on NHANES sampling patterns:

| Cycle | Males 60+ (unweighted) | Expected n |
|-------|------------------------|------------|
| B (2001-2002) | ~800 | 750 |
| C (2003-2004) | ~850 | 800 |
| D (2005-2006) | ~900 | 850 |
| E (2007-2008) | ~950 | 900 |
| F (2009-2010) | ~1000 | 950 |
| G (2011-2012) | ~1050 | 1000 |
| H (2013-2014) | ~1100 | 1050 |
| I (2015-2016) | ~1150 | 1100 |
| J (2017-2018) | ~1200 | 1150 |
| **Total** | **~9,000** | **~8,550** |

### Power Analysis

**For H1 (Chronic Conditions Effect)**:

Assumptions:
- Sample size: n = 8,000
- Design effect: ~2.0 (accounting for clustering)
- Effective n: ~4,000
- Mean physical health days: 5 (SD = 7)
- Expected IRR for 3+ conditions: 2.0
- Prevalence of 3+ conditions: 20%
- Alpha: 0.05 (two-tailed)

**Power calculation**:
```
For IRR = 2.0 with 20% exposed:
Power > 0.99 for detecting main effect
Power > 0.80 for detecting interactions with 10% subgroup
```

**For Interactions (H6-H8)**:

Minimum detectable interaction effect:
- With power = 0.80, alpha = 0.05
- Ratio of subgroup sample sizes = 1:1
- Detectable interaction OR: ~1.5

## 6. Multiple Comparison Adjustment

### Familywise Error Control
Given multiple hypotheses (H1-H8) and multiple comparisons within each:

**Primary Analysis**: No adjustment (per hypothesis testing framework)
**Secondary/Exploratory Analyses**: 
- Bonferroni adjustment for pairwise comparisons within each hypothesis family
- False Discovery Rate (FDR, Benjamini-Hochberg) for all tests combined

### Pre-specified Hierarchy
1. **Primary**: H1 (chronic conditions main effect)
2. **Secondary**: H2-H5 (covariate effects)
3. **Exploratory**: H6-H8 (interactions)

If H1 not supported at p < 0.05, interpret other findings as exploratory only.

## 7. Subgroup Analysis Specifications

### 7.1 Age Group Stratification

**Strata**:
- Young-old: 60-69 years (expected n ~3,500)
- Middle-old: 70-79 years (expected n ~3,200)
- Oldest-old: 80+ years (expected n ~1,850)

**Analysis**:
1. Fit primary model separately within each stratum
2. Test for effect modification using interaction model
3. Report stratum-specific IRRs with 95% CIs

### 7.2 Race/Ethnicity Stratification

**Strata**:
- Non-Hispanic White (reference)
- Non-Hispanic Black
- Mexican American
- Other Hispanic
- Other Race

**Analysis**:
1. Calculate standardized means (direct standardization to overall population)
2. Test for interaction: Chronic conditions × Race/Ethnicity
3. If significant: Report race-stratified chronic condition effects

### 7.3 Baseline Health Status Stratification

Using General Health Status (HSD010):
- Excellent/Very Good/Good (expected ~70%)
- Fair/Poor (expected ~30%)

**Rationale**: Effect of chronic conditions may differ by baseline health.

## 8. Sensitivity Analysis Specifications

### 8.1 Alternative Outcome Specifications

**Analysis 1a: Binary Outcome (Any Poor Days)**
```
Y = 1 if HSQ470 > 0, else 0
Model: Survey-adjusted logistic regression
Report: Odds Ratios with 95% CI
```

**Analysis 1b: Severe Outcome (Half Month or More)**
```
Y = 1 if HSQ470 ≥ 14, else 0
Model: Survey-adjusted logistic regression
Report: Odds Ratios with 95% CI
```

**Analysis 1c: Categorical Outcome**
```
Categories:
- 0 days (reference)
- 1-7 days
- 8-14 days
- 15-30 days

Model: Survey-adjusted multinomial logistic regression
Report: Relative Risk Ratios with 95% CI
```

### 8.2 Alternative Model Specifications

**Poisson Regression**:
- Use if overdispersion test not significant
- Report incidence rate ratios
- Compare fit statistics with negative binomial

**Zero-Inflated Models**:
```
Zero-inflation model: logit(π) = γ₀ + γ₁(ChronicConditions) + γ₂(Age)
Count model: NB or Poisson as above
```

**Hurdle Models**:
- Two-part: Logistic for zero vs. non-zero, then truncated count model
- Compare with ZINB using AIC/BIC

### 8.3 Missing Data Sensitivity

**Complete Case Analysis** (Primary):
- Exclude observations with any missing values
- Expected missing: <10% for most variables

**Multiple Imputation** (Sensitivity):
```
Imputation model: Predictive mean matching (continuous), logistic (binary)
Number of imputations: m = 20
Variables in imputation: All analysis variables + auxiliary variables
Pooling: Rubin's rules
```

**Inverse Probability Weighting**:
- Weight by inverse of probability of being complete
- Compare with complete case results

### 8.4 Weight Specifications

**Alternative 1: Separate Cycle Analysis**
- Analyze each 2-year cycle separately
- Meta-analyze results using random effects model
- Report I² for heterogeneity

**Alternative 2: Different Weight Variables**
- Use WTMEC2YR_D1 (day 1 weights) if dietary variables included
- Use interview weights only (WTINT2YR) for interview-only variables

### 8.5 Trimmed Analyses

**Trimming Strategies**:
1. Remove top/bottom 1% of continuous variables
2. Remove top/bottom 5% of continuous variables
3. Winsorize at 1st and 99th percentiles

**Compare**: Primary coefficients across trimming strategies

## 9. Output Specifications

### 9.1 Required Tables

**Table 1: Descriptive Characteristics**
| Characteristic | Unweighted n | Weighted % or Mean (SE) |
|----------------|--------------|-------------------------|
| Age (years) | | |
| Race/Ethnicity | | |
| ... | | |

**Table 2: Primary Hypothesis Results**
| Exposure | Model 1 (Crude) | Model 2 (Demog) | Model 3 (+SES) | Model 4 (Full) |
|----------|-----------------|-----------------|----------------|----------------|
| Chronic Conditions | | | | |
| 1 vs. 0 | IRR (95% CI) | ... | ... | ... |
| 2 vs. 0 | | | | |
| 3+ vs. 0 | | | | |

**Table 3: Secondary Hypotheses Results**
| Hypothesis | Exposure | Adjusted IRR (95% CI) | p-value |
|------------|----------|----------------------|---------|
| H2 | Mental health days | | |
| H3 | Education (<HS vs. Coll+) | | |
| ... | ... | | |

**Table 4: Interaction Analyses**
| Interaction | Test Statistic | p-value | Interpretation |
|-------------|----------------|---------|----------------|
| Chronic × Age Group | F(df1, df2) = X.XX | 0.XXX | |
| Chronic × Race | | | |

### 9.2 Required Figures

**Figure 1: STROBE Flow Diagram**
Visual representation of participant flow from initial sample to analytic sample.

**Figure 2: Distribution of Primary Outcome**
Histogram or bar chart of physical health days distribution with fitted negative binomial overlay.

**Figure 3: Effect Estimates Forest Plot**
Forest plot showing IRRs and 95% CIs for all chronic condition categories across different model specifications.

**Figure 4: Stratified Analyses**
Panel figure showing age-stratified and race-stratified effect estimates.

**Figure 5: Predicted Margins**
Plot of predicted physical health days by chronic condition count, adjusted for covariates, with confidence intervals.

### 9.3 Model Diagnostics Output

**Diagnostic Report**:
1. Overdispersion test result
2. Zero-inflation test result
3. Linearity assessment plots
4. Residual plots
5. Influence statistics (top 10 observations)
6. Multicollinearity table (VIFs)

## 10. Quality Control Checklist

### Pre-Analysis
- [ ] All variables coded correctly
- [ ] Missing value codes properly handled
- [ ] Survey design variables validated
- [ ] Weights properly scaled for pooling
- [ ] Outlier screening completed

### During Analysis
- [ ] Model convergence achieved
- [ ] No empty cells in categorical variables
- [ ] All assumptions tested
- [ ] Sensitivity analyses completed

### Post-Analysis
- [ ] All tables generated
- [ ] All figures generated at 300 DPI
- [ ] Results cross-validated
- [ ] Code documented
- [ ] Reproducibility verified

## 11. Analysis Timeline

| Phase | Task | Estimated Time |
|-------|------|----------------|
| 1 | Data preparation and cleaning | 2 days |
| 2 | Descriptive analyses | 1 day |
| 3 | Primary model fitting | 2 days |
| 4 | Model diagnostics and refinement | 2 days |
| 5 | Secondary hypotheses | 2 days |
| 6 | Interaction analyses | 2 days |
| 7 | Sensitivity analyses | 3 days |
| 8 | Output generation | 2 days |
| **Total** | | **16 days** |

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-08  
**Approved By**: Methods Definition Agent  
**Next Review**: Prior to analysis execution
