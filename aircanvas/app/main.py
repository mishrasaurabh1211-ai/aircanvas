from collections.abc import Generator, Iterable
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

from aircanvas.app.state import AppState, ToolType
from aircanvas.canvas.config import CanvasConfig
from aircanvas.canvas.smoothing import PointSmoother
from aircanvas.canvas.surface import VirtualCanvas
from aircanvas.common.config import BaseConfig, load_config
from aircanvas.common.constants import FINGER_TIPS
from aircanvas.gesture.config import GestureConfig
from aircanvas.gesture.engine import GestureEngine
from aircanvas.gesture.modifiers import get_pinch_scale
from aircanvas.gesture.states import UserIntent
from aircanvas.tracking.config import TrackingConfig
from aircanvas.tracking.tracker import HandTracker
from aircanvas.ui.config import UIConfig
from aircanvas.ui.overlay import UIOverlay


def process_stream(
    frame_source: Iterable[np.ndarray],
) -> Generator[np.ndarray, None, None]:
    """
    Core application pipeline. Consumes frames from an iterable,
    processes tracking, gestures, canvas rendering, and UI.
    """
    # Load all configurations
    base_dir = Path("configs")
    base_cfg = load_config(base_dir / "base.yaml", BaseConfig)
    tracking_cfg = load_config(base_dir / "tracking.yaml", TrackingConfig)
    gesture_cfg = load_config(base_dir / "gesture.yaml", GestureConfig)
    canvas_cfg = load_config(base_dir / "canvas.yaml", CanvasConfig)
    ui_cfg = load_config(base_dir / "ui.yaml", UIConfig)

    # Initialize subsystems
    tracker = HandTracker(tracking_cfg)
    engine = GestureEngine()
    canvas = VirtualCanvas(base_cfg.resolution.width, base_cfg.resolution.height)
    smoother = PointSmoother(canvas_cfg.smoothing_window, canvas_cfg.smoothing_type)
    ui = UIOverlay(ui_cfg)
    state = AppState(
        canvas_cfg.base_brush_thickness, canvas_cfg.max_thickness_multiplier
    )

    prev_pt: tuple[int, int] | None = None

    for frame in frame_source:
        if frame is None or frame.size == 0:
            continue

        if base_cfg.mirror_webcam:
            frame = cv2.flip(frame, 1)

        # Force frame to configured resolution
        frame = cv2.resize(
            frame, (base_cfg.resolution.width, base_cfg.resolution.height)
        )

        hand_data = tracker.process_frame(frame)

        cursor_pt: tuple[int, int] | None = None
        if hand_data.is_present:
            tip = hand_data.landmarks[FINGER_TIPS["index"]]
            cursor_pt = (int(tip[0]), int(tip[1]))

        intent = engine.eval(hand_data, gesture_cfg)
        pinch_scale = get_pinch_scale(hand_data, gesture_cfg)

        state.update(intent, cursor_pt, pinch_scale, ui)

        # Handle UI Action triggers
        if state.clear_triggered:
            canvas.clear()

        if state.save_triggered:
            artifacts_dir = Path("artifacts")
            artifacts_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
            filepath = artifacts_dir / f"output_{timestamp}.png"
            cv2.imwrite(str(filepath), canvas.grid)
            print(f"Canvas saved to {filepath}")

        # Routing the intent to the canvas
        if intent in (UserIntent.DRAW, UserIntent.ERASE) and cursor_pt is not None:
            smoothed_pt = smoother.add_point(cursor_pt)

            if prev_pt is not None:
                if intent == UserIntent.ERASE or state.current_tool == ToolType.ERASER:
                    canvas.erase_line(prev_pt, smoothed_pt, state.brush_thickness)
                else:
                    canvas.draw_line(
                        prev_pt, smoothed_pt, state.current_color, state.brush_thickness
                    )
            prev_pt = smoothed_pt
        else:
            smoother.reset()
            prev_pt = None

        if state.fill_triggered and cursor_pt is not None:
            canvas.flood_fill(cursor_pt, state.current_color)

        composited = canvas.blend(frame)
        final_output = ui.draw(
            composited,
            state.current_color,
            state.current_tool,
            state.brush_thickness,
            cursor_pt,
        )

        yield final_output

    tracker.close()


def webcam_source() -> Generator[np.ndarray, None, None]:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
    cap.release()


def run() -> None:
    for final_output in process_stream(webcam_source()):
        cv2.imshow("AirCanvas", final_output)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()