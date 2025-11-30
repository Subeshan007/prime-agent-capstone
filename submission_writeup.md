# Kaggle Submission Write-up

Use this content to fill out your submission form on Kaggle.

## Project Title
PRIME (Personal Researcher & Micro-Scientist Agent)

## Subtitle / One-Sentence Pitch
An AI-powered research assistant that transforms information overload into structured knowledge, quizzes, and visual graphs using multi-agent orchestration.

## Problem Statement
In the age of information overload, "learning" often stops at "reading." Students and professionals struggle to synthesize vast amounts of data from PDFs and web searches into actionable knowledge. Existing tools either just summarize text (losing depth) or are too complex to set up. There is a lack of tools that not only gather information but also *verify* credibility and *teach* the user through active recall.

## Solution
PRIME is a comprehensive "Micro-Scientist" that lives on your desktop. It doesn't just chat; it performs a structured research workflow:
1.  **Orchestrates** a team of specialized AI agents using **LangGraph**.
2.  **Researches** topics deeply using Web Search and RAG (Vector Search) over uploaded documents.
3.  **Synthesizes** "Study Guides" rather than simple summaries, focusing on definitions, comparisons, and processes.
4.  **Verifies** information by cross-referencing sources and scoring credibility.
5.  **Teaches** the user by automatically generating Quizzes and Flashcards for active recall.
6.  **Visualizes** connections through an interactive Knowledge Graph.

## Tech Stack
-   **Orchestration**: LangGraph (Stateful multi-agent workflow)
-   **LLM**: Google Gemini 1.5 Flash (via `google-generativeai`)
-   **Vector Database**: ChromaDB
-   **Graph Database**: SQLite (for Knowledge Graph nodes/edges)
-   **Frontend**: Streamlit
-   **Tools**: DuckDuckGo Search, ReportLab (PDF Generation), NetworkX

## Key Features
-   **Multi-Agent Architecture**: Separate agents for Research, Summarization, Credibility, and Learning ensure separation of concerns and higher quality output.
-   **Active Learning**: Goes beyond passive reading by generating interactive Quizzes and Flashcards.
-   **Knowledge Graph**: Visualizes how concepts are related (e.g., "A causes B"), helping users build mental models.
-   **Credibility Scoring**: Automatically evaluates sources for bias and reliability.
-   **PDF Report Generation**: Exports a beautifully formatted "Research Report" for offline study.

## How it uses Gemini
PRIME relies on **Gemini 1.5 Flash** for its speed and long context window.
-   **Long Context**: The Research Agent ingests entire PDF papers and web pages, fitting them into Gemini's context for accurate RAG without losing nuance.
-   **Structured Output**: We use Gemini's JSON mode to strictly format Quizzes, Knowledge Graph entities, and Credibility Scores, ensuring the UI never breaks.
-   **Reasoning**: The Summarization Agent uses Gemini to synthesize complex topics into "Feynman Explanations" (simple analogies).
