import os
import json
import time
import logging

logger = logging.getLogger("ASTRA-HAR.ReportGenerator")

class ReportGenerator:
    """
    Generates post-experiment JSON, TXT, and HTML reports summarizing execution accuracy,
    timing metrics, FPS/latency performance, and sequence validation logs.
    """

    def generate_report(self, session_id: str, experiment_name: str, duration_sec: float,
                        steps_completed: int, total_steps: int, skipped_count: int,
                        wrong_order_count: int, timeout_count: int, avg_confidence: float,
                        avg_fps: float, avg_latency_ms: float, output_dir="recordings") -> dict:

        os.makedirs(output_dir, exist_ok=True)
        final_status = "PASSED" if (steps_completed >= total_steps and skipped_count == 0 and wrong_order_count == 0) else "COMPLETED_WITH_WARNINGS"

        report_data = {
            "session_id": session_id,
            "experiment_name": experiment_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": round(duration_sec, 1),
            "final_status": final_status,
            "metrics": {
                "total_steps": total_steps,
                "completed_steps": steps_completed,
                "skipped_steps": skipped_count,
                "wrong_order_actions": wrong_order_count,
                "timeouts": timeout_count,
                "average_confidence": round(avg_confidence, 4),
                "average_fps": round(avg_fps, 1),
                "average_latency_ms": round(avg_latency_ms, 1)
            }
        }

        # 1. Save JSON Report
        json_path = os.path.join(output_dir, f"{session_id}_report.json")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to write JSON report: {e}")

        # 2. Save Human-Readable Text Report
        txt_path = os.path.join(output_dir, f"{session_id}_report.txt")
        txt_content = f"""==================================================
        ASTRA-HAR EXPERIMENT VALIDATION REPORT
==================================================
Session ID     : {session_id}
Experiment     : {experiment_name}
Timestamp      : {time.strftime('%Y-%m-%d %H:%M:%S')}
Duration       : {round(duration_sec, 1)} seconds
Final Status   : {final_status}

PERFORMANCE & ACCURACY SUMMARY:
--------------------------------------------------
Total Steps        : {total_steps}
Completed Steps    : {steps_completed}
Skipped Steps      : {skipped_count}
Wrong Order Count  : {wrong_order_count}
Timeouts           : {timeout_count}
Average Confidence : {round(avg_confidence * 100, 1)}%
Average FPS        : {round(avg_fps, 1)}
Average Latency    : {round(avg_latency_ms, 1)} ms
==================================================
"""
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(txt_content)
        except Exception as e:
            logger.error(f"Failed to write TXT report: {e}")

        return report_data

report_generator = ReportGenerator()
