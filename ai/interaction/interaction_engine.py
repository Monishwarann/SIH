import math
from core.realtime.event_types import InteractionState

class InteractionEngine:
    """Interaction Engine tracking hand-object spatial distance, overlap, velocity, and state transitions."""

    def __init__(self, contact_threshold_px: float = 40.0, near_threshold_px: float = 120.0):
        self.contact_threshold_px = contact_threshold_px
        self.near_threshold_px = near_threshold_px

    def analyze(self, hands: dict, objects: list) -> list:
        """Analyze spatial interactions between left/right hands and detected objects."""
        interactions = []

        if not hands or not objects:
            return interactions

        for hand_name, hand_info in hands.items():
            if not hand_info.get("tracked", False):
                continue

            hand_pos = hand_info.get("position", [0, 0])

            for obj in objects:
                obj_id = obj["id"]
                obj_bbox = obj["bbox"]  # [x1, y1, x2, y2]
                obj_center = [(obj_bbox[0] + obj_bbox[2]) / 2.0, (obj_bbox[1] + obj_bbox[3]) / 2.0]

                # Euclidean distance
                dist = math.hypot(hand_pos[0] - obj_center[0], hand_pos[1] - obj_center[1])

                # Hand-object overlap check
                overlap = (obj_bbox[0] <= hand_pos[0] <= obj_bbox[2]) and (obj_bbox[1] <= hand_pos[1] <= obj_bbox[3])

                # Determine interaction state
                if overlap:
                    state = InteractionState.CONTACT.value
                elif dist <= self.contact_threshold_px:
                    state = InteractionState.CONTACT.value
                elif dist <= self.near_threshold_px:
                    state = InteractionState.APPROACHING.value
                else:
                    state = InteractionState.FAR.value

                interactions.append({
                    "hand": hand_name,
                    "object": obj_id,
                    "object_name": obj.get("name", obj_id),
                    "state": state,
                    "distance_px": round(dist, 1),
                    "overlap": overlap,
                    "grasp_confidence": round(max(0.0, 1.0 - (dist / 150.0)), 2)
                })

        return interactions
