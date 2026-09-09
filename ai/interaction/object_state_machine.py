import logging

logger = logging.getLogger("ASTRA-HAR.ObjectStateMachine")

class ObjectStateMachine:
    """Object state machine monitoring individual experiment items:

    IN_CONTAINER -> DETECTED -> APPROACHED -> CONTACTED -> GRASPED -> MOVING -> TARGET_ZONE -> RELEASED -> PLACED
    """

    VALID_TRANSITIONS = {
        "IN_CONTAINER": ["DETECTED", "APPROACHED", "CONTACTED"],
        "DETECTED": ["APPROACHED", "CONTACTED", "IN_CONTAINER"],
        "APPROACHED": ["CONTACTED", "DETECTED", "FAR"],
        "CONTACTED": ["GRASPED", "APPROACHED", "RELEASED"],
        "GRASPED": ["MOVING", "RELEASED", "CONTACTED"],
        "MOVING": ["TARGET_ZONE", "GRASPED", "RELEASED"],
        "TARGET_ZONE": ["RELEASED", "PLACED", "MOVING"],
        "RELEASED": ["PLACED", "IN_CONTAINER", "DETECTED"],
        "PLACED": ["APPROACHED", "CONTACTED", "TARGET_ZONE"]
    }

    def __init__(self):
        self.object_states = {}

    def update_state(self, obj_id: str, new_state: str) -> bool:
        """Update object state and validate state transition."""
        current_state = self.object_states.get(obj_id, "IN_CONTAINER")

        if current_state == new_state:
            return True

        valid_next = self.VALID_TRANSITIONS.get(current_state, [])
        if new_state in valid_next:
            self.object_states[obj_id] = new_state
            logger.info(f"Object '{obj_id}' transitioned: {current_state} -> {new_state}")
            return True
        else:
            logger.warning(f"Invalid transition for '{obj_id}': {current_state} -> {new_state}")
            self.object_states[obj_id] = new_state
            return False

    def get_state(self, obj_id: str) -> str:
        return self.object_states.get(obj_id, "IN_CONTAINER")
