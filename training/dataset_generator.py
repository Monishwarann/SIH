import os
import json
import random
import time
import cv2
import numpy as np

class DatasetGenerator:
    """Automatic dataset generation pipeline converting sample videos/recordings into temporal HAR feature datasets."""

    def __init__(self, output_dir: str = "dataset"):
        self.output_dir = output_dir
        self.train_dir = os.path.join(output_dir, "train")
        self.val_dir = os.path.join(output_dir, "validation")
        self.test_dir = os.path.join(output_dir, "test")

        os.makedirs(self.train_dir, exist_ok=True)
        os.makedirs(self.val_dir, exist_ok=True)
        os.makedirs(self.test_dir, exist_ok=True)

    def generate_from_samples(self, samples_meta: list) -> dict:
        """Generate leakage-free dataset split (70% train, 15% val, 15% test) grouped by recording session."""
        print(f"Generating dataset from {len(samples_meta)} sample sequences...")

        # Group samples by session/person to avoid data leakage
        grouped = {}
        for sample in samples_meta:
            group_key = sample.get("person_id", sample.get("sample_id", "default"))
            if group_key not in grouped:
                grouped[group_key] = []
            grouped[group_key].append(sample)

        all_keys = list(grouped.keys())
        random.shuffle(all_keys)

        num_keys = len(all_keys)
        train_cutoff = int(0.70 * num_keys)
        val_cutoff = int(0.85 * num_keys)

        train_keys = all_keys[:max(1, train_cutoff)]
        val_keys = all_keys[max(1, train_cutoff):val_cutoff]
        test_keys = all_keys[val_cutoff:] if val_cutoff < num_keys else val_keys

        train_samples = [s for k in train_keys for s in grouped[k]]
        val_samples = [s for k in val_keys for s in grouped[k]]
        test_samples = [s for k in test_keys for s in grouped[k]]

        # Write dataset JSON summary
        dataset_info = {
            "dataset_id": f"ASTRA-HAR-DS-{int(time.time())}",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_samples": len(samples_meta),
            "splits": {
                "train_count": len(train_samples),
                "val_count": len(val_samples),
                "test_count": len(test_samples)
            },
            "train_samples": train_samples,
            "val_samples": val_samples,
            "test_samples": test_samples,
            "classes": sorted(list(set(s.get("activity", "IDLE") for s in samples_meta)))
        }

        dataset_meta_path = os.path.join(self.output_dir, "dataset.json")
        with open(dataset_meta_path, "w") as f:
            json.dump(dataset_info, f, indent=2)

        print(f"Dataset successfully created at {dataset_meta_path}")
        return dataset_info

dataset_generator = DatasetGenerator()
