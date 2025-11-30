"""
Utilities for file I/O and path handling.
"""
import os
from pathlib import Path
from loguru import logger

def ensure_directory(path: str):
    """
    Ensure a directory exists.
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
