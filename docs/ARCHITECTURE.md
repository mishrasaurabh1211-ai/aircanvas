# AirCanvas Architecture

## Data Flow
`Frame -> Tracker -> Gesture Engine -> State Machine -> Canvas -> UI -> Output`

## Module Ownership
- **tracking/**: Evaluates the frame and emits normalized coordinate landmarks via MediaPipe.
- **gesture/**: Contains pure functions defining hand states (pinch, fist, open) evaluated against per-frame coordinates.
- **canvas/**: The virtual NumPy backend handling drawing execution (cv2.line) and spatial memory.
- **ui/**: The frontend interface overlay handling palette boxes and tool selection visuals (cv2.rectangle).
- **app/**: The core state machine routing data unidirectionally across tracking, gesture detection, rendering, and UI.