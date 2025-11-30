"""
SQLite database connection and schema management.
"""
import sqlite3
import os
from loguru import logger
from prime_agent.config import DB_PATH

class Database:
    """
    Manages SQLite connection and tables.
    """
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """
        Create tables if they don't exist.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users/Sessions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            topic TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            depth INTEGER,
            summary TEXT
        )
        """)
        
        # Knowledge Graph Nodes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            label TEXT,
            type TEXT,
            metadata TEXT
        )
        """)
        
        # Knowledge Graph Edges
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS edges (
            id TEXT PRIMARY KEY,
            source_id TEXT,
            target_id TEXT,
            relation TEXT,
            metadata TEXT,
            FOREIGN KEY(source_id) REFERENCES nodes(id),
            FOREIGN KEY(target_id) REFERENCES nodes(id)
        )
        """)
        
        # Quiz Results
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            score REAL,
            total_questions INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")

    def execute(self, query: str, params: tuple = ()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except Exception as e:
            logger.error(f"DB Error: {e}")
            raise
        finally:
            conn.close()

    def fetch_all(self, query: str, params: tuple = ()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()
