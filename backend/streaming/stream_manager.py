import cv2
import time
import threading
import logging
import numpy as np
from fastapi.responses import StreamingResponse

logger = logging.getLogger("ASTRA-HAR.StreamManager")

class StreamManager:
    """Provides low-latency annotated MJPEG HTTP video streaming (/video)."""

    def __init__(self):
        self.latest_jpeg = None
        self._lock = threading.Lock()

    def update_frame(self, frame: np.ndarray):
        """Encode and update current frame for MJPEG stream."""
        if frame is None:
            return

        try:
            ret, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                with self._lock:
                    self.latest_jpeg = jpeg.tobytes()
        except Exception as e:
            logger.error(f"Error encoding stream frame: {e}")

    def generate_mjpeg_stream(self):
        """Generator function for FastAPI StreamingResponse."""
        while True:
            with self._lock:
                jpeg = self.latest_jpeg

            if jpeg is not None:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"
                )
            else:
                # Fallback blank frame
                blank = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(blank, "ASTRA-HAR VIDEO FEED", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                _, jpeg_blank = cv2.imencode(".jpg", blank)
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg_blank.tobytes() + b"\r\n"
                )

            time.sleep(0.04)  # ~25 FPS

# Global stream manager instance
stream_manager = StreamManager()
