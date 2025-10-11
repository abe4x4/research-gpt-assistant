"""
report_utils.py — handles batch run reporting (CSV logs)
--------------------------------------------------------
Creates and appends to a CSV report summarizing each processed PDF.
"""

import csv
from pathlib import Path
from datetime import datetime

REPORT_PATH = Path("results/batch_report.csv")

def append_report_row(pdf_path, query, summary_path, analysis_path, duration):
    """
    Append one processed file's results to a CSV report.
    Creates the file with a header if it doesn't exist.
    """
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = REPORT_PATH.exists()

    with REPORT_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp",
                "file",
                "query_used",
                "summary_path",
                "analysis_path",
                "duration_sec"
            ])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            pdf_path.name,
            query,
            str(summary_path),
            str(analysis_path),
            round(duration, 2)
        ])
