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
                CREATE TABLE IF NOT EXISTS experiments (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    camera_source TEXT,
                    resolution TEXT,
                    fps INTEGER,
                    steps_count INTEGER,
                    created_at REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiment_steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id TEXT,
                    step_number INTEGER,
                    step_name TEXT,
                    target_activity TEXT,
                    target_object TEXT,
                    guidance TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS training_samples (
                    id TEXT PRIMARY KEY,
                    experiment_id TEXT,
                    activity TEXT,
                    person_id TEXT,
                    video_path TEXT,
                    samples_count INTEGER,
                    duration_sec REAL,
                    created_at REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS datasets (
                    id TEXT PRIMARY KEY,
                    total_samples INTEGER,
                    train_count INTEGER,
                    val_count INTEGER,
                    test_count INTEGER,
                    created_at REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS models (
                    id TEXT PRIMARY KEY,
                    version TEXT,
                    dataset_id TEXT,
                    accuracy REAL,
                    val_accuracy REAL,
                    test_accuracy REAL,
                    inference_fps REAL,
                    model_size_mb REAL,
                    device TEXT,
                    status TEXT,
                    created_at REAL
                )
            """)
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
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    activity TEXT,
                    confidence REAL,
                    duration_sec REAL,
                    evidence TEXT,
                    timestamp REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS objects (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    color_hsv TEXT,
                    confidence REAL,
                    state TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    hand TEXT,
                    object_id TEXT,
                    state TEXT,
                    distance_px REAL,
                    timestamp REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    event_type TEXT,
                    details TEXT,
                    timestamp REAL
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    error_type TEXT,
                    message TEXT,
                    timestamp REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    fps REAL,
                    latency_ms REAL,
                    cpu_pct REAL,
                    ram_gb REAL,
                    gpu_pct REAL,
                    timestamp REAL
                )
            """)
            conn.commit()
            logger.info("SQLite Database tables initialized successfully.")

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

    def save_experiment(self, exp_data: dict):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO experiments (id, name, description, camera_source, resolution, fps, steps_count, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (exp_data["id"], exp_data["name"], exp_data.get("description", ""), exp_data.get("camera_source", "0"), exp_data.get("resolution", "1280x720"), exp_data.get("fps", 30), len(exp_data.get("steps", [])), time.time())
            )
            for idx, step in enumerate(exp_data.get("steps", [])):
                conn.execute(
                    "INSERT INTO experiment_steps (experiment_id, step_number, step_name, target_activity, target_object, guidance) VALUES (?, ?, ?, ?, ?, ?)",
                    (exp_data["id"], idx + 1, step.get("name", f"Step {idx+1}"), step.get("activity", ""), step.get("object", ""), step.get("guidance", ""))
                )

    def get_experiments(self) -> list:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, camera_source, resolution, fps, steps_count FROM experiments ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [
                {
                    "id": r[0], "name": r[1], "description": r[2],
                    "camera_source": r[3], "resolution": r[4], "fps": r[5], "steps_count": r[6]
                }
                for r in rows
            ]

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

