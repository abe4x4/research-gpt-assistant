"""
Text cleaning & chunking helpers for classical NLP (TF-IDF) & LLM prompts.
"""
import re
from typing import List

def clean_text(s: str) -> str:
    s = s.replace("\x00", " ")  # strip nulls if any
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def chunk_text(s: str, max_chars: int = 1500, overlap: int = 150) -> List[str]:
    """
    Simple character-based chunker (good enough for TF-IDF + short prompts).
    """
    s = s.strip()
    chunks = []
    start = 0
    n = len(s)
    while start < n:
        end = min(start + max_chars, n)
        chunk = s[start:end]
        chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks
