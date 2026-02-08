#!/usr/bin/env python3
"""
NHANES Analysis: Older Men and Physical Health Days
Descriptive Statistics Script (02_descriptive.py)

Generates weighted descriptive statistics for the analytic sample
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Output only aggregated results
print("=" * 70)
print("NHANES Descriptive Statistics: Older Men and Physical Health Days")
print("=" * 70)

# Paths
DATA_DIR = Path("/study/04-analysis/data")
OUTPUT_DIR = Path("/study/04-analysis/outputs")
TABLES_DIR = OUTPUT_DIR / "tables"


def load_data():
    """Load the analytic dataset."""
    df = pd.read_csv(DATA_DIR / "analytic_sample.csv")
    print(f"Loaded {len(df):,} observations")
    return df


def weighted_mean_std(x, w):
    """Calculate weighted mean and standard deviation."""
    mask = pd.notna(x) & pd.notna(w) & (w > 0)
    x_clean = x[mask]
    w_clean = w[mask]

    if len(x_clean) == 0:
        return np.nan, np.nan

    w_sum = w_clean.sum()
    w_mean = (x_clean * w_clean).sum() / w_sum
    w_var = ((w_clean * (x_clean - w_mean) ** 2).sum() / w_sum) * (
        w_clean.sum() / (w_clean.sum() - w_clean.pow(2).sum() / w_clean.sum())
    )
    w_std = np.sqrt(w_var)

    return w_mean, w_std


def weighted_median(x, w):
    """Calculate weighted median."""
    mask = pd.notna(x) & pd.notna(w) & (w > 0)
    x_clean = x[mask]
    w_clean = w[mask]

    if len(x_clean) == 0:
        return np.nan

    sorted_idx = np.argsort(x_clean)
    x_sorted = x_clean.iloc[sorted_idx]
    w_sorted = w_clean.iloc[sorted_idx]

    cumsum = np.cumsum(w_sorted)
    cutoff = w_sorted.sum() / 2

    return x_sorted[cumsum >= cutoff].iloc[0]


def weighted_percentile(x, w, p):
    """Calculate weighted percentile."""
    mask = pd.notna(x) & pd.notna(w) & (w > 0)
    x_clean = x[mask]
    w_clean = w[mask]

    if len(x_clean) == 0:
        return np.nan

    sorted_idx = np.argsort(x_clean)
    x_sorted = x_clean.iloc[sorted_idx]
    w_sorted = w_clean.iloc[sorted_idx]

    cumsum = np.cumsum(w_sorted)
    cutoff = p * w_sorted.sum() / 100

    return x_sorted[cumsum >= cutoff].iloc[0]


def categorical_summary(df, var, weight_col="weight"):
    """Generate weighted categorical summary."""
    results = []
    for cat in df[var].dropna().unique():
        mask = df[var] == cat
        n = mask.sum()
        weighted_n = df.loc[mask, weight_col].sum()
        weighted_pct = 100 * weighted_n / df[weight_col].sum()
        results.append({"Category": cat, "N": n, "Weighted_Pct": weighted_pct})
    return pd.DataFrame(results)


def continuous_summary(df, var, weight_col="weight"):
    """Generate weighted continuous summary."""
    x = df[var]
    w = df[weight_col]

    mean, std = weighted_mean_std(x, w)
    median = weighted_median(x, w)
    p25 = weighted_percentile(x, w, 25)
    p75 = weighted_percentile(x, w, 75)

    return {
        "Variable": var,
        "N": x.notna().sum(),
        "Mean": round(mean, 2) if not np.isnan(mean) else "NA",
        "SD": round(std, 2) if not np.isnan(std) else "NA",
        "Median": round(median, 1) if not np.isnan(median) else "NA",
        "Q1": round(p25, 1) if not np.isnan(p25) else "NA",
        "Q3": round(p75, 1) if not np.isnan(p75) else "NA",
    }


def generate_table1(df):
    """Generate Table 1: Baseline Characteristics (Overall)."""
    print("\n--- Generating Table 1: Baseline Characteristics ---")

    table_data = []

    # Sample size
    total_n = len(df)
    table_data.append(["Sample Size", f"{total_n:,}", "", ""])

    # Age
    age_stats = continuous_summary(df, "age")
    table_data.append(["Age (years)", "", "", ""])
    table_data.append(
        ["  Mean (SD)", f"{age_stats['Mean']} ({age_stats['SD']})", "", ""]
    )
    table_data.append(
        [
            "  Median (Q1-Q3)",
            f"{age_stats['Median']} ({age_stats['Q1']}-{age_stats['Q3']})",
            "",
            "",
        ]
    )

    # Race/Ethnicity
    race_summary = categorical_summary(df, "race_ethnicity")
    table_data.append(["Race/Ethnicity", "", "", ""])
    for _, row in race_summary.iterrows():
        table_data.append(
            [f"  {row['Category']}", f"{row['N']:,}", f"{row['Weighted_Pct']:.1f}", ""]
        )

    # Education
    edu_summary = categorical_summary(df, "education")
    table_data.append(["Education Level", "", "", ""])
    for _, row in edu_summary.iterrows():
        table_data.append(
            [f"  {row['Category']}", f"{row['N']:,}", f"{row['Weighted_Pct']:.1f}", ""]
        )

    # Marital Status
    marital_summary = categorical_summary(df, "marital_status")
    table_data.append(["Marital Status", "", "", ""])
    for _, row in marital_summary.iterrows():
        table_data.append(
            [f"  {row['Category']}", f"{row['N']:,}", f"{row['Weighted_Pct']:.1f}", ""]
        )

    # Income-to-Poverty Ratio
    pov_stats = continuous_summary(df, "poverty_ratio")
    table_data.append(["Income-to-Poverty Ratio", "", "", ""])
    table_data.append(
        ["  Mean (SD)", f"{pov_stats['Mean']} ({pov_stats['SD']})", "", ""]
    )
    table_data.append(
        [
            "  Median (Q1-Q3)",
            f"{pov_stats['Median']} ({pov_stats['Q1']}-{pov_stats['Q3']})",
            "",
            "",
        ]
    )

    # Health Insurance
    ins_summary = categorical_summary(df, "has_insurance")
    table_data.append(["Health Insurance", "", "", ""])
    for _, row in ins_summary.iterrows():
        label = "Has Insurance" if row["Category"] == 1 else "No Insurance"
        table_data.append(
            [f"  {label}", f"{row['N']:,}", f"{row['Weighted_Pct']:.1f}", ""]
        )

    # Smoking Status
    smoking_summary = categorical_summary(df, "smoking_status")
    table_data.append(["Smoking Status", "", "", ""])
    for _, row in smoking_summary.iterrows():
        table_data.append(
            [f"  {row['Category']}", f"{row['N']:,}", f"{row['Weighted_Pct']:.1f}", ""]
        )

    # Physical Activity
    activity_summary = categorical_summary(df, "activity_level")
    table_data.append(["Physical Activity Level", "", "", ""])
    for _, row in activity_summary.iterrows():
        table_data.append(
            [f"  {row['Category']}", f"{row['N']:,}", f"{row['Weighted_Pct']:.1f}", ""]
        )

    # BMI
    bmi_stats = continuous_summary(df, "bmi")
    table_data.append(["Body Mass Index (kg/m²)", "", "", ""])
    table_data.append(
        ["  Mean (SD)", f"{bmi_stats['Mean']} ({bmi_stats['SD']})", "", ""]
    )
    table_data.append(
        [
            "  Median (Q1-Q3)",
            f"{bmi_stats['Median']} ({bmi_stats['Q1']}-{bmi_stats['Q3']})",
            "",
            "",
        ]
    )

    # BMI Categories
    bmi_cat_summary = categorical_summary(df, "bmi_category")
    table_data.append(["BMI Category", "", "", ""])
    for _, row in bmi_cat_summary.iterrows():
        table_data.append(
            [f"  {row['Category']}", f"{row['N']:,}", f"{row['Weighted_Pct']:.1f}", ""]
        )

    # Outcomes
    table_data.append(["Outcomes", "", "", ""])

    phys_stats = continuous_summary(df, "physical_health_days")
    table_data.append(
        [
            "  Poor Physical Health Days (0-30)",
            f"{phys_stats['Mean']} ({phys_stats['SD']})",
            "",
            "",
        ]
    )

    mental_stats = continuous_summary(df, "mental_health_days")
    table_data.append(
        [
            "  Poor Mental Health Days (0-30)",
            f"{mental_stats['Mean']} ({mental_stats['SD']})",
            "",
            "",
        ]
    )

    activity_stats = continuous_summary(df, "activity_limitation_days")
    table_data.append(
        [
            "  Activity Limitation Days (0-30)",
            f"{activity_stats['Mean']} ({activity_stats['SD']})",
            "",
            "",
        ]
    )

    # Chronic Conditions
    table_data.append(["Chronic Conditions", "", "", ""])
    chronic_summary = categorical_summary(df, "chronic_cat")
    for _, row in chronic_summary.iterrows():
        table_data.append(
            [
                f"  {row['Category']} conditions",
                f"{row['N']:,}",
                f"{row['Weighted_Pct']:.1f}",
                "",
            ]
        )

    # Create DataFrame
    table1 = pd.DataFrame(
        table_data, columns=["Characteristic", "Value", "Weighted %", ""]
    )

    # Save to LaTeX
    latex_table = table1.to_latex(index=False, escape=False)
    with open(TABLES_DIR / "table1.tex", "w") as f:
        f.write("\\begin{table}[ht]\n")
        f.write("\\centering\n")
        f.write(
            "\\caption{Baseline Characteristics of Older Men (Age 60+), NHANES 2001-2018}\n"
        )
        f.write("\\label{tab:baseline}\n")
        f.write("\\begin{adjustbox}{width=\\textwidth}\n")
        f.write(latex_table)
        f.write("\\end{adjustbox}\n")
        f.write("\\begin{tablenotes}\n")
        f.write("\\small\n")
        f.write(
            "\\item Note: Values are n (weighted percentage) for categorical variables and mean (SD) or median (Q1-Q3) for continuous variables. All estimates use NHANES survey weights.\n"
        )
        f.write("\\end{tablenotes}\n")
        f.write("\\end{table}\n")

    print(f"Table 1 saved to: {TABLES_DIR / 'table1.tex'}")
    return table1


def generate_table1_by_chronic(df):
    """Generate Table 1 stratified by chronic condition count."""
    print("\n--- Generating Table 1 (Stratified by Chronic Conditions) ---")

    chronic_cats = ["0", "1", "2", "3+"]
    table_data = []

    # Header
    table_data.append(
        [
            "Characteristic",
            "0 Conditions",
            "1 Condition",
            "2 Conditions",
            "3+ Conditions",
            "p-value",
        ]
    )

    # Sample sizes
    ns = [len(df[df["chronic_cat"] == cat]) for cat in chronic_cats]
    table_data.append(["n", f"{ns[0]:,}", f"{ns[1]:,}", f"{ns[2]:,}", f"{ns[3]:,}", ""])

    # Age
    age_means = []
    for cat in chronic_cats:
        subset = df[df["chronic_cat"] == cat]
        mean, std = weighted_mean_std(subset["age"], subset["weight"])
        age_means.append(f"{mean:.1f} ({std:.1f})")
    table_data.append(["Age, mean (SD)"] + age_means + [""])

    # Race/Ethnicity - Non-Hispanic White %
    race_pcts = []
    for cat in chronic_cats:
        subset = df[df["chronic_cat"] == cat]
        nhw = (subset["race_ethnicity"] == "Non-Hispanic White").sum()
        race_pcts.append(f"{100 * nhw / len(subset):.1f}")
    table_data.append(["Non-Hispanic White, %"] + race_pcts + [""])

    # Education - College Graduate %
    edu_pcts = []
    for cat in chronic_cats:
        subset = df[df["chronic_cat"] == cat]
        college = (subset["education"] == "College Graduate+").sum()
        edu_pcts.append(f"{100 * college / len(subset):.1f}")
    table_data.append(["College Graduate+, %"] + edu_pcts + [""])

    # Income-to-Poverty Ratio
    pov_means = []
    for cat in chronic_cats:
        subset = df[df["chronic_cat"] == cat]
        mean, std = weighted_mean_std(subset["poverty_ratio"], subset["weight"])
        pov_means.append(f"{mean:.2f} ({std:.2f})")
    table_data.append(["Income-to-Poverty Ratio, mean (SD)"] + pov_means + [""])

    # BMI
    bmi_means = []
    for cat in chronic_cats:
        subset = df[df["chronic_cat"] == cat]
        mean, std = weighted_mean_std(subset["bmi"], subset["weight"])
        bmi_means.append(f"{mean:.1f} ({std:.1f})")
    table_data.append(["BMI, mean (SD)"] + bmi_means + [""])

    # Smoking - Current %
    smoke_pcts = []
    for cat in chronic_cats:
        subset = df[df["chronic_cat"] == cat]
        current = (subset["smoking_status"] == "Current").sum()
        smoke_pcts.append(f"{100 * current / len(subset):.1f}")
    table_data.append(["Current Smoker, %"] + smoke_pcts + [""])

    # Physical Activity - High %
    activity_pcts = []
    for cat in chronic_cats:
        subset = df[df["chronic_cat"] == cat]
        high = (subset["activity_level"] == "High").sum()
        activity_pcts.append(f"{100 * high / len(subset):.1f}")
    table_data.append(["High Physical Activity, %"] + activity_pcts + [""])

    # Physical Health Days
    phys_means = []
    for cat in chronic_cats:
        subset = df[df["chronic_cat"] == cat]
        mean, std = weighted_mean_std(subset["physical_health_days"], subset["weight"])
        phys_means.append(f"{mean:.1f} ({std:.1f})")
    table_data.append(["Physical Health Days, mean (SD)"] + phys_means + [""])

    # Create DataFrame
    table1_strat = pd.DataFrame(table_data[1:], columns=table_data[0])

    # Save to LaTeX
    latex_table = table1_strat.to_latex(index=False, escape=False)
    with open(TABLES_DIR / "table1_stratified.tex", "w") as f:
        f.write("\\begin{table}[ht]\n")
        f.write("\\centering\n")
        f.write(
            "\\caption{Baseline Characteristics by Number of Chronic Conditions, NHANES 2001-2018}\n"
        )
        f.write("\\label{tab:baseline-stratified}\n")
        f.write("\\begin{adjustbox}{width=\\textwidth}\n")
        f.write(latex_table)
        f.write("\\end{adjustbox}\n")
        f.write("\\begin{tablenotes}\n")
        f.write("\\small\n")
        f.write(
            "\\item Note: Values are mean (SD) or percentage. All estimates use NHANES survey weights.\n"
        )
        f.write("\\end{tablenotes}\n")
        f.write("\\end{table}\n")

    print(f"Table 1 (stratified) saved to: {TABLES_DIR / 'table1_stratified.tex'}")
    return table1_strat


def generate_outcome_summary(df):
    """Generate summary statistics for outcome variables."""
    print("\n--- Generating Outcome Summary ---")

    outcomes = [
        "physical_health_days",
        "mental_health_days",
        "activity_limitation_days",
    ]
    summary = {}

    for outcome in outcomes:
        stats = continuous_summary(df, outcome)
        # Calculate proportions with >=14 days
        severe = (df[outcome] >= 14).sum()
        severe_pct = 100 * severe / df[outcome].notna().sum()

        summary[outcome] = {
            "mean": stats["Mean"],
            "sd": stats["SD"],
            "median": stats["Median"],
            "q1": stats["Q1"],
            "q3": stats["Q3"],
            "severe_n": int(severe),
            "severe_pct": round(severe_pct, 1),
        }

    # Save to JSON
    with open(OUTPUT_DIR / "outcome_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("Outcome summary saved")
    return summary


def main():
    df = load_data()

    # Generate tables
    table1 = generate_table1(df)
    table1_strat = generate_table1_by_chronic(df)
    outcome_summary = generate_outcome_summary(df)

    print("\n" + "=" * 70)
    print("DESCRIPTIVE STATISTICS COMPLETE")
    print("=" * 70)
    print(f"\nKey Findings:")
    print(f"- Total sample: {len(df):,} older men")
    print(
        f"- Mean physical health days: {outcome_summary['physical_health_days']['mean']:.2f} (SD: {outcome_summary['physical_health_days']['sd']:.2f})"
    )
    print(
        f"- {outcome_summary['physical_health_days']['severe_pct']:.1f}% reported ≥14 poor physical health days"
    )
    print(
        f"- Mean mental health days: {outcome_summary['mental_health_days']['mean']:.2f} (SD: {outcome_summary['mental_health_days']['sd']:.2f})"
    )
    print(
        f"- Mean activity limitation days: {outcome_summary['activity_limitation_days']['mean']:.2f} (SD: {outcome_summary['activity_limitation_days']['sd']:.2f})"
    )


if __name__ == "__main__":
    main()
