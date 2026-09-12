import cv2
import time
import logging
import numpy as np

logger = logging.getLogger("ASTRA-HAR.AppCamera")

class CameraCapture:
    """
    OpenCV Camera Acquisition Wrapper for Laptop Webcam, USB Camera, IP Camera, or Video Stream.
    """

    def __init__(self, source=0, width=1280, height=720):
        self.source = source
        self.width = width
        self.height = height
        self.cap = None

    def open(self) -> bool:
        try:
            self.cap = cv2.VideoCapture(self.source)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            if self.cap and self.cap.isOpened():
                logger.info(f"Successfully opened camera source: {self.source}")
                return True
        except Exception as e:
            logger.error(f"Error opening camera source {self.source}: {e}")

        logger.warning(f"Camera source {self.source} unavailable. Switching to fallback synthetic frame stream.")
        return False

    def read_frame(self) -> tuple:
        """
        Returns (success: bool, frame: ndarray)
        """
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret and frame is not None:
                return True, cv2.flip(frame, 1)

        # Fallback synthetic demo frame if no camera is attached
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # Draw background grid
        for y in range(0, self.height, 40):
            cv2.line(frame, (0, y), (self.width, y), (20, 30, 40), 1)
        for x in range(0, self.width, 40):
            cv2.line(frame, (x, 0), (x, self.height), (20, 30, 40), 1)

        cv2.putText(frame, "ASTRA-HAR DEMO CAMERA FEED [SYNTHETIC STREAM]", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        return True, frame

    def release(self):
        if self.cap:
            self.cap.release()
            self.cap = None
