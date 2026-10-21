from pathlib import Path

import cv2

from aircanvas.app.main import process_stream
from aircanvas.common.config import BaseConfig, load_config


def video_source(video_path: str):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
    cap.release()


def run_headless(input_path: str, output_path: str) -> None:
    base_cfg = load_config(Path("configs/base.yaml"), BaseConfig)
    w, h = base_cfg.resolution.width, base_cfg.resolution.height
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (w, h))

    for frame in process_stream(video_source(input_path)):
        out.write(frame)
        
    out.release()
    print(f"Headless processing complete. Output saved to {output_path}")