"""
report_utils.py
----------------
Utility functions for batch processing reports in ResearchGPT Assistant.

This module provides:
✅ Timing wrappers to measure execution time per PDF
✅ CSV writing helpers to record results in `results/batch_report.csv`
✅ Safe directory creation for report outputs

Author: Ibrahim Abouzeid (@abe4x4)
"""

import csv
import time
from pathlib import Path
from datetime import datetime


def ensure_dir_exists(path: Path) -> None:
    """
    Create the directory if it does not exist.
    """
    path.mkdir(parents=True, exist_ok=True)


def start_timer() -> float:
    """
    Returns the current timestamp for timing operations.
    """
    return time.time()


def stop_timer(start: float) -> float:
    """
    Calculates elapsed time since `start`.
    """
    return round(time.time() - start, 2)


def init_batch_report(csv_path: Path) -> None:
    """
    Create or overwrite the batch report CSV file with headers.
    """
    ensure_dir_exists(csv_path.parent)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp",
            "File Name",
            "Title",
            "Query Used",
            "Summary File",
            "Analysis File",
            "Summary Word Count",
            "Analysis Word Count",
            "Duration (s)"
        ])


def append_batch_record(csv_path: Path, record: dict) -> None:
    """
    Append a single record (dict) to the batch report CSV.
    """
    ensure_dir_exists(csv_path.parent)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            record.get("file_name", ""),
            record.get("title", ""),
            record.get("query_used", ""),
            record.get("summary_file", ""),
            record.get("analysis_file", ""),
            record.get("summary_words", ""),
            record.get("analysis_words", ""),
            record.get("duration", "")
        ])


def word_count_from_file(path: Path) -> int:
    """
    Counts number of words in a text or markdown file.
    Returns 0 if file not found.
    """
    try:
        text = path.read_text(encoding="utf-8")
        return len(text.split())
    except FileNotFoundError:
        return 0


def record_pdf_summary(
    csv_path: Path,
    pdf_path: Path,
    title: str,
    query: str,
    summary_path: Path,
    analysis_path: Path,
    duration: float
) -> None:
    """
    High-level helper to gather metadata and append to batch report.
    """
    record = {
        "file_name": pdf_path.name,
        "title": title,
        "query_used": query,
        "summary_file": str(summary_path),
        "analysis_file": str(analysis_path),
        "summary_words": word_count_from_file(summary_path),
        "analysis_words": word_count_from_file(analysis_path),
        "duration": duration
    }
    append_batch_record(csv_path, record)
