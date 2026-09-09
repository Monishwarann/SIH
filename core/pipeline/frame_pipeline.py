import time
import queue
import threading
import logging
import numpy as np

logger = logging.getLogger("ASTRA-HAR.FramePipeline")

class FramePipeline:
    """Threaded frame pipeline with bounded queues and frame dropping for low latency."""

    def __init__(self, max_queue_size: int = 3):
        self.max_queue_size = max_queue_size
        self.frame_queue = queue.Queue(maxsize=max_queue_size)
        self.is_running = False
        self._thread = None
        self.dropped_frames = 0
        self.processed_frames = 0

    def push_frame(self, frame: np.ndarray, timestamp: float = None) -> bool:
        """Push a frame to the queue. Drops oldest frame if full to ensure freshness."""
        if timestamp is None:
            timestamp = time.time()

        if self.frame_queue.full():
            try:
                # Drop oldest frame
                self.frame_queue.get_nowait()
                self.dropped_frames += 1
            except queue.Empty:
                pass

        try:
            self.frame_queue.put_nowait((frame, timestamp))
            return True
        except queue.Full:
            return False

    def get_latest_frame(self, timeout: float = 0.1):
        """Fetch latest frame from queue."""
        try:
            frame, ts = self.frame_queue.get(timeout=timeout)
            self.processed_frames += 1
            return frame, ts
        except queue.Empty:
            return None, None

    def clear(self):
        """Clear all queued frames."""
        with self.frame_queue.mutex:
            self.frame_queue.queue.clear()

# Global pipeline instance
frame_pipeline = FramePipeline(max_queue_size=3)
