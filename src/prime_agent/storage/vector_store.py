"""
ChromaDB wrapper for Streamlit Cloud – in-memory only (ephemeral mode)
"""
import chromadb
chromadb.api.client.SharedSystemClient._instance = None
chromadb.api.client.SharedSystemClient._settings = None

from typing import List, Dict, Optional
import logging
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        logger.info("⬇️ Loading local embedding model 'all-MiniLM-L6-v2'...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # ✔️ Streamlit Cloud compatible
        self.settings = Settings(
            anonymized_telemetry=False
        )

        logger.info("🟦 Starting Chroma in ephemeral in-memory mode")

        self.vector_store = Chroma(
            collection_name="prime_docs",
            embedding_function=self.embeddings,
            client_settings=self.settings
        )

    def add_documents(self, documents: List[str], metadata: List[Dict], ids: List[str]):
        try:
            self.vector_store.add_texts(
                texts=documents,
                metadatas=metadata,
                ids=ids
            )
        except Exception as e:
            logger.error(f"❌ Error adding docs: {e}")

    def search(self, query: str, k: int = 5, filter: Optional[Dict] = None):
        try:
            results = self.vector_store.similarity_search(query, k=k, filter=filter)
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "id": doc.metadata.get("id", "")
                }
                for doc in results
            ]
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []

    def clear(self):
        try:
            self.vector_store.delete_collection()
        except:
            pass
