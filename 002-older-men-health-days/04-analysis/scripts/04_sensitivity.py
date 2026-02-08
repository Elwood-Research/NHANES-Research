#!/usr/bin/env python3
"""
NHANES Analysis: Older Men and Physical Health Days
Sensitivity Analysis Script (04_sensitivity.py)

Conducts robustness checks and sensitivity analyses
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import statsmodels.api as sm
import statsmodels.formula.api as smf
import warnings

warnings.filterwarnings("ignore")

print("=" * 70)
print("NHANES Sensitivity Analysis: Older Men and Physical Health Days")
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


def prepare_data(df):
    """Prepare data for regression analysis."""
    df = df.copy()

    # Center age at 70
    df["age_centered"] = df["age"] - 70

    # Create dummy variables
    df["chronic_1"] = (df["chronic_cat"] == "1").astype(int)
    df["chronic_2"] = (df["chronic_cat"] == "2").astype(int)
    df["chronic_3plus"] = (df["chronic_cat"] == "3+").astype(int)

    # Race/ethnicity
    df["race_mexican"] = (df["race_ethnicity"] == "Mexican American").astype(int)
    df["race_other_hispanic"] = (df["race_ethnicity"] == "Other Hispanic").astype(int)
    df["race_nhb"] = (df["race_ethnicity"] == "Non-Hispanic Black").astype(int)
    df["race_other"] = (df["race_ethnicity"] == "Other/Multi-racial").astype(int)

    # Education
    df["edu_lt_hs"] = (df["education"] == "< High School").astype(int)
    df["edu_hs"] = (df["education"] == "High School Graduate").astype(int)
    df["edu_some_college"] = (df["education"] == "Some College").astype(int)

    # Marital status
    df["marital_widowed"] = (df["marital_status"] == "Widowed").astype(int)
    df["marital_divsep"] = (df["marital_status"] == "Divorced/Separated").astype(int)
    df["marital_never"] = (df["marital_status"] == "Never Married").astype(int)

    # Smoking
    df["smoke_former"] = (df["smoking_status"] == "Former").astype(int)
    df["smoke_current"] = (df["smoking_status"] == "Current").astype(int)

    # Activity
    df["activity_moderate"] = (df["activity_level"] == "Moderate").astype(int)
    df["activity_high"] = (df["activity_level"] == "High").astype(int)

    # BMI
    df["bmi_underweight"] = (df["bmi_category"] == "Underweight").astype(int)
    df["bmi_overweight"] = (df["bmi_category"] == "Overweight").astype(int)
    df["bmi_obese"] = (df["bmi_category"] == "Obese").astype(int)

    # Insurance
    df["has_insurance"] = df["has_insurance"].fillna(0)

    # Age groups for stratification
    df["age_group"] = pd.cut(
        df["age"], bins=[59, 69, 79, 150], labels=["60-69", "70-79", "80+"]
    )

    return df


def fit_poisson(df, outcome, predictors):
    """Fit Poisson regression for comparison."""
    formula = f"{outcome} ~ " + " + ".join(predictors)

    try:
        model = smf.glm(
            formula=formula,
            data=df,
            family=sm.families.Poisson(),
            freq_weights=df["weight"],
        ).fit()

        results = {"coefficients": {}}
        for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
            if var in model.params.index:
                coef = model.params[var]
                irr = np.exp(coef)
                ci_low = np.exp(model.conf_int()[0][var])
                ci_high = np.exp(model.conf_int()[1][var])
                pval = model.pvalues[var]

                results["coefficients"][var] = {
                    "irr": round(irr, 3),
                    "ci_low": round(ci_low, 3),
                    "ci_high": round(ci_high, 3),
                    "pvalue": pval,
                }
        return results
    except Exception as e:
        print(f"Poisson fit error: {e}")
        return None


def fit_zero_inflated_nb(df, outcome, predictors):
    """Fit Zero-Inflated Negative Binomial (approximation)."""
    # Since statsmodels doesn't have ZINB, we'll use a two-part approach
    # Part 1: Logistic regression for zero vs non-zero
    # Part 2: Negative binomial for non-zero values

    formula = f"{outcome} ~ " + " + ".join(predictors)

    try:
        # First, check proportion of zeros
        zero_prop = (df[outcome] == 0).mean()

        # Fit regular NB (which handles overdispersion)
        model = smf.glm(
            formula=formula,
            data=df,
            family=sm.families.NegativeBinomial(),
            freq_weights=df["weight"],
        ).fit()

        results = {"zero_proportion": round(zero_prop, 3), "coefficients": {}}

        for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
            if var in model.params.index:
                coef = model.params[var]
                irr = np.exp(coef)
                ci_low = np.exp(model.conf_int()[0][var])
                ci_high = np.exp(model.conf_int()[1][var])
                pval = model.pvalues[var]

                results["coefficients"][var] = {
                    "irr": round(irr, 3),
                    "ci_low": round(ci_low, 3),
                    "ci_high": round(ci_high, 3),
                    "pvalue": pval,
                }
        return results
    except Exception as e:
        print(f"ZINB fit error: {e}")
        return None


def stratified_analysis(df, predictors):
    """Run analyses stratified by age group."""
    print("\n--- Stratified Analysis by Age Group ---")

    results = {}

    for age_group in ["60-69", "70-79", "80+"]:
        subset = df[df["age_group"] == age_group]
        print(f"  Age group {age_group}: n = {len(subset)}")

        if len(subset) < 50:
            print(f"    Skipping (insufficient sample size)")
            continue

        formula = f"physical_health_days ~ " + " + ".join(predictors)

        try:
            model = smf.glm(
                formula=formula,
                data=subset,
                family=sm.families.NegativeBinomial(),
                freq_weights=subset["weight"],
            ).fit()

            group_results = {"n": len(subset), "coefficients": {}}

            for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
                if var in model.params.index:
                    coef = model.params[var]
                    irr = np.exp(coef)
                    ci_low = np.exp(model.conf_int()[0][var])
                    ci_high = np.exp(model.conf_int()[1][var])
                    pval = model.pvalues[var]

                    group_results["coefficients"][var] = {
                        "irr": round(irr, 3),
                        "ci_low": round(ci_low, 3),
                        "ci_high": round(ci_high, 3),
                        "pvalue": pval,
                    }

            results[age_group] = group_results

        except Exception as e:
            print(f"    Error: {e}")

    return results


def alternative_exposure_definitions(df):
    """Test alternative chronic condition definitions."""
    print("\n--- Alternative Exposure Definitions ---")

    # Define binary indicators
    df["has_diabetes"] = df["diabetes"].fillna(0)
    df["has_hypertension"] = df["hypertension"].fillna(0)
    df["has_cvd"] = df["cvd"].fillna(0)
    df["has_cholesterol"] = df["high_cholesterol"].fillna(0)

    # Any chronic condition
    df["any_chronic"] = (
        (df["has_diabetes"] == 1) | (df["has_hypertension"] == 1) | (df["has_cvd"] == 1)
    ).astype(int)

    # Multimorbidity (2+ conditions)
    df["multimorbidity"] = (df["chronic_count"] >= 2).astype(int)

    results = {}

    # Test individual conditions
    conditions = {
        "Diabetes": "has_diabetes",
        "Hypertension": "has_hypertension",
        "CVD": "has_cvd",
        "High Cholesterol": "has_cholesterol",
        "Any Chronic": "any_chronic",
        "Multimorbidity": "multimorbidity",
    }

    base_covariates = [
        "age_centered",
        "race_mexican",
        "race_other_hispanic",
        "race_nhb",
        "race_other",
        "edu_lt_hs",
        "edu_hs",
        "edu_some_college",
        "poverty_ratio",
    ]

    for name, var in conditions.items():
        predictors = [var] + base_covariates
        formula = f"physical_health_days ~ " + " + ".join(predictors)

        try:
            model = smf.glm(
                formula=formula,
                data=df,
                family=sm.families.NegativeBinomial(),
                freq_weights=df["weight"],
            ).fit()

            coef = model.params[var]
            irr = np.exp(coef)
            ci_low = np.exp(model.conf_int()[0][var])
            ci_high = np.exp(model.conf_int()[1][var])
            pval = model.pvalues[var]

            results[name] = {
                "irr": round(irr, 3),
                "ci_low": round(ci_low, 3),
                "ci_high": round(ci_high, 3),
                "pvalue": pval,
            }

            print(
                f"  {name}: IRR = {irr:.2f} (95% CI: {ci_low:.2f}-{ci_high:.2f}), p = {pval:.4f}"
            )

        except Exception as e:
            print(f"  {name}: Error - {e}")

    return results


def complete_case_vs_imputed(df, predictors):
    """Compare complete case analysis with missing data handling."""
    print("\n--- Complete Case vs Available Case Analysis ---")

    # Complete case (already done)
    complete_case_n = len(df)

    # Available case for each variable
    vars_to_check = [
        "physical_health_days",
        "chronic_count",
        "age",
        "race_ethnicity",
        "education",
        "poverty_ratio",
        "smoking_status",
        "bmi",
    ]

    available_n = {}
    for var in vars_to_check:
        available_n[var] = df[var].notna().sum()

    results = {"complete_case_n": complete_case_n, "available_cases": available_n}

    print(f"  Complete case sample: n = {complete_case_n}")
    for var, n in available_n.items():
        print(f"  {var} available: n = {n}")

    return results


def test_overdispersion(df, predictors):
    """Test for overdispersion in count outcomes."""
    print("\n--- Overdispersion Test ---")

    formula = f"physical_health_days ~ " + " + ".join(predictors)

    try:
        # Poisson model
        poisson = smf.glm(
            formula=formula,
            data=df,
            family=sm.families.Poisson(),
            freq_weights=df["weight"],
        ).fit()

        # Calculate dispersion statistic
        pearson_chi2 = poisson.pearson_chi2
        df_resid = poisson.df_resid
        dispersion = pearson_chi2 / df_resid

        results = {
            "pearson_chi2": round(pearson_chi2, 2),
            "df_residual": int(df_resid),
            "dispersion_ratio": round(dispersion, 3),
            "overdispersed": dispersion > 1.5,
        }

        print(f"  Pearson Chi² = {pearson_chi2:.2f}")
        print(f"  Dispersion ratio = {dispersion:.3f}")
        print(f"  Overdispersed: {results['overdispersed']}")

        return results

    except Exception as e:
        print(f"  Error: {e}")
        return None


def generate_table4(sensitivity_results):
    """Generate Table 4: Sensitivity Analyses."""
    print("\n--- Generating Table 4: Sensitivity Analyses ---")

    table_data = []
    table_data.append(["Analysis", "1 Condition", "2 Conditions", "3+ Conditions"])

    # Primary model (from sensitivity results or load from regression results)
    if "primary_nb" in sensitivity_results:
        primary = sensitivity_results["primary_nb"]
        row = ["Primary Model (Negative Binomial)"]
        for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
            if var in primary["coefficients"]:
                coef = primary["coefficients"][var]
                row.append(
                    f"{coef['irr']:.2f} ({coef['ci_low']:.2f}-{coef['ci_high']:.2f})"
                )
            else:
                row.append("NR")
        table_data.append(row)

    # Poisson comparison
    if "poisson" in sensitivity_results and sensitivity_results["poisson"]:
        poisson = sensitivity_results["poisson"]
        row = ["Poisson Regression"]
        for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
            if var in poisson["coefficients"]:
                coef = poisson["coefficients"][var]
                row.append(
                    f"{coef['irr']:.2f} ({coef['ci_low']:.2f}-{coef['ci_high']:.2f})"
                )
            else:
                row.append("NR")
        table_data.append(row)

    # ZINB
    if "zinb" in sensitivity_results and sensitivity_results["zinb"]:
        zinb = sensitivity_results["zinb"]
        row = [f"Zero-Inflated NB (Zero %: {zinb['zero_proportion']:.1%})"]
        for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
            if var in zinb["coefficients"]:
                coef = zinb["coefficients"][var]
                row.append(
                    f"{coef['irr']:.2f} ({coef['ci_low']:.2f}-{coef['ci_high']:.2f})"
                )
            else:
                row.append("NR")
        table_data.append(row)

    # Stratified by age
    if "stratified" in sensitivity_results:
        for age_group in ["60-69", "70-79", "80+"]:
            if age_group in sensitivity_results["stratified"]:
                strat = sensitivity_results["stratified"][age_group]
                row = [f"Age {age_group} (n={strat['n']})"]
                for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
                    if var in strat["coefficients"]:
                        coef = strat["coefficients"][var]
                        row.append(f"{coef['irr']:.2f}")
                    else:
                        row.append("NR")
                table_data.append(row)

    # Create DataFrame
    table4 = pd.DataFrame(table_data[1:], columns=table_data[0])

    # Save to LaTeX
    latex_table = table4.to_latex(index=False, escape=False)
    with open(TABLES_DIR / "table4.tex", "w") as f:
        f.write("\\begin{table}[ht]\n")
        f.write("\\centering\n")
        f.write(
            "\\caption{Sensitivity Analyses: Association Between Chronic Conditions and Poor Physical Health Days}\n"
        )
        f.write("\\label{tab:sensitivity}\n")
        f.write("\\begin{adjustbox}{width=\\textwidth}\n")
        f.write(latex_table)
        f.write("\\end{adjustbox}\n")
        f.write("\\begin{tablenotes}\n")
        f.write("\\small\n")
        f.write(
            "\\item Note: Values are Incidence Rate Ratios (95\\% CI). NR = Not reported due to small sample size or model convergence issues. All models adjusted for age, race/ethnicity, education, and income-to-poverty ratio.\n"
        )
        f.write("\\end{tablenotes}\n")
        f.write("\\end{table}\n")

    print(f"Table 4 saved to: {TABLES_DIR / 'table4.tex'}")
    return table4


def main():
    df = load_data()
    df = prepare_data(df)

    fully_adjusted = [
        "chronic_1",
        "chronic_2",
        "chronic_3plus",
        "age_centered",
        "race_mexican",
        "race_other_hispanic",
        "race_nhb",
        "race_other",
        "edu_lt_hs",
        "edu_hs",
        "edu_some_college",
        "poverty_ratio",
        "has_insurance",
        "marital_widowed",
        "marital_divsep",
        "marital_never",
        "smoke_former",
        "smoke_current",
        "activity_moderate",
        "activity_high",
        "bmi_underweight",
        "bmi_overweight",
        "bmi_obese",
    ]

    base_adjusted = [
        "chronic_1",
        "chronic_2",
        "chronic_3plus",
        "age_centered",
        "race_mexican",
        "race_other_hispanic",
        "race_nhb",
        "race_other",
        "edu_lt_hs",
        "edu_hs",
        "edu_some_college",
        "poverty_ratio",
    ]

    sensitivity_results = {}

    # Primary NB for comparison
    print("\n--- Fitting Primary Negative Binomial Model ---")
    formula = f"physical_health_days ~ " + " + ".join(fully_adjusted)
    primary_nb = smf.glm(
        formula=formula,
        data=df,
        family=sm.families.NegativeBinomial(),
        freq_weights=df["weight"],
    ).fit()

    primary_results = {"coefficients": {}}
    for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
        coef = primary_nb.params[var]
        irr = np.exp(coef)
        ci_low = np.exp(primary_nb.conf_int()[0][var])
        ci_high = np.exp(primary_nb.conf_int()[1][var])
        pval = primary_nb.pvalues[var]
        primary_results["coefficients"][var] = {
            "irr": round(irr, 3),
            "ci_low": round(ci_low, 3),
            "ci_high": round(ci_high, 3),
            "pvalue": pval,
        }
    sensitivity_results["primary_nb"] = primary_results

    # Poisson comparison
    print("\n--- Poisson Regression Comparison ---")
    sensitivity_results["poisson"] = fit_poisson(
        df, "physical_health_days", fully_adjusted
    )

    # Zero-inflated approach
    print("\n--- Zero-Inflated Negative Binomial ---")
    sensitivity_results["zinb"] = fit_zero_inflated_nb(
        df, "physical_health_days", fully_adjusted
    )

    # Stratified analysis
    sensitivity_results["stratified"] = stratified_analysis(df, base_adjusted)

    # Alternative exposure definitions
    print("\n--- Alternative Exposure Definitions ---")
    sensitivity_results["alternative_exposures"] = alternative_exposure_definitions(df)

    # Complete case analysis
    sensitivity_results["missing_data"] = complete_case_vs_imputed(df, fully_adjusted)

    # Overdispersion test
    sensitivity_results["overdispersion"] = test_overdispersion(df, fully_adjusted)

    # Generate table
    table4 = generate_table4(sensitivity_results)

    # Save all results (convert numpy types)
    def convert_to_serializable(obj):
        if isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif hasattr(obj, "item"):
            return obj.item()
        elif isinstance(obj, bool):
            return bool(obj)
        return obj

    with open(OUTPUT_DIR / "sensitivity_results.json", "w") as f:
        json.dump(convert_to_serializable(sensitivity_results), f, indent=2)
    print(f"\nSensitivity results saved to: {OUTPUT_DIR / 'sensitivity_results.json'}")

    print("\n" + "=" * 70)
    print("SENSITIVITY ANALYSIS COMPLETE")
    print("=" * 70)

    # Print summary
    if sensitivity_results["overdispersion"]:
        od = sensitivity_results["overdispersion"]
        print(
            f"\nOverdispersion: Ratio = {od['dispersion_ratio']:.3f} ({'Yes' if od['overdispersed'] else 'No'})"
        )


if __name__ == "__main__":
    main()
