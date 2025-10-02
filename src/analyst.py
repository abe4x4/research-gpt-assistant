from typing import List, Dict
from mistralai import Mistral

DEFAULT_MODEL = "mistral-tiny"  # change if your account exposes a different model

SECTIONS: Dict[str, str] = {
    "Methods": (
        "From the excerpts below, extract the METHODS used. "
        "Name architectures, datasets, training setup (optimizer, lr, steps), and eval metrics. "
        "Bullet points, only facts supported by the text."
    ),
    "Key Results": (
        "From the excerpts below, extract the MAIN RESULTS. "
        "Report strongest findings, key numbers vs baselines. "
        "Bullet points, no speculation."
    ),
    "Limitations": (
        "From the excerpts below, list LIMITATIONS and open questions. "
        "Include failure modes, assumptions, scope. Bullet points."
    ),
}

def analyze_chunks(api_key: str, title: str, chunks: List[str], model: str = DEFAULT_MODEL) -> str:
    client = Mistral(api_key=api_key)
    md_parts = [f"# Analysis: {title}\n"]

    for section, instruction in SECTIONS.items():
        user_content = f"{instruction}\n\nEXCERPTS:\n" + "\n\n---\n\n".join(chunks[:8])
        resp = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": "You are a careful research analyst. Be terse and factual."},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
        )
        md_parts.append(f"\n## {section}\n")
        md_parts.append(resp.choices[0].message.content.strip())

    return "\n".join(md_parts).strip()
