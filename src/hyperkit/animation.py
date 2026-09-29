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
        self.duration = float(self.duration)
        self.delay = float(self.delay)
        self.attr = str(self.attr).strip()

        if self.duration <= 0:
            raise ValueError("Tween duration must be greater than 0.")

        if self.delay < 0:
            raise ValueError("Tween delay cannot be negative.")

        if not self.attr:
            raise ValueError("Tween attr must not be empty.")

        self._easing_func = get_easing(self.easing)

    def _start(self) -> None:
        if not hasattr(self.target, self.attr):
            raise AttributeError(
                f"Tween target has no attribute '{self.attr}'."
            )

        current_value = float(getattr(self.target, self.attr))

        self._start_value = current_value if self.from_value is None else float(
            self.from_value)
        self._end_value = float(self.to_value)

        if self.from_value is not None:
            setattr(self.target, self.attr, self._start_value)

        self._started = True

    def update(self, dt: float) -> bool:
        dt = float(dt)

        if dt < 0:
            raise ValueError("Tween dt cannot be negative.")

        if not self.active or self.completed:
            return False

        if self.delay > 0:
            if dt <= self.delay:
                self.delay -= dt
                return True

            dt -= self.delay
            self.delay = 0.0

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
                self.elapsed = self.elapsed % self.duration

                if self.yoyo:
                    self._start_value, self._end_value = self._end_value, self._start_value

                if self.elapsed > 0:
                    loop_t = self.elapsed / self.duration
                    loop_eased = self._easing_func(loop_t)
                    loop_value = self._start_value + (
                        self._end_value - self._start_value
                    ) * loop_eased
                    setattr(self.target, self.attr, loop_value)

                return True

            self.active = False
            self.completed = True

            if self.on_complete:
                self.on_complete()

            return False

        return True

    def stop(self) -> "Tween":
        self.active = False
        self.completed = True
        return self


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
        self.duration = float(self.duration)
        self.delay = float(self.delay)

        if self.duration <= 0:
            raise ValueError("ColorTween duration must be greater than 0.")

        if self.delay < 0:
            raise ValueError("ColorTween delay cannot be negative.")

        if len(self.to_color) != 4:
            raise ValueError("ColorTween to_color must contain 4 values.")

        if self.from_color is not None and len(self.from_color) != 4:
            raise ValueError("ColorTween from_color must contain 4 values.")

        self.to_color = tuple(float(value) for value in self.to_color)

        if self.from_color is not None:
            self.from_color = tuple(float(value) for value in self.from_color)

        self._easing_func = get_easing(self.easing)

    def _start(self) -> None:
        current_color = getattr(self.target, "color")

        self._start_color = current_color if self.from_color is None else self.from_color
        self._end_color = self.to_color

        if self.from_color is not None:
            self.target.color = self._start_color

        self._started = True

    def update(self, dt: float) -> bool:
        dt = float(dt)

        if dt < 0:
            raise ValueError("ColorTween dt cannot be negative.")

        if not self.active or self.completed:
            return False

        if self.delay > 0:
            if dt <= self.delay:
                self.delay -= dt
                return True

            dt -= self.delay
            self.delay = 0.0

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
                self.elapsed = self.elapsed % self.duration

                if self.yoyo:
                    self._start_color, self._end_color = self._end_color, self._start_color

                if self.elapsed > 0:
                    loop_t = self.elapsed / self.duration
                    loop_eased = self._easing_func(loop_t)
                    self.target.color = tuple(
                        self._start_color[i] + (
                            self._end_color[i] - self._start_color[i]
                        ) * loop_eased
                        for i in range(4)
                    )

                return True

            self.active = False
            self.completed = True

            if self.on_complete:
                self.on_complete()

            return False

        return True

    def stop(self) -> "ColorTween":
        self.active = False
        self.completed = True
        return self


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

    def stop(self, target: Any | None = None, attr: str | None = None) -> int:
        remaining = []
        stopped = 0

        for animation in self.animations:
            same_target = target is None or animation.target is target
            same_attr = attr is None or getattr(
                animation, "attr", None) == attr

            if same_target and same_attr:
                animation.stop()
                stopped += 1
            else:
                remaining.append(animation)

        self.animations = remaining
        return stopped

    def clear(self) -> int:
        count = len(self.animations)

        for animation in self.animations:
            animation.stop()

        self.animations.clear()
        return count

    def update(self, dt: float) -> None:
        dt = float(dt)

        if dt < 0:
            raise ValueError("AnimationManager dt cannot be negative.")
        self.animations = [
            animation
            for animation in self.animations
            if animation.update(dt)
        ]
