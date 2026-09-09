import yaml
import time
import logging
from core.realtime.event_types import EventType, SafetyState
from core.realtime.event_bus import event_bus

logger = logging.getLogger("ASTRA-HAR.SequenceEngine")

class SequenceEngine:
    """Configurable Finite State Machine (FSM) enforcing experiment step validation."""

    def __init__(self, config_path: str = "experiments/two_box_experiment.yaml"):
        self.config_path = config_path
        self.experiment_def = {}
        self.steps = []
        self.current_step_index = 0
        self.step_start_time = time.time()
        self.load_experiment_config(config_path)

    def load_experiment_config(self, config_path: str):
        """Load experiment step protocol from YAML file."""
        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
                self.experiment_def = data.get("experiment", {})
                self.steps = data.get("steps", [])
                logger.info(f"Loaded experiment '{self.experiment_def.get('name')}' with {len(self.steps)} steps.")
        except Exception as e:
            logger.error(f"Failed to load experiment YAML: {e}")

    def get_current_step_info(self) -> dict:
        """Return dict of current step details."""
        if 0 <= self.current_step_index < len(self.steps):
            step = self.steps[self.current_step_index]
            elapsed = time.time() - self.step_start_time
            return {
                "step_number": step.get("id"),
                "total_steps": len(self.steps),
                "step_name": step.get("name"),
                "expected_object": step.get("expected_object"),
                "expected_activity": step.get("expected_activity"),
                "guidance": step.get("guidance"),
                "voice_alert": step.get("voice_alert"),
                "timeout_sec": step.get("timeout_sec", 30.0),
                "elapsed_sec": round(elapsed, 1),
                "progress_pct": min(100.0, round((elapsed / step.get("timeout_sec", 30.0)) * 100.0, 1))
            }
        return {"step_number": len(self.steps), "step_name": "Completed", "progress_pct": 100.0}

    def evaluate_observation(self, current_activity: str, active_object: str, confidence: float) -> tuple:
        """Evaluate observation against current step.

        Returns:
            (step_completed: bool, step_info: dict, alert_event: dict)
        """
        if self.current_step_index >= len(self.steps):
            return False, self.get_current_step_info(), None

        step = self.steps[self.current_step_index]
        expected_act = step.get("expected_activity")
        expected_obj = step.get("expected_object")
        thresh = step.get("confidence_threshold", 0.75)

        # Check match
        act_match = (expected_act.lower() in current_activity.lower()) or (current_activity.lower() in expected_act.lower())
        obj_match = (expected_obj == active_object) or (active_object == "")

        if act_match and confidence >= thresh:
            # Advance step
            self.current_step_index += 1
            self.step_start_time = time.time()
            new_step_info = self.get_current_step_info()

            event_bus.publish(EventType.STEP_COMPLETED, {
                "completed_step": step.get("id"),
                "name": step.get("name"),
                "next_step": new_step_info.get("step_number")
            })

            return True, new_step_info, None

        return False, self.get_current_step_info(), None

    def set_step(self, step_id: int):
        """Force set current step ID."""
        for idx, s in enumerate(self.steps):
            if s.get("id") == step_id:
                self.current_step_index = idx
                self.step_start_time = time.time()
                return True
        return False
