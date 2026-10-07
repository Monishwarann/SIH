import unittest
import os
import numpy as np
from pathlib import Path

# Add project root to sys.path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ai.action_recognition import action_recognizer, ActionRecognizer

class TestBiLSTMIntegration(unittest.TestCase):

    def test_model_loaded(self):
        """Test 1: Verify model loaded status interface."""
        status = action_recognizer.get_status()
        self.assertEqual(status["model"], "best_bilstm_model.keras")
        if action_recognizer.is_loaded:
            self.assertTrue(status["loaded"])
            self.assertTrue(os.path.exists(status["model_path"]))
        else:
            self.assertFalse(status["loaded"])
            self.assertIsNotNone(status.get("error"))

    def test_model_shapes(self):
        """Test 2: Verify input and output shape definitions."""
        status = action_recognizer.get_status()
        self.assertEqual(status["num_classes"], 7)
        self.assertEqual(len(status["classes"]), 7)
        if action_recognizer.is_loaded and action_recognizer.model is not None:
            self.assertEqual(action_recognizer.model.input_shape, (None, 16, 224, 224, 3))
            self.assertEqual(action_recognizer.model.output_shape, (None, 7))

    def test_preprocessing(self):
        """Test 3: Verify preprocessing creates correct uint8 tensor shape."""
        frames = [np.zeros((480, 640, 3), dtype=np.uint8) for _ in range(16)]
        tensor = action_recognizer.preprocess_buffer(frames)
        self.assertEqual(tensor.shape, (1, 16, 224, 224, 3))
        self.assertEqual(tensor.dtype, np.uint8)

    def test_inference_from_buffer_full(self):
        """Test 4: Verify real or fallback inference returns expected structured dictionary."""
        # 16 synthetic colored frames
        frames = [np.full((224, 224, 3), fill_value=i * 15, dtype=np.uint8) for i in range(16)]
        res = action_recognizer.predict_from_buffer(frames)

        self.assertIn("activity", res)
        self.assertIn("confidence", res)
        self.assertIn("class_index", res)
        self.assertIn("probabilities", res)
        self.assertIn("status", res)

        expected_status = "ACTIVE" if action_recognizer.is_loaded else "OFFLINE_FALLBACK"
        self.assertEqual(res["status"], expected_status)
        self.assertIn(res["activity"], action_recognizer.classes)
        self.assertGreaterEqual(res["confidence"], 0.0)
        self.assertLessEqual(res["confidence"], 1.0)
        self.assertEqual(len(res["probabilities"]), 7)

        # Probabilities sum to ~1.0
        prob_sum = sum(res["probabilities"].values())
        self.assertAlmostEqual(prob_sum, 1.0, places=3)

    def test_inference_from_buffer_insufficient_frames(self):
        """Test 5: Verify WAITING_FOR_FRAMES state when buffer has fewer than 16 frames."""
        frames = [np.zeros((224, 224, 3), dtype=np.uint8) for _ in range(5)]
        res = action_recognizer.predict_from_buffer(frames)
        self.assertEqual(res["status"], "WAITING_FOR_FRAMES")

    def test_empty_buffer(self):
        """Test 6: Verify empty buffer handling."""
        res = action_recognizer.predict_from_buffer([])
        self.assertEqual(res["status"], "WAITING_FOR_FRAMES")
        self.assertEqual(res["activity"], "WAIT")

if __name__ == "__main__":
    unittest.main()
