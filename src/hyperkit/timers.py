from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


class TimerError(Exception):
    """Base error for HyperKit timer helpers."""


@dataclass
class Timer:
    """Simple countdown timer.

    Example:
        timer = Timer(1.0, repeat=True, on_complete=spawn_enemy)

        def update(dt):
            timer.update(dt)
    """

    duration: float
    repeat: bool = False
    auto_start: bool = True
    on_complete: Callable[[], None] | None = None

    elapsed: float = 0.0
    active: bool = False
    completed: bool = False

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise TimerError("Timer duration must be greater than 0.")

        self.active = self.auto_start
        self.completed = False

    @property
    def remaining(self) -> float:
        return max(0.0, self.duration - self.elapsed)

    @property
    def progress(self) -> float:
        return min(1.0, self.elapsed / self.duration)

    def start(self, reset: bool = True) -> None:
        if reset:
            self.elapsed = 0.0
            self.completed = False

        self.active = True

    def restart(self) -> None:
        self.start(reset=True)

    def pause(self) -> None:
        self.active = False

    def resume(self) -> None:
        if not self.completed:
            self.active = True

    def stop(self) -> None:
        self.active = False
        self.completed = True

    def reset(self) -> None:
        self.elapsed = 0.0
        self.completed = False
        self.active = self.auto_start

    def update(self, dt: float) -> bool:
        """Update timer.

        Returns True only on the frame when the timer completes.
        """
        if not self.active or self.completed:
            return False

        self.elapsed += max(0.0, dt)

        if self.elapsed < self.duration:
            return False

        if self.on_complete:
            self.on_complete()

        if self.repeat:
            self.elapsed = self.elapsed % self.duration
            self.completed = False
            self.active = True
        else:
            self.elapsed = self.duration
            self.completed = True
            self.active = False

        return True


@dataclass
class Cooldown:
    """Cooldown helper for actions.

    Example:
        jump_cooldown = Cooldown(0.5)

        if jump_cooldown.use():
            jump()
    """

    duration: float
    start_ready: bool = True

    elapsed: float = 0.0

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise TimerError("Cooldown duration must be greater than 0.")

        self.elapsed = self.duration if self.start_ready else 0.0

    @property
    def ready(self) -> bool:
        return self.elapsed >= self.duration

    @property
    def remaining(self) -> float:
        return max(0.0, self.duration - self.elapsed)

    @property
    def progress(self) -> float:
        return min(1.0, self.elapsed / self.duration)

    def update(self, dt: float) -> None:
        self.elapsed = min(self.duration, self.elapsed + max(0.0, dt))

    def use(self) -> bool:
        """Use the cooldown if ready.

        Returns True if the action is allowed.
        Returns False if still cooling down.
        """
        if not self.ready:
            return False

        self.elapsed = 0.0
        return True

    def reset(self) -> None:
        self.elapsed = 0.0

    def finish(self) -> None:
        self.elapsed = self.duration


class TimerManager:
    """Manage multiple timers."""

    def __init__(self) -> None:
        self.timers: list[Timer] = []

    def add(self, timer: Timer) -> Timer:
        self.timers.append(timer)
        return timer

    def after(self, duration: float, callback: Callable[[], None]) -> Timer:
        """Run callback once after duration."""
        return self.add(
            Timer(
                duration=duration,
                repeat=False,
                auto_start=True,
                on_complete=callback,
            )
        )

    def every(self, duration: float, callback: Callable[[], None]) -> Timer:
        """Run callback repeatedly every duration."""
        return self.add(
            Timer(
                duration=duration,
                repeat=True,
                auto_start=True,
                on_complete=callback,
            )
        )

    def update(self, dt: float) -> None:
        remaining_timers: list[Timer] = []

        for timer in self.timers:
            timer.update(dt)

            if not timer.completed or timer.repeat:
                remaining_timers.append(timer)

        self.timers = remaining_timers

    def clear(self) -> None:
        for timer in self.timers:
            timer.stop()

        self.timers.clear()
