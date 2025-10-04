import os, sys, json
from pathlib import Path
from dotenv import load_dotenv

# --- Setup ---
project_root = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

load_dotenv()
print("✅ Project root:", project_root)
print("✅ MISTRAL_API_KEY loaded?", bool(os.getenv("MISTRAL_API_KEY")))

# --- Imports ---
from src.config import MISTRAL_API_KEY
from src.pdf_utils import load_all_pdfs_text
from src.text_utils import clean_text, chunk_text
from src.indexer import build_index, search
from src.summarizer import summarize_chunks
from src.analyst import analyze_chunks
from src.metadata_utils import extract_metadata
from src.io_utils import safe_stem

# --- Locate PDF ---
pdf_path = project_root / "data/sample_papers/attention_is_all_you_need.pdf"
print("Looking for PDFs in:", pdf_path.parent)
pdfs = list(pdf_path.parent.glob("*.pdf"))
print("Found PDFs:", pdfs)

# --- Load PDF text ---
pairs = load_all_pdfs_text(pdf_path.parent)
if not pairs:
    raise FileNotFoundError(f"No PDFs in {pdf_path.parent}")
pdf_path, raw_text = pairs[0]
print("✅ Loaded PDF:", pdf_path)
print(raw_text[:500], "\n---\n")

# --- Metadata ---
meta = extract_metadata(pdf_path)
print("✅ Metadata:\n", json.dumps(meta, indent=2))

# --- Clean + chunk ---
txt = clean_text(raw_text)
chunks = chunk_text(txt, max_chars=1500, overlap=150)
print(f"✅ Total chunks: {len(chunks)}")

# --- Index + search ---
index = build_index([(f"{pdf_path.stem} [chunk {i+1}]", ch) for i, ch in enumerate(chunks)])
hits = search(index, "What problem does this paper solve?", k=3)
print("✅ Top hits:\n", hits[:2])

# --- Summarize + analyze ---
top_chunks = [text for _s, (_lbl, text) in hits]
summary = summarize_chunks(MISTRAL_API_KEY, "Attention Is All You Need", top_chunks)
analysis = analyze_chunks(MISTRAL_API_KEY, "Attention Is All You Need", top_chunks)
print("✅ Summary preview:\n", summary[:500])
print("\n✅ Analysis preview:\n", analysis[:500])

# --- Save metadata JSON ---
meta_out = {
    "file": pdf_path.name,
    "title": meta.get("title", pdf_path.stem),
    "authors": meta.get("authors", "Unknown"),
    "abstract": meta.get("abstract"),
    "query_used": "What problem does this paper solve?",
    "outputs": {
        "summary_preview": summary[:200] + "...",
        "analysis_preview": analysis[:200] + "..."
    }
}
out_path = project_root / "results/metadata/attention_is_all_you_need_demo_meta.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(meta_out, indent=2), encoding="utf-8")
print("✅ Metadata saved to:", out_path)
