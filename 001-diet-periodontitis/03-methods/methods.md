# Methods

## Study Design and Population
This study utilized data from the National Health and Nutrition Examination Survey (NHANES), a continuous cross-sectional survey designed to assess the health and nutritional status of the U.S. population. Data from three 2-year cycles (2009-2010, 2011-2012, and 2013-2014) were combined to ensure sufficient sample size for periodontal outcomes, which were assessed via full-mouth examination in adults aged 30 years and older during these cycles.

The study population included all adults aged 30 years and older who completed the full-mouth periodontal examination and provided valid dietary recall data. Participants were excluded if they were edentulous, pregnant, or had missing data on key covariates.

## Variable Definitions

### Periodontal Outcome
Periodontitis was defined using the Centers for Disease Control and Prevention/American Academy of Periodontology (CDC/AAP) case definitions for population-based surveillance.
- **Severe Periodontitis**: $\ge$2 interproximal sites with clinical attachment loss (CAL) $\ge$6 mm (not on the same tooth) AND $\ge$1 interproximal site with probing depth (PD) $\ge$5 mm.
- **Moderate Periodontitis**: $\ge$2 interproximal sites with CAL $\ge$4 mm (not on the same tooth) OR $\ge$2 interproximal sites with PD $\ge$5 mm (not on the same tooth).
- **Mild Periodontitis**: $\ge$2 interproximal sites with CAL $\ge$3 mm AND $\ge$2 interproximal sites with PD $\ge$4 mm (not on the same tooth) or one site with PD $\ge$5 mm.
- **Total Periodontitis**: Any classification of mild, moderate, or severe periodontitis.
- **Healthy/No Periodontitis**: Individuals not meeting the criteria for mild, moderate, or severe disease.

The primary outcome was dichotomized as **moderate/severe periodontitis** vs. **no/mild periodontitis** for logistic regression analysis, consistent with previous literature emphasizing the clinical significance of moderate-to-severe disease.

### Dietary Exposures
Dietary intake data were obtained from the first 24-hour dietary recall interview (Day 1). The primary exposures of interest were:
1.  **Total Sugars (g/day)**: Sum of all mono- and disaccharides.
2.  **Dietary Fiber (g/day)**: Total dietary fiber.
3.  **Vitamin C (mg/day)**: Total ascorbic acid.
4.  **Calcium (mg/day)**: Total calcium.

All dietary variables were modeled as continuous variables. To account for differences in total energy intake, we adjusted for total caloric intake (kcal/day) in multivariable models. Extreme outliers in dietary data (>4 SD from the mean) were excluded to prevent leverage by implausible values.

### Covariates
Covariates were selected a priori based on known associations with periodontitis and dietary habits:
- **Demographic Factors**: Age (years), Sex (Male/Female), Race/Ethnicity (Non-Hispanic White, Non-Hispanic Black, Mexican American, Other), Education (<High School, High School/GED, >High School), and Ratio of Family Income to Poverty (PIR).
- **Health Behaviors**: Smoking status (Current, Former, Never), Alcohol consumption (drinks/day), and Physical Activity (Active vs. Inactive based on moderate/vigorous recreational activity).
- **Clinical Characteristics**: Body Mass Index (BMI, kg/m²), Diabetes status (Self-reported diagnosis or HbA1c $\ge$6.5% or Fasting Plasma Glucose $\ge$126 mg/dL), and Number of Teeth present.
- **Oral Hygiene**: Frequency of interdental cleaning (flossing) was categorized as daily (7 days/week), frequent (4-6 days/week), infrequent (1-3 days/week), or never (0 days/week).

## Statistical Analysis
All statistical analyses were performed using Python (pandas, statsmodels) within a secure analysis vault, accounting for the complex survey design of NHANES.

### Weighting
Six-year examination weights (`WTMEC6YR`) were constructed by dividing the 2-year Mobile Examination Center (MEC) weights (`WTMEC2YR`) by 3, as recommended by NCHS analytical guidelines for combining three survey cycles. These weights account for unequal probabilities of selection, non-response, and oversampling of certain demographic groups.

### Descriptive Statistics
Weighted means and standard errors (SE) were calculated for continuous variables, and weighted frequencies and percentages were calculated for categorical variables. Baseline characteristics were stratified by periodontitis status (Moderate/Severe vs. None/Mild). Differences between groups were assessed using t-tests for continuous variables and Rao-Scott Chi-square tests for categorical variables.

### Regression Modeling
Multivariable logistic regression models were used to estimate odds ratios (ORs) and 95% confidence intervals (CIs) for the association between each nutrient intake and the prevalence of moderate/severe periodontitis.
- **Model 1**: Unadjusted.
- **Model 2**: Adjusted for Age, Sex, Race/Ethnicity, and Total Energy Intake.
- **Model 3**: Further adjusted for Education, Income-to-Poverty Ratio, Smoking Status, BMI, Diabetes, Alcohol Intake, Physical Activity, and Oral Hygiene (flossing).

Statistical significance was defined as a two-sided p-value < 0.05.
