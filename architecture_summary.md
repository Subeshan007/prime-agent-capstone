# PRIME Architecture Summary

PRIME is designed as a modular, multi-agent system orchestrated by **LangGraph**. The core workflow is state-driven, where a shared state object is passed between specialized agents.

**Key Components:**
1.  **Orchestrator Agent**: The central brain that plans the research session based on user input (topic, depth). It directs the flow to other agents.
2.  **Specialized Agents**:
    *   **Research Agent**: Handles information gathering (Web Search, PDF parsing) and ingestion into **ChromaDB**.
    *   **Summarization Agent**: Retrieves context and generates executive summaries and structured notes.
    *   **Credibility Agent**: Analyzes sources for bias and reliability.
    *   **Learning Agent**: Generates educational content (Quizzes, Flashcards) based on the notes.
    *   **Knowledge Graph Agent**: Extracts entities/relations to populate a **SQLite** graph database.
    *   **Progress Agent**: Tracks user sessions and learning metrics in SQLite.
3.  **Data Layer**:
    *   **ChromaDB**: Stores semantic embeddings of document chunks for RAG.
    *   **SQLite**: Stores structured relational data (User profiles, Session history, KG Nodes/Edges).
4.  **Interface**: A **Streamlit** application serves as the frontend, providing interactive tabs for different outputs (Summary, Notes, Graph, etc.) and real-time progress tracking.

This architecture ensures separation of concerns, scalability (agents can be improved independently), and a "Google-level" standard of observability and structure.
