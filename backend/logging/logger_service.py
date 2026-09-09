import os
import json
import time

class LoggerService:
    """Generates structured JSONL telemetry/event logs and human-readable experiment reports."""

    def __init__(self, log_dir: str = "logs", record_dir: str = "recordings"):
        self.log_dir = log_dir
        self.record_dir = record_dir
        os.makedirs(log_dir, exist_ok=True)
        os.makedirs(record_dir, exist_ok=True)

    def log_event(self, event_type: str, data: dict):
        """Append event to events.jsonl log."""
        file_path = os.path.join(self.log_dir, "events.jsonl")
        payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
            "unix_time": round(time.time(), 3),
            "event_type": event_type,
            "data": data
        }
        with open(file_path, "a") as f:
            f.write(json.dumps(payload) + "\n")

    def generate_experiment_report(self, session_id: str, steps: list, alerts: list, status: str = "COMPLETED"):
        """Generate experiment_YYYYMMDD_HHMMSS.json and experiment_YYYYMMDD_HHMMSS.txt."""
        timestamp_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        json_path = os.path.join(self.record_dir, f"experiment_{timestamp_str}.json")
        txt_path = os.path.join(self.record_dir, f"experiment_{timestamp_str}.txt")

        json_data = {
            "experiment_id": "EXP_001",
            "session_id": session_id,
            "start_time": timestamp_str,
            "status": status,
            "steps": steps,
            "alerts": alerts
        }

        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=2)

        with open(txt_path, "w") as f:
            f.write("EXPERIMENT REPORT\n")
            f.write("=================\n\n")
            f.write(f"Session ID: {session_id}\n")
            f.write(f"Start Time: {timestamp_str}\n")
            f.write(f"Status: {status}\n\n")

            for s in steps:
                f.write(f"STEP {s.get('step')}: {s.get('name')}\n")
                f.write(f"Status: {s.get('status')}\n")
                f.write(f"Confidence: {int(s.get('confidence', 0.0) * 100)}%\n\n")

            f.write(f"FINAL STATUS:\n{status}\n")

        return json_path, txt_path

# Global logger service instance
logger_service = LoggerService()
