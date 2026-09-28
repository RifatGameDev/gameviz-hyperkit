from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .object import GameObject


ColorValue = tuple[
    float,
    float,
    float,
    float,
]


@dataclass
class Button(GameObject):
    """Interactive rectangular button for HyperKit scenes."""

    text: str = "Button"
    on_click: Callable[[], None] | None = None
    enabled: bool = True
    font_size: int = 24
    bold: bool = False
    text_color: ColorValue = (
        1.0,
        1.0,
        1.0,
        1.0,
    )

    def click(self) -> bool:
        """Invoke the callback when this button can receive input."""

        if (
            not self.enabled
            or not self.active
            or not self.visible
        ):
            return False

        if self.on_click is not None:
            self.on_click()

        return True

    def hit_test(
        self,
        x: float,
        y: float,
    ) -> bool:
        """Return whether this button can receive a point input."""

        return (
            self.enabled
            and self.active
            and self.visible
            and self.contains(x, y)
        )


@dataclass
class TextLabel(GameObject):
    """Simple text label for showing score, messages, and UI text."""

    text: str = ""
    font_size: int = 28
    bold: bool = False

    def __post_init__(self) -> None:
        self.shape = "text"
        self.width = max(
            self.width,
            10,
        )
        self.height = max(
            self.height,
            self.font_size,
        )

    def set_text(
        self,
        text: str,
    ) -> "TextLabel":
        self.text = str(text)
        return self


def find_button_at(
    objects: Iterable[GameObject],
    x: float,
    y: float,
) -> Button | None:
    """Return the top-most interactive button at a point."""

    items = list(objects)

    for obj in reversed(items):
        if (
            isinstance(obj, Button)
            and obj.hit_test(x, y)
        ):
            return obj

    return None
