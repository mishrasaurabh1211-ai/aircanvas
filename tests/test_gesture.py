import numpy as np

from aircanvas.common.constants import FINGER_MCPS, FINGER_TIPS
from aircanvas.gesture.config import GestureConfig
from aircanvas.gesture.engine import GestureEngine
from aircanvas.gesture.modifiers import get_pinch_scale
from aircanvas.gesture.states import UserIntent
from aircanvas.tracking.models import HandData


def create_mock_hand(
    index_up: bool, middle_up: bool, ring_up: bool, pinky_up: bool
) -> HandData:
    landmarks = np.zeros((21, 2), dtype=np.float32)

    # Set base MCPs at Y=100
    for f_mcp in FINGER_MCPS.values():
        landmarks[f_mcp] = [50.0, 100.0]

    # Set tips (Y < 100 is UP, Y > 100 is DOWN)
    landmarks[FINGER_TIPS["index"]] = [50.0, 50.0 if index_up else 150.0]
    landmarks[FINGER_TIPS["middle"]] = [50.0, 50.0 if middle_up else 150.0]
    landmarks[FINGER_TIPS["ring"]] = [50.0, 50.0 if ring_up else 150.0]
    landmarks[FINGER_TIPS["pinky"]] = [50.0, 50.0 if pinky_up else 150.0]

    return HandData(landmarks=landmarks, handedness="Right", is_present=True)


def test_gesture_engine_eval() -> None:
    engine = GestureEngine()
    cfg = GestureConfig(min_pinch_dist=20.0, max_pinch_dist=150.0)

    # Not present -> IDLE
    no_hand = HandData(
        landmarks=np.zeros((21, 2), dtype=np.float32), handedness="", is_present=False
    )
    assert engine.eval(no_hand, cfg) == UserIntent.IDLE

    # FILL: All DOWN
    assert engine.eval(create_mock_hand(False, False, False, False), cfg) == UserIntent.FILL

    # ERASE: Index/Middle/Ring UP, Pinky DOWN
    assert engine.eval(create_mock_hand(True, True, True, False), cfg) == UserIntent.ERASE

    # HOVER: Index/Middle UP, Ring/Pinky DOWN
    assert engine.eval(create_mock_hand(True, True, False, False), cfg) == UserIntent.HOVER

    # DRAW: Index UP, Middle/Ring/Pinky DOWN
    assert engine.eval(create_mock_hand(True, False, False, False), cfg) == UserIntent.DRAW

    # CYCLE_COLOR: Pinky only UP
    assert engine.eval(create_mock_hand(False, False, False, True), cfg) == UserIntent.CYCLE_COLOR


def test_get_pinch_scale() -> None:
    cfg = GestureConfig(min_pinch_dist=20.0, max_pinch_dist=120.0)

    landmarks = np.zeros((21, 2), dtype=np.float32)
    hand = HandData(landmarks=landmarks, handedness="Right", is_present=True)

    # Test 1: dist < min -> 0.0
    landmarks[FINGER_TIPS["thumb"]] = [0.0, 0.0]
    landmarks[FINGER_TIPS["index"]] = [10.0, 0.0]  # dist=10
    assert get_pinch_scale(hand, cfg) == 0.0

    # Test 2: dist > max -> 1.0
    landmarks[FINGER_TIPS["index"]] = [150.0, 0.0]  # dist=150
    assert get_pinch_scale(hand, cfg) == 1.0

    # Test 3: exact middle -> 0.5
    landmarks[FINGER_TIPS["index"]] = [70.0, 0.0]  # dist=70, range=100
    assert get_pinch_scale(hand, cfg) == 0.5

    # Test 4: hand not present -> 0.0
    hand.is_present = False
    assert get_pinch_scale(hand, cfg) == 0.0