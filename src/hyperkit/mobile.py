"""Mobile runtime helpers for GameViz HyperKit."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple, Union


class DisplayOrientation(str, Enum):
    """Supported runtime display orientations."""

    AUTO = "auto"
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    SENSOR = "sensor"


@dataclass(frozen=True)
class SafeAreaInsets:
    """Safe-area insets expressed in physical screen pixels."""

    left: float = 0.0
    right: float = 0.0
    top: float = 0.0
    bottom: float = 0.0

    def __post_init__(self) -> None:
        values = (
            self.left,
            self.right,
            self.top,
            self.bottom,
        )

        if any(value < 0 for value in values):
            raise ValueError(
                "Safe-area inset values cannot be negative."
            )

    @property
    def horizontal(self) -> float:
        return self.left + self.right

    @property
    def vertical(self) -> float:
        return self.top + self.bottom

    def to_dict(self) -> dict[str, float]:
        return {
            "left": self.left,
            "right": self.right,
            "top": self.top,
            "bottom": self.bottom,
        }


@dataclass(frozen=True)
class MobileViewport:
    """Resolved physical viewport after safe-area insets are applied."""

    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                "Mobile viewport width and height must be greater than zero."
            )

    def contains(
        self,
        x: float,
        y: float,
    ) -> bool:
        return (
            self.x <= x <= self.x + self.width
            and self.y <= y <= self.y + self.height
        )


def normalize_orientation(
    value: Union[str, DisplayOrientation],
) -> DisplayOrientation:
    if isinstance(
        value,
        DisplayOrientation,
    ):
        return value

    normalized = str(value).strip().lower()

    try:
        return DisplayOrientation(
            normalized
        )

    except ValueError as exc:
        choices = ", ".join(
            item.value
            for item in DisplayOrientation
        )

        raise ValueError(
            f"Unsupported display orientation '{value}'. "
            f"Choose one of: {choices}."
        ) from exc


@dataclass(frozen=True)
class MobileDisplayProfile:
    """Runtime display policy used by HyperKit games."""

    virtual_width: int = 720
    virtual_height: int = 1280

    orientation: DisplayOrientation = (
        DisplayOrientation.AUTO
    )

    fullscreen: Optional[bool] = None
    use_safe_area: bool = True

    safe_area: SafeAreaInsets = field(
        default_factory=SafeAreaInsets
    )

    def __post_init__(self) -> None:
        if self.virtual_width <= 0:
            raise ValueError(
                "virtual_width must be greater than zero."
            )

        if self.virtual_height <= 0:
            raise ValueError(
                "virtual_height must be greater than zero."
            )

        object.__setattr__(
            self,
            "orientation",
            normalize_orientation(
                self.orientation
            ),
        )

        if not isinstance(
            self.safe_area,
            SafeAreaInsets,
        ):
            raise TypeError(
                "safe_area must be a SafeAreaInsets instance."
            )

    @property
    def virtual_size(
        self,
    ) -> Tuple[int, int]:
        width = self.virtual_width
        height = self.virtual_height

        if (
            self.orientation
            == DisplayOrientation.LANDSCAPE
            and height > width
        ):
            return height, width

        if (
            self.orientation
            == DisplayOrientation.PORTRAIT
            and width > height
        ):
            return height, width

        return width, height

    def resolve_fullscreen(
        self,
        *,
        is_mobile: bool,
    ) -> bool:
        if self.fullscreen is not None:
            return bool(
                self.fullscreen
            )

        return is_mobile

    def resolve_viewport(
        self,
        actual_width: float,
        actual_height: float,
    ) -> MobileViewport:
        if (
            actual_width <= 0
            or actual_height <= 0
        ):
            raise ValueError(
                "Actual display width and height "
                "must be greater than zero."
            )

        if not self.use_safe_area:
            return MobileViewport(
                x=0.0,
                y=0.0,
                width=float(
                    actual_width
                ),
                height=float(
                    actual_height
                ),
            )

        width = (
            float(actual_width)
            - self.safe_area.horizontal
        )

        height = (
            float(actual_height)
            - self.safe_area.vertical
        )

        if width <= 0 or height <= 0:
            raise ValueError(
                "Safe-area insets are larger "
                "than the actual display."
            )

        # Kivy uses a bottom-left origin.
        return MobileViewport(
            x=self.safe_area.left,
            y=self.safe_area.bottom,
            width=width,
            height=height,
        )

    def to_dict(
        self,
    ) -> dict[str, object]:
        width, height = (
            self.virtual_size
        )

        return {
            "virtual_width": width,
            "virtual_height": height,
            "orientation": (
                self.orientation.value
            ),
            "fullscreen": self.fullscreen,
            "use_safe_area": (
                self.use_safe_area
            ),
            "safe_area": (
                self.safe_area.to_dict()
            ),
        }
