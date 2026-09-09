import unittest
import time
from core.realtime.realtime_state import realtime_state, RealtimeState
from core.realtime.event_types import EventType, SafetyState, ErrorType
from ai.interaction.object_state_machine import ObjectStateMachine
from core.sequence.sequence_engine import SequenceEngine
from core.sequence.error_detector import ErrorDetector
from core.recovery.recovery_engine import RecoveryEngine

class TestAstraHarPipeline(unittest.TestCase):

    def setUp(self):
        self.seq_engine = SequenceEngine("experiments/two_box_experiment.yaml")
        self.error_detector = ErrorDetector()
        self.recovery_engine = RecoveryEngine()
        self.osm = ObjectStateMachine()

    def test_object_state_machine_valid_transitions(self):
        """Test valid state transitions for experiment objects."""
        res1 = self.osm.update_state("red_box", "DETECTED")
        self.assertTrue(res1)
        res2 = self.osm.update_state("red_box", "CONTACTED")
        self.assertTrue(res2)
        res3 = self.osm.update_state("red_box", "GRASPED")
        self.assertTrue(res3)

    def test_sequence_engine_step_progression(self):
        """Test normal experiment sequence step validation."""
        info = self.seq_engine.get_current_step_info()
        self.assertEqual(info["step_number"], 1)

        completed, next_info, alert = self.seq_engine.evaluate_observation("OPEN_CONTAINER", "main_container", 0.95)
        self.assertTrue(completed)
        self.assertEqual(next_info["step_number"], 2)

    def test_error_detection_wrong_object(self):
        """Test error detection when interacting with wrong box."""
        current_info = self.seq_engine.get_current_step_info()
        # Step 3 expects red_box
        self.seq_engine.set_step(3)
        current_info = self.seq_engine.get_current_step_info()

        err = self.error_detector.check_errors(current_info, "GRASP", "yellow_box", 0.90, True)
        self.assertTrue(err["has_error"])
        self.assertEqual(err["type"], ErrorType.WRONG_OBJECT.value)

    def test_recovery_engine_handling(self):
        """Test RecoveryEngine response to skipped step."""
        err_info = {"type": ErrorType.STEP_SKIPPED.value}
        current_info = {"step_name": "Move Red Box"}

        rec = self.recovery_engine.handle_error(err_info, current_info)
        self.assertEqual(rec["recovery_action"], "REQUEST_REPEAT")
        self.assertIn("skipped", rec["voice_message"].lower())

if __name__ == "__main__":
    unittest.main()
