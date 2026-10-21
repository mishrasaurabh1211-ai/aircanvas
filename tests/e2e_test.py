import os
from pathlib import Path
from unittest.mock import patch

import cv2
import numpy as np

from aircanvas.app.headless import run_headless
from aircanvas.tracking.models import HandData


def create_synthetic_video(filepath: str, frames: int = 30) -> None:
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(filepath, fourcc, 30.0, (1280, 720))
    for i in range(frames):
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        # Draw a moving white dot to represent the tracked hand
        cv2.circle(frame, (100 + i * 10, 100 + i * 10), 10, (255, 255, 255), -1)
        out.write(frame)
    out.release()


@patch("aircanvas.tracking.tracker.HandTracker.process_frame")
def test_headless_pipeline_e2e(mock_process_frame, tmp_path: Path) -> None:
    input_vid = str(tmp_path / "input.mp4")
    output_vid = str(tmp_path / "output.mp4")
    
    create_synthetic_video(input_vid)

    # Mock the tracker to always return a "DRAW" intent (Index UP)
    def mock_tracker(frame):
        lm = np.zeros((21, 2), dtype=np.float32)
        # Set base MCPs down
        lm[:] = [50.0, 150.0]
        # Set index tip UP
        lm[8] = [50.0, 50.0]
        return HandData(landmarks=lm, handedness="Right", is_present=True)
        
    mock_process_frame.side_effect = mock_tracker

    run_headless(input_vid, output_vid)

    assert os.path.exists(output_vid)
    assert os.path.getsize(output_vid) > 1000  # Ensure file is not empty