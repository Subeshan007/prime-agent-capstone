"""
Tests for vector store.
"""
import shutil
import tempfile
import os
from prime_agent.storage.vector_store import VectorStore

def test_vector_store():
    # Create a temp directory for the test
    temp_dir = tempfile.mkdtemp()
    try:
        vs = VectorStore(persist_directory=temp_dir)
        
        docs = ["This is a test document.", "Another document about AI."]
        metadatas = [{"source": "test1"}, {"source": "test2"}]
        ids = ["1", "2"]
        
        vs.add_documents(docs, metadatas, ids)
        
        results = vs.search("AI", k=1)
        assert len(results) == 1
        assert "AI" in results[0]["content"]
        
        vs.clear()
        results_after_clear = vs.search("AI", k=1)
        assert len(results_after_clear) == 0
        
    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
