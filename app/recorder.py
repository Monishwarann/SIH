import os
import cv2
import time
import logging

logger = logging.getLogger("ASTRA-HAR.AppRecorder")

class VideoRecorder:
    """
    Saves live camera footage locally under recordings/YYYY-MM-DD/EXP_001_HHMMSS.mp4
    """

    def __init__(self, output_dir="recordings"):
        self.output_dir = output_dir
        self.is_recording = False
        self.writer = None
        self.output_filepath = None

    def start_recording(self, session_id: str, width=1280, height=720, fps=30.0):
        if self.is_recording:
            return

        date_str = time.strftime("%Y-%m-%d")
        day_dir = os.path.join(self.output_dir, date_str)
        os.makedirs(day_dir, exist_ok=True)

        time_str = time.strftime("%H%M%S")
        filename = f"{session_id}_{time_str}.mp4"
        self.output_filepath = os.path.join(day_dir, filename)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.output_filepath, fourcc, fps, (width, height))
        self.is_recording = True
        logger.info(f"Started session video recording: {self.output_filepath}")

    def write_frame(self, frame):
        if self.is_recording and self.writer is not None:
            self.writer.write(frame)

    def stop_recording(self) -> str:
        if not self.is_recording:
            return ""

        self.is_recording = False
        if self.writer is not None:
            self.writer.release()
            self.writer = None

        filepath = self.output_filepath
        logger.info(f"Stopped video recording. Saved to: {filepath}")
        return filepath

app_recorder = VideoRecorder()
