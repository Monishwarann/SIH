import time
import math
import random
import logging
from core.realtime.realtime_state import realtime_state
from core.realtime.event_types import EventType, SafetyState, ErrorType
from core.realtime.event_bus import event_bus

logger = logging.getLogger("ASTRA-HAR.ScenarioEngine")

class ScenarioEngine:
    """Simulates realistic space experiment sequences and failure scenarios for demonstration & testing."""

    SCENARIOS = [
        "normal",
        "skip",
        "wrong-object",
        "out-of-sequence",
        "timeout",
        "low-confidence",
        "recovery",
        "camera-loss",
        "model-failure",
        "websocket-loss"
    ]

    def __init__(self, scenario_name: str = "normal"):
        self.scenario_name = scenario_name if scenario_name in self.SCENARIOS else "normal"
        self.step_timer = time.time()
        self.tick_count = 0
        self.is_running = True
        logger.info(f"Initialized ScenarioEngine with scenario: '{self.scenario_name}'")

    def tick(self) -> dict:
        """Advance one simulation tick (~30 Hz) and update RealtimeState."""
        self.tick_count += 1
        elapsed = time.time() - self.step_timer

        # Base simulated astronaut pose animation
        t = self.tick_count * 0.1
        hand_x = int(450 + 100 * math.sin(t))
        hand_y = int(420 + 40 * math.cos(t))

        realtime_state.timestamp = time.time()
        realtime_state.hands["right_hand"]["position"] = [hand_x, hand_y]
        realtime_state.hands["right_hand"]["velocity"] = [round(math.cos(t) * 0.1, 2), round(math.sin(t) * 0.1, 2)]

        # Update telemetry & metrics
        realtime_state.fps = 28.0 + random.uniform(-1.0, 1.5)
        realtime_state.inference_latency_ms = 32.0 + random.uniform(-2.0, 4.0)
        realtime_state.pipeline_latency_ms = 64.0 + random.uniform(-4.0, 6.0)
        realtime_state.cpu_usage = 41.0 + random.uniform(-3.0, 5.0)
        realtime_state.ram_usage_gb = 3.4
        realtime_state.gpu_usage = 56.0 + random.uniform(-4.0, 8.0)
        realtime_state.vram_usage_gb = 3.2

        # Handle specific scenario logic
        if self.scenario_name == "camera-loss" and self.tick_count > 100:
            realtime_state.person_detected = False
            realtime_state.camera_status = "DISCONNECTED"
            realtime_state.safety_state = SafetyState.ERROR.value
            realtime_state.active_alert = {
                "type": ErrorType.PERSON_LOST.value,
                "severity": "CRITICAL",
                "message": "CRITICAL: Astronaut lost from camera field of view."
            }
            return realtime_state.to_dict()

        if self.scenario_name == "model-failure" and self.tick_count > 100:
            realtime_state.model_status = "ERROR"
            realtime_state.safety_state = SafetyState.ERROR.value
            realtime_state.active_alert = {
                "type": ErrorType.MODEL_FAILURE.value,
                "severity": "CRITICAL",
                "message": "CRITICAL: AI Model inference failure."
            }
            return realtime_state.to_dict()

        # Step progression logic for scenario simulation
        step = realtime_state.current_step

        if self.scenario_name == "skip" and step == 5 and elapsed > 3.0:
            # Simulate skipping from step 5 directly to step 7
            realtime_state.current_step = 7
            realtime_state.step_name = "Place Red Box"
            realtime_state.active_alert = {
                "type": ErrorType.STEP_SKIPPED.value,
                "severity": "WARNING",
                "message": "Warning: Move step was skipped! Red box placed without move step validation."
            }
            realtime_state.safety_state = SafetyState.ERROR.value
            self.step_timer = time.time()

        elif self.scenario_name == "wrong-object" and step == 4 and elapsed > 3.0:
            # Simulate touching yellow box when red box is expected
            realtime_state.current_activity = "GRASP_YELLOW_BOX"
            realtime_state.active_alert = {
                "type": ErrorType.WRONG_OBJECT.value,
                "severity": "WARNING",
                "message": "Warning: Wrong object detected! Expected Red Box but detected Yellow Box."
            }
            realtime_state.safety_state = SafetyState.ERROR.value

        elif self.scenario_name == "timeout" and step == 5 and elapsed > 8.0:
            # Simulate step timeout
            realtime_state.active_alert = {
                "type": ErrorType.STEP_TIMEOUT.value,
                "severity": "WARNING",
                "message": f"Warning: Step 5 ('{realtime_state.step_name}') exceeded timeout threshold."
            }
            realtime_state.safety_state = SafetyState.UNCERTAIN.value

        elif self.scenario_name == "low-confidence" and step == 3:
            realtime_state.activity_confidence = 0.58
            realtime_state.safety_state = SafetyState.UNCERTAIN.value
            realtime_state.active_alert = {
                "type": ErrorType.LOW_CONFIDENCE.value,
                "severity": "WARNING",
                "message": "AI Confidence below threshold (58%). Action uncertain, verifying temporal sequence..."
            }

        else:
            # Normal sequence step progression every ~4 seconds
            if elapsed > 4.0 and step < 12:
                realtime_state.current_step += 1
                self.step_timer = time.time()
                realtime_state.safety_state = SafetyState.CONFIRMED.value
                realtime_state.active_alert = None

                # Update step metadata
                step_names = [
                    "", "Observe Payload Container", "Access Container", "Identify Red Box",
                    "Reach Red Box", "Grasp Red Box", "Move Red Box", "Place Red Box",
                    "Identify Yellow Box", "Grasp Yellow Box", "Move Yellow Box",
                    "Place Yellow Box", "Experiment Complete"
                ]
                activities = [
                    "", "OPEN_CONTAINER", "OPEN_CONTAINER", "IDENTIFY_OBJECT",
                    "REACH", "GRASP", "MOVE", "PLACE",
                    "IDENTIFY_OBJECT", "GRASP", "MOVE", "PLACE", "COMPLETE"
                ]

                if realtime_state.current_step <= 12:
                    realtime_state.step_name = step_names[realtime_state.current_step]
                    realtime_state.current_activity = activities[realtime_state.current_step]
                    realtime_state.next_step = min(12, realtime_state.current_step + 1)
                    realtime_state.next_step_name = step_names[realtime_state.next_step]
                    realtime_state.next_step_guidance = f"Perform {step_names[realtime_state.next_step]} as configured."
                    realtime_state.step_progress = round((realtime_state.current_step / 12.0) * 100.0, 1)

                    event_bus.publish(EventType.STEP_COMPLETED, {
                        "step": realtime_state.current_step,
                        "name": realtime_state.step_name
                    })

        return realtime_state.to_dict()
