"""
Tool for managing user profiles and progress.
"""
import uuid
from prime_agent.storage.db import Database
from loguru import logger

def create_session(topic: str, depth: int) -> str:
    """
    Create a new session and return session_id.
    """
    db = Database()
    session_id = str(uuid.uuid4())
    try:
        db.execute(
            "INSERT INTO sessions (id, topic, depth) VALUES (?, ?, ?)",
            (session_id, topic, depth)
        )
        return session_id
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        return ""

def update_summary(session_id: str, summary: str):
    """
    Update session summary.
    """
    db = Database()
    try:
        db.execute(
            "UPDATE sessions SET summary = ? WHERE id = ?",
            (summary, session_id)
        )
    except Exception as e:
        logger.error(f"Failed to update summary: {e}")

def log_quiz_result(session_id: str, score: float, total: int):
    """
    Log quiz result.
    """
    db = Database()
    result_id = str(uuid.uuid4())
    try:
        db.execute(
            "INSERT INTO quiz_results (id, session_id, score, total_questions) VALUES (?, ?, ?, ?)",
            (result_id, session_id, score, total)
        )
    except Exception as e:
        logger.error(f"Failed to log quiz result: {e}")

def get_session_history() -> list:
    """
    Get all sessions.
    """
    db = Database()
    try:
        return db.fetch_all("SELECT * FROM sessions ORDER BY timestamp DESC")
    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        return []
