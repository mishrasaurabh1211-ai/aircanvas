from pydantic import BaseModel


class TrackingConfig(BaseModel):
    min_detection_confidence: float
    min_tracking_confidence: float
    max_num_hands: int