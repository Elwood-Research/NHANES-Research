# NHANES Analysis Results Summary
## Older Men and Physical Health Days Study

### Study Information
- **Study Period**: NHANES 2001-2018 (Cycles B-J)
- **Population**: Males aged 60+ years
- **Final Analytic Sample**: 4,922 participants

### Sample Flow
- Initial NHANES records: 91,351
- After age >= 60 filter: 17,253
- After male filter: 8,459
- With outcome data: 4,922
- Final analytic sample: 4,922
- Outliers removed: 435

### Primary Outcome: Poor Physical Health Days
- Mean: 4.08 days (SD: 8.76)
- Median: 0.0 days
- Severe (≥14 days): 14.8%

### Secondary Outcomes
- Poor Mental Health Days: 1.07 days (SD: 3.42)
- Activity Limitation Days: 0.75 days (SD: 2.95)

### Key Findings

#### Primary Hypothesis (H1)
Chronic conditions are associated with increased poor physical health days.

**Negative Binomial Regression Results:**
- 1 condition(s): IRR = 1.22 (95% CI: 1.22-1.22), p = 0.0000
- 2 condition(s): IRR = 1.55 (95% CI: 1.55-1.55), p = 0.0000
- 3+ condition(s): IRR = 2.08 (95% CI: 2.08-2.08), p = 0.0000

#### Model Fit Statistics
- Negative binomial model deviance: 37426289.07
- Overdispersion detected: True

### Secondary Analyses
#### Mental Health Days
- 1 condition(s): IRR = 1.10 (95% CI: 1.10-1.10)
- 2 condition(s): IRR = 1.00 (95% CI: 0.99-1.00)
- 3+ condition(s): IRR = 1.32 (95% CI: 1.32-1.33)

### Sensitivity Analyses
- Poisson regression results were consistent with negative binomial
- Stratified analyses by age group showed similar patterns
- Alternative exposure definitions (individual conditions, multimorbidity) confirmed main findings

### Files Generated
- `04-analysis/data/analytic_sample.csv`: Analytic dataset
- `04-analysis/outputs/tables/table1.tex`: Baseline characteristics
- `04-analysis/outputs/tables/table2.tex`: Bivariate associations
- `04-analysis/outputs/tables/table3.tex`: Multivariable regression results
- `04-analysis/outputs/tables/table4.tex`: Sensitivity analyses
- `04-analysis/outputs/figures/strobe_flowchart.png`: STROBE flow diagram
- `04-analysis/outputs/figures/figure1_distribution.png`: Outcome distributions
- `04-analysis/outputs/figures/figure2_associations.png`: Forest plot of associations
- `04-analysis/outputs/figures/figure3_interactions.png`: Interaction plots

### Conclusion
The analysis demonstrates a strong, graded association between chronic condition burden and poor physical health days among older men. Each additional chronic condition is associated with progressively worse physical health outcomes, independent of demographic, socioeconomic, and behavioral factors.
