import logging
from typing import List, Dict, Optional

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        logger.info("🟦 Starting Chroma LOCAL (No Global Singleton)")

        # 🔥 Force wipe the shared client
        try:
            chromadb.api.client.SharedSystemClient._instance = None
        except:
            pass

        # 🔥 Load embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # 🔥 MOST IMPORTANT FIX: Force LocalAPI backend
        client_settings = Settings(
            is_persistent=False,
            allow_reset=True,
            anonymized_telemetry=False,
            chroma_api_impl="chromadb.api.local.LocalAPI",  # 💥 disables SharedSystem
        )

        # Create Chroma in full local mode
        self.vector_store = Chroma(
            collection_name="prime_docs",
            embedding_function=self.embeddings,
            client_settings=client_settings,
        )

    def add_documents(self, documents, metadata, ids):
        batch = 32
        for i in range(0, len(documents), batch):
            self.vector_store.add_texts(
                texts=documents[i:i+batch],
                metadatas=metadata[i:i+batch],
                ids=ids[i:i+batch]
            )

    def search(self, query, k=5, filter=None):
        results = self.vector_store.similarity_search(query, k=k, filter=filter)
        return [
            {
                "content": r.page_content,
                "metadata": r.metadata,
                "id": r.metadata.get("id", "")
            }
            for r in results
        ]

    def clear(self):
        try:
            self.vector_store.delete_collection()
        except:
            pass
