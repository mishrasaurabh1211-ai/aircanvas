from enum import Enum, auto

from aircanvas.gesture.states import UserIntent
from aircanvas.ui.components import check_collision
from aircanvas.ui.overlay import UIOverlay


class ToolType(Enum):
    BRUSH = auto()
    ERASER = auto()
    BUCKET = auto()


class AppState:
    def __init__(self, base_thickness: int, max_multiplier: int) -> None:
        self.palette = [
            (0, 0, 255), (0, 255, 0), (255, 0, 0),
            (0, 255, 255), (255, 0, 255)
        ]
        self.color_idx = 0
        self.current_color = self.palette[self.color_idx]
        self.current_tool = ToolType.BRUSH
        
        self.base_thickness = base_thickness
        self.brush_thickness = base_thickness
        self.max_multiplier = max_multiplier
        
        self.last_intent = UserIntent.IDLE
        self.fill_triggered = False
        self.save_triggered = False
        self.clear_triggered = False
        self.last_hovered_btn_id: str | None = None

    def update(
        self,
        intent: UserIntent,
        finger_pt: tuple[int, int] | None,
        pinch_scale: float,
        ui: UIOverlay,
    ) -> None:
        self.fill_triggered = False
        self.save_triggered = False
        self.clear_triggered = False

        if intent == UserIntent.FILL and self.last_intent != UserIntent.FILL:
            self.fill_triggered = True

        if intent == UserIntent.CYCLE_COLOR and self.last_intent != UserIntent.CYCLE_COLOR:
            self.color_idx = (self.color_idx + 1) % len(self.palette)
            self.current_color = self.palette[self.color_idx]
            self.current_tool = ToolType.BRUSH

        current_hover_id = None
        if intent == UserIntent.HOVER and finger_pt is not None:
            for btn in ui.buttons:
                if check_collision(finger_pt, btn):
                    current_hover_id = btn.id
                    if btn.id.startswith("COLOR_"):
                        self.current_color = btn.color
                        self.current_tool = ToolType.BRUSH
                    elif btn.id == "TOOL_ERASER":
                        self.current_tool = ToolType.ERASER
                    elif btn.id == "SIZE_UP":
                        self.base_thickness = min(50, self.base_thickness + 1)
                    elif btn.id == "SIZE_DOWN":
                        self.base_thickness = max(2, self.base_thickness - 1)
                    elif btn.id == "ACTION_SAVE" and self.last_hovered_btn_id != "ACTION_SAVE":
                        self.save_triggered = True
                    elif btn.id == "ACTION_CLEAR" and self.last_hovered_btn_id != "ACTION_CLEAR":
                        self.clear_triggered = True
                    break

        self.last_hovered_btn_id = current_hover_id
        self.brush_thickness = int(
            self.base_thickness * (1 + (self.max_multiplier * pinch_scale))
        )
        self.last_intent = intent