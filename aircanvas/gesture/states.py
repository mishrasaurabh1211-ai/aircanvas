from enum import Enum, auto


class UserIntent(Enum):
    IDLE = auto()
    HOVER = auto()
    DRAW = auto()
    ERASE = auto()
    FILL = auto()
    CYCLE_COLOR = auto()