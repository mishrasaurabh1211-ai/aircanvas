import json
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))

from aircanvas.tracking.config import TrackingConfig
from aircanvas.tracking.tracker import HandTracker


def generate_fixture(video_path: str, output_path: str) -> None:
    config = TrackingConfig(
        min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1
    )
    tracker = HandTracker(config)
    cap = cv2.VideoCapture(video_path)

    fixture_data = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        hand_data = tracker.process_frame(frame)
        frame_data = {
            "is_present": hand_data.is_present,
            "handedness": hand_data.handedness,
            "landmarks": hand_data.landmarks.tolist(),
        }
        fixture_data.append(frame_data)

    cap.release()
    tracker.close()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fixture_data, f)
    print(f"Fixture saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        generate_fixture(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python scripts/generate_fixture.py <input.mp4> <output.json>")