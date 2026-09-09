import os
import json
import time

class DatasetRecorder:
    """Dataset recording application tool saving frame metadata, pose keypoints, and activity labels."""

    def __init__(self, dataset_dir: str = "dataset"):
        self.dataset_dir = dataset_dir
        self.is_recording = False
        self.current_sequence_id = ""
        self.recorded_frames = []

        os.makedirs(os.path.join(dataset_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(dataset_dir, "annotations"), exist_ok=True)
        os.makedirs(os.path.join(dataset_dir, "metadata"), exist_ok=True)

    def start_recording(self, sequence_label: str = "normal_sequence"):
        self.is_recording = True
        self.current_sequence_id = f"SEQ_{int(time.time())}_{sequence_label}"
        self.recorded_frames = []
        print(f"Dataset recording started: {self.current_sequence_id}")

    def record_frame(self, frame_data: dict):
        if not self.is_recording:
            return
        self.recorded_frames.append(frame_data)

    def stop_recording(self) -> str:
        if not self.is_recording:
            return ""

        self.is_recording = False
        out_path = os.path.join(self.dataset_dir, "annotations", f"{self.current_sequence_id}.json")
        with open(out_path, "w") as f:
            json.dump({
                "sequence_id": self.current_sequence_id,
                "total_frames": len(self.recorded_frames),
                "frames": self.recorded_frames
            }, f, indent=2)

        print(f"Saved dataset annotation: {out_path} ({len(self.recorded_frames)} frames)")
        return out_path

if __name__ == "__main__":
    recorder = DatasetRecorder()
    recorder.start_recording("test_run")
    recorder.record_frame({"frame": 1, "activity": "REACH", "box": [100, 100, 200, 200]})
    recorder.stop_recording()
