"""
Configuration loader for environment variables (.env).
"""
import os
from dotenv import load_dotenv

load_dotenv()  # loads MISTRAL_API_KEY, OPENAI_API_KEY if present

MISTRAL_API_KEY: str | None = os.getenv("MISTRAL_API_KEY")
# You can add more later:
# OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
