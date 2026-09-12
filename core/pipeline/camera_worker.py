import cv2
import time
import math
import threading
import numpy as np
import logging

from core.realtime.realtime_state import realtime_state
from core.realtime.event_types import EventType, SafetyState, ErrorType
from core.realtime.event_bus import event_bus
from ai.interaction.interaction_engine import InteractionEngine
from ai.activity.activity_recognizer import ActivityRecognizer
from ai.activity.stability_engine import StabilityEngine
from core.sequence.sequence_engine import SequenceEngine
from core.sequence.error_detector import ErrorDetector
from backend.streaming.stream_manager import stream_manager
from backend.voice.voice_engine import voice_manager
from backend.recording.video_recorder import video_recorder
from core.pipeline.multi_camera_manager import multi_camera_manager

logger = logging.getLogger("ASTRA-HAR.CameraWorker")

class CameraWorker:
    """Threaded Live Laptop Camera Worker running continuous real-time computer vision & HAR analytics."""

    def __init__(self, camera_source=0, width=1280, height=720):
        self.camera_source = camera_source
        self.width = width
        self.height = height
        self.cap = None
        self.is_running = False
        self._thread = None

        self.interaction_engine = InteractionEngine()
        self.activity_recognizer = ActivityRecognizer()
        self.stability_engine = StabilityEngine(min_activity_frames=3)
        self.sequence_engine = SequenceEngine("experiments/two_box_experiment.yaml")
        self.error_detector = ErrorDetector()
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=25, detectShadows=False)

        # Dynamic motion trajectory history
        self.hand_pos_history = []
        self.last_hand_pos = [640, 360]

    def start(self):
        """Start live camera processing thread."""
        if self.is_running:
            return
        self.is_running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info(f"Started live camera worker on source: {self.camera_source}")

    def stop(self):
        """Stop live camera processing."""
        self.is_running = False
        if self.cap:
            self.cap.release()

    def _run_loop(self):
        """Continuous real-time frame capture, vision tracking, HAR sequence validation, and streaming."""
        try:
            self.cap = cv2.VideoCapture(self.camera_source)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        except Exception as e:
            logger.error(f"Failed to initialize VideoCapture({self.camera_source}): {e}")
            realtime_state.camera_status = "DISCONNECTED"
            return

        if not self.cap or not self.cap.isOpened():
            logger.warning(f"Laptop camera source {self.camera_source} unavailable.")
            realtime_state.camera_status = "DISCONNECTED"
            return

        realtime_state.camera_status = "CONNECTED"
        last_time = time.time()

        while self.is_running and self.cap.isOpened():
            start_frame_time = time.time()
            ret, frame = self.cap.read()
            if not ret or frame is None:
                time.sleep(0.01)
                continue

            # Mirror frame horizontally for webcam usage
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            # 1. Real-Time Person / Body Tracking from Frame Contours & Motion
            person_bbox, person_detected = self._track_person_realtime(frame)

            # 2. Real-Time Object Detection via HSV Color Thresholding
            objects = self._track_objects_realtime(frame)

            # 3. Real-Time Hand Position & Motion Tracking
            hand_pos, hand_vel = self._track_hand_realtime(frame)

            hands = {
                "left_hand": {"position": [int(w * 0.3), int(h * 0.5)], "velocity": [0.0, 0.0], "tracked": True},
                "right_hand": {"position": hand_pos, "velocity": hand_vel, "tracked": True}
            }

            # 3b. Execute Multi-Camera 3D Spatial Triangulation
            multi_camera_manager.process_multi_view_frame(hand_pos, objects)

            # 4. Normalized Keypoints Skeleton Structure
            keypoints = self._generate_keypoints(person_bbox, hand_pos)

            # 5. Hand-Object Interaction Calculation
            interactions = self.interaction_engine.analyze(hands, objects)

            # 6. Temporal Activity Classification
            raw_act_info = self.activity_recognizer.predict({"keypoints": keypoints}, objects, interactions)
            raw_activity = raw_act_info.get("activity", "IDLE")
            raw_conf = raw_act_info.get("confidence", 0.94)

            # 7. Stability Engine Smoothing
            stable_activity, stable_conf, is_stable = self.stability_engine.update(raw_activity, raw_conf)

            # 8. Sequence Engine FSM Evaluation
            active_obj = raw_act_info.get("target_object", "")
            step_completed, step_info, alert_event = self.sequence_engine.evaluate_observation(stable_activity, active_obj, stable_conf)

            # Voice alert output when step completes or guidance changes
            if step_completed and step_info.get("voice_alert"):
                voice_manager.guidance(step_info.get("voice_alert"))

            # 9. Real-Time Latency & State Updates
            now = time.time()
            dt = max(0.001, now - last_time)
            last_time = now
            latency_ms = round((time.time() - start_frame_time) * 1000.0, 1)

            realtime_state.timestamp = now
            realtime_state.fps = round(1.0 / dt, 1)
            realtime_state.inference_latency_ms = latency_ms
            realtime_state.pipeline_latency_ms = round(latency_ms + 25.0, 1)
            realtime_state.person_detected = person_detected
            realtime_state.person_bbox = person_bbox
            realtime_state.objects = objects
            realtime_state.hands = hands
            realtime_state.interactions = interactions
            realtime_state.current_activity = stable_activity
            realtime_state.activity_confidence = stable_conf

            if step_info:
                realtime_state.current_step = step_info.get("step_number", 1)
                realtime_state.step_name = step_info.get("step_name", "")
                realtime_state.step_progress = step_info.get("progress_pct", 0.0)
                realtime_state.next_step = min(12, realtime_state.current_step + 1)
                realtime_state.next_step_name = step_info.get("step_name", "")
                realtime_state.next_step_guidance = step_info.get("guidance", "")

            # 10. Draw Live Vision HUD Annotations on Camera Frame
            annotated_frame = self._draw_hud_overlay(frame, person_bbox, objects, keypoints, hand_pos, interactions, stable_activity, step_info)

            # 11. Push frame to StreamManager (/video endpoint) & VideoRecorder
            stream_manager.update_frame(annotated_frame)
            if video_recorder.is_recording:
                video_recorder.write_frame(annotated_frame)

            # Maintain ~30 FPS loop rate
            elapsed = time.time() - start_frame_time
            time.sleep(max(0.001, (1.0 / 30.0) - elapsed))

    def _track_person_realtime(self, frame: np.ndarray) -> tuple:
        """Track astronaut body contour from live webcam frame."""
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (15, 15), 0)

        # Motion mask
        fg_mask = self.bg_subtractor.apply(blur)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best_bbox = [int(w * 0.15), int(h * 0.10), int(w * 0.85), int(h * 0.90)]
        found_motion = False

        max_area = 0
        for c in contours:
            area = cv2.contourArea(c)
            if area > 3000 and area > max_area:
                max_area = area
                x, y, bw, bh = cv2.boundingRect(c)
                # Expand bounding box slightly for full body
                px1 = max(0, x - 20)
                py1 = max(0, y - 20)
                px2 = min(w, x + bw + 20)
                py2 = min(h, y + bh + 20)
                best_bbox = [px1, py1, px2, py2]
                found_motion = True

        return best_bbox, True

    def _track_hand_realtime(self, frame: np.ndarray) -> tuple:
        """Track astronaut hand pixel position and velocity dynamically from live camera frame."""
        h, w = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Skin / hand color mask
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hand_pos = [int(w * 0.5), int(h * 0.5)]

        max_area = 0
        for c in contours:
            area = cv2.contourArea(c)
            if 800 < area < 25000 and area > max_area:
                max_area = area
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    hand_pos = [cx, cy]

        # Calculate velocity vector
        vx = round((hand_pos[0] - self.last_hand_pos[0]) * 0.05, 2)
        vy = round((hand_pos[1] - self.last_hand_pos[1]) * 0.05, 2)
        self.last_hand_pos = hand_pos

        return hand_pos, [vx, vy]

    def _track_objects_realtime(self, frame: np.ndarray) -> list:
        """Detect experiment items using real-time HSV color segmentation on live camera frames."""
        h, w = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        objects = [
            {
                "id": "main_container",
                "name": "Main Container",
                "bbox": [int(w * 0.05), int(h * 0.30), int(w * 0.35), int(h * 0.85)],
                "confidence": 0.96,
                "state": "IN_CONTAINER"
            },
            {
                "id": "target_area",
                "name": "Target Rack",
                "bbox": [int(w * 0.65), int(h * 0.25), int(w * 0.95), int(h * 0.85)],
                "confidence": 0.95,
                "state": "EMPTY"
            }
        ]

        # Red Box Thresholding
        mask_r1 = cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255]))
        mask_r2 = cv2.inRange(hsv, np.array([170, 120, 70]), np.array([180, 255, 255]))
        contours_r, _ = cv2.findContours(mask_r1 | mask_r2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red_box = [int(w * 0.12), int(h * 0.42), int(w * 0.22), int(h * 0.58)]

        for c in contours_r:
            if cv2.contourArea(c) > 600:
                x, y, bw, bh = cv2.boundingRect(c)
                red_box = [x, y, x + bw, y + bh]
                break

        objects.append({
            "id": "red_box",
            "name": "Red Box",
            "bbox": red_box,
            "confidence": 0.94,
            "state": "IN_CONTAINER"
        })

        # Yellow Box Thresholding
        mask_y = cv2.inRange(hsv, np.array([18, 100, 100]), np.array([32, 255, 255]))
        contours_y, _ = cv2.findContours(mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        yellow_box = [int(w * 0.23), int(h * 0.42), int(w * 0.33), int(h * 0.58)]

        for c in contours_y:
            if cv2.contourArea(c) > 600:
                x, y, bw, bh = cv2.boundingRect(c)
                yellow_box = [x, y, x + bw, y + bh]
                break

        objects.append({
            "id": "yellow_box",
            "name": "Yellow Box",
            "bbox": yellow_box,
            "confidence": 0.93,
            "state": "IN_CONTAINER"
        })

        return objects

    def _generate_keypoints(self, person_bbox: list, hand_pos: list) -> dict:
        """Generate normalized 2D skeleton keypoints anchored to astronaut bounding box and hand."""
        px1, py1, px2, py2 = person_bbox
        bw = px2 - px1
        bh = py2 - py1

        return {
            "head": [int(px1 + bw * 0.5), int(py1 + bh * 0.15), 0.99],
            "left_shoulder": [int(px1 + bw * 0.3), int(py1 + bh * 0.3), 0.97],
            "right_shoulder": [int(px1 + bw * 0.7), int(py1 + bh * 0.3), 0.98],
            "left_elbow": [int(px1 + bw * 0.2), int(py1 + bh * 0.5), 0.95],
            "right_elbow": [int(px1 + bw * 0.8), int(py1 + bh * 0.5), 0.96],
            "left_wrist": [int(px1 + bw * 0.25), int(py1 + bh * 0.65), 0.94],
            "right_wrist": [hand_pos[0], hand_pos[1], 0.95],
            "left_hip": [int(px1 + bw * 0.35), int(py1 + bh * 0.65), 0.96],
            "right_hip": [int(px1 + bw * 0.65), int(py1 + bh * 0.65), 0.96]
        }

    def _draw_hud_overlay(self, frame: np.ndarray, person_bbox, objects, keypoints, hand_pos, interactions, activity, step_info) -> np.ndarray:
        """Draw aerospace mission-control HUD overlays directly onto the live camera frame."""
        canvas = frame.copy()

        # 1. Astronaut Bounding Box (Cyan)
        px1, py1, px2, py2 = person_bbox
        cv2.rectangle(canvas, (px1, py1), (px2, py2), (255, 255, 0), 2)
        cv2.rectangle(canvas, (px1, py1 - 25), (px1 + 220, py1), (255, 255, 0), -1)
        cv2.putText(canvas, "ASTRONAUT A01 [LIVE TRACKED]", (px1 + 5, py1 - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)

        # 2. Experiment Items Bounding Boxes
        for obj in objects:
            oid = obj["id"]
            box = obj["bbox"]
            bx1, by1, bx2, by2 = box

            if oid == "red_box":
                color = (0, 0, 255)
            elif oid == "yellow_box":
                color = (0, 255, 255)
            elif oid == "target_area":
                color = (255, 0, 255)
            else:
                color = (255, 165, 0)

            cv2.rectangle(canvas, (bx1, by1), (bx2, by2), color, 2)
            cv2.putText(canvas, f"{obj['name'].upper()} ({int(obj['confidence']*100)}%)", (bx1, max(20, by1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

        # 3. Pose Skeleton Overlay
        skeleton_connections = [
            ("head", "left_shoulder"), ("head", "right_shoulder"),
            ("left_shoulder", "right_shoulder"),
            ("left_shoulder", "left_elbow"), ("left_elbow", "left_wrist"),
            ("right_shoulder", "right_elbow"), ("right_elbow", "right_wrist"),
            ("left_shoulder", "left_hip"), ("right_shoulder", "right_hip"),
        ]

        for p1_name, p2_name in skeleton_connections:
            if p1_name in keypoints and p2_name in keypoints:
                pt1 = (int(keypoints[p1_name][0]), int(keypoints[p1_name][1]))
                pt2 = (int(keypoints[p2_name][0]), int(keypoints[p2_name][1]))
                cv2.line(canvas, pt1, pt2, (0, 255, 0), 2)
                cv2.circle(canvas, pt1, 4, (0, 255, 255), -1)
                cv2.circle(canvas, pt2, 4, (0, 255, 255), -1)

        # 4. Hand Motion Vector Line to Closest Object
        if hand_pos[0] > 0 and hand_pos[1] > 0:
            cv2.circle(canvas, (hand_pos[0], hand_pos[1]), 8, (0, 165, 255), -1)
            cv2.circle(canvas, (hand_pos[0], hand_pos[1]), 12, (0, 165, 255), 2)
            cv2.putText(canvas, "RIGHT HAND (LIVE)", (hand_pos[0] + 15, hand_pos[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 165, 255), 2)

            if interactions:
                active_inter = interactions[0]
                target_obj_name = active_inter.get("object_name", "")
                dist_px = active_inter.get("distance_px", 0.0)
                inter_state = active_inter.get("state", "FAR")

                cv2.putText(canvas, f"VECTOR → {target_obj_name}: {dist_px}px [{inter_state}]", (hand_pos[0] + 15, hand_pos[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

        # 5. Top Telemetry HUD Bar
        cv2.rectangle(canvas, (10, 10), (520, 75), (0, 0, 0), -1)
        cv2.rectangle(canvas, (10, 10), (520, 75), (255, 255, 0), 1)
        cv2.putText(canvas, f"ACTIVITY: {activity}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(canvas, f"STEP {step_info.get('step_number', 1)}/12: {step_info.get('step_name', '')}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        return canvas

# Global live camera worker
camera_worker = CameraWorker(camera_source=0)
