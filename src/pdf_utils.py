"""
PDF loading utilities using PyPDF2.
"""
from pathlib import Path
from typing import List
from PyPDF2 import PdfReader

def load_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts = []
    for page in reader.pages:
        text = (page.extract_text() or "").strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts)

def load_all_pdfs_text(folder: Path) -> list[tuple[Path, str]]:
    pdfs = sorted(folder.glob("*.pdf"))
    results: List[tuple[Path, str]] = []
    for p in pdfs:
        try:
            results.append((p, load_pdf_text(p)))
        except Exception as e:
            print(f"[WARN] Failed to parse {p.name}: {e}")
    return results
