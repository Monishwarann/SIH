import math
import time
import logging
from core.realtime.event_types import InteractionState

logger = logging.getLogger("ASTRA-HAR.InteractionEngine")

class InteractionEngine:
    """
    Advanced Multimodal Interaction Engine tracking spatial distance vectors,
    hand-object 2D/3D bounding box overlaps, relative velocity, grasp probability,
    and bimanual payload manipulation.
    """

    def __init__(self, contact_threshold_px: float = 45.0, near_threshold_px: float = 140.0):
        self.contact_threshold_px = contact_threshold_px
        self.near_threshold_px = near_threshold_px
        self.interaction_history = {}  # Tracks (hand, obj_id) -> last_dist, last_time

    def analyze(self, hands: dict, objects: list) -> list:
        """
        Analyze spatial interactions between tracked hands and detected payload items.
        Returns ranked list of interaction dicts sorted by grasp confidence and proximity.
        """
        interactions = []

        if not hands or not objects:
            return interactions

        now = time.time()

        for hand_name, hand_info in hands.items():
            if not hand_info or not hand_info.get("tracked", False):
                continue

            hand_pos = hand_info.get("position", [0, 0])
            hand_vel = hand_info.get("velocity", [0.0, 0.0])
            hand_pos_3d = hand_info.get("position_3d", None)

            for obj in objects:
                obj_id = obj.get("id", "unknown")
                obj_name = obj.get("name", obj_id)
                obj_bbox = obj.get("bbox", [0, 0, 100, 100])  # [x1, y1, x2, y2]
                obj_center = [(obj_bbox[0] + obj_bbox[2]) / 2.0, (obj_bbox[1] + obj_bbox[3]) / 2.0]
                obj_vel = obj.get("velocity", {"vx": 0.0, "vy": 0.0})

                # 1. 2D Euclidean Distance Calculation
                dist_2d = math.hypot(hand_pos[0] - obj_center[0], hand_pos[1] - obj_center[1])

                # 2. 3D Spatial Distance Estimation (if available)
                dist_3d = None
                obj_3d = obj.get("position_3d", None)
                if hand_pos_3d and obj_3d:
                    dist_3d = math.sqrt(
                        (hand_pos_3d[0] - obj_3d[0])**2 +
                        (hand_pos_3d[1] - obj_3d[1])**2 +
                        (hand_pos_3d[2] - obj_3d[2])**2
                    )

                # 3. Bounding Box Overlap & Containment Check
                overlap = (obj_bbox[0] <= hand_pos[0] <= obj_bbox[2]) and (obj_bbox[1] <= hand_pos[1] <= obj_bbox[3])

                # 4. Relative Approach / Departure Velocity (px/s)
                hist_key = (hand_name, obj_id)
                relative_vel = 0.0
                dwell_duration_ms = 0

                if hist_key in self.interaction_history:
                    prev_dist, prev_time = self.interaction_history[hist_key]
                    dt = max(0.001, now - prev_time)
                    relative_vel = round((dist_2d - prev_dist) / dt, 1)  # Negative = approaching, Positive = departing
                    dwell_duration_ms = int((now - prev_time) * 1000)

                self.interaction_history[hist_key] = (dist_2d, now)

                # 5. Physics-Based Grasp Confidence Rating
                hand_speed = math.hypot(hand_vel[0], hand_vel[1])
                proximity_score = max(0.0, 1.0 - (dist_2d / 180.0))
                speed_penalty = min(0.3, hand_speed * 0.01)
                overlap_bonus = 0.25 if overlap else 0.0

                grasp_confidence = min(0.99, max(0.05, proximity_score + overlap_bonus - speed_penalty))

                # 6. Interaction State Machine Classification
                if overlap or dist_2d <= self.contact_threshold_px:
                    if hand_speed > 15.0 or abs(obj_vel.get("vx", 0)) > 10.0:
                        state = "GRASPING"
                    else:
                        state = InteractionState.CONTACT.value
                elif dist_2d <= self.near_threshold_px:
                    if relative_vel < -5.0:
                        state = InteractionState.APPROACHING.value
                    else:
                        state = "PROXIMITY"
                else:
                    state = InteractionState.FAR.value

                interactions.append({
                    "hand": hand_name,
                    "object": obj_id,
                    "object_name": obj_name,
                    "state": state,
                    "distance_px": round(dist_2d, 1),
                    "distance_3d_m": round(dist_3d, 3) if dist_3d is not None else None,
                    "overlap": overlap,
                    "relative_velocity_px_s": relative_vel,
                    "grasp_probability": round(grasp_confidence, 2),
                    "grasp_confidence": round(grasp_confidence, 2),
                    "duration_ms": dwell_duration_ms,
                    "timestamp": now
                })

        # Rank interactions primarily by grasp probability and proximity distance
        interactions.sort(key=lambda x: (x["grasp_probability"], -x["distance_px"]), reverse=True)
        return interactions

# Global interaction engine singleton
interaction_engine = InteractionEngine()
