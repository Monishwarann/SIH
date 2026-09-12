import os
import json
import time
import sqlite3
import logging

logger = logging.getLogger("ASTRA-HAR.EventLogger")

class EventLogger:
    """
    Offline Timestamped Event Logger saving events to SQLite and local JSONL log files.
    """

    def __init__(self, db_path="data/sih_database.db", log_dir="logs"):
        self.db_path = db_path
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.jsonl_path = os.path.join(self.log_dir, "events.jsonl")

        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS event_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        timestamp TEXT,
                        event_type TEXT,
                        action TEXT,
                        confidence REAL,
                        object_detected TEXT,
                        status TEXT,
                        details TEXT
                    )
                """)
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to initialize SQLite log DB: {e}")

    def log_event(self, session_id: str, event_type: str, action: str, confidence: float = 0.95, object_detected: str = "", status: str = "VALIDATED", details: dict = None):
        ts_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        details_str = json.dumps(details or {})

        # 1. Save to SQLite
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO event_logs (session_id, timestamp, event_type, action, confidence, object_detected, status, details)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (session_id, ts_str, event_type, action, confidence, object_detected, status, details_str))
                conn.commit()
        except Exception as e:
            logger.error(f"SQLite log insertion failed: {e}")

        # 2. Save to JSONL
        event_dict = {
            "session_id": session_id,
            "timestamp": ts_str,
            "event_type": event_type,
            "action": action,
            "confidence": confidence,
            "object_detected": object_detected,
            "status": status,
            "details": details or {}
        }

        try:
            with open(self.jsonl_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_dict) + "\n")
        except Exception as e:
            logger.error(f"JSONL log append failed: {e}")

event_logger = EventLogger()
