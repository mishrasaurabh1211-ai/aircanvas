from aircanvas.common.constants import FINGER_MCPS, FINGER_TIPS
from aircanvas.gesture.config import GestureConfig
from aircanvas.gesture.states import UserIntent
from aircanvas.tracking.geometry import is_finger_up
from aircanvas.tracking.models import HandData


class GestureEngine:
    def eval(self, hand: HandData, cfg: GestureConfig) -> UserIntent:
        if not hand.is_present:
            return UserIntent.IDLE

        lm = hand.landmarks

        index_up = is_finger_up(FINGER_TIPS["index"], FINGER_MCPS["index"], lm)
        middle_up = is_finger_up(FINGER_TIPS["middle"], FINGER_MCPS["middle"], lm)
        ring_up = is_finger_up(FINGER_TIPS["ring"], FINGER_MCPS["ring"], lm)
        pinky_up = is_finger_up(FINGER_TIPS["pinky"], FINGER_MCPS["pinky"], lm)

        # Rule 1: FIST (bucket fill) - all 4 fingers DOWN
        if not index_up and not middle_up and not ring_up and not pinky_up:
            return UserIntent.FILL

        # Rule 2: ERASE (3 fingers) - Index, Middle, and Ring UP, Pinky DOWN
        if index_up and middle_up and ring_up and not pinky_up:
            return UserIntent.ERASE

        # Rule 3: HOVER (navigation) - index and middle UP, ring and pinky DOWN
        if index_up and middle_up and not ring_up and not pinky_up:
            return UserIntent.HOVER

        # Rule 4: DRAW - index UP, middle, ring, pinky DOWN
        if index_up and not middle_up and not ring_up and not pinky_up:
            return UserIntent.DRAW

        # Rule 5: CYCLE_COLOR - Only Pinky UP
        if not index_up and not middle_up and not ring_up and pinky_up:
            return UserIntent.CYCLE_COLOR

        # Fallback
        return UserIntent.IDLE