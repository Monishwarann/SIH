import math
import logging

logger = logging.getLogger("ASTRA-HAR.ActivityFusion")

class ActivityFusionEngine:
    """
    Fuses multi-modal observations: Hand positions + Pose Keypoints + Detected Objects
    into unified hand-object interaction states and temporal activity descriptors.
    """

    def analyze_interaction(self, hands: dict, objects: list) -> list:
        """
        Input:
          hands: {'right_hand': {'position': [x,y], ...}, ...}
          objects: [{'id': 'red_box', 'name': 'Red Box', 'bbox': [x1,y1,x2,y2], ...}]
        
        Returns:
          list of interactions sorted by proximity:
          [{'object_id': str, 'object_name': str, 'distance_px': float, 'state': 'GRASPED'|'PROXIMITY'|'FAR', 'hand': 'right_hand'}]
        """
        interactions = []

        if not hands or not objects:
            return interactions

        right_hand = hands.get("right_hand", {})
        rx, ry = right_hand.get("position", [0, 0])

        for obj in objects:
            oid = obj.get("id", "")
            oname = obj.get("name", "Object")
            bbox = obj.get("bbox", [0, 0, 0, 0])

            # Calculate centroid of object bounding box
            cx = (bbox[0] + bbox[2]) // 2
            cy = (bbox[1] + bbox[3]) // 2

            # Euclidean distance from hand to object centroid
            dist = math.sqrt((rx - cx)**2 + (ry - cy)**2)

            if dist < 45:
                state = "GRASPED"
            elif dist < 85:
                state = "CONTACT"
            elif dist < 160:
                state = "PROXIMITY"
            else:
                state = "FAR"

            interactions.append({
                "object_id": oid,
                "object_name": oname,
                "distance_px": round(dist, 1),
                "state": state,
                "hand": "right_hand",
                "object_bbox": bbox
            })

        # Sort by distance
        interactions.sort(key=lambda x: x["distance_px"])
        return interactions

fusion_engine = ActivityFusionEngine()
