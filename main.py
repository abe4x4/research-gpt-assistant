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
DATA_DIR = Path("data/sample_papers")
SUM_DIR  = Path("results/summaries")
ANA_DIR  = Path("results/analyses")
META_DIR = Path("results/metadata")
SUM_DIR.mkdir(parents=True, exist_ok=True)
ANA_DIR.mkdir(parents=True, exist_ok=True)
META_DIR.mkdir(parents=True, exist_ok=True)

# --- Defaults from env (can be overridden by CLI) ---
DEFAULT_TOP_K = int(os.environ.get("RGPT_TOP_K", 5))
DEFAULT_QUERY = os.environ.get(
    "RGPT_QUERY",
    "What problem does this paper address and what methods are used?",
)

def parse_args():
    p = argparse.ArgumentParser(description="Summarize & analyze research PDFs")
    p.add_argument(
        "--k", type=int, default=DEFAULT_TOP_K,
        help="Top-K chunks to retrieve (default from env RGPT_TOP_K or 5)",
    )
    p.add_argument(
        "--query", type=str, default=DEFAULT_QUERY,
        help="Retrieval query (default from env RGPT_QUERY)",
    )
    p.add_argument(
        "--prompt", type=str, default=None,
        help="Optional prompt file to guide style (e.g., prompts/summarize_contributions.txt)",
    )
    return p.parse_args()

def ensure_api_key():
    if not MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY is missing. Put it in .env and reload your shell.")

def summarize_and_analyze_pdf(
    pdf_path: Path,
    raw_text: str,
    k: int,
    query: str,
    prompt_text: str | None,
    prompt_file: str | None,
) -> tuple[Path, Path]:
    # ---- Metadata extraction (heuristic) ----
    md = extract_metadata(pdf_path)
    title    = md.get("title")   or pdf_path.stem
    authors  = md.get("authors") or "Unknown"
    abstract = md.get("abstract")

    # ---- Clean & chunk ----
    txt = clean_text(raw_text)
    chunks = chunk_text(txt, max_chars=1500, overlap=150)
    if not chunks:
        raise RuntimeError(f"No extractable text from: {pdf_path.name}")

    # ---- Index & retrieve ----
    labeled_chunks: List[Tuple[str, str]] = [
        (f"{pdf_path.stem} [chunk {i+1}]", ch) for i, ch in enumerate(chunks)
    ]
    index = build_index(labeled_chunks)
    hits = search(index, query, k=k)

    # Collect chunks and (score, label) refs for a Sources section
    top_chunks: list[str] = []
    refs: list[tuple[float, str]] = []
    for score, (lbl, text) in hits:
        top_chunks.append(text)
        refs.append((score, lbl))

    # Optional: inject prompt steering text as first chunk
    if prompt_text:
        top_chunks = [prompt_text] + top_chunks

    # ---- Summary ----
    header = f"# {title}\n\n**Authors:** {authors}\n\n"
    if abstract:
        header += f"**Abstract (detected):** {abstract}\n\n---\n\n"

    summary_md = header + summarize_chunks(MISTRAL_API_KEY, title, top_chunks)
    if refs:
        summary_md += "\n\n---\n\n## Sources (top retrieved chunks)\n"
        for sc, lbl in refs:
            summary_md += f"- {lbl} (score: {sc:.3f})\n"

    sum_path = SUM_DIR / f"{safe_stem(pdf_path)}_summary.md"
    sum_path.write_text(summary_md, encoding="utf-8")

    # ---- Analysis ----
    analysis_md = analyze_chunks(MISTRAL_API_KEY, title, top_chunks)
    ana_path = ANA_DIR / f"{safe_stem(pdf_path)}_analysis.md"
    ana_path.write_text(analysis_md, encoding="utf-8")

    # ---- Per-PDF metadata JSON ----
    meta = {
        "file": pdf_path.name,
        "pdf_path": str(pdf_path),
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "query_used": query,
        "prompt_file": prompt_file,  # may be None
        "outputs": {
            "summary_md": str(sum_path),
            "analysis_md": str(ana_path),
        },
    }
    meta_path = META_DIR / f"{safe_stem(pdf_path)}_meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return sum_path, ana_path

def main():
    args = parse_args()
    ensure_api_key()

    # Load optional prompt file
    prompt_text, prompt_file = None, None
    if args.prompt:
        pf = Path(args.prompt)
        if not pf.exists():
            raise FileNotFoundError(f"--prompt file not found: {pf}")
        prompt_text = pf.read_text(encoding="utf-8").strip()
        prompt_file = str(pf)

    # Load PDFs
    pairs = load_all_pdfs_text(DATA_DIR)
    if not pairs:
        print(f"No PDFs found in {DATA_DIR}. Place some .pdf files and retry.")
        return

    # Process each PDF
    for pdf_path, raw in pairs:
        try:
            s, a = summarize_and_analyze_pdf(
                pdf_path, raw, k=args.k, query=args.query,
                prompt_text=prompt_text, prompt_file=prompt_file,
            )
            print(f"Saved summary  → {s}")
            print(f"Saved analysis → {a}")
        except Exception as e:
            print(f"[WARN] {pdf_path.name}: {e}")

if __name__ == "__main__":
    main()
