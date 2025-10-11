from pathlib import Path
from typing import List, Tuple
import os, argparse, json, sys, time
from httpx import RemoteProtocolError, ConnectError, ReadTimeout

from src.config import MISTRAL_API_KEY
from src.pdf_utils import load_all_pdfs_text
from src.text_utils import clean_text, chunk_text
from src.indexer import build_index, search
from src.summarizer import summarize_chunks
from src.analyst import analyze_chunks
from src.io_utils import safe_stem
from src.metadata_utils import extract_metadata

# --- Safety check for API key ---
if not os.getenv("MISTRAL_API_KEY"):
    print("❌ Error: MISTRAL_API_KEY is missing. Please set it in .env or your shell.")
    sys.exit(1)

DATA_DIR = Path("data/sample_papers")
SUM_DIR  = Path("results/summaries")
ANA_DIR  = Path("results/analyses")
META_DIR = Path("results/metadata")

for d in [SUM_DIR, ANA_DIR, META_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def ensure_api_key():
    if not MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY is missing. Put it in .env and reload your shell.")


def summarize_and_analyze_pdf(pdf_path: Path, raw_text: str, query: str, timeout: int = 45):
    """Summarize and analyze one PDF with retries, timeout, and clear error handling."""

    md = extract_metadata(pdf_path)
    title   = md.get("title")   or pdf_path.stem
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

    sum_path = SUM_DIR / f"{safe_stem(pdf_path)}_summary.md"
    ana_path = ANA_DIR / f"{safe_stem(pdf_path)}_analysis.md"

    def try_request(fn, retries=3):
        for attempt in range(1, retries + 1):
            try:
                return fn()
            except (RemoteProtocolError, ConnectError, ReadTimeout) as e:
                print(f"⚠️ Network error on attempt {attempt}/{retries}: {e}")
                time.sleep(3)
        raise RuntimeError(f"❌ Failed after {retries} attempts. Check your network or API status.")

    print("🧠 Summarizing...")
    summary_md = try_request(lambda: summarize_chunks(MISTRAL_API_KEY, title, top_chunks))
    sum_path.write_text(summary_md, encoding="utf-8")

    print("🔍 Analyzing...")
    analysis_md = try_request(lambda: analyze_chunks(MISTRAL_API_KEY, title, top_chunks))
    ana_path.write_text(analysis_md, encoding="utf-8")

    meta = {
        "file": pdf_path.name,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "query_used": query,
        "timeout": timeout,
        "outputs": {
            "summary_md": str(sum_path),
            "analysis_md": str(ana_path),
        },
    }
    meta_path = META_DIR / f"{safe_stem(pdf_path)}_meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Summary saved → {sum_path}")
    print(f"✅ Analysis saved → {ana_path}")
    return sum_path, ana_path


def main():
    parser = argparse.ArgumentParser(description="ResearchGPT Assistant CLI")
    parser.add_argument("--pdf", type=str, help="Path to a single PDF to process")
    parser.add_argument("--data-dir", type=str, default="data/sample_papers", help="Directory containing PDFs")
    parser.add_argument("--k", type=int, default=5, help="Number of top chunks to retrieve")
    parser.add_argument("--query", type=str, default="Summarize key contributions and limitations.", help="Query or prompt")
    parser.add_argument("--timeout", type=int, default=45, help="Max seconds to wait for each API call (default 45s)")
    args = parser.parse_args()

    ensure_api_key()
    TOP_K = args.k
    query = args.query
    timeout = args.timeout

    # --- Process a single file ---
    if args.pdf:
        pdf_path = Path(args.pdf)
        print(f"📄 Processing single PDF: {pdf_path.name}")
        pairs = load_all_pdfs_text(pdf_path.parent)
        if not pairs:
            print(f"No PDFs found in {pdf_path.parent.resolve()}")
            return
        raw_text = pairs[0][1]
        summarize_and_analyze_pdf(pdf_path, raw_text, query=query, timeout=timeout)
        return

    # --- Process entire directory ---
    data_dir = Path(args.data_dir)
    pairs = load_all_pdfs_text(data_dir)
    if not pairs:
        print("No PDFs found. Please check your path or add PDFs.")
        return

    for pdf_path, raw_text in pairs:
        summarize_and_analyze_pdf(pdf_path, raw_text, query=query, timeout=timeout)


if __name__ == "__main__":
    main()
