#!/usr/bin/env python3
"""
ResearchGPT Assistant — Capstone Project
Main entry point for:
  - Single or batch PDF processing
  - Summarization and analysis
  - Metadata + CSV report saving
  - Bonus: PDF comparison feature
"""

import os
import json
import time
import argparse
from pathlib import Path
from typing import List, Tuple

from mistralai import Mistral  # ✅ new API client (replaces MistralClient)

# --- Project imports ---
from src.config import MISTRAL_API_KEY
from src.pdf_utils import load_all_pdfs_text
from src.text_utils import clean_text, chunk_text
from src.indexer import build_index, search
from src.summarizer import summarize_chunks
from src.analyst import analyze_chunks
from src.io_utils import safe_stem
from src.metadata_utils import extract_metadata
from src.report_utils import append_report_row

# --- Constants & directories ---
DATA_DIR = Path("data/sample_papers")
RESULTS_DIR = Path("results")
SUM_DIR = RESULTS_DIR / "summaries"
ANA_DIR = RESULTS_DIR / "analyses"
META_DIR = RESULTS_DIR / "metadata"
COMP_DIR = RESULTS_DIR / "comparisons"
for d in [SUM_DIR, ANA_DIR, META_DIR, COMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------

def ensure_api_key():
    """Ensure MISTRAL_API_KEY is loaded or raise a clear error."""
    if not MISTRAL_API_KEY:
        raise RuntimeError(
            "❌ MISTRAL_API_KEY not found. Please add it to .env and reload the environment."
        )

def summarize_and_analyze_pdf(pdf_path: Path, raw_text: str, query: str) -> Tuple[Path, Path, float]:
    """Perform the summarization and analysis pipeline for a single PDF."""
    start_time = time.time()

    md = extract_metadata(pdf_path)
    title = md.get("title", pdf_path.stem)
    authors = md.get("authors", "Unknown")
    abstract = md.get("abstract")

    txt = clean_text(raw_text)
    chunks = chunk_text(txt, max_chars=1500, overlap=150)
    if not chunks:
        raise ValueError(f"No extractable text from {pdf_path.name}")

    labeled_chunks: List[Tuple[str, str]] = [(f"{pdf_path.stem} [chunk {i+1}]", ch) for i, ch in enumerate(chunks)]
    index = build_index(labeled_chunks)
    hits = search(index, query, k=5)
    top_chunks = [text for _s, (_lbl, text) in hits]

    # Summarization
    header = f"# {title}\n\n**Authors:** {authors}\n\n"
    if abstract:
        header += f"**Abstract:** {abstract}\n\n---\n\n"
    summary_md = header + summarize_chunks(MISTRAL_API_KEY, title, top_chunks)
    sum_path = SUM_DIR / f"{safe_stem(pdf_path)}_summary.md"
    sum_path.write_text(summary_md, encoding="utf-8")

    # Analysis
    analysis_md = analyze_chunks(MISTRAL_API_KEY, title, top_chunks)
    ana_path = ANA_DIR / f"{safe_stem(pdf_path)}_analysis.md"
    ana_path.write_text(analysis_md, encoding="utf-8")

    # Metadata JSON
    meta = {
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
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    duration = round(time.time() - start_time, 2)
    return sum_path, ana_path, duration


# ---------------------------------------------------------------
# Bonus Feature: Compare Two PDFs
# ---------------------------------------------------------------

def compare_pdfs(pdf1: Path, pdf2: Path):
    """Compare two PDFs using the new Mistral SDK."""
    print("🧠 Comparing papers:")
    print(f"  1️⃣ {pdf1.name} \n  2️⃣ {pdf2.name}")

    pairs1 = load_all_pdfs_text(pdf1.parent)
    pairs2 = load_all_pdfs_text(pdf2.parent)
    raw1 = next((r for p, r in pairs1 if p == pdf1), None)
    raw2 = next((r for p, r in pairs2 if p == pdf2), None)

    if not raw1 or not raw2:
        raise ValueError("Could not extract text from one or both PDFs.")

    # ✅ Use new Mistral client
    client = Mistral(api_key=MISTRAL_API_KEY)

    prompt = f"""
Compare the following two research papers in terms of:
- Main research questions
- Methodologies
- Findings
- Strengths and limitations
- Overall impact and novelty

Paper 1 ({pdf1.name}):
{raw1[:2000]}

Paper 2 ({pdf2.name}):
{raw2[:2000]}

Provide a concise, well-structured comparison summary.
"""

    # ✅ New client call syntax
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}],
    )

    # ✅ FIXED: Use the correct response structure for Mistral AI SDK
    comparison_text = response.choices[0].message.content
    
    output_path = COMP_DIR / f"compare_{safe_stem(pdf1)}_vs_{safe_stem(pdf2)}.md"
    output_path.write_text(comparison_text, encoding="utf-8")

    print(f"✅ Comparison saved to: {output_path}")
    return output_path


# ---------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="ResearchGPT Assistant CLI")
    parser.add_argument("--pdf", type=str, help="Path to a single PDF file")
    parser.add_argument("--data-dir", type=str, default="data/sample_papers", help="Directory containing PDFs")
    parser.add_argument("--query", type=str, default="What problem does this paper solve?", help="User query for summarization")
    parser.add_argument("--report", action="store_true", help="Generate batch CSV report")
    parser.add_argument("--compare", nargs=2, metavar=("PDF1", "PDF2"), help="Compare two research papers")
    args = parser.parse_args()

    ensure_api_key()

    if args.compare:
        pdf1 = Path(args.compare[0])
        pdf2 = Path(args.compare[1])
        compare_pdfs(pdf1, pdf2)
        return

    if args.pdf:
        pdf_path = Path(args.pdf)
        print(f"📄 Processing single PDF: {pdf_path.name}")
        pairs = load_all_pdfs_text(pdf_path.parent)
        raw_text = next((r for p, r in pairs if p == pdf_path), None)
        if not raw_text:
            print(f"❌ Could not extract text from {pdf_path}")
            return
        s, a, dur = summarize_and_analyze_pdf(pdf_path, raw_text, args.query)
        print(f"✅ Summary → {s}")
        print(f"✅ Analysis → {a}")
        print(f"⏱ Duration: {dur:.2f}s")
        return

    data_dir = Path(args.data_dir)
    pairs = load_all_pdfs_text(data_dir)
    if not pairs:
        print(f"No PDFs found in {data_dir}")
        return

    for pdf_path, raw in pairs:
        try:
            s, a, dur = summarize_and_analyze_pdf(pdf_path, raw, args.query)
            print(f"✅ Processed: {pdf_path.name}")
            append_report_row(pdf_path, args.query, s, a, dur)
        except Exception as e:
            print(f"[WARN] {pdf_path.name}: {e}")

if __name__ == "__main__":
    main()