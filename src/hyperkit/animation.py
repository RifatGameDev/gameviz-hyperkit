from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


EasingFunction = Callable[[float], float]


def linear(t: float) -> float:
    return t


def ease_in_quad(t: float) -> float:
    return t * t


def ease_out_quad(t: float) -> float:
    return t * (2 - t)


def ease_in_out_quad(t: float) -> float:
    if t < 0.5:
        return 2 * t * t

    return -1 + (4 - 2 * t) * t


EASING_FUNCTIONS: dict[str, EasingFunction] = {
    "linear": linear,
    "ease_in_quad": ease_in_quad,
    "ease_out_quad": ease_out_quad,
    "ease_in_out_quad": ease_in_out_quad,
}


def get_easing(easing: str | EasingFunction) -> EasingFunction:
    if callable(easing):
        return easing

    if easing not in EASING_FUNCTIONS:
        available = ", ".join(EASING_FUNCTIONS.keys())
        raise ValueError(
            f"Unknown easing '{easing}'. Available easing: {available}")

    return EASING_FUNCTIONS[easing]


@dataclass
class Tween:
    """Animate one numeric property on an object.

    Example:
        Tween(player, "x", 500, duration=0.5)
    """

    target: Any
    attr: str
    to_value: float
    duration: float
    easing: str | EasingFunction = "linear"
    from_value: float | None = None
    delay: float = 0.0
    loop: bool = False
    yoyo: bool = False
    on_complete: Callable[[], None] | None = None

    elapsed: float = 0.0
    active: bool = True
    completed: bool = False

    _started: bool = False
    _start_value: float = field(default=0.0, init=False)
    _end_value: float = field(default=0.0, init=False)
    _easing_func: EasingFunction = field(default=linear, init=False)

    def __post_init__(self):
        if self.duration <= 0:
            raise ValueError("Tween duration must be greater than 0.")

        self._easing_func = get_easing(self.easing)

    def _start(self) -> None:
        current_value = float(getattr(self.target, self.attr))

        self._start_value = current_value if self.from_value is None else float(
            self.from_value)
        self._end_value = float(self.to_value)

        if self.from_value is not None:
            setattr(self.target, self.attr, self._start_value)

        self._started = True

    def update(self, dt: float) -> bool:
        if not self.active or self.completed:
            return False

        if self.delay > 0:
            self.delay -= dt
            if self.delay > 0:
                return True

        if not self._started:
            self._start()

        self.elapsed += dt

        t = min(self.elapsed / self.duration, 1.0)
        eased_t = self._easing_func(t)

        value = self._start_value + \
            (self._end_value - self._start_value) * eased_t
        setattr(self.target, self.attr, value)

        if t >= 1.0:
            if self.loop:
                self.elapsed = 0.0

                if self.yoyo:
                    self._start_value, self._end_value = self._end_value, self._start_value

                return True

            self.active = False
            self.completed = True

            if self.on_complete:
                self.on_complete()

            return False

        return True

    def stop(self) -> None:
        self.active = False
        self.completed = True


@dataclass
class ColorTween:
    """Animate a GameObject color tuple."""

    target: Any
    to_color: tuple[float, float, float, float]
    duration: float
    easing: str | EasingFunction = "linear"
    from_color: tuple[float, float, float, float] | None = None
    delay: float = 0.0
    loop: bool = False
    yoyo: bool = False
    on_complete: Callable[[], None] | None = None

    elapsed: float = 0.0
    active: bool = True
    completed: bool = False

    _started: bool = False
    _start_color: tuple[float, float, float, float] = field(
        default=(1, 1, 1, 1),
        init=False,
    )
    _end_color: tuple[float, float, float, float] = field(
        default=(1, 1, 1, 1),
        init=False,
    )
    _easing_func: EasingFunction = field(default=linear, init=False)

    def __post_init__(self):
        if self.duration <= 0:
            raise ValueError("ColorTween duration must be greater than 0.")

        self._easing_func = get_easing(self.easing)

    def _start(self) -> None:
        current_color = getattr(self.target, "color")

        self._start_color = current_color if self.from_color is None else self.from_color
        self._end_color = self.to_color

        if self.from_color is not None:
            self.target.color = self._start_color

        self._started = True

    def update(self, dt: float) -> bool:
        if not self.active or self.completed:
            return False

        if self.delay > 0:
            self.delay -= dt
            if self.delay > 0:
                return True

        if not self._started:
            self._start()

        self.elapsed += dt

        t = min(self.elapsed / self.duration, 1.0)
        eased_t = self._easing_func(t)

        self.target.color = tuple(
            self._start_color[i] + (self._end_color[i] -
                                    self._start_color[i]) * eased_t
            for i in range(4)
        )

        if t >= 1.0:
            if self.loop:
                self.elapsed = 0.0

                if self.yoyo:
                    self._start_color, self._end_color = self._end_color, self._start_color

                return True

            self.active = False
            self.completed = True

            if self.on_complete:
                self.on_complete()

            return False

        return True

    def stop(self) -> None:
        self.active = False
        self.completed = True


class AnimationManager:
    """Manage and update multiple animations."""

    def __init__(self):
        self.animations: list[Tween | ColorTween] = []

    def add(self, animation: Tween | ColorTween):
        self.animations.append(animation)
        return animation

    def animate(
        self,
        target: Any,
        attr: str,
        to_value: float,
        duration: float = 0.3,
        easing: str | EasingFunction = "ease_out_quad",
        from_value: float | None = None,
        delay: float = 0.0,
        loop: bool = False,
        yoyo: bool = False,
        on_complete: Callable[[], None] | None = None,
    ) -> Tween:
        tween = Tween(
            target=target,
            attr=attr,
            to_value=to_value,
            duration=duration,
            easing=easing,
            from_value=from_value,
            delay=delay,
            loop=loop,
            yoyo=yoyo,
            on_complete=on_complete,
        )

        return self.add(tween)

    def move_to(
        self,
        target: Any,
        x: float | None = None,
        y: float | None = None,
        duration: float = 0.3,
        easing: str | EasingFunction = "ease_out_quad",
    ) -> list[Tween]:
        tweens = []

        if x is not None:
            tweens.append(self.animate(target, "x", x, duration, easing))

        if y is not None:
            tweens.append(self.animate(target, "y", y, duration, easing))

        return tweens

    def resize_to(
        self,
        target: Any,
        width: float | None = None,
        height: float | None = None,
        duration: float = 0.3,
        easing: str | EasingFunction = "ease_out_quad",
        loop: bool = False,
        yoyo: bool = False,
    ) -> list[Tween]:
        tweens = []

        if width is not None:
            tweens.append(
                self.animate(
                    target,
                    "width",
                    width,
                    duration,
                    easing,
                    loop=loop,
                    yoyo=yoyo,
                )
            )

        if height is not None:
            tweens.append(
                self.animate(
                    target,
                    "height",
                    height,
                    duration,
                    easing,
                    loop=loop,
                    yoyo=yoyo,
                )
            )

        return tweens

    def color_to(
        self,
        target: Any,
        color: tuple[float, float, float, float],
        duration: float = 0.3,
        easing: str | EasingFunction = "ease_out_quad",
        loop: bool = False,
        yoyo: bool = False,
    ) -> ColorTween:
        tween = ColorTween(
            target=target,
            to_color=color,
            duration=duration,
            easing=easing,
            loop=loop,
            yoyo=yoyo,
        )

        return self.add(tween)

    def stop(self, target: Any | None = None, attr: str | None = None) -> None:
        remaining = []

        for animation in self.animations:
            same_target = target is None or animation.target is target
            same_attr = attr is None or getattr(
                animation, "attr", None) == attr

            if same_target and same_attr:
                animation.stop()
            else:
                remaining.append(animation)

        self.animations = remaining

    def clear(self) -> None:
        for animation in self.animations:
            animation.stop()

        self.animations.clear()

    def update(self, dt: float) -> None:
        self.animations = [
            animation
            for animation in self.animations
            if animation.update(dt)
        ]
