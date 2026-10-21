# Tracking Layer

The tracking layer acts as the bridge between the raw camera input and the gesture engine.

## HandData Guarantee
The `HandData` dataclass enforces strict boundaries:
- **Shape**: The `landmarks` attribute is strictly a `(21, 2)` float32 NumPy array.
- **Pixel-Space**: Coordinates emitted from `HandTracker` are pre-multiplied by the frame's width and height. They represent absolute pixel values `(x, y)` on the screen.
- **State**: If `is_present` is False, the `landmarks` array safely returns all zeros to prevent `NoneType` errors downstream.