import sqlite3
import os
import json
import time
import logging
import yaml

logger = logging.getLogger("ASTRA-HAR.Database")

# Try importing psycopg2 for PostgreSQL support
try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    logger.warning("psycopg2 module not found. PostgreSQL support disabled until psycopg2-binary is installed. Defaulting to SQLite.")

class DBService:
    """Enterprise-grade DB Service supporting PostgreSQL and SQLite databases for ASTRA-HAR."""

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.engine = "sqlite"
        self.db_path = "data/experiment.db"
        self.pg_config = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
            "user": os.getenv("POSTGRES_USER", "postgres"),
            "password": os.getenv("POSTGRES_PASSWORD", "password"),
            "dbname": os.getenv("POSTGRES_DB", "astra_har")
        }
        self.connected_db_type = "sqlite"
        self.load_config()
        self.init_db()

    def load_config(self):
        """Load database configuration from YAML file or environment variables."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    cfg = yaml.safe_load(f)
                    db_cfg = cfg.get("database", {})
                    self.engine = os.getenv("DB_ENGINE", db_cfg.get("engine", "postgresql")).lower()
                    self.db_path = db_cfg.get("path", "data/experiment.db")
                    self.pg_config["host"] = os.getenv("POSTGRES_HOST", db_cfg.get("host", "localhost"))
                    self.pg_config["port"] = int(os.getenv("POSTGRES_PORT", str(db_cfg.get("port", 5432))))
                    self.pg_config["user"] = os.getenv("POSTGRES_USER", db_cfg.get("user", "postgres"))
                    self.pg_config["password"] = os.getenv("POSTGRES_PASSWORD", db_cfg.get("password", "password"))
                    self.pg_config["dbname"] = os.getenv("POSTGRES_DB", db_cfg.get("dbname", "astra_har"))
            except Exception as e:
                logger.warning(f"Could not parse config YAML: {e}. Falling back to default settings.")

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _ensure_pg_database_exists(self):
        """Connect to default 'postgres' database to ensure target database exists."""
        if not PSYCOPG2_AVAILABLE:
            return False
        try:
            conn = psycopg2.connect(
                host=self.pg_config["host"],
                port=self.pg_config["port"],
                user=self.pg_config["user"],
                password=self.pg_config["password"],
                dbname="postgres"
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.pg_config["dbname"],))
            exists = cursor.fetchone()
            if not exists:
                logger.info(f"Creating PostgreSQL database: {self.pg_config['dbname']}")
                cursor.execute(f'CREATE DATABASE "{self.pg_config["dbname"]}"')
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.warning(f"Failed to check/create PostgreSQL database '{self.pg_config['dbname']}': {e}")
            return False

    def get_connection(self):
        """Establish database connection (PostgreSQL with graceful fallback to SQLite)."""
        if self.engine == "postgresql" and PSYCOPG2_AVAILABLE:
            try:
                conn = psycopg2.connect(
                    host=self.pg_config["host"],
                    port=self.pg_config["port"],
                    user=self.pg_config["user"],
                    password=self.pg_config["password"],
                    dbname=self.pg_config["dbname"]
                )
                self.connected_db_type = "postgresql"
                return conn
            except Exception as e:
                logger.warning(f"PostgreSQL connection failed ({e}). Attempting auto-creation of database...")
                if self._ensure_pg_database_exists():
                    try:
                        conn = psycopg2.connect(
                            host=self.pg_config["host"],
                            port=self.pg_config["port"],
                            user=self.pg_config["user"],
                            password=self.pg_config["password"],
                            dbname=self.pg_config["dbname"]
                        )
                        self.connected_db_type = "postgresql"
                        return conn
                    except Exception as ex:
                        logger.warning(f"Retry connecting to PostgreSQL failed: {ex}.")

                logger.warning("Falling back to local SQLite database engine.")

        # Fallback SQLite
        self.connected_db_type = "sqlite"
        return sqlite3.connect(self.db_path)

    def _execute(self, conn, sql: str, params: tuple = ()):
        """Execute query handling syntax differences between SQLite and PostgreSQL."""
        cursor = conn.cursor()
        is_pg = self.connected_db_type == "postgresql"

        formatted_sql = sql
        if is_pg:
            # Convert SQLite parameter marker '?' to PostgreSQL '%s'
            formatted_sql = formatted_sql.replace("?", "%s")

        cursor.execute(formatted_sql, params)
        return cursor

    def init_db(self):
        """Create tables for sessions, experiments, steps, telemetry, alerts, and errors."""
        try:
            conn = self.get_connection()
            is_pg = self.connected_db_type == "postgresql"
            auto_inc = "SERIAL" if is_pg else "INTEGER PRIMARY KEY AUTOINCREMENT"
            pk_auto = f"id {auto_inc}" if is_pg else "id INTEGER PRIMARY KEY AUTOINCREMENT"

            tables = [
                f"""CREATE TABLE IF NOT EXISTS experiments (
                    id VARCHAR(100) PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    camera_source TEXT,
                    resolution TEXT,
                    fps INTEGER,
                    steps_count INTEGER,
                    created_at DOUBLE PRECISION
                )""",

                f"""CREATE TABLE IF NOT EXISTS experiment_steps (
                    {pk_auto},
                    experiment_id TEXT,
                    step_number INTEGER,
                    step_name TEXT,
                    target_activity TEXT,
                    target_object TEXT,
                    guidance TEXT
                )""",

                f"""CREATE TABLE IF NOT EXISTS training_samples (
                    id VARCHAR(100) PRIMARY KEY,
                    experiment_id TEXT,
                    activity TEXT,
                    person_id TEXT,
                    video_path TEXT,
                    samples_count INTEGER,
                    duration_sec DOUBLE PRECISION,
                    created_at DOUBLE PRECISION
                )""",

                f"""CREATE TABLE IF NOT EXISTS datasets (
                    id VARCHAR(100) PRIMARY KEY,
                    total_samples INTEGER,
                    train_count INTEGER,
                    val_count INTEGER,
                    test_count INTEGER,
                    created_at DOUBLE PRECISION
                )""",

                f"""CREATE TABLE IF NOT EXISTS models (
                    id VARCHAR(100) PRIMARY KEY,
                    version TEXT,
                    dataset_id TEXT,
                    accuracy DOUBLE PRECISION,
                    val_accuracy DOUBLE PRECISION,
                    test_accuracy DOUBLE PRECISION,
                    inference_fps DOUBLE PRECISION,
                    model_size_mb DOUBLE PRECISION,
                    device TEXT,
                    status TEXT,
                    created_at DOUBLE PRECISION
                )""",

                f"""CREATE TABLE IF NOT EXISTS sessions (
                    session_id VARCHAR(100) PRIMARY KEY,
                    experiment_id TEXT,
                    start_time DOUBLE PRECISION,
                    end_time DOUBLE PRECISION,
                    status TEXT,
                    total_steps INTEGER
                )""",

                f"""CREATE TABLE IF NOT EXISTS step_logs (
                    {pk_auto},
                    session_id TEXT,
                    step_number INTEGER,
                    step_name TEXT,
                    timestamp DOUBLE PRECISION,
                    confidence DOUBLE PRECISION,
                    status TEXT,
                    evidence TEXT
                )""",

                f"""CREATE TABLE IF NOT EXISTS activities (
                    {pk_auto},
                    session_id TEXT,
                    activity TEXT,
                    confidence DOUBLE PRECISION,
                    duration_sec DOUBLE PRECISION,
                    evidence TEXT,
                    timestamp DOUBLE PRECISION
                )""",

                f"""CREATE TABLE IF NOT EXISTS objects (
                    id VARCHAR(100) PRIMARY KEY,
                    name TEXT,
                    color_hsv TEXT,
                    confidence DOUBLE PRECISION,
                    state TEXT
                )""",

                f"""CREATE TABLE IF NOT EXISTS interactions (
                    {pk_auto},
                    session_id TEXT,
                    hand TEXT,
                    object_id TEXT,
                    state TEXT,
                    distance_px DOUBLE PRECISION,
                    timestamp DOUBLE PRECISION
                )""",

                f"""CREATE TABLE IF NOT EXISTS events (
                    {pk_auto},
                    session_id TEXT,
                    event_type TEXT,
                    details TEXT,
                    timestamp DOUBLE PRECISION
                )""",

                f"""CREATE TABLE IF NOT EXISTS alert_logs (
                    {pk_auto},
                    session_id TEXT,
                    timestamp DOUBLE PRECISION,
                    alert_type TEXT,
                    severity TEXT,
                    message TEXT
                )""",

                f"""CREATE TABLE IF NOT EXISTS errors (
                    {pk_auto},
                    session_id TEXT,
                    error_type TEXT,
                    message TEXT,
                    timestamp DOUBLE PRECISION
                )""",

                f"""CREATE TABLE IF NOT EXISTS telemetry (
                    {pk_auto},
                    session_id TEXT,
                    fps DOUBLE PRECISION,
                    latency_ms DOUBLE PRECISION,
                    cpu_pct DOUBLE PRECISION,
                    ram_gb DOUBLE PRECISION,
                    gpu_pct DOUBLE PRECISION,
                    timestamp DOUBLE PRECISION
                )"""
            ]

            cursor = conn.cursor()
            for query in tables:
                cursor.execute(query)
            conn.commit()
            conn.close()
            logger.info(f"Database initialized successfully using [{self.connected_db_type.upper()}] engine.")
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")

    def log_session_start(self, session_id: str, experiment_id: str, total_steps: int):
        """Record the start of an experiment session."""
        try:
            conn = self.get_connection()
            is_pg = self.connected_db_type == "postgresql"
            if is_pg:
                query = """INSERT INTO sessions (session_id, experiment_id, start_time, status, total_steps)
                           VALUES (?, ?, ?, ?, ?)
                           ON CONFLICT (session_id) DO UPDATE SET
                           experiment_id = EXCLUDED.experiment_id, start_time = EXCLUDED.start_time, status = EXCLUDED.status, total_steps = EXCLUDED.total_steps"""
            else:
                query = "INSERT OR REPLACE INTO sessions (session_id, experiment_id, start_time, status, total_steps) VALUES (?, ?, ?, ?, ?)"

            self._execute(conn, query, (session_id, experiment_id, time.time(), "RUNNING", total_steps))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error logging session start: {e}")

    def log_step(self, session_id: str, step_number: int, step_name: str, confidence: float, status: str, evidence: dict):
        """Log individual step completion or evaluation."""
        try:
            conn = self.get_connection()
            query = "INSERT INTO step_logs (session_id, step_number, step_name, timestamp, confidence, status, evidence) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self._execute(conn, query, (session_id, step_number, step_name, time.time(), confidence, status, json.dumps(evidence)))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error logging step: {e}")

    def log_alert(self, session_id: str, alert_type: str, severity: str, message: str):
        """Log an alert event to the database."""
        try:
            conn = self.get_connection()
            query = "INSERT INTO alert_logs (session_id, timestamp, alert_type, severity, message) VALUES (?, ?, ?, ?, ?)"
            self._execute(conn, query, (session_id, time.time(), alert_type, severity, message))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error logging alert: {e}")

    def save_experiment(self, exp_data: dict):
        """Save a new experiment protocol with its sequence steps."""
        try:
            conn = self.get_connection()
            is_pg = self.connected_db_type == "postgresql"
            if is_pg:
                query = """INSERT INTO experiments (id, name, description, camera_source, resolution, fps, steps_count, created_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                           ON CONFLICT (id) DO UPDATE SET
                           name = EXCLUDED.name, description = EXCLUDED.description, camera_source = EXCLUDED.camera_source,
                           resolution = EXCLUDED.resolution, fps = EXCLUDED.fps, steps_count = EXCLUDED.steps_count, created_at = EXCLUDED.created_at"""
            else:
                query = "INSERT OR REPLACE INTO experiments (id, name, description, camera_source, resolution, fps, steps_count, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            self._execute(conn, query, (exp_data["id"], exp_data["name"], exp_data.get("description", ""), exp_data.get("camera_source", "0"), exp_data.get("resolution", "1280x720"), exp_data.get("fps", 30), len(exp_data.get("steps", [])), time.time()))

            for idx, step in enumerate(exp_data.get("steps", [])):
                step_query = "INSERT INTO experiment_steps (experiment_id, step_number, step_name, target_activity, target_object, guidance) VALUES (?, ?, ?, ?, ?, ?)"
                self._execute(conn, step_query, (exp_data["id"], idx + 1, step.get("name", f"Step {idx+1}"), step.get("activity", ""), step.get("object", ""), step.get("guidance", "")))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error saving experiment: {e}")

    def get_experiments(self) -> list:
        """Fetch list of stored experiment protocols."""
        try:
            conn = self.get_connection()
            cursor = self._execute(conn, "SELECT id, name, description, camera_source, resolution, fps, steps_count FROM experiments ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": r[0], "name": r[1], "description": r[2],
                    "camera_source": r[3], "resolution": r[4], "fps": r[5], "steps_count": r[6]
                }
                for r in rows
            ]
        except Exception as e:
            logger.error(f"Error fetching experiments: {e}")
            return []

    def get_session_history(self) -> list:
        """Fetch session execution history."""
        try:
            conn = self.get_connection()
            cursor = self._execute(conn, "SELECT session_id, experiment_id, start_time, end_time, status, total_steps FROM sessions ORDER BY start_time DESC")
            rows = cursor.fetchall()
            conn.close()
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
        except Exception as e:
            logger.error(f"Error fetching session history: {e}")
            return []

    def get_db_info(self) -> dict:
        """Return diagnostic status of active database engine."""
        return {
            "configured_engine": self.engine,
            "active_engine": self.connected_db_type.upper(),
            "status": "CONNECTED",
            "host": self.pg_config["host"] if self.connected_db_type == "postgresql" else "local_file",
            "database": self.pg_config["dbname"] if self.connected_db_type == "postgresql" else self.db_path,
            "psycopg2_installed": PSYCOPG2_AVAILABLE
        }

# Global database instance
db_service = DBService()
