"""Mobile runtime frame and performance helpers for HyperKit."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PerformanceMode(str, Enum):
    """Common mobile performance targets."""

    BATTERY = "battery"
    BALANCED = "balanced"
    PERFORMANCE = "performance"


@dataclass(frozen=True)
class PerformanceProfile:
    """Runtime performance policy for a HyperKit game."""

    target_fps: int = 60
    max_frame_delta: float = 0.1
    fixed_step: float = 1.0 / 60.0
    max_substeps: int = 5

    def __post_init__(self) -> None:
        if self.target_fps <= 0:
            raise ValueError(
                "target_fps must be greater than zero."
            )

        if self.max_frame_delta <= 0:
            raise ValueError(
                "max_frame_delta must be greater than zero."
            )

        if self.fixed_step <= 0:
            raise ValueError(
                "fixed_step must be greater than zero."
            )

        if self.max_substeps <= 0:
            raise ValueError(
                "max_substeps must be greater than zero."
            )

    @classmethod
    def from_mode(
        cls,
        mode: PerformanceMode | str,
    ) -> "PerformanceProfile":
        try:
            normalized = (
                mode
                if isinstance(
                    mode,
                    PerformanceMode,
                )
                else PerformanceMode(
                    str(mode)
                    .strip()
                    .lower()
                )
            )
        except ValueError as exc:
            raise ValueError(
                "Unsupported performance mode. "
                "Choose battery, balanced, "
                "or performance."
            ) from exc

        if normalized == PerformanceMode.BATTERY:
            return cls(
                target_fps=30,
                max_frame_delta=0.15,
                fixed_step=1.0 / 30.0,
                max_substeps=3,
            )

        if normalized == PerformanceMode.PERFORMANCE:
            return cls(
                target_fps=60,
                max_frame_delta=0.075,
                fixed_step=1.0 / 60.0,
                max_substeps=6,
            )

        return cls()


class FrameTimeController:
    """Clamp frame delta and track runtime hitch information."""

    def __init__(
        self,
        profile: PerformanceProfile | None = None,
    ) -> None:
        self.profile = (
            profile
            if profile is not None
            else PerformanceProfile()
        )

        if not isinstance(
            self.profile,
            PerformanceProfile,
        ):
            raise TypeError(
                "profile must be a PerformanceProfile."
            )

        self.frame_count = 0
        self.hitch_count = 0
        self.clamped_time = 0.0
        self.last_raw_dt = 0.0
        self.last_dt = 0.0

    def normalize(
        self,
        dt: float,
    ) -> float:
        raw_dt = float(
            dt
        )

        if raw_dt < 0:
            raise ValueError(
                "dt cannot be negative."
            )

        normalized = min(
            raw_dt,
            self.profile.max_frame_delta,
        )

        self.frame_count += 1
        self.last_raw_dt = raw_dt
        self.last_dt = normalized

        if raw_dt > normalized:
            self.hitch_count += 1
            self.clamped_time += (
                raw_dt
                - normalized
            )

        return normalized

    def reset(
        self,
    ) -> "FrameTimeController":
        self.frame_count = 0
        self.hitch_count = 0
        self.clamped_time = 0.0
        self.last_raw_dt = 0.0
        self.last_dt = 0.0
        return self


class FixedStepClock:
    """Accumulate variable frame time into bounded fixed simulation steps."""

    def __init__(
        self,
        *,
        step: float = 1.0 / 60.0,
        max_substeps: int = 5,
    ) -> None:
        step = float(
            step
        )
        max_substeps = int(
            max_substeps
        )

        if step <= 0:
            raise ValueError(
                "step must be greater than zero."
            )

        if max_substeps <= 0:
            raise ValueError(
                "max_substeps must be greater than zero."
            )

        self.step = step
        self.max_substeps = max_substeps
        self.accumulator = 0.0
        self.dropped_time = 0.0

    @property
    def alpha(
        self,
    ) -> float:
        return min(
            1.0,
            self.accumulator
            / self.step,
        )

    def advance(
        self,
        dt: float,
    ) -> int:
        dt = float(
            dt
        )

        if dt < 0:
            raise ValueError(
                "dt cannot be negative."
            )

        self.accumulator += dt

        steps = min(
            int(
                self.accumulator
                / self.step
            ),
            self.max_substeps,
        )

        consumed = (
            steps
            * self.step
        )

        self.accumulator -= consumed

        max_backlog = (
            self.step
            * self.max_substeps
        )

        if self.accumulator > max_backlog:
            self.dropped_time += (
                self.accumulator
                - max_backlog
            )
            self.accumulator = max_backlog

        return steps

    def reset(
        self,
    ) -> "FixedStepClock":
        self.accumulator = 0.0
        self.dropped_time = 0.0
        return self
