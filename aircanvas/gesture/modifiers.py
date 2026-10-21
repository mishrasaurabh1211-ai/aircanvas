from aircanvas.common.constants import FINGER_TIPS
from aircanvas.gesture.config import GestureConfig
from aircanvas.tracking.geometry import euclidean_distance
from aircanvas.tracking.models import HandData


def get_pinch_scale(hand: HandData, cfg: GestureConfig) -> float:
    """
    Returns the distance between thumb and index tip normalized [0.0, 1.0].
    """
    if not hand.is_present:
        return 0.0

    dist = euclidean_distance(
        FINGER_TIPS["thumb"], FINGER_TIPS["index"], hand.landmarks
    )

    if dist <= cfg.min_pinch_dist:
        return 0.0
    if dist >= cfg.max_pinch_dist:
        return 1.0

    return (dist - cfg.min_pinch_dist) / (cfg.max_pinch_dist - cfg.min_pinch_dist)