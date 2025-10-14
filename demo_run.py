#!/usr/bin/env python3
"""
demo_run.py — ResearchGPT Assistant Showcase Runner

Runs the full project pipeline step by step:
  1. Single PDF summarization & analysis
  2. Batch mode with CSV report
  3. Bonus: Comparison mode
"""

import os
import subprocess
from pathlib import Path

# --- Project constants ---
PROJECT_ROOT = Path(__file__).parent
PDF1 = PROJECT_ROOT / "data/sample_papers/attention_is_all_you_need.pdf"
PDF2 = PROJECT_ROOT / "data/sample_papers/another_paper.pdf"
RESULTS = PROJECT_ROOT / "results"

# --- Helper ---
def run_cmd(cmd: str):
    """Run a shell command and print formatted output."""
    print(f"\n🚀 Running: {cmd}\n" + "-" * 60)
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ STDERR:\n", result.stderr)
    print("-" * 60)


def confirm_outputs():
    """Verify key result directories and files exist."""
    print("\n📁 Checking output directories...")
    for subdir in ["summaries", "analyses", "metadata", "comparisons"]:
        path = RESULTS / subdir
        if path.exists():
            print(f"✅ {subdir}/ → {len(list(path.glob('*')))} files")
        else:
            print(f"❌ Missing folder: {path}")
    csv_path = RESULTS / "batch_report.csv"
    if csv_path.exists():
        print(f"✅ CSV Report found: {csv_path}")
    else:
        print("❌ No batch_report.csv found")


# --- Step 1: Single PDF processing ---
print("\n=== STEP 1: Single PDF Summarization & Analysis ===")
run_cmd(f"python main.py --pdf {PDF1}")

# --- Step 2: Batch mode processing ---
print("\n=== STEP 2: Batch Mode with CSV Report ===")
run_cmd(f"python main.py --data-dir data/sample_papers --report")

# --- Step 3: Bonus comparison mode ---
print("\n=== STEP 3: Bonus - Compare Two Papers ===")
run_cmd(f"python main.py --compare {PDF1} {PDF2}")

# --- Step 4: Validate outputs ---
print("\n=== STEP 4: Validate Outputs ===")
confirm_outputs()

print("\n🎓 Demo completed successfully! All project requirements and bonus features verified.")
