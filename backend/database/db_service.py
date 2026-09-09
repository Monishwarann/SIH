import sqlite3
import os
import json
import time
import logging

logger = logging.getLogger("ASTRA-HAR.Database")

class DBService:
    """Non-blocking SQLite database for storing experiment sessions, steps, alerts, and system events."""

    def __init__(self, db_path: str = "data/experiment.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Create tables if they do not exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    experiment_id TEXT,
                    start_time REAL,
                    end_time REAL,
                    status TEXT,
                    total_steps INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS step_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    step_number INTEGER,
                    step_name TEXT,
                    timestamp REAL,
                    confidence REAL,
                    status TEXT,
                    evidence TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alert_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp REAL,
                    alert_type TEXT,
                    severity TEXT,
                    message TEXT
                )
            """)
            conn.commit()
            logger.info("SQLite Database initialized successfully.")

    def log_session_start(self, session_id: str, experiment_id: str, total_steps: int):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO sessions (session_id, experiment_id, start_time, status, total_steps) VALUES (?, ?, ?, ?, ?)",
                (session_id, experiment_id, time.time(), "RUNNING", total_steps)
            )

    def log_step(self, session_id: str, step_number: int, step_name: str, confidence: float, status: str, evidence: dict):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO step_logs (session_id, step_number, step_name, timestamp, confidence, status, evidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (session_id, step_number, step_name, time.time(), confidence, status, json.dumps(evidence))
            )

    def log_alert(self, session_id: str, alert_type: str, severity: str, message: str):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO alert_logs (session_id, timestamp, alert_type, severity, message) VALUES (?, ?, ?, ?, ?)",
                (session_id, time.time(), alert_type, severity, message)
            )

    def get_session_history(self) -> list:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT session_id, experiment_id, start_time, end_time, status, total_steps FROM sessions ORDER BY start_time DESC")
            rows = cursor.fetchall()
            return [
                {
                    "session_id": r[0],
                    "experiment_id": r[1],
                    "start_time": r[2],
                    "end_time": r[3],
                    "status": r[4],
                    "total_steps": r[5]
                }
                for r in rows
            ]

# Global database instance
db_service = DBService()
