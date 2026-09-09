import time
from core.realtime.event_types import ErrorType, SafetyState

class ErrorDetector:
    """Real-time Error Detector identifying sequence anomalies:

    STEP_SKIPPED, OUT_OF_SEQUENCE, WRONG_OBJECT, WRONG_ACTION, STEP_TIMEOUT, LOW_CONFIDENCE, PERSON_LOST.
    """

    def check_errors(self, current_step_info: dict, observed_activity: str, observed_object: str, confidence: float, person_detected: bool) -> dict:
        """Evaluate observation against current step and raise anomaly alert if present."""

        if not person_detected:
            return {
                "has_error": True,
                "type": ErrorType.PERSON_LOST.value,
                "severity": "CRITICAL",
                "message": "Astronaut lost from camera field of view.",
                "safety_state": SafetyState.ERROR.value
            }

        elapsed = current_step_info.get("elapsed_sec", 0.0)
        timeout = current_step_info.get("timeout_sec", 30.0)
        expected_obj = current_step_info.get("expected_object", "")

        # Check step timeout
        if elapsed > timeout:
            return {
                "has_error": True,
                "type": ErrorType.STEP_TIMEOUT.value,
                "severity": "WARNING",
                "message": f"Step '{current_step_info.get('step_name')}' exceeded timeout limit ({int(timeout)}s).",
                "safety_state": SafetyState.UNCERTAIN.value
            }

        # Check low confidence
        if 0.0 < confidence < 0.65:
            return {
                "has_error": True,
                "type": ErrorType.LOW_CONFIDENCE.value,
                "severity": "WARNING",
                "message": f"Low AI confidence ({int(confidence * 100)}%). Verifying observation...",
                "safety_state": SafetyState.UNCERTAIN.value
            }

        # Check wrong object
        if observed_object and expected_obj and observed_object != expected_obj and observed_object not in ["main_container", "target_area"]:
            return {
                "has_error": True,
                "type": ErrorType.WRONG_OBJECT.value,
                "severity": "WARNING",
                "message": f"Expected '{expected_obj}', but detected interaction with '{observed_object}'.",
                "safety_state": SafetyState.ERROR.value
            }

        return {"has_error": False, "safety_state": SafetyState.CONFIRMED.value}
