import math
import time
from collections import deque


class OneEuroFilter:
    """A robust low-pass filter for noisy input signals."""

    def __init__(
        self,
        t0: float,
        x0: float,
        dx0: float = 0.0,
        min_cutoff: float = 1.0,
        beta: float = 0.0,
        d_cutoff: float = 1.0,
    ) -> None:
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_prev = x0
        self.dx_prev = dx0
        self.t_prev = t0

    def __call__(self, t: float, x: float) -> float:
        t_e = t - self.t_prev
        if t_e <= 0.0:
            return x
        a_d = self._smoothing_factor(t_e, self.d_cutoff)
        dx = (x - self.x_prev) / t_e
        dx_hat = self._exponential_smoothing(a_d, dx, self.dx_prev)
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = self._smoothing_factor(t_e, cutoff)
        x_hat = self._exponential_smoothing(a, x, self.x_prev)
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t
        return x_hat

    def _smoothing_factor(self, t_e: float, cutoff: float) -> float:
        r = 2 * math.pi * cutoff * t_e
        return r / (r + 1)

    def _exponential_smoothing(self, a: float, x: float, x_prev: float) -> float:
        return a * x + (1 - a) * x_prev


class PointSmoother:
    def __init__(self, window_size: int, smoothing_type: str = "average") -> None:
        self.window_size = window_size
        self.smoothing_type = smoothing_type
        self.pts: deque[tuple[int, int]] = deque(maxlen=window_size)
        self.filter_x: OneEuroFilter | None = None
        self.filter_y: OneEuroFilter | None = None

    def add_point(self, pt: tuple[int, int]) -> tuple[int, int]:
        if self.smoothing_type == "one_euro":
            t = time.time()
            if self.filter_x is None or self.filter_y is None:
                self.filter_x = OneEuroFilter(t, float(pt[0]), min_cutoff=0.1, beta=0.5)
                self.filter_y = OneEuroFilter(t, float(pt[1]), min_cutoff=0.1, beta=0.5)
                return pt

            x_hat = self.filter_x(t, float(pt[0]))
            y_hat = self.filter_y(t, float(pt[1]))
            return (int(x_hat), int(y_hat))
        else:
            self.pts.append(pt)
            x_avg = sum(p[0] for p in self.pts) // len(self.pts)
            y_avg = sum(p[1] for p in self.pts) // len(self.pts)
            return (x_avg, y_avg)

    def reset(self) -> None:
        self.pts.clear()
        self.filter_x = None
        self.filter_y = None