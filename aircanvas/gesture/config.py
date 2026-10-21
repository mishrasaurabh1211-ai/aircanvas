from pydantic import BaseModel


class GestureConfig(BaseModel):
    min_pinch_dist: float
    max_pinch_dist: float