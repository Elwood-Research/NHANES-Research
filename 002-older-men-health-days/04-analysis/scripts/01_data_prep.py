#!/usr/bin/env python3
"""
NHANES Analysis: Older Men and Physical Health Days
Data Preparation Script (01_data_prep.py)

Loads, merges, and cleans NHANES data for cycles B-J (2001-2018)
Creates analytic dataset with chronic condition count and all covariates
"""

import pandas as pd
import numpy as np
import os
import sys
import json
from pathlib import Path

# Output only aggregated results - no individual data
np.random.seed(42)

# Paths (inside Docker vault)
DATA_DIR = Path("/data")
STUDY_DIR = Path("/study")
OUTPUT_DIR = STUDY_DIR / "04-analysis"
DATA_OUTPUT = OUTPUT_DIR / "data"

# Cycles to include (B-J = 2001-2018)
CYCLES = ["B", "C", "D", "E", "F", "G", "H", "I", "J"]
CYCLE_YEARS = {
    "B": "2001-2002",
    "C": "2003-2004",
    "D": "2005-2006",
    "E": "2007-2008",
    "F": "2009-2010",
    "G": "2011-2012",
    "H": "2013-2014",
    "I": "2015-2016",
    "J": "2017-2018",
}

# Number of cycles for weight adjustment
N_CYCLES = len(CYCLES)

print("=" * 70)
print("NHANES Data Preparation: Older Men and Physical Health Days")
print("=" * 70)
print(f"Cycles: {', '.join([f'{c} ({CYCLE_YEARS[c]})' for c in CYCLES])}")
print(f"Output Directory: {OUTPUT_DIR}")
print("=" * 70)

# Tracking for STROBE flow diagram
flow_counts = {
    "initial_records": 0,
    "after_age_filter": 0,
    "after_sex_filter": 0,
    "with_outcome_data": 0,
    "final_analytic_sample": 0,
    "outliers_removed": 0,
    "missing_covariates": 0,
}


def load_and_merge_cycle(cycle):
    """Load and merge all datasets for a single cycle."""
    print(f"\n--- Processing Cycle {cycle} ({CYCLE_YEARS[cycle]}) ---")

    datasets = {}

    # Load core datasets
    try:
        datasets["demo"] = pd.read_csv(DATA_DIR / f"DEMO_{cycle}.csv")
        print(f"  DEMO: {len(datasets['demo'])} records")
    except Exception as e:
        print(f"  ERROR loading DEMO_{cycle}: {e}")
        return None

    try:
        datasets["hsq"] = pd.read_csv(DATA_DIR / f"HSQ_{cycle}.csv")
        print(f"  HSQ: {len(datasets['hsq'])} records")
    except Exception as e:
        print(f"  ERROR loading HSQ_{cycle}: {e}")
        return None

    # Load condition datasets
    for prefix in ["DIQ", "BPQ", "CDQ"]:
        try:
            datasets[prefix.lower()] = pd.read_csv(DATA_DIR / f"{prefix}_{cycle}.csv")
            print(f"  {prefix}: {len(datasets[prefix.lower()])} records")
        except Exception as e:
            print(f"  WARNING: {prefix}_{cycle} not found, creating empty")
            datasets[prefix.lower()] = pd.DataFrame(columns=["SEQN"])

    # Load covariate datasets
    for prefix in ["PAQ", "SMQ", "BMX", "HIQ"]:
        try:
            datasets[prefix.lower()] = pd.read_csv(DATA_DIR / f"{prefix}_{cycle}.csv")
            print(f"  {prefix}: {len(datasets[prefix.lower()])} records")
        except Exception as e:
            print(f"  WARNING: {prefix}_{cycle} not found, creating empty")
            datasets[prefix.lower()] = pd.DataFrame(columns=["SEQN"])

    # Merge all datasets on SEQN
    merged = datasets["demo"].copy()
    for name, df in datasets.items():
        if name != "demo":
            merged = merged.merge(df, on="SEQN", how="left")

    # Add cycle identifier
    merged["cycle"] = cycle
    merged["cycle_year"] = CYCLE_YEARS[cycle]

    print(f"  Merged: {len(merged)} records")
    return merged


def safe_map(df, col, condition_true, condition_false, condition_missing=None):
    """Safely map values, handling missing columns."""
    if col not in df.columns:
        return np.nan
    if condition_missing is None:
        condition_missing = df[col].isna()
    return np.where(condition_true, 1, np.where(condition_false, 0, np.nan))


def process_chronic_conditions(df):
    """Create chronic condition indicators and count."""
    # Diabetes (DIQ010): 1=Yes, 2=No, 3=Borderline
    if "DIQ010" in df.columns:
        df["diabetes"] = np.where(
            df["DIQ010"].isin([1, 3]), 1, np.where(df["DIQ010"] == 2, 0, np.nan)
        )
    else:
        df["diabetes"] = np.nan

    # Hypertension (BPQ020): 1=Yes, 2=No
    if "BPQ020" in df.columns:
        df["hypertension"] = np.where(
            df["BPQ020"] == 1, 1, np.where(df["BPQ020"] == 2, 0, np.nan)
        )
    else:
        df["hypertension"] = np.nan

    # High Cholesterol (BPQ080): 1=Yes, 2=No
    if "BPQ080" in df.columns:
        df["high_cholesterol"] = np.where(
            df["BPQ080"] == 1, 1, np.where(df["BPQ080"] == 2, 0, np.nan)
        )
    else:
        df["high_cholesterol"] = np.nan

    # Cardiovascular Disease (from CDQ001, CDQ009)
    # CDQ001: chest pain, CDQ009: severe chest pain >30 min
    if "CDQ001" in df.columns:
        df["chest_pain"] = np.where(
            df["CDQ001"] == 1, 1, np.where(df["CDQ001"] == 2, 0, np.nan)
        )
    else:
        df["chest_pain"] = np.nan

    if "CDQ009" in df.columns:
        df["severe_chest_pain"] = np.where(
            df["CDQ009"] == 1, 1, np.where(df["CDQ009"] == 2, 0, np.nan)
        )
    else:
        df["severe_chest_pain"] = np.nan

    # CVD = either chest pain indicator
    df["cvd"] = np.where(
        (df["chest_pain"] == 1) | (df["severe_chest_pain"] == 1),
        1,
        np.where((df["chest_pain"] == 0) & (df["severe_chest_pain"] == 0), 0, np.nan),
    )

    # Chronic condition count
    conditions = ["diabetes", "hypertension", "high_cholesterol", "cvd"]
    df["chronic_count"] = df[conditions].sum(axis=1, min_count=1)

    # Categorize
    df["chronic_cat"] = np.where(
        df["chronic_count"] >= 3,
        "3+",
        np.where(
            df["chronic_count"] == 2, "2", np.where(df["chronic_count"] == 1, "1", "0")
        ),
    )

    return df


def process_outcomes(df):
    """Process health outcome variables."""
    # Physical health days (HSQ470): 0-30, 77=refused, 99=don't know
    df["physical_health_days"] = np.where(
        df["HSQ470"].isin([77, 99]),
        np.nan,
        np.where((df["HSQ470"] >= 0) & (df["HSQ470"] <= 30), df["HSQ470"], np.nan),
    )

    # Mental health days (HSQ480): 0-30, 77=refused, 99=don't know
    df["mental_health_days"] = np.where(
        df["HSQ480"].isin([77, 99]),
        np.nan,
        np.where((df["HSQ480"] >= 0) & (df["HSQ480"] <= 30), df["HSQ480"], np.nan),
    )

    # Activity limitation days (HSQ490): 0-30, 77=refused, 99=don't know
    df["activity_limitation_days"] = np.where(
        df["HSQ490"].isin([77, 99]),
        np.nan,
        np.where((df["HSQ490"] >= 0) & (df["HSQ490"] <= 30), df["HSQ490"], np.nan),
    )

    # General health status (HSD010): 1-5, 7=refused, 9=don't know
    df["general_health"] = np.where(
        df["HSD010"].isin([7, 9]),
        np.nan,
        np.where((df["HSD010"] >= 1) & (df["HSD010"] <= 5), df["HSD010"], np.nan),
    )

    return df


def process_demographics(df):
    """Process demographic variables."""
    # Age (already in RIDAGEYR)
    df["age"] = df["RIDAGEYR"]

    # Sex (1=Male, 2=Female)
    df["sex"] = df["RIAGENDR"]

    # Race/Ethnicity
    race_map = {
        1: "Mexican American",
        2: "Other Hispanic",
        3: "Non-Hispanic White",
        4: "Non-Hispanic Black",
        5: "Other/Multi-racial",
    }
    df["race_ethnicity"] = df["RIDRETH1"].map(race_map)

    # Education
    # 1=<9th, 2=9-11th, 3=HS grad, 4=Some college, 5=College+, 7=Refused, 9=Don't know
    edu_map = {
        1: "< High School",
        2: "< High School",
        3: "High School Graduate",
        4: "Some College",
        5: "College Graduate+",
    }
    df["education"] = df["DMDEDUC2"].map(edu_map)

    # Marital status
    # 1=Married, 2=Widowed, 3=Divorced, 4=Separated, 5=Never married, 6=Living with partner
    marital_map = {
        1: "Married/Partner",
        2: "Widowed",
        3: "Divorced/Separated",
        4: "Divorced/Separated",
        5: "Never Married",
        6: "Married/Partner",
    }
    df["marital_status"] = df["DMDMARTL"].map(marital_map)

    return df


def process_ses(df):
    """Process socioeconomic variables."""
    # Income-to-poverty ratio
    if "INDFMPIR" in df.columns:
        df["poverty_ratio"] = df["INDFMPIR"]
        df["poverty_ratio"] = np.where(df["poverty_ratio"] > 5, 5, df["poverty_ratio"])
    else:
        df["poverty_ratio"] = np.nan

    # Health insurance (HIQ011): 1=Yes, 2=No
    if "HIQ011" in df.columns:
        df["has_insurance"] = np.where(
            df["HIQ011"] == 1, 1, np.where(df["HIQ011"] == 2, 0, np.nan)
        )
    else:
        df["has_insurance"] = np.nan

    return df


def process_health_behaviors(df):
    """Process health behavior variables."""
    # Smoking status
    # SMQ020: 1=Yes smoked 100+, 2=No
    # SMQ040: 1=Every day, 2=Some days, 3=Not at all
    df["smoking_status"] = "Unknown"
    if "SMQ020" in df.columns:
        df.loc[df["SMQ020"] == 2, "smoking_status"] = "Never"
        if "SMQ040" in df.columns:
            df.loc[(df["SMQ020"] == 1) & (df["SMQ040"] == 3), "smoking_status"] = (
                "Former"
            )
            df.loc[
                (df["SMQ020"] == 1) & (df["SMQ040"].isin([1, 2])), "smoking_status"
            ] = "Current"

    # Physical activity (simplified version)
    # Any vigorous activity
    vig_work = df.get("PAQ605", pd.Series([np.nan] * len(df)))
    vig_rec = df.get("PAQ650", pd.Series([np.nan] * len(df)))
    mod_work = df.get("PAQ620", pd.Series([np.nan] * len(df)))
    mod_rec = df.get("PAQ665", pd.Series([np.nan] * len(df)))

    df["vigorous_activity"] = np.where(
        (vig_work == 1) | (vig_rec == 1),
        1,
        np.where((vig_work == 2) & (vig_rec == 2), 0, np.nan),
    )

    # Any moderate activity
    df["moderate_activity"] = np.where(
        (mod_work == 1) | (mod_rec == 1),
        1,
        np.where((mod_work == 2) & (mod_rec == 2), 0, np.nan),
    )

    # Activity level categorization
    df["activity_level"] = "Unknown"
    df.loc[df["vigorous_activity"] == 1, "activity_level"] = "High"
    df.loc[
        (df["vigorous_activity"] == 0) & (df["moderate_activity"] == 1),
        "activity_level",
    ] = "Moderate"
    df.loc[
        (df["vigorous_activity"] == 0) & (df["moderate_activity"] == 0),
        "activity_level",
    ] = "Low"

    return df


def process_anthropometrics(df):
    """Process anthropometric variables."""
    # BMI
    if "BMXBMI" in df.columns:
        df["bmi"] = df["BMXBMI"]
        # BMI categories
        df["bmi_category"] = np.where(
            df["bmi"] < 18.5,
            "Underweight",
            np.where(
                df["bmi"] < 25,
                "Normal",
                np.where(
                    df["bmi"] < 30,
                    "Overweight",
                    np.where(df["bmi"] >= 30, "Obese", "Unknown"),
                ),
            ),
        )
    else:
        df["bmi"] = np.nan
        df["bmi_category"] = "Unknown"

    # Waist circumference
    if "BMXWAIST" in df.columns:
        df["waist_circumference"] = df["BMXWAIST"]
    else:
        df["waist_circumference"] = np.nan

    return df


def process_survey_weights(df):
    """Process survey design variables."""
    # Adjust weights for pooling (divide by number of cycles)
    if "WTMEC2YR" in df.columns:
        df["weight"] = df["WTMEC2YR"] / N_CYCLES
    else:
        df["weight"] = 1.0

    # Stratum and PSU
    if "SDMVSTRA" in df.columns:
        df["stratum"] = df["SDMVSTRA"]
    else:
        df["stratum"] = 1

    if "SDMVPSU" in df.columns:
        df["psu"] = df["SDMVPSU"]
    else:
        df["psu"] = 1

    return df


def remove_outliers(df):
    """Remove extreme outliers (|z| > 4) for continuous variables."""
    continuous_vars = [
        "age",
        "physical_health_days",
        "mental_health_days",
        "activity_limitation_days",
        "bmi",
        "poverty_ratio",
    ]

    outlier_count = 0
    for var in continuous_vars:
        if var in df.columns:
            valid = df[var].dropna()
            if len(valid) > 0:
                mean = valid.mean()
                std = valid.std()
                if std > 0:
                    z_scores = np.abs((df[var] - mean) / std)
                    outliers = (z_scores > 4) & df[var].notna()
                    outlier_count += outliers.sum()
                    df.loc[outliers, var] = np.nan

    return df, outlier_count


def main():
    print("\nLoading and merging data from all cycles...")

    # Load all cycles
    all_cycles = []
    for cycle in CYCLES:
        cycle_data = load_and_merge_cycle(cycle)
        if cycle_data is not None:
            all_cycles.append(cycle_data)

    if not all_cycles:
        print("ERROR: No data loaded!")
        sys.exit(1)

    # Combine all cycles
    df = pd.concat(all_cycles, ignore_index=True)
    flow_counts["initial_records"] = len(df)
    print(f"\n{'=' * 70}")
    print(f"Total records across all cycles: {flow_counts['initial_records']:,}")
    print(f"{'=' * 70}")

    # Process demographics first (needed for filtering)
    print("\n--- Processing Demographics ---")
    df["age"] = df["RIDAGEYR"]
    df["sex"] = df["RIAGENDR"]

    # Apply inclusion criteria
    print("\n--- Applying Inclusion Criteria ---")

    # Age 60+
    df = df[df["age"] >= 60].copy()
    flow_counts["after_age_filter"] = len(df)
    print(f"After age >= 60 filter: {flow_counts['after_age_filter']:,}")

    # Male only
    df = df[df["sex"] == 1].copy()
    flow_counts["after_sex_filter"] = len(df)
    print(f"After male filter: {flow_counts['after_sex_filter']:,}")

    # Process all variables
    print("\n--- Processing Variables ---")
    df = process_chronic_conditions(df)
    print("  Chronic conditions processed")

    df = process_outcomes(df)
    print("  Outcome variables processed")

    df = process_demographics(df)
    print("  Demographics processed")

    df = process_ses(df)
    print("  Socioeconomic variables processed")

    df = process_health_behaviors(df)
    print("  Health behaviors processed")

    df = process_anthropometrics(df)
    print("  Anthropometrics processed")

    df = process_survey_weights(df)
    print("  Survey weights processed")

    # Remove outliers
    print("\n--- Removing Outliers (|z| > 4) ---")
    df, outlier_count = remove_outliers(df)
    flow_counts["outliers_removed"] = outlier_count
    print(f"Outliers removed: {outlier_count}")

    # Filter to those with outcome data
    df_outcome = df[df["physical_health_days"].notna()].copy()
    flow_counts["with_outcome_data"] = len(df_outcome)
    print(f"\nWith physical health days data: {flow_counts['with_outcome_data']:,}")

    # Final analytic sample (complete cases for key variables)
    required_vars = [
        "chronic_count",
        "age",
        "race_ethnicity",
        "weight",
        "stratum",
        "psu",
    ]
    df_complete = df_outcome.dropna(subset=required_vars).copy()
    flow_counts["final_analytic_sample"] = len(df_complete)
    flow_counts["missing_covariates"] = (
        flow_counts["with_outcome_data"] - flow_counts["final_analytic_sample"]
    )
    print(
        f"Final analytic sample (complete cases): {flow_counts['final_analytic_sample']:,}"
    )

    # Select columns for analytic dataset
    keep_cols = [
        "SEQN",
        "cycle",
        "cycle_year",
        "physical_health_days",
        "mental_health_days",
        "activity_limitation_days",
        "general_health",
        "diabetes",
        "hypertension",
        "high_cholesterol",
        "cvd",
        "chronic_count",
        "chronic_cat",
        "age",
        "race_ethnicity",
        "education",
        "marital_status",
        "poverty_ratio",
        "has_insurance",
        "smoking_status",
        "activity_level",
        "vigorous_activity",
        "moderate_activity",
        "bmi",
        "bmi_category",
        "waist_circumference",
        "weight",
        "stratum",
        "psu",
    ]

    df_final = df_complete[keep_cols].copy()

    # Save flow counts (convert numpy types to Python types)
    flow_path = OUTPUT_DIR / "flow_counts.json"
    flow_counts_serializable = {
        k: int(v) if hasattr(v, "item") else v for k, v in flow_counts.items()
    }
    with open(flow_path, "w") as f:
        json.dump(flow_counts_serializable, f, indent=2)
    print(f"\nFlow counts saved to: {flow_path}")

    # Save analytic dataset (columns only metadata, no actual data to stdout)
    data_path = DATA_OUTPUT / "analytic_sample.csv"
    df_final.to_csv(data_path, index=False)
    print(f"Analytic dataset saved to: {data_path}")

    # Output summary statistics (aggregated only)
    print(f"\n{'=' * 70}")
    print("ANALYTIC DATASET SUMMARY (Aggregated Statistics Only)")
    print(f"{'=' * 70}")
    print(f"Final Sample Size: {len(df_final):,} older men")
    print(f"Cycles: {df_final['cycle'].nunique()}")
    print(f"Age range: {df_final['age'].min():.0f} - {df_final['age'].max():.0f}")
    print(
        f"Physical health days - Mean: {df_final['physical_health_days'].mean():.2f}, SD: {df_final['physical_health_days'].std():.2f}"
    )
    print(f"Chronic conditions distribution:")
    print(df_final["chronic_cat"].value_counts().sort_index())

    # Save column metadata (for documentation)
    metadata = {
        "n_observations": len(df_final),
        "n_cycles": df_final["cycle"].nunique(),
        "cycles": sorted(df_final["cycle"].unique().tolist()),
        "variables": {col: str(df_final[col].dtype) for col in df_final.columns},
        "missing_percentages": {
            col: round(df_final[col].isna().mean() * 100, 2) for col in df_final.columns
        },
    }

    meta_path = OUTPUT_DIR / "analytic_metadata.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nMetadata saved to: {meta_path}")

    print(f"\n{'=' * 70}")
    print("DATA PREPARATION COMPLETE")
    print(f"{'=' * 70}")

    return df_final


if __name__ == "__main__":
    main()
