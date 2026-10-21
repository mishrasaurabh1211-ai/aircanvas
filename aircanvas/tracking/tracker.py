import cv2
import mediapipe as mp  # type: ignore
import numpy as np

from aircanvas.tracking.config import TrackingConfig
from aircanvas.tracking.models import HandData


class HandTracker:
    def __init__(self, config: TrackingConfig) -> None:
        # We use the standard import structure here
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=config.max_num_hands,
            min_detection_confidence=config.min_detection_confidence,
            min_tracking_confidence=config.min_tracking_confidence,
        )

    def process_frame(self, frame: np.ndarray) -> HandData:
        """
        Converts a BGR frame to RGB, processes it through MediaPipe,
        and returns pixel-space coordinates.
        """
        if frame is None or frame.size == 0:
            return self._empty_hand_data()

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if not results.multi_hand_landmarks:
            return self._empty_hand_data()

        # Extract first hand (based on max_num_hands=1)
        hand_landmarks = results.multi_hand_landmarks[0]
        handedness_info = results.multi_handedness[0].classification[0].label

        landmarks_array = np.zeros((21, 2), dtype=np.float32)
        for i, lm in enumerate(hand_landmarks.landmark):
            # Convert normalized coordinates [0.0, 1.0] to pixel coordinates
            landmarks_array[i] = [lm.x * w, lm.y * h]

        return HandData(
            landmarks=landmarks_array,
            handedness=handedness_info,
            is_present=True,
        )

    def _empty_hand_data(self) -> HandData:
        return HandData(
            landmarks=np.zeros((21, 2), dtype=np.float32),
            handedness="",
            is_present=False,
        )

    def close(self) -> None:
        """Close the underlying MediaPipe Hands instance safely."""
        if hasattr(self, 'hands'):
            try:
                self.hands.close()
            except ValueError:
                pass  # Ignore MediaPipe's internal double-close bug

    def __del__(self) -> None:
        self.close()