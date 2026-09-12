import time
import logging
from experiments.experiment_loader import experiment_loader

logger = logging.getLogger("ASTRA-HAR.SequenceValidator")

class SequenceValidator:
    """
    Finite State Machine (FSM) Engine for validating real-time human activity sequences
    against loaded space experiment protocols.
    Detects:
    1. Correct step execution & sequence progression
    2. Skipped steps
    3. Wrong order actions
    4. Step timeouts
    """

    def __init__(self, experiment_id="two_box_sorting"):
        self.protocol = experiment_loader.load_protocol(experiment_id)
        self.steps = self.protocol.get("steps", [])
        self.current_step_idx = 0
        self.step_start_time = time.time()
        self.status = "INITIALIZED"
        self.detected_sequence = []
        self.violations = []
        self.is_completed = False

    def reset(self, experiment_id=None):
        if experiment_id:
            self.protocol = experiment_loader.load_protocol(experiment_id)
            self.steps = self.protocol.get("steps", [])
        self.current_step_idx = 0
        self.step_start_time = time.time()
        self.status = "IN_PROGRESS"
        self.detected_sequence = []
        self.violations = []
        self.is_completed = False
        logger.info(f"Reset sequence engine for experiment: {self.protocol.get('name')}")

    def evaluate(self, detected_action: str, confidence: float = 0.90) -> dict:
        """
        Input: detected action string (e.g. 'PICK_OBJECT') & confidence
        Returns evaluation result dictionary:
        {
          'status': 'CORRECT' | 'SKIPPED' | 'WRONG_ORDER' | 'TIMEOUT' | 'IN_PROGRESS',
          'current_step': int,
          'expected_action': str,
          'detected_action': str,
          'alert': str,
          'voice_alert': str,
          'completed': bool
        }
        """
        if self.is_completed or not self.steps:
            return {
                "status": "COMPLETED",
                "current_step": len(self.steps),
                "total_steps": len(self.steps),
                "alert": "Experiment already completed.",
                "voice_alert": "Experiment sequence completed.",
                "completed": True
            }

        expected_step = self.steps[self.current_step_idx]
        expected_action = expected_step.get("action")
        timeout_sec = expected_step.get("timeout", 30)

        now = time.time()
        elapsed = now - self.step_start_time

        # 1. Check for Step Timeout
        if elapsed > timeout_sec:
            self.violations.append({
                "type": "TIMEOUT",
                "step": self.current_step_idx + 1,
                "expected": expected_action,
                "timestamp": now
            })
            alert_msg = f"⚠ TIMEOUT: Step {self.current_step_idx + 1} ({expected_action}) exceeded allowed time of {timeout_sec}s."
            voice_msg = f"Timeout warning. Action {expected_action} was not detected within allowed time."
            
            # Reset step timer to avoid spamming
            self.step_start_time = now
            return {
                "status": "TIMEOUT",
                "current_step": self.current_step_idx + 1,
                "expected_action": expected_action,
                "detected_action": detected_action,
                "alert": alert_msg,
                "voice_alert": voice_msg,
                "completed": False
            }

        # Ignore generic waiting or low confidence
        if detected_action in ["WAIT", "IDLE"] or confidence < 0.60:
            return {
                "status": "IN_PROGRESS",
                "current_step": self.current_step_idx + 1,
                "expected_action": expected_action,
                "detected_action": detected_action,
                "completed": False
            }

        # 2. Case: Action matches Expected Action -> CORRECT
        if detected_action == expected_action:
            self.detected_sequence.append(detected_action)
            self.current_step_idx += 1
            self.step_start_time = now

            if self.current_step_idx >= len(self.steps):
                self.is_completed = True
                return {
                    "status": "CORRECT",
                    "current_step": len(self.steps),
                    "expected_action": expected_action,
                    "detected_action": detected_action,
                    "alert": "✓ EXPERIMENT SEQUENCE COMPLETED",
                    "voice_alert": "Experiment completed successfully.",
                    "completed": True
                }

            next_step = self.steps[self.current_step_idx]
            return {
                "status": "CORRECT",
                "current_step": self.current_step_idx + 1,
                "expected_action": next_step.get("action"),
                "detected_action": detected_action,
                "alert": f"✓ Step {self.current_step_idx} Verified: {detected_action}",
                "voice_alert": expected_step.get("voice_alert", f"Step {self.current_step_idx} complete."),
                "completed": False
            }

        # 3. Case: Action matches a FUTURE step -> SKIPPED STEP
        future_indices = [
            idx for idx, s in enumerate(self.steps)
            if s.get("action") == detected_action and idx > self.current_step_idx
        ]

        if future_indices:
            skipped_step = self.steps[self.current_step_idx].get("action")
            self.violations.append({
                "type": "SKIPPED_STEP",
                "step": self.current_step_idx + 1,
                "skipped_action": skipped_step,
                "detected_action": detected_action,
                "timestamp": now
            })
            
            # Jump forward to detected step
            self.current_step_idx = future_indices[0] + 1
            self.step_start_time = now

            return {
                "status": "SKIPPED",
                "current_step": self.current_step_idx + 1,
                "expected_action": expected_action,
                "detected_action": detected_action,
                "alert": f"⚠ STEP SKIPPED: Expected {skipped_step}, but detected {detected_action}.",
                "voice_alert": f"Warning! Step {skipped_step} was skipped. Please verify protocol.",
                "completed": self.current_step_idx >= len(self.steps)
            }

        # 4. Case: Action matches a PREVIOUS step -> WRONG ORDER
        past_indices = [
            idx for idx, s in enumerate(self.steps)
            if s.get("action") == detected_action and idx < self.current_step_idx
        ]

        if past_indices:
            self.violations.append({
                "type": "WRONG_ORDER",
                "step": self.current_step_idx + 1,
                "expected": expected_action,
                "detected_action": detected_action,
                "timestamp": now
            })
            return {
                "status": "WRONG_ORDER",
                "current_step": self.current_step_idx + 1,
                "expected_action": expected_action,
                "detected_action": detected_action,
                "alert": f"⚠ WRONG SEQUENCE: Detected {detected_action}. Expected {expected_action}.",
                "voice_alert": f"Wrong sequence. Action {detected_action} performed out of order. Expected {expected_action}.",
                "completed": False
            }

        return {
            "status": "IN_PROGRESS",
            "current_step": self.current_step_idx + 1,
            "expected_action": expected_action,
            "detected_action": detected_action,
            "completed": False
        }

sequence_validator = SequenceValidator()
