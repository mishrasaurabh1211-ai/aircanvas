from dataclasses import dataclass


@dataclass
class Button:
    x: int
    y: int
    w: int
    h: int
    color: tuple[int, int, int]
    id: str


def check_collision(pt: tuple[int, int] | None, btn: Button) -> bool:
    """Returns True if the point is within the button's bounding box."""
    if pt is None:
        return False
    return (btn.x <= pt[0] <= btn.x + btn.w) and (btn.y <= pt[1] <= btn.y + btn.h)