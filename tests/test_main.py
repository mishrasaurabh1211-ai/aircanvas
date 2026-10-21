import numpy as np

from aircanvas.app.main import process_stream


def test_process_stream_smoke_test() -> None:
    """
    Feeds synthetic frames through the entire application loop to ensure
    all subsystems communicate correctly without crashing.
    """
    # Create an iterable of 3 black synthetic 720p frames
    frames = [np.zeros((720, 1280, 3), dtype=np.uint8) for _ in range(3)]

    # Consume the generator
    output_frames = list(process_stream(frames))

    assert len(output_frames) == 3
    for out_frame in output_frames:
        assert out_frame.shape == (720, 1280, 3)