import cv2
import numpy as np

class HUDDashboard:
    """
    Renders real-time scientific/space-mission HUD overlays directly onto OpenCV frames.
    """

    def render(self, frame: np.ndarray, res: dict) -> np.ndarray:
        if frame is None:
            return frame

        canvas = frame.copy()
        h, w = canvas.shape[:2]

        fps = res.get("fps", 30.0)
        latency = res.get("latency_ms", 45.0)
        action = res.get("detected_action", "APPROACH_OBJECT")
        conf = res.get("confidence", 0.94)
        objects = res.get("objects", [])
        keypoints = res.get("keypoints", {})
        seq_res = res.get("sequence_result", {})

        # 1. Bounding Boxes & Skeleton
        for obj in objects:
            box = obj.get("bbox", [0, 0, 0, 0])
            name = obj.get("name", "Object")
            c_val = int(obj.get("confidence", 0.9) * 100)
            cv2.rectangle(canvas, (box[0], box[1]), (box[2], box[3]), (0, 255, 255), 2)
            cv2.putText(canvas, f"{name.upper()} ({c_val}%)", (box[0], max(20, box[1] - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 2)

        # Pose skeleton lines
        if keypoints:
            connections = [("head", "left_shoulder"), ("head", "right_shoulder"),
                           ("left_shoulder", "right_shoulder"), ("left_shoulder", "left_elbow"),
                           ("right_shoulder", "right_elbow"), ("left_elbow", "left_wrist"),
                           ("right_elbow", "right_wrist")]
            for p1, p2 in connections:
                if p1 in keypoints and p2 in keypoints:
                    pt1 = (keypoints[p1][0], keypoints[p1][1])
                    pt2 = (keypoints[p2][0], keypoints[p2][1])
                    cv2.line(canvas, pt1, pt2, (0, 255, 0), 2)
                    cv2.circle(canvas, pt1, 4, (0, 255, 255), -1)

        # 2. Top-Left HUD Overlay Box
        cv2.rectangle(canvas, (10, 10), (450, 130), (15, 23, 42), -1)
        cv2.rectangle(canvas, (10, 10), (450, 130), (0, 255, 255), 1)

        cv2.putText(canvas, "ASTRA-HAR :: BAS AI EXPERIMENT MONITOR", (20, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        cv2.putText(canvas, f"FPS: {fps} | Latency: {latency} ms", (20, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        cv2.putText(canvas, f"ACTIVITY : {action}", (20, 82),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
        cv2.putText(canvas, f"CONFIDENCE : {round(conf*100, 1)}%", (20, 108),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

        # 3. Top-Right Sequence HUD
        cv2.rectangle(canvas, (w - 360, 10), (w - 10, 130), (15, 23, 42), -1)
        cv2.rectangle(canvas, (w - 360, 10), (w - 10, 130), (255, 0, 255), 1)
        step_num = seq_res.get("current_step", 1)
        status_txt = seq_res.get("status", "IN_PROGRESS")
        alert_txt = seq_res.get("alert", f"Step {step_num} Active")

        cv2.putText(canvas, f"SEQUENCE STEP: {step_num} / 5", (w - 345, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(canvas, f"STATUS: {status_txt}", (w - 345, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        cv2.putText(canvas, f"{alert_txt[:35]}", (w - 345, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # 4. Bottom System Status Bar
        cv2.rectangle(canvas, (10, h - 35), (w - 10, h - 10), (15, 23, 42), -1)
        cv2.putText(canvas, "SYSTEM STATUS :: CAMERA [●]  AI [●]  OBJECT [●]  POSE [●]  VOICE [●]  OFFLINE EDGE",
                    (20, h - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        return canvas

dashboard_hud = HUDDashboard()
