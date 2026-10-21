import numpy as np


def euclidean_distance(idx1: int, idx2: int, landmarks: np.ndarray) -> float:
    """Calculate the Euclidean distance between two landmarks."""
    p1 = landmarks[idx1]
    p2 = landmarks[idx2]
    return float(np.linalg.norm(p1 - p2))


def is_finger_up(tip_idx: int, mcp_idx: int, landmarks: np.ndarray) -> bool:
    """
    Determine if a finger is up.
    Since the y-axis goes down in OpenCV/MediaPipe, a smaller y-value
    means the point is higher on the screen.
    """
    return bool(landmarks[tip_idx][1] < landmarks[mcp_idx][1])