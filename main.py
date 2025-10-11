#!/usr/bin/env python3
"""
ResearchGPT Assistant
---------------------------------------
Now with:
- --report flag to generate batch summary CSV
- --timeout flag to control API timeout
- Live progress logging for each stage
"""

import os, json, time, argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

from src.config import MISTRAL_API_KEY
from src.pdf_utils import load_all_pdfs_text
from src.text_utils import clean_text, chunk_text
from src.indexer import build_index, search
from src.summarizer import summarize_chunks
from src.analyst import analyze_chunks
from src.metadata_utils import extract_metadata
from src.io_utils import safe_stem
from src.report_utils import append_report_row

DATA_DIR = Path("data/sample_papers")
SUM_DIR  = Path("results/summaries")
ANA_DIR  = Path("results/analyses")
META_DIR = Path("results/metadata")
SUM_DIR.mkdir(parents=True, exist_ok=True)
ANA_DIR.mkdir(parents=True, exist_ok=True)
META_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------- Helper ----------------------
def ensure_api_key():
    if not MISTRAL_API_KEY:
        raise RuntimeError("❌ MISTRAL_API_KEY is missing — check your .env file.")


# ---------------------- Core ----------------------
def summarize_and_analyze_pdf(pdf_path: Path, raw_text: str, query: str, timeout: int = 60) -> Tuple[Path, Path]:
    start_time = time.time()
    print(f"⏳ Processing {pdf_path.name} ...")

    md = extract_metadata(pdf_path)
    title   = md.get("title") or pdf_path.stem
    authors = md.get("authors") or "Unknown"
    abstract = md.get("abstract")

    txt = clean_text(raw_text)
    chunks = chunk_text(txt, max_chars=1500, overlap=150)
    if not chunks:
        raise RuntimeError(f"No extractable text from: {pdf_path.name}")

    labeled_chunks: List[Tuple[str, str]] = [(f"{pdf_path.stem} [chunk {i+1}]", ch) for i, ch in enumerate(chunks)]
    index = build_index(labeled_chunks)
    hits = search(index, query, k=5)
    top_chunks = [text for _s, (_lbl, text) in hits]

    try:
        summary_md = summarize_chunks(MISTRAL_API_KEY, title, top_chunks)
        analysis_md = analyze_chunks(MISTRAL_API_KEY, title, top_chunks)
    except Exception as e:
        raise RuntimeError(f"⚠️ API request failed ({type(e).__name__}): {e}")

    sum_path = SUM_DIR / f"{safe_stem(pdf_path)}_summary.md"
    ana_path = ANA_DIR / f"{safe_stem(pdf_path)}_analysis.md"
    sum_path.write_text(summary_md, encoding="utf-8")
    ana_path.write_text(analysis_md, encoding="utf-8")

    meta = {
        "file": pdf_path.name,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "query_used": query,
        "outputs": {
            "summary_md": str(sum_path),
            "analysis_md": str(ana_path),
        },
        "timestamp": datetime.now().isoformat()
    }
    meta_path = META_DIR / f"{safe_stem(pdf_path)}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    elapsed = time.time() - start_time
    print(f"✅ Done {pdf_path.name} in {elapsed:.1f}s")

    return sum_path, ana_path, elapsed


# ---------------------- Main ----------------------
def main():
    ensure_api_key()

    parser = argparse.ArgumentParser(description="ResearchGPT Assistant CLI")
    parser.add_argument("--data-dir", type=str, default=str(DATA_DIR), help="Directory containing PDF files")
    parser.add_argument("--pdf", type=str, help="Process only this PDF file")
    parser.add_argument("--query", type=str, default="Summarize contributions and limitations.", help="Query for summarization")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout (seconds) for API calls")
    parser.add_argument("--report", action="store_true", help="Save a batch summary report CSV")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    query = args.query
    timeout = args.timeout
    generate_report = args.report

    if args.pdf:
        pdf_path = Path(args.pdf)
        print(f"📄 Processing single PDF: {pdf_path.name}")
        pairs = [(pdf_path, pdf_path.read_bytes())] if pdf_path.exists() else []
    else:
        pairs = load_all_pdfs_text(data_dir)

    if not pairs:
        print(f"❌ No PDFs found in {data_dir}. Add files or check path.")
        return

    batch_start = time.time()
    for pdf_path, raw in pairs:
        try:
            s, a, dur = summarize_and_analyze_pdf(pdf_path, raw, query, timeout)
            if generate_report:
                append_report_row(pdf_path, query, s, a, dur)
        except Exception as e:
            print(f"[WARN] {pdf_path.name}: {e}")

    if generate_report:
        print("📊 Batch summary written to results/batch_report.csv")

    print(f"🏁 All done in {time.time() - batch_start:.1f}s")


if __name__ == "__main__":
    main()
