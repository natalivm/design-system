# Countdown

Live timer for the wait before stars convert.

- Format 3:14:03, not 03h:14m:03s
- VoiceOver reads "3 hours, 14 minutes"

Two formats. The test is whether the number counts:

| | Use | Where |
|---|---|---|
| Clock | `3:14:03` | It counts in front of the player: Countdown, FlipTimer, the TimePill on the boost, the 15:00 boost. No padding on the first unit, no unit letters, tabular digits, and `role="timer"` with the spoken form as its label. |
| Time left | `3h 45m`, `3d 8h` | It is a span that sits still: InfoRow, the event banner’s "Ends in", the missions card. Two units at most, largest first, no padding, no colons. |

