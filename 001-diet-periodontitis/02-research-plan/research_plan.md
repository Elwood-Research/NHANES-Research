# Research Plan: Dietary nutrient intake and periodontitis

## 1. Title and Objective
**Title:** Association between dietary nutrient intake and periodontitis in U.S. adults: NHANES 2009-2014.

**Objective:** To investigate the association between dietary intakes of sugars, fiber, vitamin C, and calcium with the prevalence and severity of periodontitis in a representative sample of U.S. adults.

## 2. Study Design
- **Design:** Cross-sectional analysis.
- **Data Source:** National Health and Nutrition Examination Survey (NHANES).
- **Cycles:** 2009-2010 (F), 2011-2012 (G), 2013-2014 (H).
- **Rationale:** These cycles contain the full-mouth periodontal examination (FMPE) and consistent dietary recall data.

## 3. Study Population
### Inclusion Criteria
- Adults aged 30 years and older (target population for periodontal exam).
- Completed the full-mouth periodontal examination (Status code `OHDPDSTS` = 1).
- Completed the first 24-hour dietary recall (Day 1) with reliable status (`DR1DRSTZ` = 1).

### Exclusion Criteria
- Edentulous participants (missing periodontal measurements).
- Medical exclusion from periodontal examination (`OHDEXCLU` = 1).
- Pregnant or lactating women.
- Missing covariate data (education, income, BMI, smoking, diabetes status).

## 4. Variables
### Exposure: Dietary Nutrient Intake (24-hour recall)
Derived from `DR1TOT` (Day 1 Total Nutrients):
- **Total Sugars:** `DR1TSUGR` (g/day).
- **Dietary Fiber:** `DR1TFIBE` (g/day).
- **Vitamin C:** `DR1TVC` (mg/day).
- **Calcium:** `DR1TCALC` (mg/day).
- **Total Energy:** `DR1TKCAL` (kcal/day) - *Adjustment variable*.

### Outcome: Periodontitis Status
Derived from `OHXPER` (Periodontal Exam):
- **Clinical Attachment Loss (CAL):** `OHX*LA*` (Calculated as Pocket Depth + Recession).
- **Probing Depth (PD):** `OHX*PC*`.
- **Case Definitions (CDC/AAP):**
    - **Severe Periodontitis:** $\ge$ 2 interproximal sites with AL $\ge$ 6mm (not on same tooth) AND $\ge$ 1 interproximal site with PD $\ge$ 5mm.
    - **Moderate Periodontitis:** $\ge$ 2 interproximal sites with AL $\ge$ 4mm (not on same tooth) OR $\ge$ 2 interproximal sites with PD $\ge$ 5mm (not on same tooth).
    - **Mild/No Periodontitis:** Neither moderate nor severe.
    - *Binary Outcome:* Moderate/Severe vs. Mild/None.

### Covariates
- **Demographics:** Age (`RIDAGEYR`), Gender (`RIAGENDR`), Race/Ethnicity (`RIDRETH1`), Education (`DMDEDUC2`), Ratio of family income to poverty (`INDFMPIR`).
- **Health Behaviors:** Smoking status (`SMQ` - current/former/never), Alcohol use (`ALQ`).
- **Health Status:** BMI (`BMXBMI`), Diabetes (`DIQ010`), Number of teeth (`OHXDEN`).
- **Oral Hygiene:** Frequency of interdental cleaning/flossing (`OHQ`).

## 5. Statistical Analysis Plan
1.  **Descriptive Statistics:**
    - Means and SE for continuous variables.
    - Frequencies and weighted percentages for categorical variables.
    - Comparison of characteristics by periodontitis status (Rao-Scott Chi-Square / t-tests).

2.  **Regression Analysis:**
    - **Model:** Multivariable logistic regression.
    - **Outcome:** Periodontitis (Moderate/Severe vs. None/Mild).
    - **Exposures:** Nutrient intakes (continuous or quartiles).
    - **Adjustments:**
        - Model 1: Unadjusted.
        - Model 2: Age, Gender, Race, Energy Intake.
        - Model 3: Model 2 + Education, Income, BMI, Smoking, Diabetes, Oral Hygiene.
    - **Survey Weights:** Construct 6-year weights (`WTMEC6YR`) by dividing the 2-year MEC weight (`WTMEC2YR`) by 3.

3.  **Sensitivity Analysis:**
    - Adjusting for frequency of dental visits.
    - Excluding diabetics.
