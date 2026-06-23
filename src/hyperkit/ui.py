from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .object import GameObject


@dataclass
class Button(GameObject):
    """Very small rectangle button object for prototypes."""

    text: str = "Button"
    on_click: Callable[[], None] | None = None

    def click(self) -> None:
        if self.on_click:
            self.on_click()


@dataclass
class TextLabel(GameObject):
    """Simple text label for showing score, messages, and UI text."""

    text: str = ""
    font_size: int = 28
    bold: bool = False

    def __post_init__(self) -> None:
        self.shape = "text"
        self.width = max(self.width, 10)
        self.height = max(self.height, self.font_size)

    def set_text(self, text: str) -> "TextLabel":
        self.text = str(text)
        return self
