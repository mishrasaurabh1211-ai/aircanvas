from pydantic import BaseModel

class CanvasConfig(BaseModel):
    base_brush_thickness: int
    base_eraser_thickness: int
    max_thickness_multiplier: int
    smoothing_window: int
    smoothing_type: str = "average"