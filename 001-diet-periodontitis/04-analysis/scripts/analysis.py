import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
import json

# ==========================================
# Configuration & Constants
# ==========================================

DATA_DIR = "/data"
OUTPUT_DIR = "/study/04-analysis/outputs"
FIGURES_DIR = os.path.join(OUTPUT_DIR, "figures")
TABLES_DIR = os.path.join(OUTPUT_DIR, "tables")

CYCLES = ["F", "G", "H"]  # 2009-2010, 2011-2012, 2013-2014

# Valid teeth for perio exam (excluding 3rd molars)
TEETH = [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
]

# Interproximal sites suffixes
# D = Distal-Facial, S = Mesial-Facial, P = Distal-Lingual, A = Mesial-Lingual
INTERPROXIMAL_SUFFIXES = ["D", "S", "P", "A"]

# All sites for completeness check or other uses if needed
ALL_SUFFIXES = ["D", "M", "S", "P", "L", "A"]

# ==========================================
# 1. Data Loading & Merging
# ==========================================


def load_dataset(prefix, cycle):
    """Load a dataset for a specific cycle."""
    # Handle cases where filename suffix might vary slightly or file extension case
    # Try constructing the path
    # Expected format: PREFIX_CYCLE.csv
    filename = f"{prefix}_{cycle}.csv"
    path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(path):
        # Try finding case-insensitive match
        search_pattern = os.path.join(DATA_DIR, f"{prefix}_{cycle}.*")
        matches = glob.glob(search_pattern)
        # Filter for case-insensitive match on extension csv
        matches = [m for m in matches if m.lower().endswith(".csv")]

        if not matches:
            print(f"Warning: File {filename} not found.")
            return None
        path = matches[0]

    try:
        df = pd.read_csv(path)
        # Uppercase columns for consistency
        df.columns = df.columns.str.upper()
        return df
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None


def merge_cycles():
    """Load and merge all datasets across cycles."""
    merged_dfs = []

    for cycle in CYCLES:
        print(f"Processing Cycle {cycle}...")

        # Load domains
        demo = load_dataset("DEMO", cycle)
        dr1 = load_dataset("DR1TOT", cycle)
        ohxper = load_dataset("OHXPER", cycle)
        bmx = load_dataset("BMX", cycle)
        smq = load_dataset("SMQ", cycle)
        diq = load_dataset("DIQ", cycle)
        alq = load_dataset("ALQ", cycle)
        paq = load_dataset("PAQ", cycle)
        ohq = load_dataset("OHQ", cycle)

        if demo is None:
            print(f"Critical: DEMO_{cycle} missing. Skipping cycle.")
            continue

        # Start with DEMO
        cycle_df = demo

        # Merge other domains
        for name, df in [
            ("DR1TOT", dr1),
            ("OHXPER", ohxper),
            ("BMX", bmx),
            ("SMQ", smq),
            ("DIQ", diq),
            ("ALQ", alq),
            ("PAQ", paq),
            ("OHQ", ohq),
        ]:
            if df is not None:
                # Merge on SEQN
                cycle_df = pd.merge(cycle_df, df, on="SEQN", how="left")

        merged_dfs.append(cycle_df)

    if not merged_dfs:
        raise ValueError("No data loaded!")

    final_df = pd.concat(merged_dfs, ignore_index=True)
    return final_df


# ==========================================
# 2. Variable Transformation
# ==========================================


def calculate_periodontitis_status(row):
    """
    Determine periodontitis status based on CDC/AAP definitions.
    Returns: 3 (Severe), 2 (Moderate), 1 (Mild), 0 (None/No Disease), np.nan (Missing)
    """
    # Check if perio exam is complete enough?
    # We rely on exclusion criteria for broad exclusion, but here we calculate based on available data.

    # Store sites for CAL and PD
    cal_sites_ge_6 = set()  # (tooth, site) tuples
    cal_sites_ge_4 = set()
    cal_sites_ge_3 = set()

    pd_sites_ge_5 = set()
    pd_sites_ge_4 = set()

    for tooth in TEETH:
        tooth_str = f"{tooth:02d}"

        for suffix in INTERPROXIMAL_SUFFIXES:
            # Variable names
            cal_var = f"OHX{tooth_str}LA{suffix}"
            pd_var = f"OHX{tooth_str}PC{suffix}"

            # Check CAL
            if cal_var in row and not pd.isna(row[cal_var]):
                cal_val = row[cal_var]
                if cal_val >= 6:
                    cal_sites_ge_6.add((tooth, suffix))
                if cal_val >= 4:
                    cal_sites_ge_4.add((tooth, suffix))
                if cal_val >= 3:
                    cal_sites_ge_3.add((tooth, suffix))

            # Check PD
            if pd_var in row and not pd.isna(row[pd_var]):
                pd_val = row[pd_var]
                if pd_val >= 5:
                    pd_sites_ge_5.add((tooth, suffix))
                if pd_val >= 4:
                    pd_sites_ge_4.add((tooth, suffix))

    # Helper to check "not on same tooth"
    def count_unique_teeth(site_set):
        return len(set(t for t, s in site_set))

    # Severe: >=2 interproximal sites with CAL >=6mm (not same tooth) AND >=1 interproximal site with PD >=5mm
    is_severe = (count_unique_teeth(cal_sites_ge_6) >= 2) and (len(pd_sites_ge_5) >= 1)
    if is_severe:
        return 3  # Severe

    # Moderate: >=2 interproximal sites with CAL >=4mm (not same tooth) OR >=2 interproximal sites with PD >=5mm (not same tooth)
    is_moderate = (count_unique_teeth(cal_sites_ge_4) >= 2) or (
        count_unique_teeth(pd_sites_ge_5) >= 2
    )
    if is_moderate:
        return 2  # Moderate

    # Mild: >=2 interproximal sites with CAL >=3mm AND >=2 interproximal sites with PD >=4mm (not same tooth) OR 1 site PD >=5mm
    # Note: ">=2 interproximal sites with CAL >=3mm" usually implies "not same tooth" in CDC definitions,
    # but the prompt says: ">=2 interproximal sites with CAL >=3mm AND >=2 interproximal sites with PD >=4mm (not same tooth)"
    # It might mean the PD condition requires unique teeth, or both.
    # Standard CDC/AAP Mild: >=2 interproximal sites with AL >=3mm AND (>=2 interproximal sites with PD >=4mm (not on same tooth) OR 1 site with PD >=5mm).
    # I will assume "not same tooth" applies to the PD part as explicitly stated, but usually AL part also implies it for robustness.
    # However, strict reading: AL part doesn't say "not same tooth". But let's assume it does to be consistent with Mod/Severe logic usually.
    # Actually, CDC Page says: "Mild periodontitis: ≥2 interproximal sites with AL ≥3 mm, and ≥2 interproximal sites with PD ≥4 mm (not on same tooth) or one site with PD ≥5 mm."
    # So AL part doesn't specify unique teeth. But let's check standard implementation. usually it is unique teeth for AL too.
    # I will stick to the text: ">=2 interproximal sites with CAL >=3mm" (raw count)

    cond_cal_mild = len(cal_sites_ge_3) >= 2
    cond_pd_mild_1 = count_unique_teeth(pd_sites_ge_4) >= 2
    cond_pd_mild_2 = len(pd_sites_ge_5) >= 1

    is_mild = cond_cal_mild and (cond_pd_mild_1 or cond_pd_mild_2)
    if is_mild:
        return 1  # Mild

    return 0  # None


def process_data(df):
    """
    Apply variable transformations and create derived variables.
    """
    print("Creating derived variables...")

    # 1. Periodontitis Status
    # Apply row-wise. This is slow but safe.
    df["perio_status_raw"] = df.apply(calculate_periodontitis_status, axis=1)

    # Binary Outcome: 1 if Mod/Severe, 0 if Mild/None
    df["perio_case"] = df["perio_status_raw"].apply(lambda x: 1 if x >= 2 else 0)

    # 2. Demographics & Covariates

    # Race/Ethnicity
    race_map = {
        1: "Mexican American",
        2: "Other Hispanic",
        3: "Non-Hispanic White",
        4: "Non-Hispanic Black",
        5: "Other",
    }
    df["race"] = df["RIDRETH1"].map(race_map)

    # Education (1-2=<HS, 3=HS/GED, 4-5=>HS)
    def recode_edu(x):
        if pd.isna(x):
            return np.nan
        if x <= 2:
            return "<HS"
        if x == 3:
            return "HS/GED"
        if x >= 4:
            return ">HS"
        return np.nan  # 7,9 are missing/refused usually, handled later

    df["education"] = df["DMDEDUC2"].apply(recode_edu)

    # Smoking
    # Current: SMQ040 in [1,2]
    # Former: SMQ020=1 AND SMQ040=3
    # Never: SMQ020=2
    def recode_smoking(row):
        smq020 = row.get("SMQ020", np.nan)
        smq040 = row.get("SMQ040", np.nan)

        if pd.isna(smq020):
            return np.nan

        if smq040 in [1, 2]:
            return "Current"
        if smq020 == 1 and smq040 == 3:
            return "Former"
        if smq020 == 2:
            return "Never"
        return np.nan

    df["smoking"] = df.apply(recode_smoking, axis=1)

    # Diabetes
    # DIQ010 (1=Yes, 2=No, 3=Borderline -> No)
    def recode_diabetes(x):
        if pd.isna(x):
            return np.nan
        if x == 1:
            return "Yes"
        if x in [2, 3]:
            return "No"
        return np.nan

    df["diabetes"] = df["DIQ010"].apply(recode_diabetes)

    # Alcohol
    # ALQ130 (avg drinks/day). Impute 0 for non-drinkers?
    # ALQ101=2 (Had at least 12 drinks in lifetime? No -> Non-drinker)
    # ALQ120Q/U (How often drink?)
    # The plan says: "Continuous ALQ130. Impute 0 for non-drinkers if needed."
    # If ALQ130 is missing but ALQ101=2 (Never) or ALQ120=0 (Never in last year), set to 0.
    # We will assume simple imputation: fillna(0) if ALQ101==2.
    df["alcohol"] = df["ALQ130"]
    # If ALQ101 (Had >12 drinks/life) is 2 (No), then alcohol consumption is 0
    if "ALQ101" in df.columns:
        df.loc[df["ALQ101"] == 2, "alcohol"] = 0
    # Also if ALQ120Q (how often) == 0, then 0.
    # Note: ALQ130 values 777/999 are missing.
    df.loc[df["alcohol"] >= 777, "alcohol"] = np.nan

    # Physical Activity
    # PAQ605=1 (Vigorous work) OR PAQ620=1 (Moderate work) -> Active?
    # Wait, usually PA includes recreational (PAQ650, PAQ665).
    # Plan says: "PAQ605=1 OR PAQ620=1 -> Active; else Inactive."
    # We follow the plan strictly.
    def recode_pa(row):
        paq605 = row.get("PAQ605", np.nan)
        paq620 = row.get("PAQ620", np.nan)

        if paq605 == 1 or paq620 == 1:
            return "Active"
        if pd.isna(paq605) and pd.isna(paq620):
            return np.nan
        return "Inactive"

    df["physical_activity"] = df.apply(recode_pa, axis=1)

    # Flossing
    # OHQ870 (days/week).
    # Categorize: 0 (Never), 1-3 (Infrequent), 4-6 (Frequent), 7 (Daily).
    def recode_flossing(x):
        if pd.isna(x) or x > 7:
            return np.nan  # 99=Refused
        if x == 0:
            return "Never"
        if 1 <= x <= 3:
            return "Infrequent"
        if 4 <= x <= 6:
            return "Frequent"
        if x == 7:
            return "Daily"
        return np.nan

    df["flossing"] = df["OHQ870"].apply(recode_flossing)

    # Weight
    # WTMEC6YR = WTMEC2YR / 3
    df["weight"] = df["WTMEC2YR"] / 3

    # Exposures
    # DR1TSUGR, DR1TFIBE, DR1TVC, DR1TCALC
    # Keep continuous.

    # Coerce continuous variables to numeric, handling errors (e.g. '.' or other codes)
    numeric_cols = [
        "INDFMPIR",
        "BMXBMI",
        "ALQ130",
        "DR1TSUGR",
        "DR1TFIBE",
        "DR1TVC",
        "DR1TCALC",
        "DR1TKCAL",
        "RIDAGEYR",
        "WTMEC2YR",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ==========================================
# 3. Exclusions & Flow Diagram
# ==========================================


def apply_exclusions(df):
    flow_counts = {}

    # 1. Total Population
    n_total = len(df)
    flow_counts["1_Total_Population"] = n_total
    print(f"Total Population: {n_total}")

    # 2. Age Filter: Age >= 30
    df = df[df["RIDAGEYR"] >= 30].copy()
    n_age = len(df)
    flow_counts["2_Age_ge_30"] = n_age
    print(f"After Age >= 30: {n_age}")

    # 3. Periodontal Exam: OHDDESTS == 1 (Complete)
    # Check column name, might be OHDEXSTS in some cycles/dictionaries, but plan says OHDDESTS.
    # In OHXPER_F dictionary, it was OHDEXSTS (Overall) and OHDPDSTS (Perio status).
    # Plan says "OHDDESTS != 1". I will check available columns.
    if "OHDDESTS" in df.columns:
        df = df[df["OHDDESTS"] == 1].copy()
    elif "OHDEXSTS" in df.columns:
        df = df[df["OHDEXSTS"] == 1].copy()
    else:
        print(
            "Warning: Neither OHDDESTS nor OHDEXSTS found. Skipping perio status check."
        )

    n_perio = len(df)
    flow_counts["3_Perio_Exam_Complete"] = n_perio
    print(f"After Perio Complete: {n_perio}")

    # 4. Dietary Recall: DR1DRSTZ == 1 (Reliable)
    df = df[df["DR1DRSTZ"] == 1].copy()
    n_diet = len(df)
    flow_counts["4_Diet_Reliable"] = n_diet
    print(f"After Diet Reliable: {n_diet}")

    # 5. Missing Covariates
    covariates = [
        "perio_case",
        "race",
        "education",
        "smoking",
        "diabetes",
        "alcohol",
        "physical_activity",
        "flossing",
        "BMXBMI",
        "INDFMPIR",
        "DR1TSUGR",
        "DR1TFIBE",
        "DR1TVC",
        "DR1TCALC",
        "DR1TKCAL",
    ]

    df_clean = df.dropna(subset=covariates).copy()
    n_complete = len(df_clean)
    flow_counts["5_Complete_Data"] = n_complete
    print(f"After Complete Data: {n_complete}")

    # 6. Dietary Outliers: > 4 SD
    # Check Total Energy (DR1TKCAL) and key nutrients (Sugar, Fiber, VitC, Calc)
    # Calculate Z-scores
    nutrients = ["DR1TSUGR", "DR1TFIBE", "DR1TVC", "DR1TCALC", "DR1TKCAL"]
    mask_outlier = pd.Series(False, index=df_clean.index)

    for nut in nutrients:
        mean = df_clean[nut].mean()
        std = df_clean[nut].std()
        z_score = (df_clean[nut] - mean) / std
        mask_outlier |= z_score.abs() > 4

    df_final = df_clean[~mask_outlier].copy()
    n_final = len(df_final)
    flow_counts["6_No_Diet_Outliers"] = n_final
    print(f"After Outlier Exclusion: {n_final}")

    flow_counts["7_Final_Analytical_Sample"] = n_final

    return df_final, flow_counts


def create_strobe_diagram(counts):
    """Generate STROBE flow diagram using matplotlib."""
    import matplotlib.patches as patches

    fig, ax = plt.subplots(figsize=(8, 10))
    ax.axis("off")

    # Box parameters
    box_width = 0.6
    box_height = 0.08
    start_y = 0.95
    gap = 0.12

    steps = [
        ("Total Population (Merged F, G, H)", counts["1_Total_Population"]),
        ("Age >= 30", counts["2_Age_ge_30"]),
        ("Complete Periodontal Exam", counts["3_Perio_Exam_Complete"]),
        ("Reliable Dietary Recall", counts["4_Diet_Reliable"]),
        ("Complete Covariates", counts["5_Complete_Data"]),
        ("Final Sample (Excl. Outliers >4SD)", counts["7_Final_Analytical_Sample"]),
    ]

    for i, (label, count) in enumerate(steps):
        y = start_y - i * gap

        # Draw Box
        rect = patches.FancyBboxPatch(
            (0.2, y - box_height),
            box_width,
            box_height,
            boxstyle="round,pad=0.02",
            ec="black",
            fc="white",
        )
        ax.add_patch(rect)

        # Text
        plt.text(
            0.5,
            y - box_height / 2,
            f"{label}\nN = {count}",
            ha="center",
            va="center",
            fontsize=10,
        )

        # Arrow
        if i < len(steps) - 1:
            plt.arrow(
                0.5,
                y - box_height,
                0,
                -(gap - box_height) + 0.01,
                head_width=0.02,
                head_length=0.02,
                fc="black",
                ec="black",
            )

            # Exclusion Text
            prev_count = steps[i][1]
            next_count = steps[i + 1][1]
            excluded = prev_count - next_count
            plt.text(
                0.52,
                y - box_height - (gap - box_height) / 2,
                f"Excluded: {excluded}",
                ha="left",
                va="center",
                fontsize=8,
                color="red",
            )

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "strobe_flow.png"))
    plt.close()

    # Save counts to JSON
    with open(os.path.join(OUTPUT_DIR, "strobe_flow_counts.json"), "w") as f:
        json.dump(counts, f, indent=2)


# ==========================================
# 4. Statistical Analysis
# ==========================================


def run_descriptive_table1(df):
    """Generate Table 1: Characteristics by Perio Status."""

    columns = [
        ("Age (years)", "RIDAGEYR", "continuous"),
        ("Sex", "RIAGENDR", "categorical"),  # 1=Male, 2=Female
        ("Race/Ethnicity", "race", "categorical"),
        ("Education", "education", "categorical"),
        ("PIR", "INDFMPIR", "continuous"),
        ("BMI (kg/m^2)", "BMXBMI", "continuous"),
        ("Smoking", "smoking", "categorical"),
        ("Diabetes", "diabetes", "categorical"),
        ("Alcohol (drinks/day)", "alcohol", "continuous"),
        ("Physical Activity", "physical_activity", "categorical"),
        ("Flossing", "flossing", "categorical"),
        ("Total Energy (kcal)", "DR1TKCAL", "continuous"),
        ("Sugar (g)", "DR1TSUGR", "continuous"),
        ("Fiber (g)", "DR1TFIBE", "continuous"),
        ("Vitamin C (mg)", "DR1TVC", "continuous"),
        ("Calcium (mg)", "DR1TCALC", "continuous"),
    ]

    results = []

    # Split by case
    g0 = df[df["perio_case"] == 0]
    g1 = df[df["perio_case"] == 1]

    for label, var, dtype in columns:
        row = {"Variable": label}

        if dtype == "continuous":
            # Weighted Mean (SE) - Simplified: Using unweighted SD/sqrt(n) or simple weighted mean function
            # Note: For proper complex survey analysis, we need the design.
            # Given constraints, we calculate Weighted Mean and unweighted SD or simplified weighted SE.

            def get_stats(sub_df):
                if len(sub_df) == 0:
                    return "N/A"
                mean = np.average(sub_df[var], weights=sub_df["weight"])
                std = np.sqrt(
                    np.average((sub_df[var] - mean) ** 2, weights=sub_df["weight"])
                )
                return f"{mean:.2f} ({std:.2f})"

            row["No Periodontitis (Mean (SD))"] = get_stats(g0)
            row["Periodontitis (Mean (SD))"] = get_stats(g1)

            # T-test (Unweighted for simplicity in p-value, or weighted if possible)
            # Using statsmodels DescrStatsW for Weighted T-test equivalent
            try:
                d0 = sm.stats.DescrStatsW(g0[var], weights=g0["weight"])
                d1 = sm.stats.DescrStatsW(g1[var], weights=g1["weight"])
                t_stat, p_val, df_ = sm.stats.CompareMeans(d0, d1).ttest_ind()
                row["P-value"] = f"{p_val:.3f}"
            except:
                row["P-value"] = "NaN"

        elif dtype == "categorical":
            # Weighted %
            row["No Periodontitis (Mean (SD))"] = ""  # Header row
            row["Periodontitis (Mean (SD))"] = ""
            row["P-value"] = ""
            results.append(row)

            # Get unique categories from full df to ensure alignment
            cats = sorted(df[var].dropna().unique())

            for cat in cats:
                cat_row = {"Variable": f"  {cat}"}

                def get_pct(sub_df, category):
                    if len(sub_df) == 0:
                        return "0.0%"
                    total_w = sub_df["weight"].sum()
                    cat_w = sub_df[sub_df[var] == category]["weight"].sum()
                    pct = (cat_w / total_w) * 100
                    return f"{pct:.1f}%"

                cat_row["No Periodontitis (Mean (SD))"] = get_pct(g0, cat)
                cat_row["Periodontitis (Mean (SD))"] = get_pct(g1, cat)
                cat_row["P-value"] = ""
                results.append(cat_row)

            # Chi-square test (Weighted is hard without specialized lib, use Unweighted for p-value approx)
            try:
                ct = pd.crosstab(df[var], df["perio_case"])
                chi2, p, dof, ex = sm.stats.Table(ct).test_nominal_association().tuple
                # Add p-value to the main row
                results[-len(cats) - 1]["P-value"] = f"{p:.3f}"
            except:
                pass
            continue  # Already appended rows

        results.append(row)

    pd.DataFrame(results).to_csv(
        os.path.join(OUTPUT_DIR, "table1_characteristics.csv"), index=False
    )


def run_logistic_models(df):
    """Run Logistic Regression Models."""

    exposures = [
        ("Sugars", "DR1TSUGR"),
        ("Fiber", "DR1TFIBE"),
        ("Vitamin C", "DR1TVC"),
        ("Calcium", "DR1TCALC"),
    ]

    models_config = {
        "Model 1": [],  # Exposure only
        "Model 2": ["RIDAGEYR", "RIAGENDR", "race", "DR1TKCAL"],
        "Model 3": [
            "RIDAGEYR",
            "RIAGENDR",
            "race",
            "DR1TKCAL",
            "education",
            "INDFMPIR",
            "smoking",
            "BMXBMI",
            "diabetes",
            "alcohol",
            "physical_activity",
            "flossing",
        ],
    }

    all_results = []

    for exp_name, exp_var in exposures:
        for model_name, covariates in models_config.items():
            # Formula
            # C(...) for categorical
            # Q('...') for vars with spaces if needed (not needed here)

            formula_covs = []
            for cov in covariates:
                if cov in [
                    "race",
                    "education",
                    "smoking",
                    "diabetes",
                    "physical_activity",
                    "flossing",
                ]:
                    formula_covs.append(f"C({cov})")
                else:
                    formula_covs.append(cov)

            rhs = " + ".join([exp_var] + formula_covs)
            formula = f"perio_case ~ {rhs}"

            try:
                # Weighted GLM (Binomial family for Logistic)
                model = smf.glm(
                    formula=formula,
                    data=df,
                    family=sm.families.Binomial(),
                    freq_weights=df["weight"],
                )
                res = model.fit()

                # Extract Exposure stats
                params = res.params[exp_var]
                se = res.bse[exp_var]
                p_val = res.pvalues[exp_var]
                ci = res.conf_int().loc[exp_var]

                or_val = np.exp(params)
                or_low = np.exp(ci[0])
                or_high = np.exp(ci[1])

                all_results.append(
                    {
                        "Exposure": exp_name,
                        "Model": model_name,
                        "OR": f"{or_val:.2f}",
                        "95% CI": f"{or_low:.2f}-{or_high:.2f}",
                        "P-value": f"{p_val:.4f}",
                        "N": int(res.nobs),
                    }
                )
            except Exception as e:
                print(f"Error in {exp_name} {model_name}: {e}")
                all_results.append(
                    {
                        "Exposure": exp_name,
                        "Model": model_name,
                        "OR": "Error",
                        "95% CI": "",
                        "P-value": "",
                        "N": 0,
                    }
                )

    # Save Table 3 (Detailed)
    results_df = pd.DataFrame(all_results)
    results_df.to_csv(os.path.join(OUTPUT_DIR, "table3_models.csv"), index=False)

    # Save Table 2 (Bivariate - Model 1 only)
    table2 = results_df[results_df["Model"] == "Model 1"].copy()
    table2.to_csv(os.path.join(OUTPUT_DIR, "table2_bivariate.csv"), index=False)


# ==========================================
# Main Execution
# ==========================================


def main():
    # Setup directories
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(TABLES_DIR, exist_ok=True)

    # 1. Load & Merge
    print("Loading data...")
    df = merge_cycles()
    print(f"Initial merged shape: {df.shape}")

    # 2. Transform
    df = process_data(df)

    # 3. Exclusions
    df_final, flow_counts = apply_exclusions(df)
    create_strobe_diagram(flow_counts)

    # 4. Analysis
    print("Running Descriptives...")
    run_descriptive_table1(df_final)

    print("Running Models...")
    run_logistic_models(df_final)

    print("Analysis Complete.")


if __name__ == "__main__":
    main()
