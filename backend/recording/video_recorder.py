import cv2
import os
import time
import threading
import logging
import numpy as np

logger = logging.getLogger("ASTRA-HAR.VideoRecorder")

class VideoRecorder:
    """Asynchronous Video Recorder saving experiment sessions into MP4 files."""

    def __init__(self, record_dir: str = "recordings"):
        self.record_dir = record_dir
        os.makedirs(record_dir, exist_ok=True)
        self.writer = None
        self.is_recording = False
        self.output_filepath = ""
        self._lock = threading.Lock()

    def start_recording(self, session_id: str, width: int = 1280, height: int = 720, fps: int = 30):
        """Initialize OpenCV VideoWriter for session MP4 recording."""
        timestamp_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.output_filepath = os.path.join(self.record_dir, f"experiment_{timestamp_str}.mp4")

        try:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(self.output_filepath, fourcc, fps, (width, height))
            self.is_recording = True
            logger.info(f"Started video recording: {self.output_filepath}")
        except Exception as e:
            logger.error(f"Failed to initialize VideoWriter: {e}")

    def write_frame(self, frame: np.ndarray):
        """Write frame asynchronously to video file."""
        if not self.is_recording or self.writer is None or frame is None:
            return

        try:
            with self._lock:
                self.writer.write(frame)
        except Exception as e:
            logger.error(f"Error writing frame to recording: {e}")

    def stop_recording(self) -> str:
        """Release VideoWriter and finalize file."""
        if self.writer is not None:
            with self._lock:
                self.writer.release()
                self.writer = None
            self.is_recording = False
            logger.info(f"Stopped video recording: {self.output_filepath}")
            return self.output_filepath
        return ""

# Global recorder instance
video_recorder = VideoRecorder()
