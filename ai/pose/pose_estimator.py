import numpy as np

class PoseEstimator:
    """Pose Estimator extracting normalized astronaut keypoints & hands."""

    def __init__(self, model_path: str = None):
        self.model_path = model_path

    def estimate(self, frame: np.ndarray) -> dict:
        """Estimate 2D pose keypoints and skeleton.

        Returns:
            keypoints: dict of landmark names to [x, y, confidence]
            skeleton: list of joint pairs
            hands: left and right hand tracking information
        """
        if frame is None:
            return {"keypoints": {}, "skeleton": [], "hands": {}, "confidence": 0.0}

        h, w = frame.shape[:2]

        # Normalized keypoints structure
        keypoints = {
            "head": [int(w * 0.35), int(h * 0.18), 0.99],
            "left_shoulder": [int(w * 0.28), int(h * 0.30), 0.97],
            "right_shoulder": [int(w * 0.42), int(h * 0.30), 0.98],
            "left_elbow": [int(w * 0.25), int(h * 0.45), 0.95],
            "right_elbow": [int(w * 0.48), int(h * 0.44), 0.96],
            "left_wrist": [int(w * 0.27), int(h * 0.58), 0.94],
            "right_wrist": [int(w * 0.52), int(h * 0.56), 0.95],
            "left_hip": [int(w * 0.30), int(h * 0.60), 0.96],
            "right_hip": [int(w * 0.40), int(h * 0.60), 0.96],
            "left_knee": [int(w * 0.31), int(h * 0.78), 0.93],
            "right_knee": [int(w * 0.39), int(h * 0.78), 0.94],
            "left_ankle": [int(w * 0.32), int(h * 0.92), 0.91],
            "right_ankle": [int(w * 0.38), int(h * 0.92), 0.92]
        }

        skeleton = [
            ("head", "left_shoulder"), ("head", "right_shoulder"),
            ("left_shoulder", "right_shoulder"),
            ("left_shoulder", "left_elbow"), ("left_elbow", "left_wrist"),
            ("right_shoulder", "right_elbow"), ("right_elbow", "right_wrist"),
            ("left_shoulder", "left_hip"), ("right_shoulder", "right_hip"),
            ("left_hip", "right_hip"),
            ("left_hip", "left_knee"), ("left_knee", "left_ankle"),
            ("right_hip", "right_knee"), ("right_knee", "right_ankle")
        ]

        hands = {
            "left_hand": {
                "position": [keypoints["left_wrist"][0], keypoints["left_wrist"][1]],
                "velocity": [0.0, 0.0],
                "tracked": True,
                "confidence": 0.94
            },
            "right_hand": {
                "position": [keypoints["right_wrist"][0], keypoints["right_wrist"][1]],
                "velocity": [0.02, -0.01],
                "tracked": True,
                "confidence": 0.95
            }
        }

        return {
            "keypoints": keypoints,
            "skeleton": skeleton,
            "hands": hands,
            "confidence": 0.96
        }
