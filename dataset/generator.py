import os
import json
import random
import time

class SyntheticDatasetGenerator:
    """Synthetic dataset generator producing visual variations (lighting, camera orientation, background)."""

    def __init__(self, output_dir: str = "dataset"):
        self.output_dir = output_dir
        os.makedirs(os.path.join(output_dir, "train"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "val"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "test"), exist_ok=True)

    def generate_synthetic_samples(self, count: int = 100):
        """Generate synthetic activity observation JSON sequences."""
        activities = ["IDLE", "REACH", "OPEN_CONTAINER", "IDENTIFY_OBJECT", "GRASP", "MOVE", "PLACE", "RELEASE"]
        samples = []

        for i in range(count):
            act = random.choice(activities)
            sample = {
                "id": f"SYNTH_{i:04d}",
                "timestamp": time.time(),
                "activity": act,
                "confidence": round(random.uniform(0.80, 0.99), 3),
                "lighting_lux": random.randint(300, 1000),
                "camera_pitch_deg": round(random.uniform(-30.0, 30.0), 1),
                "hand_object_dist_px": round(random.uniform(5.0, 150.0), 1)
            }
            samples.append(sample)

        out_file = os.path.join(self.output_dir, "train", "synthetic_activity_dataset.json")
        with open(out_file, "w") as f:
            json.dump(samples, f, indent=2)

        print(f"Generated {count} synthetic dataset samples: {out_file}")

if __name__ == "__main__":
    gen = SyntheticDatasetGenerator()
    gen.generate_synthetic_samples(50)
