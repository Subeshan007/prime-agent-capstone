"""
ChromaDB wrapper using Local Embeddings (HuggingFace) to avoid API rate limits.
"""
import chromadb
chromadb.api.client.SharedSystemClient._instance = None
from typing import List, Dict, Optional
import logging
import shutil
import os
import time # Import time for retry delays
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.config import Settings 
from prime_agent.config import CHROMA_PATH

logger = logging.getLogger(__name__)

class VectorStore:
    """
    Manages ChromaDB interactions using local CPU embeddings.
    """
    def __init__(self, persist_directory: str = CHROMA_PATH):
        self.persist_directory = persist_directory
        
        # Initialize Local Embeddings
        logger.info("⬇️ Loading local embedding model 'all-MiniLM-L6-v2'...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # --- CRITICAL FIX: Robust Database Initialization ---
        # We try to initialize Chroma. If it fails with the "different settings" error,
        # we forcefully delete the folder and try again.
        try:
            self._init_chroma()
        except ValueError as e:
            if "different settings" in str(e):
                logger.warning("⚠️ Database settings conflict detected. Wiping and resetting ChromaDB...")
                self._force_wipe()
                self._init_chroma() # Try again fresh
            else:
                raise e # Re-raise other errors
        except Exception as e:
            # Catch-all for other corruption errors
            logger.error(f"⚠️ Database error: {e}. Attempting reset...")
            self._force_wipe()
            self._init_chroma()

    def _init_chroma(self):
        """Helper to initialize the Chroma client"""
        self.vector_store = Chroma(
            collection_name="prime_docs",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
            client_settings=Settings(anonymized_telemetry=False)
        )

    def _force_wipe(self):
        """Helper to delete the database folder"""
        if os.path.exists(self.persist_directory):
            try:
                shutil.rmtree(self.persist_directory)
                time.sleep(1) # Wait for file system to catch up
                logger.info("✅ Old database folder deleted.")
            except Exception as e:
                logger.error(f"❌ Failed to delete database: {e}")

    # ... The rest of your add_documents, search, and clear methods remain the same ...
    def add_documents(self, documents: List[str], metadata: List[Dict], ids: List[str]):
        # ... (keep existing code) ...
        batch_size = 32
        total_docs = len(documents)
        logger.info(f"🚀 Embedding {total_docs} documents locally...")
        for i in range(0, total_docs, batch_size):
            batch_docs = documents[i : i + batch_size]
            batch_meta = metadata[i : i + batch_size]
            batch_ids = ids[i : i + batch_size]
            try:
                self.vector_store.add_texts(texts=batch_docs, metadatas=batch_meta, ids=batch_ids)
                logger.info(f"✅ Processed batch {i//batch_size + 1}")
            except Exception as e:
                logger.error(f"❌ Error embedding batch: {e}")

    def search(self, query: str, k: int = 5, filter: Optional[Dict] = None) -> List[Dict]:
        # ... (keep existing code) ...
        try:
            results = self.vector_store.similarity_search(query, k=k, filter=filter)
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "id": doc.metadata.get("id", "")
                })
            return formatted_results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def clear(self):
        # ... (keep existing code) ...
        try:
            self.vector_store.delete_collection()
            logger.info("✅ Vector store cleared.")
        except Exception as e:
            logger.warning(f"Could not clear vector store: {e}")
