import numpy as np

from aircanvas.canvas.smoothing import PointSmoother
from aircanvas.canvas.surface import VirtualCanvas


def test_draw_line() -> None:
    canvas = VirtualCanvas(100, 100)
    canvas.draw_line((10, 10), (20, 20), (0, 0, 255), 2)
    # Validate that at least some pixels in the expected region changed to red
    assert np.any(canvas.grid[15, 15] == [0, 0, 255])


def test_erase_line() -> None:
    canvas = VirtualCanvas(100, 100)
    canvas.draw_line((10, 10), (20, 20), (0, 0, 255), 2)
    canvas.erase_line((10, 10), (20, 20), 4)
    # The canvas should be entirely black again
    assert np.all(canvas.grid == 0)


def test_flood_fill() -> None:
    canvas = VirtualCanvas(100, 100)
    # Fill the entire blank canvas with green
    canvas.flood_fill((50, 50), (0, 255, 0))
    assert np.all(canvas.grid[50, 50] == [0, 255, 0])

    # Ensure out-of-bounds seed points do not crash the engine
    canvas.flood_fill((200, 200), (255, 0, 0))


def test_clear() -> None:
    canvas = VirtualCanvas(100, 100)
    canvas.draw_line((10, 10), (20, 20), (0, 0, 255), 2)
    canvas.clear()
    assert np.all(canvas.grid == 0)


def test_blend() -> None:
    canvas = VirtualCanvas(100, 100)
    canvas.draw_line((10, 10), (20, 20), (0, 0, 255), 5)

    # Synthetic physical webcam frame (pure white)
    white_frame = np.ones((100, 100, 3), dtype=np.uint8) * 255
    blended = canvas.blend(white_frame)

    # Verify the line was successfully pasted onto the white frame
    assert np.any(blended[15, 15] == [0, 0, 255])
    # Verify the background remained white
    assert np.all(blended[90, 90] == [255, 255, 255])


def test_point_smoother() -> None:
    smoother = PointSmoother(window_size=2, smoothing_type="average")
    pt1 = smoother.add_point((10, 10))
    assert pt1 == (10, 10)
    pt2 = smoother.add_point((20, 20))
    assert pt2 == (15, 15)
    smoother.reset()
    pt3 = smoother.add_point((30, 30))
    assert pt3 == (30, 30)

    smoother_euro = PointSmoother(window_size=2, smoothing_type="one_euro")
    pt1_e = smoother_euro.add_point((10, 10))
    assert pt1_e == (10, 10)