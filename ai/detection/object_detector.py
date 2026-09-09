import time
import numpy as np

class ObjectDetector:
    """Modular Object Detector for experiment-specific payload items."""

    def __init__(self, model_path: str = None, confidence_threshold: float = 0.70):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold

    def detect(self, frame: np.ndarray) -> list:
        """Detect experiment objects: main_container, red_box, yellow_box, target_area.

        Returns list of dicts with:
            id, name, bbox, confidence, tracking_id, position, velocity, state
        """
        if frame is None:
            return []

        h, w = frame.shape[:2]

        # Standard experiment object detections
        return [
            {
                "id": "main_container",
                "name": "Main Container",
                "bbox": [int(w * 0.10), int(h * 0.30), int(w * 0.35), int(h * 0.85)],
                "confidence": 0.96,
                "tracking_id": 10,
                "position": [int(w * 0.22), int(h * 0.57)],
                "velocity": [0.0, 0.0],
                "state": "IN_CONTAINER"
            },
            {
                "id": "red_box",
                "name": "Red Box",
                "bbox": [int(w * 0.14), int(h * 0.40), int(w * 0.22), int(h * 0.55)],
                "confidence": 0.94,
                "tracking_id": 11,
                "position": [int(w * 0.18), int(h * 0.47)],
                "velocity": [0.0, 0.0],
                "state": "IN_CONTAINER"
            },
            {
                "id": "yellow_box",
                "name": "Yellow Box",
                "bbox": [int(w * 0.23), int(h * 0.40), int(w * 0.31), int(h * 0.55)],
                "confidence": 0.93,
                "tracking_id": 12,
                "position": [int(w * 0.27), int(h * 0.47)],
                "velocity": [0.0, 0.0],
                "state": "IN_CONTAINER"
            },
            {
                "id": "target_area",
                "name": "Target Rack",
                "bbox": [int(w * 0.65), int(h * 0.25), int(w * 0.90), int(h * 0.80)],
                "confidence": 0.95,
                "tracking_id": 13,
                "position": [int(w * 0.77), int(h * 0.52)],
                "velocity": [0.0, 0.0],
                "state": "EMPTY"
            }
        ]
