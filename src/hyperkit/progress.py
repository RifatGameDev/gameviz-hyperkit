from __future__ import annotations

from typing import Any

from .object import GameObject
from .ui import TextLabel


class ProgressBarError(Exception):
    """Base error for HyperKit progress bars."""


class ProgressBar:
    """Simple UI progress bar helper.

    It creates:
    - background GameObject
    - fill GameObject
    - optional TextLabel

    Example:
        health = ProgressBar(scene=self, x=50, y=1100, width=600, height=35)
        health.set_value(75)
    """

    def __init__(
        self,
        scene: Any,
        x: float,
        y: float,
        width: float,
        height: float,
        value: float = 100,
        max_value: float = 100,
        background_color: tuple[float, float,
                                float, float] = (0.15, 0.15, 0.2, 1),
        fill_color: tuple[float, float, float, float] = (0.2, 0.75, 1.0, 1),
        text_color: tuple[float, float, float, float] = (1, 1, 1, 1),
        show_text: bool = True,
        text_format: str = "{percent:.0f}%",
        name: str = "progress_bar",
    ) -> None:
        if width <= 0:
            raise ProgressBarError("ProgressBar width must be greater than 0.")

        if height <= 0:
            raise ProgressBarError(
                "ProgressBar height must be greater than 0.")

        if max_value <= 0:
            raise ProgressBarError(
                "ProgressBar max_value must be greater than 0.")

        self.scene = scene
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.max_value = float(max_value)
        self.value = 0.0
        self.text_format = text_format
        self.show_text = show_text
        self.name = name

        self.background = self.scene.add(
            GameObject(
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                color=background_color,
                name=f"{name}_background",
            )
        )

        self.fill = self.scene.add(
            GameObject(
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                color=fill_color,
                name=f"{name}_fill",
            )
        )

        self.label: TextLabel | None = None

        if self.show_text:
            self.label = self.scene.add(
                TextLabel(
                    x=self.x + self.width / 2 - 35,
                    y=self.y + self.height / 2 - 14,
                    text="100%",
                    font_size=22,
                    bold=True,
                    color=text_color,
                )
            )

        self.set_value(value)

    @property
    def progress(self) -> float:
        return self.value / self.max_value

    @property
    def percent(self) -> float:
        return self.progress * 100

    def set_value(self, value: float) -> None:
        self.value = max(0.0, min(float(value), self.max_value))
        self._refresh()

    def add_value(self, amount: float) -> None:
        self.set_value(self.value + amount)

    def subtract_value(self, amount: float) -> None:
        self.set_value(self.value - amount)

    def set_max_value(self, max_value: float, keep_percent: bool = True) -> None:
        if max_value <= 0:
            raise ProgressBarError(
                "ProgressBar max_value must be greater than 0.")

        old_progress = self.progress
        self.max_value = float(max_value)

        if keep_percent:
            self.value = self.max_value * old_progress
        else:
            self.value = min(self.value, self.max_value)

        self._refresh()

    def set_fill_color(self, color: tuple[float, float, float, float]) -> None:
        self.fill.color = color

    def set_background_color(self, color: tuple[float, float, float, float]) -> None:
        self.background.color = color

    def show(self) -> None:
        self.background.visible = True
        self.fill.visible = True

        if self.label is not None:
            self.label.visible = True

    def hide(self) -> None:
        self.background.visible = False
        self.fill.visible = False

        if self.label is not None:
            self.label.visible = False

    def set_position(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

        self.background.x = self.x
        self.background.y = self.y

        self.fill.x = self.x
        self.fill.y = self.y

        if self.label is not None:
            self.label.x = self.x + self.width / 2 - 35
            self.label.y = self.y + self.height / 2 - 14

    def _refresh(self) -> None:
        self.fill.width = self.width * self.progress

        if self.label is not None:
            self.label.set_text(
                self.text_format.format(
                    value=self.value,
                    max_value=self.max_value,
                    progress=self.progress,
                    percent=self.percent,
                )
            )
