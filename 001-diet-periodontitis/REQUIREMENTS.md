# Requirements

## Data domains
This study requires dietary intake totals, periodontal examination measures, and standard confounders from demographic, questionnaire, and exam components.

## Candidate datasets (processed)
- Demographics: `DEMO`
- Dietary totals (24-hour recall): `DR1TOT` (and `DR2TOT` if using 2-day averages / usual intake sensitivity)
- Periodontal examination: `OHXPER` (2009-2010 through 2013-2014 are expected to be key)
- Oral health questionnaire (dental care / hygiene): `OHQ`
- Dentition / tooth count: `OHXDEN` (and/or `OHXDENT`)
- Smoking: `SMQ`
- Diabetes: `DIQ`
- Body measures: `BMX`
- Physical activity: `PAQ`
- Alcohol: `ALQ`

## High-level variable feasibility checks (docs-based)
- Periodontal outcome availability:
  - `OHXPER` contains periodontal exam status, exclusion flags, a periodontal status code, and site-level measures for clinical attachment loss (loss of attachment) with wide coverage in years F/G/H.
- Dietary exposure availability:
  - `DR1TOT` contains day-1 totals for total energy, total sugars, dietary fiber, vitamin C, calcium (and many other nutrients) across multiple cycles.
- Oral hygiene / dental care covariates:
  - `OHQ` includes time since last dental visit and flossing frequency (available in multiple cycles).

## Notes on weights
Final analysis will need a consistent weighting strategy that aligns dietary recall and periodontal exam participation (e.g., MEC exam weights vs dietary day-1 weights), with cycle combination handled per NHANES guidance.

## Technical Constraints
- Use only local NHANES processed data and docs in this repository.
- Run analysis only in nhanes-analysis-vault with --network none.
- Mount data as /data:ro and the active study folder as /study.
- Never output participant-level rows; aggregate results only.
- Use human-readable variable labels in manuscript, tables, and figures.
- Apply outlier rule |z| > 4 and categorical exclusion <5% with STROBE accounting.
- Publish to GitHub: true
- Target repo: https://github.com/Elwood-Research/NHANES-Research
