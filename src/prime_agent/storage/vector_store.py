import logging
from typing import List, Dict, Optional

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        logger.info("🟦 Starting Chroma in clean EPHEMERAL mode")

        # 🔥 CRITICAL FIX: Reset Chroma singleton system
        try:
            chromadb.api.client.SharedSystemClient.reset_system()
            logger.info("🔄 Chroma system reset successfully")
        except:
            logger.warning("⚠️ Chroma system reset not supported, continuing")

        # Load embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # Create Chroma instance WITHOUT persistence
        self.vector_store = Chroma(
            collection_name="prime_docs",
            embedding_function=self.embeddings,
            client_settings=Settings()   # DEFAULT only
        )

    def add_documents(self, documents: List[str], metadata: List[Dict], ids: List[str]):
        batch = 32
        for i in range(0, len(documents), batch):
            try:
                self.vector_store.add_texts(
                    texts=documents[i:i+batch],
                    metadatas=metadata[i:i+batch],
                    ids=ids[i:i+batch]
                )
            except Exception as e:
                logger.error(f"Batch embedding failed: {e}")

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
            logger.error(f"Search error: {e}")
            return []

    def clear(self):
        try:
            self.vector_store.delete_collection()
        except Exception:
            pass
