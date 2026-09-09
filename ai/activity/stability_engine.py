from collections import Counter

class StabilityEngine:
    """Temporal voting and hysteresis engine preventing frame flicker in activity classification."""

    def __init__(self, min_activity_frames: int = 5):
        self.min_activity_frames = min_activity_frames
        self.recent_activities = []
        self.current_stable_activity = "IDLE"
        self.stable_confidence = 0.95

    def update(self, raw_activity: str, raw_confidence: float) -> tuple:
        """Process frame activity and return smoothed (stable_activity, stable_confidence, is_stable)."""
        self.recent_activities.append(raw_activity)
        if len(self.recent_activities) > self.min_activity_frames:
            self.recent_activities.pop(0)

        # Majority vote across recent window
        counts = Counter(self.recent_activities)
        most_common, count = counts.most_common(1)[0]

        if count >= (self.min_activity_frames // 2 + 1):
            self.current_stable_activity = most_common
            self.stable_confidence = raw_confidence
            is_stable = True
        else:
            is_stable = False

        return self.current_stable_activity, self.stable_confidence, is_stable
