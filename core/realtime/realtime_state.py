import time
import os

class RealtimeState:
    """Centralized single source of truth for ASTRA-HAR (ISRO PS-26174) matching Section 2 & 45 contract."""

    def __init__(self):
        self.session_id = f"EXP-{time.strftime('%Y%m%d')}-001"
        self.experiment_id = "two_box_sorting"
        self.experiment_name = "Two-Box Sorting Experiment"
        self.start_time = time.time()
        self.frame_id = 0
        self.sequence_counter = 0

        # System health
        self.status = "ONLINE"
        self.mode = "LIVE_AI"
        self.cpu_percent = 42.0
        self.ram_percent = 58.0
        self.gpu_percent = 67.0
        self.temperature_c = 58.4

        # Camera telemetry
        self.camera_connected = True
        self.camera_status = "CONNECTED"
        self.model_status = "LIVE"
        self.fps = 29.7
        self.resolution = "1280x720"
        self.brightness = 0.72
        self.blur_score = 0.08
        self.dropped_frames = 0

        # Astronaut perception
        self.astronaut_detected = True
        self.astronaut_track_id = 1
        self.astronaut_confidence = 0.97
        self.astronaut_position = {"x": 0.48, "y": 0.52}
        self.person_bbox = [180, 100, 580, 680]

        # Activity recognition
        self.current_activity = "OPEN_CONTAINER"
        self.activity_confidence = 0.94
        self.activity_stable = True
        self.activity_duration_ms = 1250

        # Experiment sequence FSM
        self.experiment_status = "RUNNING"
        self.current_step = 1
        self.total_steps = 12
        self.step_name = "Observe Payload Container"
        self.progress_pct = 8.3
        self.expected_action = "OPEN_CONTAINER"
        self.sequence_valid = True
        self.safety_state = "CONFIRMED"

        # Objects & Hand Interactions
        self.objects = [
            {
                "id": "main_container",
                "class": "MAIN_CONTAINER",
                "name": "Main Container",
                "confidence": 0.96,
                "bbox": [120, 240, 420, 640],
                "center": {"x": 0.22, "y": 0.57},
                "track_id": 10,
                "velocity": {"vx": 0.0, "vy": 0.0},
                "state": "IN_CONTAINER",
                "last_seen": time.time()
            },
            {
                "id": "red_box",
                "class": "RED_BOX",
                "name": "Red Box",
                "confidence": 0.94,
                "bbox": [160, 320, 260, 420],
                "center": {"x": 0.18, "y": 0.47},
                "track_id": 11,
                "velocity": {"vx": 0.0, "vy": 0.0},
                "state": "IN_CONTAINER",
                "last_seen": time.time()
            },
            {
                "id": "yellow_box",
                "class": "YELLOW_BOX",
                "name": "Yellow Box",
                "confidence": 0.93,
                "bbox": [280, 320, 380, 420],
                "center": {"x": 0.27, "y": 0.47},
                "track_id": 12,
                "velocity": {"vx": 0.0, "vy": 0.0},
                "state": "IN_CONTAINER",
                "last_seen": time.time()
            },
            {
                "id": "target_area",
                "class": "TARGET_RACK",
                "name": "Target Rack",
                "confidence": 0.95,
                "bbox": [750, 200, 1050, 600],
                "center": {"x": 0.77, "y": 0.52},
                "track_id": 13,
                "velocity": {"vx": 0.0, "vy": 0.0},
                "state": "EMPTY",
                "last_seen": time.time()
            }
        ]

        self.hands = {
            "left_hand": {"position": [380, 360], "velocity": [0.0, 0.0], "tracked": True},
            "right_hand": {"position": [450, 420], "velocity": [0.02, -0.01], "tracked": True}
        }

        self.interactions = [
            {
                "hand": "RIGHT",
                "object": "main_container",
                "object_name": "Main Container",
                "state": "APPROACHING",
                "contact": True,
                "grasp_probability": 0.94,
                "distance_px": 38.0,
                "duration_ms": 840
            }
        ]

        # Next Step Intelligence
        self.next_step_id = 2
        self.next_step_description = "Access the container access latch"
        self.next_step_name = "Access Container"
        self.next_step_guidance = "Open the main container access latch."
        self.next_step_confidence = 0.92

        # Active Alerts
        self.alerts = []
        self.active_alert = None
        self.recovery_action = None

        # Performance Latency Metrics
        self.inference_ms = 34
        self.tracking_ms = 7
        self.sequence_ms = 2
        self.total_latency_ms = 43
        self.latency_p50 = 44.0
        self.latency_p95 = 67.0
        self.latency_p99 = 91.0
        self.mission_health_score = 96

        # Multi-Camera 3D Spatial Fusion State
        self.multi_camera_state = {
            "fused_hand_3d": [0.0, 0.0, 1.2],
            "fused_confidence": 0.95,
            "active_cameras": 3,
            "camera_statuses": [
                {"camera_id": "cam_1", "name": "Primary Workstation", "status": "ONLINE", "coverage_angle_deg": 75.0, "position_3d": [0.0, 0.0, 1.5], "occlusion_level": "LOW"},
                {"camera_id": "cam_2", "name": "Overhead Payload View", "status": "SIMULATED", "coverage_angle_deg": 75.0, "position_3d": [0.0, 1.2, 2.0], "occlusion_level": "LOW"},
                {"camera_id": "cam_3", "name": "Side Angle View", "status": "SIMULATED", "coverage_angle_deg": 75.0, "position_3d": [1.5, 0.5, 1.2], "occlusion_level": "LOW"}
            ],
            "fused_objects_3d": [
                {"name": "Main Container", "position_3d": [-0.3, -0.1, 1.0], "confidence": 0.96, "occluded": False},
                {"name": "Red Box", "position_3d": [-0.2, 0.1, 1.15], "confidence": 0.94, "occluded": False},
                {"name": "Yellow Box", "position_3d": [0.2, 0.1, 1.15], "confidence": 0.93, "occluded": False}
            ],
            "spatial_coverage_score": 0.98
        }

    def to_dict(self):
        """Serialize complete state dictionary for WebSocket & REST API schema."""
        self.frame_id += 1
        self.sequence_counter += 1
        now = time.time()

        return {
            "schema_version": "1.0",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.", time.gmtime(now)) + f"{int((now % 1) * 1000):03d}Z",
            "unix_timestamp": round(now, 3),
            "session_id": self.session_id,
            "frame_id": self.frame_id,
            "sequence": self.sequence_counter,

            "system": {
                "status": self.status,
                "mode": self.mode,
                "uptime": int(now - self.start_time),
                "cpu_percent": round(self.cpu_percent, 1),
                "ram_percent": round(self.ram_percent, 1),
                "gpu_percent": round(self.gpu_percent, 1),
                "temperature": round(self.temperature_c, 1)
            },

            "camera": {
                "connected": self.camera_connected,
                "fps": round(self.fps, 1),
                "resolution": self.resolution,
                "brightness": round(self.brightness, 2),
                "blur_score": round(self.blur_score, 2),
                "dropped_frames": self.dropped_frames
            },

            "astronaut": {
                "detected": self.astronaut_detected,
                "track_id": self.astronaut_track_id,
                "confidence": round(self.astronaut_confidence, 2),
                "position": self.astronaut_position,
                "bbox": self.person_bbox
            },

            "activity": {
                "current": self.current_activity,
                "confidence": round(self.activity_confidence, 2),
                "stable": self.activity_stable,
                "duration_ms": self.activity_duration_ms
            },

            "objects": self.objects,
            "hands": self.hands,
            "interactions": self.interactions,

            "experiment": {
                "status": self.experiment_status,
                "current_step": self.current_step,
                "total_steps": self.total_steps,
                "step_name": self.step_name,
                "progress": round(self.progress_pct, 1),
                "expected_action": self.expected_action
            },

            "validation": {
                "status": self.safety_state,
                "sequence_valid": self.sequence_valid
            },

            "next_step": {
                "id": self.next_step_id,
                "name": self.next_step_name,
                "description": self.next_step_description,
                "guidance": self.next_step_guidance,
                "confidence": round(self.next_step_confidence, 2)
            },

            "alerts": self.alerts,
            "active_alert": self.active_alert,
            "recovery_action": self.recovery_action,

            "performance": {
                "inference_ms": self.inference_ms,
                "tracking_ms": self.tracking_ms,
                "sequence_ms": self.sequence_ms,
                "total_latency_ms": self.total_latency_ms,
                "p50_ms": self.latency_p50,
                "p95_ms": self.latency_p95,
                "p99_ms": self.latency_p99,
                "fps": round(self.fps, 1)
            },

            "camera_status": self.camera_status,
            "model_status": self.model_status,
            "mission_health_score": self.mission_health_score,
            "multi_camera": self.multi_camera_state
        }

# Global singleton state
realtime_state = RealtimeState()
