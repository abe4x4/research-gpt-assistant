"""
Mistral wrapper for quick summaries.
"""
from typing import List
from mistralai import Mistral

DEFAULT_MODEL = "mistral-tiny"

def summarize_chunks(api_key: str, title: str, chunks: List[str], model: str = DEFAULT_MODEL) -> str:
    """
    Very small prompt to generate a concise summary from top chunks.
    """
    client = Mistral(api_key=api_key)

    # Keep the prompt lightweight for first test
    system = (
        "You are a concise research assistant. "
        "Summarize the user's provided excerpts into 5-7 bullet points using plain language. "
        "Avoid speculation; focus on what is explicitly supported."
    )
    user_content = f"TITLE: {title}\n\nEXCERPTS:\n" + "\n\n---\n\n".join(chunks[:5])

    resp = client.chat.complete(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content
