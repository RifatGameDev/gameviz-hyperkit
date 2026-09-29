from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


ActionCallback = Callable[["InputActionEvent"], None]

VALID_INPUT_KINDS = {
    "tap",
    "area",
    "swipe",
}


def _normalize_action(
    action: str,
) -> str:
    value = str(
        action
    ).strip()

    if not value:
        raise ValueError(
            "Input action name must not be empty."
        )

    return value


def _normalize_direction(
    direction: str | None,
) -> str | None:
    if direction is None:
        return None

    value = str(
        direction
    ).strip().lower()

    if not value:
        raise ValueError(
            "Swipe direction must not be empty."
        )

    return value


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
    data: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class InputActionBinding:
    """Stores one input-to-action binding."""

    action: str
    kind: str
    callback: ActionCallback | None = None
    direction: str | None = None
    rect: tuple[
        float,
        float,
        float,
        float,
    ] | None = None
    enabled: bool = True
    data: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(
        self,
    ) -> None:
        self.action = _normalize_action(
            self.action
        )
        self.kind = str(
            self.kind
        ).strip().lower()

        if self.kind not in VALID_INPUT_KINDS:
            raise ValueError(
                f"Unsupported input binding kind '{self.kind}'."
            )

        self.direction = _normalize_direction(
            self.direction
        )

        if self.kind == "area":
            if self.rect is None:
                raise ValueError(
                    "Area bindings require a rect."
                )

            rx, ry, rw, rh = self.rect

            if rw <= 0 or rh <= 0:
                raise ValueError(
                    "Area binding width and height must be greater than zero."
                )

            self.rect = (
                float(rx),
                float(ry),
                float(rw),
                float(rh),
            )

        self.data = dict(
            self.data
        )

    def matches_tap(
        self,
        x: float,
        y: float,
    ) -> bool:
        if not self.enabled:
            return False

        if self.kind == "tap":
            return True

        if (
            self.kind == "area"
            and self.rect is not None
        ):
            rx, ry, rw, rh = (
                self.rect
            )

            return (
                rx
                <= x
                <= rx + rw
                and ry
                <= y
                <= ry + rh
            )

        return False

    def matches_swipe(
        self,
        direction: str,
    ) -> bool:
        if not self.enabled:
            return False

        if self.kind != "swipe":
            return False

        normalized = (
            _normalize_direction(
                direction
            )
        )

        return (
            self.direction is None
            or self.direction
            == normalized
        )


class InputActionMap:
    """Map tap/swipe input to named actions."""

    def __init__(
        self,
    ) -> None:
        self.bindings: list[
            InputActionBinding
        ] = []
        self.enabled: bool = True
        self.last_event: (
            InputActionEvent
            | None
        ) = None

    def add_binding(
        self,
        binding: InputActionBinding,
    ) -> InputActionBinding:
        if not isinstance(
            binding,
            InputActionBinding,
        ):
            raise TypeError(
                "binding must be an InputActionBinding."
            )

        self.bindings.append(
            binding
        )

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
                data=(
                    {}
                    if data is None
                    else data
                ),
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
                rect=(
                    x,
                    y,
                    width,
                    height,
                ),
                callback=callback,
                data=(
                    {}
                    if data is None
                    else data
                ),
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
                data=(
                    {}
                    if data is None
                    else data
                ),
            )
        )

    def handle_tap(
        self,
        x: float,
        y: float,
    ) -> InputActionEvent | None:
        if not self.enabled:
            return None

        x = float(
            x
        )
        y = float(
            y
        )

        for binding in reversed(
            self.bindings
        ):
            if binding.matches_tap(
                x,
                y,
            ):
                event = InputActionEvent(
                    action=binding.action,
                    kind=binding.kind,
                    x=x,
                    y=y,
                    data=dict(
                        binding.data
                    ),
                )

                self._dispatch(
                    binding,
                    event,
                )

                return event

        return None

    def handle_swipe(
        self,
        start: tuple[
            float,
            float,
        ],
        end: tuple[
            float,
            float,
        ],
        direction: str,
    ) -> InputActionEvent | None:
        if not self.enabled:
            return None

        normalized_direction = (
            _normalize_direction(
                direction
            )
        )

        start_point = (
            float(
                start[0]
            ),
            float(
                start[1]
            ),
        )
        end_point = (
            float(
                end[0]
            ),
            float(
                end[1]
            ),
        )

        for binding in reversed(
            self.bindings
        ):
            if binding.matches_swipe(
                normalized_direction
            ):
                event = InputActionEvent(
                    action=binding.action,
                    kind="swipe",
                    direction=normalized_direction,
                    start=start_point,
                    end=end_point,
                    data=dict(
                        binding.data
                    ),
                )

                self._dispatch(
                    binding,
                    event,
                )

                return event

        return None

    def _dispatch(
        self,
        binding: InputActionBinding,
        event: InputActionEvent,
    ) -> None:
        self.last_event = event

        if (
            binding.callback
            is not None
        ):
            binding.callback(
                event
            )

    def set_enabled(
        self,
        enabled: bool,
    ) -> "InputActionMap":
        self.enabled = bool(
            enabled
        )
        return self

    def has_action(
        self,
        action: str,
    ) -> bool:
        target = _normalize_action(
            action
        )

        return any(
            binding.action
            == target
            for binding
            in self.bindings
        )

    def bindings_for(
        self,
        action: str,
    ) -> list[
        InputActionBinding
    ]:
        target = _normalize_action(
            action
        )

        return [
            binding
            for binding
            in self.bindings
            if binding.action
            == target
        ]

    def enable_action(
        self,
        action: str,
    ) -> int:
        count = 0

        for binding in self.bindings_for(
            action
        ):
            binding.enabled = True
            count += 1

        return count

    def disable_action(
        self,
        action: str,
    ) -> int:
        count = 0

        for binding in self.bindings_for(
            action
        ):
            binding.enabled = False
            count += 1

        return count

    def remove_action(
        self,
        action: str,
    ) -> int:
        target = _normalize_action(
            action
        )

        before = len(
            self.bindings
        )

        self.bindings = [
            binding
            for binding
            in self.bindings
            if binding.action
            != target
        ]

        return (
            before
            - len(
                self.bindings
            )
        )

    def clear(
        self,
    ) -> "InputActionMap":
        self.bindings.clear()
        self.last_event = None
        return self

    def actions(
        self,
    ) -> list[str]:
        return sorted(
            {
                binding.action
                for binding
                in self.bindings
            }
        )
