# Data and Variable Requirements

## Primary Outcome Variables

### Physical Health Days (Primary)
- **Dataset**: HSQ (Current Health Status)
- **Variable**: HSQ470
- **Label**: Number of days physical health was not good
- **Range**: 0-30 days
- **Target**: Males age 60+

### Activity Limitation Days (Secondary)
- **Dataset**: HSQ
- **Variable**: HSQ490
- **Label**: Inactive days due to physical/mental health
- **Range**: 0-30 days

### Mental Health Days (Covariate)
- **Dataset**: HSQ
- **Variable**: HSQ480
- **Label**: Number of days mental health was not good
- **Range**: 0-30 days

## Demographic Variables (DEMO)
- RIAGENDR: Gender (filter: Male = 1)
- RIDAGEYR: Age in years (filter: >= 60)
- RIDRETH1/RIDRETH3: Race/Ethnicity
- DMDEDUC2: Education level
- DMDMARTL: Marital status
- INDFMPIR: Family income-to-poverty ratio
- SDMVSTRA: Sampling strata
- SDMVPSU: Primary sampling unit
- WTMEC2YR/WTMECPRP: Examination weights

## Health-Related Covariates to Explore

### Chronic Conditions
- BPQ: Blood pressure/cholesterol
- DIQ: Diabetes
- CDQ: Cardiovascular disease
- KIQ: Kidney conditions
- MCQ: Medical conditions

### Physical Function
- PFQ: Physical functioning
- DLQ: Disability

### Lifestyle Factors
- PAQ: Physical activity
- SMQ: Smoking
- ALQ: Alcohol use

### Anthropometrics (BMX)
- BMXBMI: Body mass index
- BMXWAIST: Waist circumference

## Data Years Required
- Minimum: Multiple cycles for adequate sample size of older men
- Preferred: 2001-2018 (cycles B through J) for comprehensive analysis
- Single cycle minimum sample: ~200-300 older men per 2-year cycle

## Quality Criteria
- Sample size target: N >= 1000 older men
- Missing data handling: Document exclusions
- Survey weights: Must use appropriate MEC weights
