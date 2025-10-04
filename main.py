from pathlib import Path
from typing import List, Tuple
import os, argparse, json

from src.config import MISTRAL_API_KEY
from src.pdf_utils import load_all_pdfs_text
from src.text_utils import clean_text, chunk_text
from src.indexer import build_index, search
from src.summarizer import summarize_chunks
from src.analyst import analyze_chunks
from src.io_utils import safe_stem
from src.metadata_utils import extract_metadata

# --- Directories ---
DEFAULT_DATA_DIR = Path("data/sample_papers")
SUM_DIR  = Path("results/summaries")
ANA_DIR  = Path("results/analyses")
META_DIR = Path("results/metadata")

for d in [SUM_DIR, ANA_DIR, META_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- Defaults from environment ---
TOP_K = int(os.environ.get('RGPT_TOP_K', 5))
QUERY = os.environ.get(
    'RGPT_QUERY',
    "What problem does this paper address and what methods are used?"
)

def ensure_api_key():
    if not MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY is missing. Put it in .env and reload into your shell.")

def summarize_and_analyze_pdf(pdf_path: Path, raw_text: str, query: str, top_k: int) -> tuple[Path, Path]:
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
    labeled_chunks: List[Tuple[str, str]] = [
        (f"{pdf_path.stem} [chunk {i+1}]", ch) for i, ch in enumerate(chunks)
    ]
    index = build_index(labeled_chunks)
    hits = search(index, query, k=top_k)
    top_chunks = [text for _s, (_lbl, text) in hits]

    # --- Summary ---
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
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return sum_path, ana_path

def main():
    ensure_api_key()

    parser = argparse.ArgumentParser(description="ResearchGPT Assistant")
    parser.add_argument("--k", type=int, default=TOP_K, help="Number of chunks to retrieve")
    parser.add_argument("--query", type=str, default=QUERY, help="Custom query to guide summarization")
    parser.add_argument("--pdf", type=str, help="Path to a single PDF file (optional)")
    parser.add_argument("--data-dir", type=str, help="Path to a folder containing PDFs (optional)")
    args = parser.parse_args()

    # Decide which PDFs to load
    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Specified PDF not found: {pdf_path}")
        pairs = [(pdf_path, load_all_pdfs_text(pdf_path.parent)[0][1])]
    else:
        data_dir = Path(args.data_dir) if args.data_dir else DEFAULT_DATA_DIR
        pairs = load_all_pdfs_text(data_dir)

    if not pairs:
        print("No PDFs found. Please check your path or add PDFs.")
        return

    for pdf_path, raw in pairs:
        try:
            s, a = summarize_and_analyze_pdf(pdf_path, raw, args.query, args.k)
            print(f"Saved summary  → {s}")
            print(f"Saved analysis → {a}")
        except Exception as e:
            print(f"[WARN] {pdf_path.name}: {e}")

if __name__ == "__main__":
    main()
