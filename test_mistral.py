import os
from mistralai import Mistral

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY is not set in the environment!")

client = Mistral(api_key=api_key)

model = "mistral-tiny"  # try other models if needed: mistral-small, mistral-medium

resp = client.chat.complete(
    model=model,
    messages=[{"role": "user", "content": "Hello from my capstone project!"}]
)

print("Mistral API response:")
print(resp.choices[0].message.content)
