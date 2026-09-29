"""Developer-facing runtime diagnostics for HyperKit."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque

from .ui import TextLabel


@dataclass(frozen=True)
class RuntimeSnapshot:
    """Immutable runtime performance snapshot."""

    fps: float
    frame_ms: float
    frame_count: int
    elapsed_seconds: float
    dropped_frames: int

    def as_dict(self) -> dict[str, float | int]:
        return {
            "fps": self.fps,
            "frame_ms": self.frame_ms,
            "frame_count": self.frame_count,
            "elapsed_seconds": self.elapsed_seconds,
            "dropped_frames": self.dropped_frames,
        }


class RuntimeDiagnostics:
    """Track lightweight frame timing information.

    The helper is intentionally renderer-independent so it can be used
    from desktop, Android, tests, or custom game loops.
    """

    def __init__(
        self,
        *,
        target_fps: float = 60.0,
        sample_window: int = 60,
    ) -> None:
        target_fps = float(target_fps)
        sample_window = int(sample_window)

        if target_fps <= 0:
            raise ValueError(
                "target_fps must be greater than zero."
            )

        if sample_window <= 0:
            raise ValueError(
                "sample_window must be greater than zero."
            )

        self.target_fps = target_fps
        self.sample_window = sample_window
        self._samples: Deque[float] = deque(
            maxlen=sample_window
        )
        self.frame_count = 0
        self.elapsed_seconds = 0.0
        self.dropped_frames = 0

    @property
    def fps(self) -> float:
        if not self._samples:
            return 0.0

        average_dt = (
            sum(self._samples)
            / len(self._samples)
        )

        if average_dt <= 0:
            return 0.0

        return 1.0 / average_dt

    @property
    def frame_ms(self) -> float:
        if not self._samples:
            return 0.0

        return (
            sum(self._samples)
            / len(self._samples)
            * 1000.0
        )

    def update(
        self,
        dt: float,
    ) -> RuntimeSnapshot:
        dt = float(dt)

        if dt < 0:
            raise ValueError(
                "dt cannot be negative."
            )

        self.frame_count += 1
        self.elapsed_seconds += dt

        if dt > 0:
            self._samples.append(
                dt
            )

            expected_dt = (
                1.0
                / self.target_fps
            )

            if dt > expected_dt * 1.5:
                self.dropped_frames += 1

        return self.snapshot()

    def snapshot(
        self,
    ) -> RuntimeSnapshot:
        return RuntimeSnapshot(
            fps=self.fps,
            frame_ms=self.frame_ms,
            frame_count=self.frame_count,
            elapsed_seconds=self.elapsed_seconds,
            dropped_frames=self.dropped_frames,
        )

    def reset(
        self,
    ) -> "RuntimeDiagnostics":
        self._samples.clear()
        self.frame_count = 0
        self.elapsed_seconds = 0.0
        self.dropped_frames = 0
        return self


class DebugOverlay:
    """Small on-screen runtime diagnostics overlay."""

    def __init__(
        self,
        scene,
        *,
        x: float = 20,
        y: float = 20,
        font_size: int = 18,
        target_fps: float = 60.0,
        visible: bool = True,
    ) -> None:
        if scene is None or not hasattr(
            scene,
            "add",
        ):
            raise ValueError(
                "DebugOverlay requires a scene with add()."
            )

        self.scene = scene
        self.diagnostics = RuntimeDiagnostics(
            target_fps=target_fps
        )
        self.label = scene.add(
            TextLabel(
                x=x,
                y=y,
                text="FPS: --",
                font_size=font_size,
                color=(0.8, 1.0, 0.8, 1.0),
            )
        )
        self.visible = bool(
            visible
        )
        self.label.visible = self.visible

    def update(
        self,
        dt: float,
    ) -> RuntimeSnapshot:
        snapshot = self.diagnostics.update(
            dt
        )

        self.label.set_text(
            "FPS: "
            f"{snapshot.fps:.1f} | "
            "Frame: "
            f"{snapshot.frame_ms:.2f} ms | "
            "Dropped: "
            f"{snapshot.dropped_frames}"
        )

        return snapshot

    def show(
        self,
    ) -> "DebugOverlay":
        self.visible = True
        self.label.visible = True
        return self

    def hide(
        self,
    ) -> "DebugOverlay":
        self.visible = False
        self.label.visible = False
        return self

    def toggle(
        self,
    ) -> bool:
        if self.visible:
            self.hide()
        else:
            self.show()

        return self.visible
