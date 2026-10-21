# Gestures Truth Table

The pure gesture engine maps coordinate logic to semantic `UserIntent` states. Evaluation stops at the first matching rule.

| Intent | Index | Middle | Ring | Pinky | Condition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FILL** | DOWN | DOWN | DOWN | DOWN | All fingers folded into a fist. Used for bucket fill. |
| **ERASE** | UP | UP | UP | UP | Open hand. Used for erasing. |
| **HOVER** | UP | UP | DOWN | DOWN | Index and middle fingers extended. Used for menu navigation. |
| **DRAW** | UP | DOWN | DOWN | DOWN | Only the index finger extended. Used for drawing. |
| **IDLE** | * | * | * | * | Any state not defined above, or when the hand is not present. |

## Pinch Scale Modifiers
`get_pinch_scale` provides continuous logic based on the distance between the thumb tip (4) and the index tip (8). Distances are clamped and normalized to a `[0.0, 1.0]` range.