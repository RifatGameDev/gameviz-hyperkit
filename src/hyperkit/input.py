from __future__ import annotations

from dataclasses import dataclass
from time import monotonic


@dataclass
class TouchEvent:
    x: float
    y: float
    timestamp: float


@dataclass
class TouchGesture:
    kind: str
    start: tuple[float, float]
    end: tuple[float, float]
    direction: str | None = None
    duration: float = 0.0


class TouchTracker:
    """Detect tap and swipe gestures from down/move/up touch events."""

    def __init__(self, tap_max_distance: float = 25.0, tap_max_duration: float = 0.25, swipe_min_distance: float = 80.0) -> None:
        self.tap_max_distance = tap_max_distance
        self.tap_max_duration = tap_max_duration
        self.swipe_min_distance = swipe_min_distance
        self._start: TouchEvent | None = None

    def touch_down(self, x: float, y: float, timestamp: float | None = None) -> None:
        self._start = TouchEvent(x=x, y=y, timestamp=timestamp or monotonic())

    def touch_up(self, x: float, y: float, timestamp: float | None = None) -> TouchGesture | None:
        if self._start is None:
            return None

        end_time = timestamp or monotonic()
        dx = x - self._start.x
        dy = y - self._start.y
        distance = (dx * dx + dy * dy) ** 0.5
        duration = end_time - self._start.timestamp
        start_tuple = (self._start.x, self._start.y)
        end_tuple = (x, y)
        self._start = None

        if distance <= self.tap_max_distance and duration <= self.tap_max_duration:
            return TouchGesture(kind="tap", start=start_tuple, end=end_tuple, duration=duration)

        if distance >= self.swipe_min_distance:
            if abs(dx) >= abs(dy):
                direction = "right" if dx > 0 else "left"
            else:
                direction = "up" if dy > 0 else "down"
            return TouchGesture(kind="swipe", start=start_tuple, end=end_tuple, direction=direction, duration=duration)

        return TouchGesture(kind="drag", start=start_tuple, end=end_tuple, duration=duration)
