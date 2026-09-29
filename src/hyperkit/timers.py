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
    times_fired: int = 0
    times_fired: int = 0

    def __post_init__(self) -> None:
        self.duration = float(self.duration)

        if self.duration <= 0:
            raise TimerError("Timer duration must be greater than 0.")

        self.active = bool(self.auto_start)
        self.completed = False
        self.times_fired = 0

    @property
    def remaining(self) -> float:
        return max(0.0, self.duration - self.elapsed)

    @property
    def progress(self) -> float:
        return min(1.0, self.elapsed / self.duration)

    def start(self, reset: bool = True) -> "Timer":
        if reset:
            self.elapsed = 0.0
            self.completed = False
            self.times_fired = 0

        self.active = True
        return self

    def restart(self) -> "Timer":
        return self.start(reset=True)

    def pause(self) -> "Timer":
        self.active = False
        return self

    def resume(self) -> "Timer":
        if not self.completed:
            self.active = True

        return self

    def stop(self) -> "Timer":
        self.active = False
        self.completed = True
        return self

    def reset(self) -> "Timer":
        self.elapsed = 0.0
        self.completed = False
        self.times_fired = 0
        self.active = bool(self.auto_start)
        return self

    def update(self, dt: float) -> bool:
        """Update timer.

        Returns True only on the frame when the timer completes.
        """
        dt = float(dt)

        if dt < 0:
            raise TimerError("Timer dt must be non-negative.")

        if not self.active or self.completed or dt == 0:
            return False

        self.elapsed += dt

        if self.elapsed < self.duration:
            return False

        if not self.repeat:
            self.elapsed = self.duration
            self.completed = True
            self.active = False
            self.times_fired += 1

            if self.on_complete:
                self.on_complete()

            return True

        fire_count = int(self.elapsed // self.duration)
        self.elapsed = self.elapsed % self.duration

        for _ in range(fire_count):
            self.times_fired += 1

            if self.on_complete:
                self.on_complete()

            if not self.active:
                break

        self.completed = False
        return fire_count > 0


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
        self.duration = float(self.duration)

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

    def update(self, dt: float) -> "Cooldown":
        dt = float(dt)

        if dt < 0:
            raise TimerError("Cooldown dt must be non-negative.")

        self.elapsed = min(self.duration, self.elapsed + dt)
        return self

    def use(self) -> bool:
        """Use the cooldown if ready.

        Returns True if the action is allowed.
        Returns False if still cooling down.
        """
        if not self.ready:
            return False

        self.elapsed = 0.0
        return True

    def reset(self) -> "Cooldown":
        self.elapsed = 0.0
        return self

    def finish(self) -> "Cooldown":
        self.elapsed = self.duration
        return self


class TimerManager:
    """Manage multiple timers."""

    def __init__(self) -> None:
        self.timers: list[Timer] = []

    def add(self, timer: Timer) -> Timer:
        self.timers.append(timer)
        return timer

    def remove(self, timer: Timer, *, stop: bool = True) -> bool:
        """Remove a managed timer."""

        if timer not in self.timers:
            return False

        self.timers.remove(timer)

        if stop:
            timer.stop()

        return True

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
        dt = float(dt)

        if dt < 0:
            raise TimerError("TimerManager dt must be non-negative.")

        remaining_timers: list[Timer] = []

        for timer in list(self.timers):
            timer.update(dt)

            if not timer.completed or timer.repeat:
                remaining_timers.append(timer)

        self.timers = remaining_timers

    def pause_all(self) -> None:
        for timer in self.timers:
            timer.pause()

    def resume_all(self) -> None:
        for timer in self.timers:
            timer.resume()

    def pause_all(self) -> None:
        for timer in self.timers:
            timer.pause()

    def resume_all(self) -> None:
        for timer in self.timers:
            timer.resume()

    def clear(self) -> None:
        for timer in self.timers:
            timer.stop()

        self.timers.clear()
