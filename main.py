"""
main.py
--------
ResearchGPT Assistant — Capstone Project
Enhanced with batch reporting and execution timing.

Features:
✅ Summarize & analyze single or multiple PDFs
✅ CLI flags for query, data-dir, pdf, timeout, top-k
✅ Automatic metadata saving
✅ Automatic CSV batch report with timing & word counts

Author: Ibrahim Abouzeid (@abe4x4)
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Tuple

from src.config import MISTRAL_API_KEY
from src.pdf_utils import load_all_pdfs_text
from src.text_utils import clean_text, chunk_text
from src.indexer import build_index, search
from src.summarizer import summarize_chunks
from src.analyst import analyze_chunks
from src.io_utils import safe_stem
from src.metadata_utils import extract_metadata
from src.report_utils import (
    start_timer,
    stop_timer,
    init_batch_report,
    record_pdf_summary,
)

# Define directory constants
DATA_DIR = Path("data/sample_papers")
SUM_DIR = Path("results/summaries")
ANA_DIR = Path("results/analyses")
META_DIR = Path("results/metadata")
BATCH_REPORT = Path("results/batch_report.csv")

# Ensure directories exist
for d in [SUM_DIR, ANA_DIR, META_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def ensure_api_key():
    """Check for required Mistral API key."""
    if not MISTRAL_API_KEY:
        raise RuntimeError(
            "❌ MISTRAL_API_KEY missing — please add it to your .env file and reload your shell."
        )


def summarize_and_analyze_pdf(pdf_path: Path, raw_text: str, query: str) -> tuple[Path, Path, str]:
    """
    Process a single PDF end-to-end: metadata extraction, cleaning, chunking,
    retrieval, summarization, and analysis.
    """
    # --- Metadata Extraction ---
    meta = extract_metadata(pdf_path)
    title = meta.get("title") or pdf_path.stem
    authors = meta.get("authors") or "Unknown"
    abstract = meta.get("abstract")

    # --- Clean & Chunk ---
    txt = clean_text(raw_text)
    chunks = chunk_text(txt, max_chars=1500, overlap=150)
    if not chunks:
        raise RuntimeError(f"No extractable text from: {pdf_path.name}")

    # --- Indexing & Retrieval ---
    labeled_chunks: List[Tuple[str, str]] = [
        (f"{pdf_path.stem} [chunk {i+1}]", ch) for i, ch in enumerate(chunks)
    ]
    index = build_index(labeled_chunks)
    hits = search(index, query, k=int(os.getenv("RGPT_TOP_K", 5)))
    top_chunks = [text for _s, (_lbl, text) in hits]

    # --- Summarization ---
    header = f"# {title}\n\n**Authors:** {authors}\n\n"
    if abstract:
        header += f"**Abstract (detected):** {abstract}\n\n---\n\n"

    summary_md = header + summarize_chunks(MISTRAL_API_KEY, title, top_chunks)
    sum_path = SUM_DIR / f"{safe_stem(pdf_path)}_summary.md"
    sum_path.write_text(summary_md, encoding="utf-8")

    # --- Analysis ---
    analysis_md = analyze_chunks(MISTRAL_API_KEY, title, top_chunks)
    ana_path = ANA_DIR / f"{safe_stem(pdf_path)}_analysis.md"
    ana_path.write_text(analysis_md, encoding="utf-8")

    # --- Metadata JSON ---
    meta_json = {
        "file": pdf_path.name,
        "pdf_path": str(pdf_path),
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "query_used": query,
        "outputs": {
            "summary_md": str(sum_path),
            "analysis_md": str(ana_path),
        },
    }
    meta_path = META_DIR / f"{safe_stem(pdf_path)}_meta.json"
    meta_path.write_text(json.dumps(meta_json, indent=2, ensure_ascii=False), encoding="utf-8")

    return sum_path, ana_path, title


def process_pdf_batch(data_dir: Path, query: str, timeout: int = 45):
    """
    Process all PDFs in the given data directory.
    Saves batch CSV report for all processed papers.
    """
    print(f"📂 Scanning directory: {data_dir.resolve()}")
    pairs = load_all_pdfs_text(data_dir)
    if not pairs:
        print("❌ No PDFs found. Please check your path or add PDFs.")
        return

    init_batch_report(BATCH_REPORT)
    print("🧾 Batch report initialized →", BATCH_REPORT)

    for pdf_path, raw_text in pairs:
        print(f"\n📄 Processing: {pdf_path.name}")
        try:
            start = start_timer()
            s_path, a_path, title = summarize_and_analyze_pdf(pdf_path, raw_text, query)
            duration = stop_timer(start)
            record_pdf_summary(BATCH_REPORT, pdf_path, title, query, s_path, a_path, duration)
            print(f"✅ Done: {pdf_path.name} in {duration}s")
        except Exception as e:
            print(f"[WARN] Skipped {pdf_path.name}: {e}")

    print("\n📊 All results summarized in:", BATCH_REPORT)


def main():
    parser = argparse.ArgumentParser(description="ResearchGPT Assistant CLI")
    parser.add_argument("--pdf", type=str, help="Process a single PDF file path")
    parser.add_argument("--data-dir", type=str, default="data/sample_papers", help="Folder of PDFs")
    parser.add_argument("--k", type=int, default=5, help="Number of top chunks for summarization")
    parser.add_argument("--query", type=str, default="What problem does this paper solve?")
    parser.add_argument("--timeout", type=int, default=45, help="Timeout for API calls (seconds)")
    args = parser.parse_args()

    ensure_api_key()

    os.environ["RGPT_TOP_K"] = str(args.k)
    query = args.query

    if args.pdf:
        pdf_path = Path(args.pdf)
        print(f"📄 Processing single PDF: {pdf_path.name}")
        if not pdf_path.exists():
            raise FileNotFoundError(f"File not found: {pdf_path}")
        raw_pairs = load_all_pdfs_text(pdf_path.parent)
        match = [p for p in raw_pairs if p[0].name == pdf_path.name]
        if not match:
            raise FileNotFoundError(f"No text extracted for {pdf_path.name}")
        raw_text = match[0][1]
        s, a, title = summarize_and_analyze_pdf(pdf_path, raw_text, query)
        print("✅ Summary →", s)
        print("✅ Analysis →", a)
    else:
        process_pdf_batch(Path(args.data_dir), query, args.timeout)


if __name__ == "__main__":
    main()
