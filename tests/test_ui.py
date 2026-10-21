import numpy as np

from aircanvas.app.state import AppState, ToolType
from aircanvas.gesture.states import UserIntent
from aircanvas.ui.components import Button, check_collision
from aircanvas.ui.config import ButtonConfig, UIConfig
from aircanvas.ui.overlay import UIOverlay


def test_check_collision() -> None:
    btn = Button(x=10, y=10, w=50, h=50, color=(255, 0, 0), id="TEST")
    
    # Inside bounding box
    assert check_collision((20, 20), btn) is True
    # Outside bounding box
    assert check_collision((100, 100), btn) is False
    # None protection
    assert check_collision(None, btn) is False


def test_app_state_update() -> None:
    cfg = UIConfig(
        buttons=[
            ButtonConfig(id="COLOR_RED", x=0, y=0, w=50, h=50, color=(0, 0, 255)),
            ButtonConfig(id="TOOL_ERASER", x=100, y=0, w=50, h=50, color=(200, 200, 200)),
            ButtonConfig(id="ACTION_SAVE", x=200, y=0, w=50, h=50, color=(0, 255, 0)),
        ]
    )
    ui = UIOverlay(cfg)
    state = AppState(base_thickness=5, max_multiplier=4)

    assert state.save_triggered is False
    # Hover over the save button
    state.update(UserIntent.HOVER, (210, 10), 0.0, ui)
    assert state.save_triggered is True

    # Hovering again shouldn't trigger multiple saves
    state.update(UserIntent.HOVER, (210, 10), 0.0, ui)
    assert state.save_triggered is False


def test_ui_draw() -> None:
    cfg = UIConfig(
        buttons=[ButtonConfig(id="COLOR_RED", x=10, y=10, w=50, h=50, color=(0, 0, 255))]
    )
    ui = UIOverlay(cfg)
    
    # Synthetic physical frame
    frame = np.zeros((100, 100, 3), dtype=np.uint8)

    # Draw the UI
    out_frame = ui.draw(
        frame=frame,
        active_color=(0, 0, 255),
        active_tool=ToolType.BRUSH,
        brush_radius=10,
        cursor_pt=(50, 50),
    )
    
    # Validate the red button was rendered to the array
    assert np.any(out_frame[20, 20] == [0, 0, 255])
    # Validate the cursor circle was drawn
    assert np.any(out_frame[50, 50] == [255, 255, 255])  # Tiny center dot