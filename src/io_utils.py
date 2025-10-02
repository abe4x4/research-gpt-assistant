from pathlib import Path
import re

def safe_stem(p: Path) -> str:
    # Convert a PDF path to a safe filename stem
    stem = p.stem.strip().lower()
    stem = re.sub(r"[^a-z0-9]+", "_", stem)
    stem = re.sub(r"_+", "_", stem).strip("_")
    return stem
