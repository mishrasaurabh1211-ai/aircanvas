import cv2
import numpy as np


class VirtualCanvas:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width, 3), dtype=np.uint8)

    def draw_line(
        self,
        p1: tuple[int, int],
        p2: tuple[int, int],
        color: tuple[int, int, int],
        thickness: int,
    ) -> None:
        cv2.line(self.grid, p1, p2, color, thickness)

    def erase_line(
        self, p1: tuple[int, int], p2: tuple[int, int], thickness: int
    ) -> None:
        # Drawing with black (0, 0, 0) effectively erases on our mask
        cv2.line(self.grid, p1, p2, (0, 0, 0), thickness)

    def flood_fill(
        self, seed_point: tuple[int, int], color: tuple[int, int, int]
    ) -> None:
        x, y = seed_point
        if 0 <= x < self.width and 0 <= y < self.height:
            # OpenCV floodFill requires a mask that is 2 pixels larger in each dimension
            mask = np.zeros((self.height + 2, self.width + 2), dtype=np.uint8)
            cv2.floodFill(self.grid, mask, (x, y), color)

    def clear(self) -> None:
        self.grid.fill(0)

    def blend(self, frame: np.ndarray) -> np.ndarray:
        """
        Overlays the canvas onto the physical webcam frame.
        """
        # Create a mask of all non-black pixels on the canvas
        gray_canvas = cv2.cvtColor(self.grid, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_canvas, 0, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # Black-out the drawn area in the physical frame
        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)

        # Extract only the drawn regions from the canvas
        canvas_fg = cv2.bitwise_and(self.grid, self.grid, mask=mask)

        # Superimpose the canvas drawing onto the physical frame
        return cv2.add(frame_bg, canvas_fg)