import os
import json
import yaml
import logging

logger = logging.getLogger("ASTRA-HAR.ExperimentLoader")

class ExperimentLoader:
    """
    Loads JSON and YAML experiment protocols for on-board BAS human activity recognition.
    """

    def __init__(self, protocols_dir="experiments/protocols"):
        self.protocols_dir = protocols_dir
        os.makedirs(self.protocols_dir, exist_ok=True)

    def load_protocol(self, filepath_or_id: str) -> dict:
        """Loads experiment protocol by file path or experiment ID."""
        # 1. Direct path check
        if os.path.exists(filepath_or_id):
            return self._parse_file(filepath_or_id)

        # 2. Check in protocols directory
        json_path = os.path.join(self.protocols_dir, f"{filepath_or_id}.json")
        if os.path.exists(json_path):
            return self._parse_file(json_path)

        yaml_path = os.path.join(self.protocols_dir, f"{filepath_or_id}.yaml")
        if os.path.exists(yaml_path):
            return self._parse_file(yaml_path)

        # Default fallback protocol: Two-Box Sorting
        default_protocol_path = os.path.join(self.protocols_dir, "two_box_sorting.json")
        if os.path.exists(default_protocol_path):
            return self._parse_file(default_protocol_path)

        logger.warning(f"Protocol file {filepath_or_id} not found. Generating default protocol structure.")
        return {
            "experiment_id": "EXP_001",
            "name": "Two-Box Sorting",
            "steps": [
                {"id": 1, "name": "Approach Object", "action": "APPROACH_OBJECT", "timeout": 20},
                {"id": 2, "name": "Identify Object", "action": "IDENTIFY_OBJECT", "timeout": 20},
                {"id": 3, "name": "Pick Object", "action": "PICK_OBJECT", "timeout": 20},
                {"id": 4, "name": "Move Object", "action": "MOVE_OBJECT", "timeout": 20},
                {"id": 5, "name": "Place Object", "action": "PLACE_OBJECT", "timeout": 20}
            ]
        }

    def list_available_experiments(self) -> list:
        """Returns list of all available experiment protocol configurations."""
        experiments = []
        # Check protocols folder
        for folder in [self.protocols_dir, "experiments"]:
            if not os.path.exists(folder):
                continue
            for f in os.listdir(folder):
                if f.endswith(".json") or f.endswith(".yaml") or f.endswith(".yml"):
                    full_p = os.path.join(folder, f)
                    try:
                        proto = self._parse_file(full_p)
                        experiments.append({
                            "id": proto.get("experiment_id", f),
                            "name": proto.get("name", f),
                            "file": f,
                            "steps_count": len(proto.get("steps", []))
                        })
                    except Exception:
                        pass
        return experiments

    def _parse_file(self, filepath: str) -> dict:
        with open(filepath, "r", encoding="utf-8") as f:
            if filepath.endswith(".json"):
                return json.load(f)
            else:
                return yaml.safe_load(f)

experiment_loader = ExperimentLoader()
