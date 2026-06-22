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
