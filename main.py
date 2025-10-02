from pathlib import Path
from typing import List, Tuple
import os

from src.config import MISTRAL_API_KEY
from src.pdf_utils import load_all_pdfs_text
from src.text_utils import clean_text, chunk_text
from src.indexer import build_index, search
from src.summarizer import summarize_chunks
from src.analyst import analyze_chunks
from src.io_utils import safe_stem
from src.metadata_utils import extract_metadata

DATA_DIR = Path("data/sample_papers")
SUM_DIR  = Path("results/summaries")
ANA_DIR  = Path("results/analyses")
SUM_DIR.mkdir(parents=True, exist_ok=True)
ANA_DIR.mkdir(parents=True, exist_ok=True)

TOP_K = int(os.environ.get('RGPT_TOP_K', 5))
QUERY = os.environ.get('RGPT_QUERY', "What problem does this paper address and what methods are used?")

def ensure_api_key():
    if not MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY is missing. Put it in .env and reload into your shell.")

def summarize_and_analyze_pdf(pdf_path: Path, raw_text: str) -> tuple[Path, Path]:
    # Metadata
    md = extract_metadata(pdf_path)
    title   = md.get("title")   or pdf_path.stem
    authors = md.get("authors") or "Unknown"
    abstract = md.get("abstract")

    # Clean & chunk
    txt = clean_text(raw_text)
    chunks = chunk_text(txt, max_chars=1500, overlap=150)
    if not chunks:
        raise RuntimeError(f"No extractable text from: {pdf_path.name}")

    # Index & retrieve
    labeled_chunks: List[Tuple[str, str]] = [(f"{pdf_path.stem} [chunk {i+1}]", ch) for i, ch in enumerate(chunks)]
    index = build_index(labeled_chunks)
    hits = search(index, QUERY, k=TOP_K)
    top_chunks = [text for _s, (_lbl, text) in hits]

    # Summary
    header = f"# {title}\n\n**Authors:** {authors}\n\n"
    if abstract:
        header += f"**Abstract (detected):** {abstract}\n\n---\n\n"
    summary_md = header + summarize_chunks(MISTRAL_API_KEY, title, top_chunks)
    if refs:
        summary_md += "\n\n---\n\n## Sources (top retrieved chunks)\n"
        for sc,lbl in refs:
            summary_md += f"- {lbl} (score: {sc:.3f})\n"
    sum_path = SUM_DIR / f"{safe_stem(pdf_path)}_summary.md"
    sum_path.write_text(summary_md, encoding="utf-8")

    # Analysis
    analysis_md = analyze_chunks(MISTRAL_API_KEY, title, top_chunks)
    ana_path = ANA_DIR / f"{safe_stem(pdf_path)}_analysis.md"
    ana_path.write_text(analysis_md, encoding="utf-8")

    return sum_path, ana_path

def main():
    ensure_api_key()
    pairs = load_all_pdfs_text(DATA_DIR)
    if not pairs:
        print(f"No PDFs found in {DATA_DIR}. Place some .pdf files and retry.")
        return

    for pdf_path, raw in pairs:
        try:
            s, a = summarize_and_analyze_pdf(pdf_path, raw)
            print(f"Saved summary  → {s}")
            print(f"Saved analysis → {a}")
        except Exception as e:
            print(f"[WARN] {pdf_path.name}: {e}")

if __name__ == "__main__":
    main()
