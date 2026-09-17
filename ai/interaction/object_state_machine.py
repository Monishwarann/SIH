import time
import logging

logger = logging.getLogger("ASTRA-HAR.ObjectStateMachine")

class ObjectStateMachine:
    """
    Advanced Object State Machine monitoring individual BAS experiment payload items:
    IN_CONTAINER -> DETECTED -> APPROACHED -> CONTACTED -> GRASPED -> MOVING -> TARGET_ZONE -> RELEASED -> PLACED
    
    Includes transition validation, anomaly detection, state dwell time analysis, and audit logging.
    """

    VALID_TRANSITIONS = {
        "IN_CONTAINER": ["DETECTED", "APPROACHED", "CONTACTED", "GRASPED"],
        "DETECTED": ["APPROACHED", "CONTACTED", "IN_CONTAINER", "GRASPED"],
        "APPROACHED": ["CONTACTED", "GRASPED", "DETECTED", "FAR", "IN_CONTAINER"],
        "CONTACTED": ["GRASPED", "MOVING", "APPROACHED", "RELEASED"],
        "GRASPED": ["MOVING", "TARGET_ZONE", "RELEASED", "CONTACTED"],
        "MOVING": ["TARGET_ZONE", "PLACED", "GRASPED", "RELEASED"],
        "TARGET_ZONE": ["RELEASED", "PLACED", "MOVING"],
        "RELEASED": ["PLACED", "IN_CONTAINER", "DETECTED", "TARGET_ZONE"],
        "PLACED": ["APPROACHED", "CONTACTED", "TARGET_ZONE", "IN_CONTAINER"]
    }

    def __init__(self):
        self.object_states = {}       # obj_id -> current_state
        self.state_entry_times = {}   # obj_id -> timestamp
        self.transition_history = []  # List of audit transition records

    def update_state(self, obj_id: str, new_state: str) -> bool:
        """
        Update object state and validate state transition.
        Returns True if transition is valid, False if an anomaly / out-of-sequence jump is detected.
        """
        now = time.time()
        current_state = self.object_states.get(obj_id, "IN_CONTAINER")

        if current_state == new_state:
            return True

        valid_next = self.VALID_TRANSITIONS.get(current_state, [])
        is_valid = new_state in valid_next

        # Dwell time in previous state
        prev_entry = self.state_entry_times.get(obj_id, now)
        dwell_sec = round(now - prev_entry, 2)

        record = {
            "object_id": obj_id,
            "from_state": current_state,
            "to_state": new_state,
            "valid": is_valid,
            "dwell_sec": dwell_sec,
            "timestamp": now
        }
        self.transition_history.append(record)

        self.object_states[obj_id] = new_state
        self.state_entry_times[obj_id] = now

        if is_valid:
            logger.info(f"Object '{obj_id}' state transition: {current_state} -> {new_state} (Dwell: {dwell_sec}s)")
        else:
            logger.warning(f"State transition anomaly for '{obj_id}': {current_state} -> {new_state} (Out-of-order execution)")

        return is_valid

    def get_state(self, obj_id: str) -> str:
        """Get current state for a given payload object."""
        return self.object_states.get(obj_id, "IN_CONTAINER")

    def get_dwell_time(self, obj_id: str) -> float:
        """Get duration in seconds the object has spent in its current state."""
        entry = self.state_entry_times.get(obj_id, time.time())
        return round(time.time() - entry, 2)

    def get_all_states(self) -> dict:
        """Return snapshot of all tracked object states and dwell times."""
        now = time.time()
        return {
            obj_id: {
                "state": state,
                "dwell_sec": round(now - self.state_entry_times.get(obj_id, now), 2)
            }
            for obj_id, state in self.object_states.items()
        }

    def get_audit_trail(self, obj_id: str = None) -> list:
        """Return timestamped transition audit log."""
        if obj_id:
            return [t for t in self.transition_history if t["object_id"] == obj_id]
        return self.transition_history

# Global object state machine singleton
object_state_machine = ObjectStateMachine()
