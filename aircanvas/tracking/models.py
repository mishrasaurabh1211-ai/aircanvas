from dataclasses import dataclass

import numpy as np


@dataclass
class HandData:
    landmarks: np.ndarray  # shape (21, 2) float32 [x, y in pixels]
    handedness: str
    is_present: bool