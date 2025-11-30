"""
Tests for text utilities.
"""
from prime_agent.utils.text_utils import clean_text, chunk_text

def test_clean_text():
    text = "  Hello   World  \n\n"
    assert clean_text(text) == "Hello World"

def test_chunk_text():
    text = "Word " * 500
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) > 1
    assert len(chunks[0]) <= 100
