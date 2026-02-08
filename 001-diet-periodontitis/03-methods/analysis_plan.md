# Statistical Analysis Plan

## 1. Data Preparation

### 1.1 Datasets
Load and merge the following datasets for cycles 2009-2010 (F), 2011-2012 (G), and 2013-2014 (H):
- **Demographics**: `DEMO` (SEQN, RIDAGEYR, RIAGENDR, RIDRETH1, DMDEDUC2, INDFMPIR, WTMEC2YR, SDMVPSU, SDMVSTRA)
- **Dietary**: `DR1TOT` (SEQN, DR1TSUGR, DR1TFIBE, DR1TVC, DR1TCALC, DR1TKCAL, DR1DRSTZ)
- **Periodontal**: `OHXPER` (SEQN, OHDDESTS, and all OHX*LA* / OHX*PC* columns)
- **Dentition**: `OHXDEN` (SEQN, OHXDEN) - *Optional if needed for tooth count*
- **BMI**: `BMX` (SEQN, BMXBMI)
- **Smoking**: `SMQ` (SEQN, SMQ020, SMQ040)
- **Diabetes**: `DIQ` (SEQN, DIQ010)
- **Alcohol**: `ALQ` (SEQN, ALQ130)
- **Physical Activity**: `PAQ` (SEQN, PAQ605, PAQ620)
- **Oral Health Q**: `OHQ` (SEQN, OHQ870)

### 1.2 Merging
1.  Concatenate cycles vertically (F+G+H).
2.  Merge all domains on `SEQN`.

### 1.3 Exclusion Criteria (Sequential)
Create a STROBE flow diagram tracking counts at each step:
1.  **Total Population**: All participants in merged dataset.
2.  **Age Filter**: Exclude age < 30.
3.  **Periodontal Exam**: Exclude if periodontal status code `OHDDESTS` != 1 (Complete).
4.  **Dietary Recall**: Exclude if `DR1DRSTZ` != 1 (Reliable).
5.  **Missing Covariates**: Exclude rows with missing data for any model covariate.
6.  **Dietary Outliers**: Exclude if total energy or key nutrients > 4 SD from mean.
7.  **Final Analytical Sample**: Count $N$.

## 2. Variable Transformation

### 2.1 Outcome: Periodontitis Status
Implement CDC/AAP case definitions using `OHX*LA*` (CAL) and `OHX*PC*` (PD) columns.
*Note: Ensure you handle the "not on same tooth" logic by grouping sites by tooth ID.*

- **Severe**: $\ge$2 interproximal sites with CAL $\ge$6mm (not same tooth) AND $\ge$1 interproximal site with PD $\ge$5mm.
- **Moderate**: $\ge$2 interproximal sites with CAL $\ge$4mm (not same tooth) OR $\ge$2 interproximal sites with PD $\ge$5mm (not same tooth).
- **Mild**: $\ge$2 interproximal sites with CAL $\ge$3mm AND $\ge$2 interproximal sites with PD $\ge$4mm (not same tooth) OR 1 site PD $\ge$5mm.

**Binary Outcome**:
- `perio_case`: 1 if Moderate or Severe; 0 if Mild or None.

### 2.2 Exposures
- Keep continuous: `DR1TSUGR` (Sugars), `DR1TFIBE` (Fiber), `DR1TVC` (Vit C), `DR1TCALC` (Calcium).
- Calculate z-scores for descriptive checking, but use raw units in models.

### 2.3 Covariates
- **Race/Ethnicity**: Recode `RIDRETH1` (1=MexAm, 2=OtherHisp, 3=White, 4=Black, 5=Other) -> {1: 'Mexican American', 2: 'Other Hispanic', 3: 'Non-Hispanic White', 4: 'Non-Hispanic Black', 5: 'Other'}.
- **Education**: Recode `DMDEDUC2` (1-2=<HS, 3=HS/GED, 4-5=>HS).
- **Smoking**:
  - Current: `SMQ040` in [1,2].
  - Former: `SMQ020`=1 AND `SMQ040`=3.
  - Never: `SMQ020`=2.
- **Diabetes**: `DIQ010` (1=Yes, 2=No, 3=Borderline -> No).
- **Alcohol**: Continuous `ALQ130` (avg drinks/day). Impute 0 for non-drinkers if needed.
- **Physical Activity**: `PAQ605`=1 OR `PAQ620`=1 -> Active; else Inactive.
- **Flossing**: `OHQ870` (days/week). Categorize: 0 (Never), 1-3 (Infrequent), 4-6 (Frequent), 7 (Daily).
- **Weight**: Create `WTMEC6YR` = `WTMEC2YR` / 3.

## 3. Statistical Analysis

### 3.1 Descriptive Statistics (Table 1)
- Stratify by `perio_case` (0 vs 1).
- Continuous: Weighted Mean (SE). Test: T-test.
- Categorical: Weighted % (SE). Test: Chi-square.

### 3.2 Regression Models (Table 2 & 3)
Run separate logistic regression models for each exposure (Sugars, Fiber, Vit C, Calcium).

- **Model 1**: Exposure + Constant.
- **Model 2**: Exposure + Age + Sex + Race + Kcal.
- **Model 3**: Exposure + Age + Sex + Race + Kcal + Education + PIR + Smoking + BMI + Diabetes + Alcohol + PA + Flossing.

Report: Odds Ratio (OR), 95% CI, p-value.

### 3.3 Sensitivity Analysis
- Rerun Model 3 excluding participants with extreme dietary values (>4 SD).

## 4. Outputs
Save the following to `04-analysis/outputs/`:
- `table1_characteristics.csv`
- `table2_bivariate.csv`
- `table3_models.csv` (Coefficients, ORs, CIs, P-values)
- `strobe_flow_counts.json` (Counts for each step)
- `figures/strobe_flow.png` (Visual flow diagram)
