from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic
from typing import (
    Dict,
    Hashable,
    Optional,
    Tuple,
)


PointerId = Hashable


@dataclass(frozen=True)
class TouchEvent:
    x: float
    y: float
    timestamp: float

    pointer_id: PointerId = field(
        default=0,
        compare=False,
    )


@dataclass(frozen=True)
class TouchGesture:
    kind: str
    start: Tuple[float, float]
    end: Tuple[float, float]

    direction: Optional[str] = None
    duration: float = 0.0

    distance: float = field(
        default=0.0,
        compare=False,
    )

    delta_x: float = field(
        default=0.0,
        compare=False,
    )

    delta_y: float = field(
        default=0.0,
        compare=False,
    )

    pointer_id: PointerId = field(
        default=0,
        compare=False,
    )


class TouchTracker:
    """Detect tap, swipe, and drag gestures.

    Independent pointer state allows the same API to support
    desktop mouse input and mobile multi-touch input.
    """

    def __init__(
        self,
        tap_max_distance: float = 25.0,
        tap_max_duration: float = 0.25,
        swipe_min_distance: float = 80.0,
    ) -> None:
        if tap_max_distance < 0:
            raise ValueError(
                "tap_max_distance cannot be negative."
            )

        if tap_max_duration < 0:
            raise ValueError(
                "tap_max_duration cannot be negative."
            )

        if swipe_min_distance < 0:
            raise ValueError(
                "swipe_min_distance cannot be negative."
            )

        self.tap_max_distance = float(
            tap_max_distance
        )

        self.tap_max_duration = float(
            tap_max_duration
        )

        self.swipe_min_distance = float(
            swipe_min_distance
        )

        self._starts: Dict[
            PointerId,
            TouchEvent,
        ] = {}

        self._current: Dict[
            PointerId,
            TouchEvent,
        ] = {}

    @property
    def active_touch_count(
        self,
    ) -> int:
        return len(
            self._starts
        )

    @property
    def _start(
        self,
    ) -> Optional[TouchEvent]:
        """Backward-compatible primary pointer start."""

        return self._starts.get(
            0
        )

    @_start.setter
    def _start(
        self,
        value: Optional[TouchEvent],
    ) -> None:
        if value is None:
            self._starts.pop(
                0,
                None,
            )

            self._current.pop(
                0,
                None,
            )

            return

        self._starts[0] = value
        self._current[0] = value

    def is_touch_active(
        self,
        pointer_id: PointerId = 0,
    ) -> bool:
        return (
            pointer_id
            in self._starts
        )

    def get_touch_position(
        self,
        pointer_id: PointerId = 0,
    ) -> Optional[
        Tuple[float, float]
    ]:
        event = self._current.get(
            pointer_id
        )

        if event is None:
            return None

        return (
            event.x,
            event.y,
        )

    def touch_down(
        self,
        x: float,
        y: float,
        timestamp: Optional[
            float
        ] = None,
        *,
        pointer_id: PointerId = 0,
    ) -> TouchEvent:
        event = TouchEvent(
            x=float(x),
            y=float(y),
            timestamp=(
                monotonic()
                if timestamp is None
                else float(timestamp)
            ),
            pointer_id=pointer_id,
        )

        self._starts[
            pointer_id
        ] = event

        self._current[
            pointer_id
        ] = event

        return event

    def touch_move(
        self,
        x: float,
        y: float,
        timestamp: Optional[
            float
        ] = None,
        *,
        pointer_id: PointerId = 0,
    ) -> Optional[TouchEvent]:
        if (
            pointer_id
            not in self._starts
        ):
            return None

        event = TouchEvent(
            x=float(x),
            y=float(y),
            timestamp=(
                monotonic()
                if timestamp is None
                else float(timestamp)
            ),
            pointer_id=pointer_id,
        )

        self._current[
            pointer_id
        ] = event

        return event

    def touch_up(
        self,
        x: float,
        y: float,
        timestamp: Optional[
            float
        ] = None,
        *,
        pointer_id: PointerId = 0,
    ) -> Optional[TouchGesture]:
        start = self._starts.pop(
            pointer_id,
            None,
        )

        self._current.pop(
            pointer_id,
            None,
        )

        if start is None:
            return None

        end_time = (
            monotonic()
            if timestamp is None
            else float(timestamp)
        )

        dx = (
            float(x)
            - start.x
        )

        dy = (
            float(y)
            - start.y
        )

        distance = (
            dx * dx
            + dy * dy
        ) ** 0.5

        duration = max(
            0.0,
            end_time
            - start.timestamp,
        )

        start_tuple = (
            start.x,
            start.y,
        )

        end_tuple = (
            float(x),
            float(y),
        )

        common = {
            "start": start_tuple,
            "end": end_tuple,
            "duration": duration,
            "distance": distance,
            "delta_x": dx,
            "delta_y": dy,
            "pointer_id": pointer_id,
        }

        if (
            distance
            <= self.tap_max_distance
            and duration
            <= self.tap_max_duration
        ):
            return TouchGesture(
                kind="tap",
                **common,
            )

        if (
            distance
            >= self.swipe_min_distance
        ):
            if (
                abs(dx)
                >= abs(dy)
            ):
                direction = (
                    "right"
                    if dx > 0
                    else "left"
                )

            else:
                direction = (
                    "up"
                    if dy > 0
                    else "down"
                )

            return TouchGesture(
                kind="swipe",
                direction=direction,
                **common,
            )

        return TouchGesture(
            kind="drag",
            **common,
        )

    def cancel_touch(
        self,
        pointer_id: PointerId = 0,
    ) -> bool:
        existed = (
            pointer_id
            in self._starts
            or pointer_id
            in self._current
        )

        self._starts.pop(
            pointer_id,
            None,
        )

        self._current.pop(
            pointer_id,
            None,
        )

        return existed

    def cancel_all(
        self,
    ) -> None:
        self._starts.clear()
        self._current.clear()
