#!/usr/bin/env python3
"""
NHANES Analysis Master Script
Runs all analysis scripts in sequence
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "01_data_prep.py",
    "02_descriptive.py",
    "03_regression.py",
    "04_sensitivity.py",
    "05_outputs.py",
]


def main():
    script_dir = Path("/study/04-analysis/scripts")

    print("=" * 70)
    print("NHANES ANALYSIS PIPELINE")
    print("Older Men and Physical Health Days Study")
    print("=" * 70)

    for i, script in enumerate(SCRIPTS, 1):
        print(f"\n{'=' * 70}")
        print(f"STEP {i}/{len(SCRIPTS)}: Running {script}")
        print(f"{'=' * 70}")

        script_path = script_dir / script
        result = subprocess.run(
            [sys.executable, str(script_path)], capture_output=False, text=True
        )

        if result.returncode != 0:
            print(f"ERROR: {script} failed with return code {result.returncode}")
            sys.exit(1)

        print(f"\n{script} completed successfully")

    print(f"\n{'=' * 70}")
    print("ALL ANALYSES COMPLETED SUCCESSFULLY")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
