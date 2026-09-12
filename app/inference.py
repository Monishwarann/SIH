import os
import time
import collections
import logging
from ai.action_recognition import action_recognizer
from ai.object_detection import object_detector
from ai.pose_estimation import pose_estimator
from ai.hand_tracking import hand_tracker
from ai.fusion import fusion_engine
from experiments.sequence_validator import sequence_validator
import importlib.util
spec = importlib.util.spec_from_file_location("local_event_logger", os.path.join(os.path.dirname(__file__), "..", "logging", "event_logger.py"))
event_logger_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(event_logger_mod)
event_logger = event_logger_mod.event_logger
from voice.offline_tts import offline_tts

logger = logging.getLogger("ASTRA-HAR.AppInference")

class RealtimeInferencePipeline:
    """
    Complete real-time AI processing pipeline combining:
    Frame Buffer -> Action Model -> Object Model -> Pose/Hand Tracking -> Activity Fusion -> Sequence Engine -> Voice -> Log
    """

    def __init__(self, buffer_size=16):
        self.buffer_size = buffer_size
        self.frame_buffer = collections.deque(maxlen=buffer_size)
        self.session_id = f"EXP_{int(time.time())}"
        self.last_inference_time = time.time()
        self.fps = 30.0
        self.latency_ms = 45.0

    def process_frame(self, frame) -> dict:
        """
        Processes a single live camera frame through the entire multi-modal AI pipeline.
        """
        start_t = time.time()

        # 1. Rolling Frame Buffer
        self.frame_buffer.append(frame)

        # 2. Object Detection
        objects = object_detector.detect(frame)

        # 3. Hand Tracking
        hands = hand_tracker.track(frame)

        # 4. Pose Estimation
        keypoints = pose_estimator.estimate(frame)

        # 5. Activity Fusion
        interactions = fusion_engine.analyze_interaction(hands, objects)

        # 6. Action Recognition (3D CNN / MoViNet / Kinematic Classifier)
        action_res = action_recognizer.predict_from_buffer(self.frame_buffer, keypoints, interactions)
        detected_action = action_res.get("activity", "WAIT")
        confidence = action_res.get("confidence", 0.90)

        # 7. Sequence Validation FSM Engine
        seq_res = sequence_validator.evaluate(detected_action, confidence)

        # Voice & Event Logging Trigger
        if seq_res.get("status") in ["CORRECT", "SKIPPED", "WRONG_ORDER", "TIMEOUT"]:
            if seq_res.get("voice_alert"):
                offline_tts.speak(seq_res.get("voice_alert"))

            event_logger.log_event(
                session_id=self.session_id,
                event_type=seq_res.get("status"),
                action=detected_action,
                confidence=confidence,
                object_detected=action_res.get("target_object", ""),
                status=seq_res.get("status"),
                details=seq_res
            )

        # Measure FPS and Latency
        now = time.time()
        dt = max(0.001, now - self.last_inference_time)
        self.last_inference_time = now
        self.fps = round(1.0 / dt, 1)
        self.latency_ms = round((now - start_t) * 1000.0, 1)

        return {
            "timestamp": now,
            "fps": self.fps,
            "latency_ms": self.latency_ms,
            "detected_action": detected_action,
            "confidence": confidence,
            "objects": objects,
            "hands": hands,
            "keypoints": keypoints,
            "interactions": interactions,
            "sequence_result": seq_res
        }

inference_pipeline = RealtimeInferencePipeline()
