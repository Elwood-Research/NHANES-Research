# Reproducibility Information

## Analysis Execution

All analyses were conducted in the `nhanes-analysis-vault` Docker container with the following specifications:

### Docker Command
```bash
docker run --rm \
  --network none \
  -v "/home/joshbot/NHANES_BOT/Processed Data/Data:/data:ro" \
  -v "/home/joshbot/NHANES_BOT/studies/older-men-health-days-2026-02-08:/study" \
  nhanes-analysis-vault \
  python3 /study/04-analysis/scripts/<script_name>.py
```

### Script Execution Order
1. `01_data_prep.py` - Data loading, merging, and cleaning
2. `02_descriptive.py` - Weighted descriptive statistics
3. `03_regression.py` - Primary and secondary regression models
4. `04_sensitivity.py` - Robustness checks and sensitivity analyses
5. `05_outputs.py` - Figure and table generation

### Output Artifacts

#### Data Files
- `04-analysis/data/analytic_sample.csv`: Cleaned analytic dataset
- `04-analysis/outputs/analytic_metadata.json`: Dataset metadata
- `04-analysis/outputs/flow_counts.json`: STROBE flow counts
- `04-analysis/outputs/outcome_summary.json`: Outcome statistics
- `04-analysis/outputs/regression_results.json`: Full regression results
- `04-analysis/outputs/sensitivity_results.json`: Sensitivity analysis results

#### Tables (LaTeX format)
- `04-analysis/outputs/tables/table1.tex`: Baseline characteristics
- `04-analysis/outputs/tables/table1_stratified.tex`: Stratified baseline characteristics
- `04-analysis/outputs/tables/table2.tex`: Bivariate associations
- `04-analysis/outputs/tables/table3.tex`: Multivariable regression results
- `04-analysis/outputs/tables/table4.tex`: Sensitivity analyses

#### Figures (300 DPI PNG)
- `04-analysis/outputs/figures/strobe_flowchart.png`: STROBE flow diagram
- `04-analysis/outputs/figures/figure1_distribution.png`: Outcome distributions
- `04-analysis/outputs/figures/figure2_associations.png`: Forest plot
- `04-analysis/outputs/figures/figure3_interactions.png`: Interaction plots

### Software Versions
- Python: 3.9+
- pandas: 1.5+
- numpy: 1.23+
- statsmodels: 0.13+
- matplotlib: 3.6+
- seaborn: 0.12+

### Data Source
- NHANES 2001-2018 (9 cycles, B-J)
- Downloaded from: https://www.cdc.gov/nchs/nhanes/

### Quality Control Measures
- Outliers removed: |z| > 4 for continuous variables
- Missing data: Listwise deletion for incomplete cases
- Survey weights: WTMEC2YR divided by number of cycles (9)
- Variance estimation: Taylor series linearization

### Privacy Protection
- No individual-level data in outputs
- Only aggregated statistics reported
- Docker container run with --network none
