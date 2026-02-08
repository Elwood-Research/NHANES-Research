#!/usr/bin/env python3
"""
NHANES Analysis: Older Men and Physical Health Days
Regression Analysis Script (03_regression.py)

Fits primary and secondary regression models with survey weights
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
import warnings

warnings.filterwarnings("ignore")

print("=" * 70)
print("NHANES Regression Analysis: Older Men and Physical Health Days")
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

    # Create dummy variables for categorical variables
    # Chronic conditions (reference: 0)
    df["chronic_1"] = (df["chronic_cat"] == "1").astype(int)
    df["chronic_2"] = (df["chronic_cat"] == "2").astype(int)
    df["chronic_3plus"] = (df["chronic_cat"] == "3+").astype(int)

    # Race/ethnicity (reference: Non-Hispanic White)
    df["race_mexican"] = (df["race_ethnicity"] == "Mexican American").astype(int)
    df["race_other_hispanic"] = (df["race_ethnicity"] == "Other Hispanic").astype(int)
    df["race_nhb"] = (df["race_ethnicity"] == "Non-Hispanic Black").astype(int)
    df["race_other"] = (df["race_ethnicity"] == "Other/Multi-racial").astype(int)

    # Education (reference: College Graduate+)
    df["edu_lt_hs"] = (df["education"] == "< High School").astype(int)
    df["edu_hs"] = (df["education"] == "High School Graduate").astype(int)
    df["edu_some_college"] = (df["education"] == "Some College").astype(int)

    # Marital status (reference: Married/Partner)
    df["marital_widowed"] = (df["marital_status"] == "Widowed").astype(int)
    df["marital_divsep"] = (df["marital_status"] == "Divorced/Separated").astype(int)
    df["marital_never"] = (df["marital_status"] == "Never Married").astype(int)

    # Smoking (reference: Never)
    df["smoke_former"] = (df["smoking_status"] == "Former").astype(int)
    df["smoke_current"] = (df["smoking_status"] == "Current").astype(int)

    # Activity level (reference: Low)
    df["activity_moderate"] = (df["activity_level"] == "Moderate").astype(int)
    df["activity_high"] = (df["activity_level"] == "High").astype(int)

    # BMI category (reference: Normal)
    df["bmi_underweight"] = (df["bmi_category"] == "Underweight").astype(int)
    df["bmi_overweight"] = (df["bmi_category"] == "Overweight").astype(int)
    df["bmi_obese"] = (df["bmi_category"] == "Obese").astype(int)

    # Insurance
    df["has_insurance"] = df["has_insurance"].fillna(0)

    # Ensure weights are positive
    df = df[df["weight"] > 0].copy()

    return df


def fit_linear_model(df, outcome, predictors, model_name):
    """Fit weighted linear regression model."""

    # Prepare formula
    formula = f"{outcome} ~ " + " + ".join(predictors)

    # Fit model with weights
    try:
        model = smf.wls(formula=formula, data=df, weights=df["weight"]).fit()

        results = {
            "model_name": model_name,
            "outcome": outcome,
            "n_obs": int(model.nobs),
            "r_squared": round(model.rsquared, 3),
            "adj_r_squared": round(model.rsquared_adj, 3),
            "f_statistic": round(model.fvalue, 2),
            "f_pvalue": model.f_pvalue,
            "coefficients": {},
        }

        for var in model.params.index:
            coef = model.params[var]
            se = model.bse[var]
            ci_low = model.conf_int()[0][var]
            ci_high = model.conf_int()[1][var]
            pval = model.pvalues[var]

            results["coefficients"][var] = {
                "coef": round(coef, 3),
                "se": round(se, 3),
                "ci_low": round(ci_low, 3),
                "ci_high": round(ci_high, 3),
                "pvalue": pval,
            }

        return results, model
    except Exception as e:
        print(f"Error fitting {model_name}: {e}")
        return None, None


def fit_negative_binomial(df, outcome, predictors, model_name):
    """Fit negative binomial regression (for count outcomes)."""

    formula = f"{outcome} ~ " + " + ".join(predictors)

    try:
        model = smf.glm(
            formula=formula,
            data=df,
            family=sm.families.NegativeBinomial(),
            freq_weights=df["weight"],
        ).fit()

        results = {
            "model_name": model_name,
            "outcome": outcome,
            "n_obs": int(model.nobs),
            "deviance": round(model.deviance, 2),
            "pearson_chi2": round(model.pearson_chi2, 2),
            "coefficients": {},
        }

        for var in model.params.index:
            coef = model.params[var]
            se = model.bse[var]
            ci_low = model.conf_int()[0][var]
            ci_high = model.conf_int()[1][var]
            pval = model.pvalues[var]
            irr = np.exp(coef)
            irr_low = np.exp(ci_low)
            irr_high = np.exp(ci_high)

            results["coefficients"][var] = {
                "coef": round(coef, 3),
                "se": round(se, 3),
                "irr": round(irr, 3),
                "irr_ci_low": round(irr_low, 3),
                "irr_ci_high": round(irr_high, 3),
                "pvalue": pval,
            }

        return results, model
    except Exception as e:
        print(f"Error fitting {model_name}: {e}")
        return None, None


def run_primary_analysis(df):
    """Run primary regression analysis."""
    print("\n--- Primary Analysis: Physical Health Days ---")

    # Predictor sets
    chronic_only = ["chronic_1", "chronic_2", "chronic_3plus"]

    demo_adjusted = [
        "chronic_1",
        "chronic_2",
        "chronic_3plus",
        "age_centered",
        "race_mexican",
        "race_other_hispanic",
        "race_nhb",
        "race_other",
    ]

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

    results = {}

    # Model 1: Chronic conditions only (linear)
    print("  Fitting Model 1: Chronic conditions only (Linear)...")
    res1, mod1 = fit_linear_model(
        df, "physical_health_days", chronic_only, "Model 1: Crude"
    )
    if res1:
        results["model1_linear"] = res1
        print(f"    R² = {res1['r_squared']:.3f}, n = {res1['n_obs']}")

    # Model 2: Demographic-adjusted (linear)
    print("  Fitting Model 2: Demographic-adjusted (Linear)...")
    res2, mod2 = fit_linear_model(
        df, "physical_health_days", demo_adjusted, "Model 2: Demographic-adjusted"
    )
    if res2:
        results["model2_linear"] = res2
        print(f"    R² = {res2['r_squared']:.3f}, n = {res2['n_obs']}")

    # Model 3: Fully adjusted (linear)
    print("  Fitting Model 3: Fully adjusted (Linear)...")
    res3, mod3 = fit_linear_model(
        df, "physical_health_days", fully_adjusted, "Model 3: Fully adjusted"
    )
    if res3:
        results["model3_linear"] = res3
        print(f"    R² = {res3['r_squared']:.3f}, n = {res3['n_obs']}")

    # Model 4: Negative Binomial (primary)
    print("  Fitting Model 4: Fully adjusted (Negative Binomial)...")
    res4, mod4 = fit_negative_binomial(
        df, "physical_health_days", fully_adjusted, "Model 4: Negative Binomial"
    )
    if res4:
        results["model4_nb"] = res4
        print(f"    Deviance = {res4['deviance']:.2f}, n = {res4['n_obs']}")

    return results


def run_secondary_analyses(df):
    """Run secondary analyses for other outcomes."""
    print("\n--- Secondary Analyses ---")

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

    results = {}

    # Mental health days
    print("  Mental Health Days (Negative Binomial)...")
    res_mental, _ = fit_negative_binomial(
        df, "mental_health_days", fully_adjusted, "Mental Health Days"
    )
    if res_mental:
        results["mental_health"] = res_mental

    # Activity limitation days
    print("  Activity Limitation Days (Negative Binomial)...")
    res_activity, _ = fit_negative_binomial(
        df, "activity_limitation_days", fully_adjusted, "Activity Limitation Days"
    )
    if res_activity:
        results["activity_limitation"] = res_activity

    return results


def run_interaction_tests(df):
    """Test for interactions."""
    print("\n--- Interaction Tests ---")

    results = {}

    # Age × Chronic conditions
    print("  Testing Age × Chronic Conditions interaction...")
    df["age_chronic1"] = df["age_centered"] * df["chronic_1"]
    df["age_chronic2"] = df["age_centered"] * df["chronic_2"]
    df["age_chronic3"] = df["age_centered"] * df["chronic_3plus"]

    base_predictors = [
        "chronic_1",
        "chronic_2",
        "chronic_3plus",
        "age_centered",
        "race_mexican",
        "race_other_hispanic",
        "race_nhb",
        "race_other",
    ]
    interaction_predictors = base_predictors + [
        "age_chronic1",
        "age_chronic2",
        "age_chronic3",
    ]

    res_base, mod_base = fit_linear_model(
        df, "physical_health_days", base_predictors, "Base"
    )
    res_int, mod_int = fit_linear_model(
        df, "physical_health_days", interaction_predictors, "With Interactions"
    )

    if res_base and res_int:
        # F-test for interaction terms
        from statsmodels.stats.anova import anova_lm

        try:
            anova_res = anova_lm(mod_base, mod_int)
            f_pvalue = anova_res["Pr(>F)"].iloc[1]
            results["age_chronic_interaction"] = {
                "f_pvalue": f_pvalue,
                "significant": f_pvalue < 0.05,
            }
            print(f"    Interaction p-value: {f_pvalue:.4f}")
        except:
            print("    Could not compute interaction test")

    # Physical Activity × Chronic conditions
    print("  Testing Physical Activity × Chronic Conditions interaction...")
    df["activity_chronic1"] = (
        df["activity_moderate"] * df["chronic_1"]
        + df["activity_high"] * df["chronic_1"]
    )
    df["activity_chronic2"] = (
        df["activity_moderate"] * df["chronic_2"]
        + df["activity_high"] * df["chronic_2"]
    )
    df["activity_chronic3"] = (
        df["activity_moderate"] * df["chronic_3plus"]
        + df["activity_high"] * df["chronic_3plus"]
    )

    # Simple test: compare high activity vs low activity across chronic groups
    for chronic_cat in ["0", "1", "2", "3+"]:
        subset = df[df["chronic_cat"] == chronic_cat]
        low_activity = subset[subset["activity_level"] == "Low"][
            "physical_health_days"
        ].mean()
        high_activity = subset[subset["activity_level"] == "High"][
            "physical_health_days"
        ].mean()
        diff = (
            low_activity - high_activity
            if not pd.isna(low_activity) and not pd.isna(high_activity)
            else np.nan
        )
        print(
            f"    Chronic {chronic_cat}: Low activity mean = {low_activity:.1f}, High activity mean = {high_activity:.1f}, Diff = {diff:.1f}"
        )

    return results


def generate_table3(primary_results):
    """Generate Table 3: Multivariable Regression Results."""
    print("\n--- Generating Table 3: Regression Results ---")

    if "model4_nb" not in primary_results:
        print("ERROR: Negative binomial results not available")
        return None

    nb_results = primary_results["model4_nb"]

    # Extract chronic condition coefficients
    table_data = []
    table_data.append(["Variable", "IRR", "95% CI", "p-value"])

    chronic_vars = {
        "chronic_1": "1 Chronic Condition",
        "chronic_2": "2 Chronic Conditions",
        "chronic_3plus": "3+ Chronic Conditions",
    }

    for var, label in chronic_vars.items():
        if var in nb_results["coefficients"]:
            coef = nb_results["coefficients"][var]
            irr = coef["irr"]
            ci = f"{coef['irr_ci_low']:.2f}-{coef['irr_ci_high']:.2f}"
            pval = coef["pvalue"]
            p_str = "<0.001" if pval < 0.001 else f"{pval:.3f}"
            table_data.append([label, f"{irr:.2f}", ci, p_str])

    # Other key covariates
    covariate_vars = {
        "age_centered": "Age (per 10 years)",
        "race_mexican": "Mexican American",
        "race_nhb": "Non-Hispanic Black",
        "edu_lt_hs": "Less than High School",
        "poverty_ratio": "Income-to-Poverty Ratio",
        "smoke_current": "Current Smoker",
        "activity_high": "High Physical Activity",
        "bmi_obese": "Obese (BMI ≥30)",
    }

    table_data.append(["", "", "", ""])  # Separator

    for var, label in covariate_vars.items():
        if var in nb_results["coefficients"]:
            coef = nb_results["coefficients"][var]
            irr = coef["irr"]
            ci = f"{coef['irr_ci_low']:.2f}-{coef['irr_ci_high']:.2f}"
            pval = coef["pvalue"]
            p_str = "<0.001" if pval < 0.001 else f"{pval:.3f}"
            table_data.append([label, f"{irr:.2f}", ci, p_str])

    # Create DataFrame
    table3 = pd.DataFrame(table_data[1:], columns=table_data[0])

    # Save to LaTeX
    latex_table = table3.to_latex(index=False, escape=False)
    with open(TABLES_DIR / "table3.tex", "w") as f:
        f.write("\\begin{table}[ht]\n")
        f.write("\\centering\n")
        f.write(
            "\\caption{Association Between Chronic Conditions and Poor Physical Health Days Among Older Men (Negative Binomial Regression)}\n"
        )
        f.write("\\label{tab:regression}\n")
        f.write("\\begin{adjustbox}{width=\\textwidth}\n")
        f.write(latex_table)
        f.write("\\end{adjustbox}\n")
        f.write("\\begin{tablenotes}\n")
        f.write("\\small\n")
        f.write(
            "\\item Note: IRR = Incidence Rate Ratio. Reference category for chronic conditions: 0 conditions. Model adjusted for age, race/ethnicity, education, income-to-poverty ratio, health insurance, marital status, smoking status, physical activity level, and BMI category.\n"
        )
        f.write("\\end{tablenotes}\n")
        f.write("\\end{table}\n")

    print(f"Table 3 saved to: {TABLES_DIR / 'table3.tex'}")
    return table3


def convert_to_serializable(obj):
    """Convert numpy/pandas types to Python native types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif hasattr(obj, "item"):  # numpy types
        return obj.item()
    elif isinstance(obj, bool):
        return bool(obj)
    return obj


def save_all_results(primary_results, secondary_results, interaction_results):
    """Save all regression results to JSON."""
    all_results = {
        "primary_analysis": primary_results,
        "secondary_analysis": secondary_results,
        "interaction_tests": interaction_results,
    }

    # Convert to serializable types
    all_results = convert_to_serializable(all_results)

    with open(OUTPUT_DIR / "regression_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print(
        f"\nAll regression results saved to: {OUTPUT_DIR / 'regression_results.json'}"
    )


def main():
    df = load_data()
    df = prepare_data(df)

    # Run analyses
    primary_results = run_primary_analysis(df)
    secondary_results = run_secondary_analyses(df)
    interaction_results = run_interaction_tests(df)

    # Generate tables
    table3 = generate_table3(primary_results)

    # Save results
    save_all_results(primary_results, secondary_results, interaction_results)

    # Print key findings
    print("\n" + "=" * 70)
    print("REGRESSION ANALYSIS COMPLETE")
    print("=" * 70)

    if "model4_nb" in primary_results:
        nb_res = primary_results["model4_nb"]
        print("\nKey Findings (Negative Binomial Model):")

        for var in ["chronic_1", "chronic_2", "chronic_3plus"]:
            if var in nb_res["coefficients"]:
                coef = nb_res["coefficients"][var]
                label = (
                    var.replace("chronic_", "").replace("3plus", "3+") + " condition(s)"
                )
                print(
                    f"  {label}: IRR = {coef['irr']:.2f} (95% CI: {coef['irr_ci_low']:.2f}-{coef['irr_ci_high']:.2f}), p = {coef['pvalue']:.4f}"
                )


if __name__ == "__main__":
    main()
