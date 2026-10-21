from enum import Enum

import cv2
import numpy as np

from aircanvas.ui.components import Button
from aircanvas.ui.config import UIConfig


class UIOverlay:
    def __init__(self, cfg: UIConfig) -> None:
        self.buttons = [
            Button(x=b.x, y=b.y, w=b.w, h=b.h, color=b.color, id=b.id)
            for b in cfg.buttons
        ]

    def draw(
        self,
        frame: np.ndarray,
        active_color: tuple[int, int, int],
        active_tool: Enum,
        brush_radius: int,
        cursor_pt: tuple[int, int] | None,
    ) -> np.ndarray:
        """
        Draws the UI overlay onto the frame, highlighting the active tool/color.
        """
        out_frame = frame.copy()

        for btn in self.buttons:
            # Determine if this specific button is currently active
            is_active = False
            if btn.id.startswith("COLOR_") and btn.color == active_color and active_tool.name == "BRUSH" or btn.id == "TOOL_ERASER" and active_tool.name == "ERASER":
                is_active = True

            # Draw filled button
            cv2.rectangle(
                out_frame,
                (btn.x, btn.y),
                (btn.x + btn.w, btn.y + btn.h),
                btn.color,
                -1,
            )
            
            # Draw border (white if active, black if inactive)
            border_color = (255, 255, 255) if is_active else (0, 0, 0)
            cv2.rectangle(
                out_frame,
                (btn.x, btn.y),
                (btn.x + btn.w, btn.y + btn.h),
                border_color,
                3 if is_active else 1,
            )

        if cursor_pt is not None:
            # Draw the cursor brush indicator based on radius and color
            cv2.circle(out_frame, cursor_pt, brush_radius, active_color, 2)
            # Draw a tiny dot for the exact center
            cv2.circle(out_frame, cursor_pt, 2, (255, 255, 255), -1)

        return out_frame