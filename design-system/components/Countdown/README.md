# Countdown

Live timer for the wait before stars convert.

- Format 3:14:03, not 03h:14m:03s
- VoiceOver reads "3 hours, 14 minutes"

Two formats, by whether the seconds matter:

| | Use | Where |
|---|---|---|
| Clock | `3:14:03` | A timer that ticks in front of the player: Countdown, FlipTimer, the 15:00 boost. No padding on the first unit, no unit letters. |
| Time left | `3h 45m`, `3d 8h` | A span read at a glance, in a sentence or a chip, where seconds are noise: InfoRow, TimePill, the event banner, the missions card. Two units at most, largest first, no padding, no colons. |

