import logging
from core.realtime.event_types import EventType
from core.realtime.event_bus import event_bus

logger = logging.getLogger("ASTRA-HAR.RecoveryEngine")

class RecoveryEngine:
    """Recovery Engine managing real-time recovery actions:

    WAIT, RETRY_CURRENT_STEP, REQUEST_REPEAT, ROLLBACK, PAUSE_EXPERIMENT, RESUME
    """

    def handle_error(self, error_info: dict, current_step_info: dict) -> dict:
        """Determine appropriate recovery action based on error type and severity."""
        error_type = error_info.get("type", "")

        if error_type == "STEP_SKIPPED":
            recovery_action = "REQUEST_REPEAT"
            voice_msg = f"Warning: Step skipped. Please repeat {current_step_info.get('step_name')}."
        elif error_type == "WRONG_OBJECT":
            recovery_action = "RETRY_CURRENT_STEP"
            voice_msg = f"Warning: Incorrect object. Please interact with {current_step_info.get('expected_object')}."
        elif error_type == "OUT_OF_SEQUENCE":
            recovery_action = "ROLLBACK"
            voice_msg = "Warning: Out of sequence action detected. Please return to previous step."
        elif error_type == "PERSON_LOST":
            recovery_action = "PAUSE_EXPERIMENT"
            voice_msg = "Critical: Astronaut lost from view. Experiment paused."
        elif error_type == "STEP_TIMEOUT":
            recovery_action = "WAIT"
            voice_msg = f"Step timeout warning. Please complete {current_step_info.get('step_name')}."
        else:
            recovery_action = "WAIT"
            voice_msg = "Observation uncertain. Continuing verification."

        recovery_payload = {
            "recovery_action": recovery_action,
            "voice_message": voice_msg,
            "error_type": error_type
        }

        event_bus.publish(EventType.RECOVERY_STARTED, recovery_payload)
        return recovery_payload
