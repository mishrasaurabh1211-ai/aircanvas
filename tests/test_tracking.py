
import numpy as np

from aircanvas.common.constants import FINGER_MCPS, FINGER_TIPS
from aircanvas.tracking.config import TrackingConfig
from aircanvas.tracking.geometry import euclidean_distance, is_finger_up
from aircanvas.tracking.tracker import HandTracker


def test_tracker_no_hand() -> None:
    config = TrackingConfig(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
        max_num_hands=1,
    )
    tracker = HandTracker(config)
    
    # Synthetic black frame
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    result = tracker.process_frame(dummy_frame)
    
    assert result.is_present is False
    assert result.handedness == ""
    assert result.landmarks.shape == (21, 2)
    assert np.all(result.landmarks == 0)
    
    tracker.close()


def test_euclidean_distance() -> None:
    landmarks = np.zeros((21, 2), dtype=np.float32)
    landmarks[0] = [0.0, 0.0]
    landmarks[1] = [3.0, 4.0]
    
    dist = euclidean_distance(0, 1, landmarks)
    assert np.isclose(dist, 5.0)


def test_is_finger_up() -> None:
    landmarks = np.zeros((21, 2), dtype=np.float32)
    tip_idx = FINGER_TIPS["index"]
    mcp_idx = FINGER_MCPS["index"]
    
    # Y goes down. Smaller Y means higher up.
    # Case 1: Finger is UP (Tip is physically above MCP)
    landmarks[tip_idx] = [10.0, 50.0]
    landmarks[mcp_idx] = [10.0, 100.0]
    assert is_finger_up(tip_idx, mcp_idx, landmarks) is True
    
    # Case 2: Finger is DOWN (Tip is physically below MCP)
    landmarks[tip_idx] = [10.0, 150.0]
    assert is_finger_up(tip_idx, mcp_idx, landmarks) is False