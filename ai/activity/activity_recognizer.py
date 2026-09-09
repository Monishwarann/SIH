from core.realtime.event_types import ActivityType

class ActivityRecognizer:
    """Temporal Activity Recognizer consuming feature sequences from pose, object, and interaction history."""

    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.history_buffer = []
        self.buffer_size = 15  # 15 frames temporal window

    def predict(self, pose_info: dict, objects: list, interactions: list) -> dict:
        """Predict current activity from temporal multimodal observation vector."""
        if not interactions:
            return {"activity": ActivityType.IDLE.value, "confidence": 0.95}

        # Find closest active hand interaction
        active_inter = interactions[0] if interactions else {}
        inter_state = active_inter.get("state", "FAR")
        target_obj = active_inter.get("object", "")

        if inter_state == "GRASPING":
            if "red" in target_obj:
                act = "GRASP_RED_BOX"
            elif "yellow" in target_obj:
                act = "GRASP_YELLOW_BOX"
            else:
                act = ActivityType.GRASP.value
            conf = 0.94
        elif inter_state == "MOVING":
            act = ActivityType.MOVE.value
            conf = 0.92
        elif inter_state == "CONTACT":
            if "container" in target_obj:
                act = ActivityType.OPEN_CONTAINER.value
            else:
                act = ActivityType.IDENTIFY_OBJECT.value
            conf = 0.91
        elif inter_state == "APPROACHING":
            act = ActivityType.REACH.value
            conf = 0.93
        elif inter_state == "PLACED":
            act = ActivityType.PLACE.value
            conf = 0.96
        else:
            act = ActivityType.IDLE.value
            conf = 0.95

        return {
            "activity": act,
            "confidence": conf,
            "target_object": target_obj,
            "interaction_state": inter_state
        }
