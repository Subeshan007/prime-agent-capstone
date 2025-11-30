"""
Global configuration settings for PRIME.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "prime_data.db"))
CHROMA_PATH = os.getenv("CHROMA_PATH", str(BASE_DIR / "chroma_db"))

# LLM Config
# Switch to 1.5-flash for better Rate Limits (RPM)
DEFAULT_MODEL = "gemini-1.5-flash"
FAST_MODEL = "gemini-1.5-flash"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
