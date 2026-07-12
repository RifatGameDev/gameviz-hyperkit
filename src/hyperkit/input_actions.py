from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


ActionCallback = Callable[["InputActionEvent"], None]


@dataclass
class InputActionEvent:
    """Event data sent to input action callbacks."""

    action: str
    kind: str
    x: float | None = None
    y: float | None = None
    direction: str | None = None
    start: tuple[float, float] | None = None
    end: tuple[float, float] | None = None
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class InputActionBinding:
    """Stores one input-to-action binding."""

    action: str
    kind: str
    callback: ActionCallback | None = None
    direction: str | None = None
    rect: tuple[float, float, float, float] | None = None
    enabled: bool = True
    data: dict[str, Any] = field(default_factory=dict)

    def matches_tap(self, x: float, y: float) -> bool:
        if not self.enabled:
            return False

        if self.kind == "tap":
            return True

        if self.kind == "area" and self.rect is not None:
            rx, ry, rw, rh = self.rect
            return rx <= x <= rx + rw and ry <= y <= ry + rh

        return False

    def matches_swipe(self, direction: str) -> bool:
        if not self.enabled:
            return False

        if self.kind != "swipe":
            return False

        return self.direction is None or self.direction == direction


class InputActionMap:
    """Map tap/swipe input to named actions.

    Example:
        actions = InputActionMap()
        actions.map_tap("jump", callback=jump)
        actions.map_swipe("left", direction="left", callback=move_left)
    """

    def __init__(self) -> None:
        self.bindings: list[InputActionBinding] = []
        self.enabled: bool = True
        self.last_event: InputActionEvent | None = None

    def add_binding(self, binding: InputActionBinding) -> InputActionBinding:
        self.bindings.append(binding)
        return binding

    def map_tap(
        self,
        action: str,
        callback: ActionCallback | None = None,
        data: dict[str, Any] | None = None,
    ) -> InputActionBinding:
        return self.add_binding(
            InputActionBinding(
                action=action,
                kind="tap",
                callback=callback,
                data=data or {},
            )
        )

    def map_area(
        self,
        action: str,
        x: float,
        y: float,
        width: float,
        height: float,
        callback: ActionCallback | None = None,
        data: dict[str, Any] | None = None,
    ) -> InputActionBinding:
        return self.add_binding(
            InputActionBinding(
                action=action,
                kind="area",
                rect=(x, y, width, height),
                callback=callback,
                data=data or {},
            )
        )

    def map_swipe(
        self,
        action: str,
        direction: str | None = None,
        callback: ActionCallback | None = None,
        data: dict[str, Any] | None = None,
    ) -> InputActionBinding:
        return self.add_binding(
            InputActionBinding(
                action=action,
                kind="swipe",
                direction=direction,
                callback=callback,
                data=data or {},
            )
        )

    def handle_tap(self, x: float, y: float) -> InputActionEvent | None:
        if not self.enabled:
            return None

        for binding in reversed(self.bindings):
            if binding.matches_tap(x, y):
                event = InputActionEvent(
                    action=binding.action,
                    kind=binding.kind,
                    x=x,
                    y=y,
                    data=dict(binding.data),
                )

                self._dispatch(binding, event)
                return event

        return None

    def handle_swipe(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        direction: str,
    ) -> InputActionEvent | None:
        if not self.enabled:
            return None

        for binding in reversed(self.bindings):
            if binding.matches_swipe(direction):
                event = InputActionEvent(
                    action=binding.action,
                    kind="swipe",
                    direction=direction,
                    start=start,
                    end=end,
                    data=dict(binding.data),
                )

                self._dispatch(binding, event)
                return event

        return None

    def _dispatch(self, binding: InputActionBinding, event: InputActionEvent) -> None:
        self.last_event = event

        if binding.callback is not None:
            binding.callback(event)

    def enable_action(self, action: str) -> None:
        for binding in self.bindings:
            if binding.action == action:
                binding.enabled = True

    def disable_action(self, action: str) -> None:
        for binding in self.bindings:
            if binding.action == action:
                binding.enabled = False

    def remove_action(self, action: str) -> None:
        self.bindings = [
            binding for binding in self.bindings if binding.action != action
        ]

    def clear(self) -> None:
        self.bindings.clear()
        self.last_event = None

    def actions(self) -> list[str]:
        return sorted({binding.action for binding in self.bindings})
