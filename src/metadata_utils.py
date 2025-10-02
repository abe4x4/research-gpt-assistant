from __future__ import annotations
from pathlib import Path
from typing import Optional, Dict, List
from PyPDF2 import PdfReader
import re

BANNER_PATTERNS = [
    r"provided proper attribution is provided",
    r"permission to (?:use|reproduce)",
    r"google (?:hereby )?grants permission",
    r"arxiv:",
    r"conference on",
    r"proceedings of",
]

def _is_banner(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in BANNER_PATTERNS)

def extract_first_page_lines(pdf_path: Path) -> List[str]:
    reader = PdfReader(str(pdf_path))
    if not reader.pages:
        return []
    raw = (reader.pages[0].extract_text() or "")
    # normalize whitespace
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    lines = [ln.strip() for ln in raw.splitlines()]
    # drop empties
    lines = [ln for ln in lines if ln]
    return lines

def guess_title(lines: List[str]) -> Optional[str]:
    """
    Heuristic:
      - consider lines before 'Abstract'
      - ignore obvious banners
      - prefer the longest line with 3–20 words
      - exclude lines with email/affiliation hints
    """
    pre_abstract: List[str] = []
    for ln in lines:
        if re.match(r"^\s*abstract\b", ln, flags=re.I):
            break
        pre_abstract.append(ln)

    candidates = []
    for ln in pre_abstract[:20]:
        if _is_banner(ln):
            continue
        if re.search(r"@|university|institute|laboratory|department", ln, flags=re.I):
            continue
        wc = len(ln.split())
        if 3 <= wc <= 20:
            candidates.append(ln)

    if not candidates:
        return None

    # Prefer the line with the highest “title case” ratio, break ties by length
    def title_score(s: str):
        words = s.split()
        tc = sum(1 for w in words if re.match(r"^[A-Z][a-zA-Z0-9\-]*$", w))
        return (tc / max(1, len(words)), len(s))

    candidates.sort(key=title_score, reverse=True)
    return candidates[0]

def guess_authors(lines: List[str]) -> Optional[str]:
    """
    Heuristic:
      - look near the title for a line with comma-separated capitalized names or 'et al.'
      - avoid affiliations/emails
    """
    window = lines[:30]
    for ln in window:
        if _is_banner(ln):
            continue
        if re.search(r"@|university|institute|laboratory|department", ln, flags=re.I):
            continue
        if re.search(r"\bet al\.?\b", ln, flags=re.I):
            return ln
        # comma-separated names like "Ashish Vaswani, Noam Shazeer, Niki Parmar, ... "
        parts = [p.strip() for p in ln.split(",") if p.strip()]
        if 2 <= len(parts) <= 12:
            caps_like = sum(
                1 for p in parts if re.search(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)*$", p)
            )
            if caps_like >= max(2, len(parts)//2):
                return ln
    return None

def guess_abstract(lines: List[str]) -> Optional[str]:
    text = "\n".join(lines)
    m = re.search(r"(?:^|\n)(abstract)[:\s]*\n?(.*?)(?:\n[A-Z][A-Za-z ]{2,}:|\Z)", text, flags=re.I | re.S)
    if m:
        return m.group(2).strip()
    return None

def extract_metadata(pdf_path: Path) -> Dict[str, Optional[str]]:
    lines = extract_first_page_lines(pdf_path)
    title = guess_title(lines)
    authors = guess_authors(lines)
    abstract = guess_abstract(lines)

    if not title:
        # fallback to embedded PDF metadata
        try:
            info = PdfReader(str(pdf_path)).metadata or {}
            title = getattr(info, "title", None)
        except Exception:
            title = None

    return {"title": title, "authors": authors, "abstract": abstract}
