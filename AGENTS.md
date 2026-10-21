1. Data flow is unidirectional: Frame -> Tracker -> Gesture Engine -> State Machine -> Canvas -> UI -> Output.
2. Every tunable (colors, threshold distances, window sizes, UI box coordinates) lives in configs/*.yaml. No magic numbers in code.
3. Every module ships with tests. Tests run with synthetic NumPy arrays or dummy frames, NEVER requiring a live webcam.
4. OpenCV functions that draw (cv2.line, cv2.rectangle) belong ONLY in canvas/ or ui/.
5. Report only numbers produced by running code in this session. Paste the command and its output.
6. Interfaces defined in an earlier phase are frozen. Changing one means updating every caller and test in the same change and saying so.
7. Finish the whole phase. If something is blocked, deliver everything else and say exactly what is missing.