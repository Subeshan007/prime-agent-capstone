"""
ChromaDB wrapper using Local Embeddings (HuggingFace) to avoid API rate limits.
"""
import chromadb
chromadb.api.client.SharedSystemClient._instance = None
from typing import List, Dict, Optional
import logging
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.config import Settings
from prime_agent.config import CHROMA_PATH

logger = logging.getLogger(__name__)

class VectorStore:
    """
    Manages ChromaDB interactions using a fully local persistent store.
    """
    def __init__(self, persist_directory: str = CHROMA_PATH):
        self.persist_directory = persist_directory

        # Local embedding model
        logger.info("⬇️ Loading local embedding model 'all-MiniLM-L6-v2'...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory,
            anonymized_telemetry=False,
            allow_reset=True,
            is_persistent=True,
            caller="local",
            disable_scheduler=True
        )

        self.vector_store = Chroma(
            collection_name="prime_docs",
            embedding_function=self.embeddings,
            persist_directory=persist_directory,
            client_settings=settings
        )


    def add_documents(self, documents: List[str], metadata: List[Dict], ids: List[str]):
        """
        Adds documents to the vector store using local embeddings.
        """
        batch_size = 32
        total_docs = len(documents)
        logger.info(f"🚀 Embedding {total_docs} documents locally...")

        for i in range(0, total_docs, batch_size):
            try:
                batch_docs = documents[i:i + batch_size]
                batch_meta = metadata[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]

                self.vector_store.add_texts(
                    texts=batch_docs,
                    metadatas=batch_meta,
                    ids=batch_ids
                )
                logger.info(f"✅ Batch {i//batch_size + 1} stored.")
            except Exception as e:
                logger.error(f"❌ Error embedding batch: {e}")

    def search(self, query: str, k: int = 5, filter: Optional[Dict] = None):
        """
        Search for relevant documents.
        """
        try:
            results = self.vector_store.similarity_search(query, k=k, filter=filter)

            formatted = []
            for doc in results:
                formatted.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "id": doc.metadata.get("id", "")
                })

            return formatted
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def clear(self):
        """
        Clear the vector collection.
        """
        try:
            self.vector_store.delete_collection()
            logger.info("🧹 Vector store cleared.")
        except Exception as e:
            logger.warning(f"Could not clear vector store: {e}")
