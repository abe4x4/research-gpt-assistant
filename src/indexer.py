"""
Tiny TF-IDF index to support 'intelligent search' across chunks.
"""
from typing import List, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@dataclass
class TfidfIndex:
    vectorizer: TfidfVectorizer
    matrix: np.ndarray
    docs: List[Tuple[str, str]]  # (doc_label, chunk_text)

def build_index(docs: List[Tuple[str, str]]) -> TfidfIndex:
    """
    docs: list of (label, text_chunk)
    """
    texts = [t for _, t in docs]
    vec = TfidfVectorizer(stop_words="english", lowercase=True, max_df=0.9)
    mat = vec.fit_transform(texts)
    return TfidfIndex(vectorizer=vec, matrix=mat, docs=docs)

def search(index: TfidfIndex, query: str, k: int = 5) -> List[Tuple[float, Tuple[str, str]]]:
    qv = index.vectorizer.transform([query])
    sims = cosine_similarity(qv, index.matrix)[0]
    top_idx = sims.argsort()[-k:][::-1]
    return [(float(sims[i]), index.docs[i]) for i in top_idx]
