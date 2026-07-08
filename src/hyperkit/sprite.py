from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class SpriteAnimationError(Exception):
    """Base error for sprite animation."""


@dataclass
class SpriteAnimation:
    """Frame-based sprite animation.

    Example:
        SpriteAnimation(
            name="run",
            frames=["run_1.png", "run_2.png", "run_3.png"],
            fps=8,
            loop=True,
        )
    """

    name: str
    frames: list[str]
    fps: float = 8.0
    loop: bool = True
    on_complete: Callable[[], None] | None = None

    current_index: int = 0
    elapsed: float = 0.0
    playing: bool = True
    completed: bool = False

    def __post_init__(self) -> None:
        if not self.frames:
            raise SpriteAnimationError(
                "SpriteAnimation requires at least one frame.")

        if self.fps <= 0:
            raise SpriteAnimationError(
                "SpriteAnimation fps must be greater than 0.")

    @property
    def frame_duration(self) -> float:
        return 1.0 / self.fps

    @property
    def current_frame(self) -> str:
        return self.frames[self.current_index]

    def reset(self) -> None:
        self.current_index = 0
        self.elapsed = 0.0
        self.playing = True
        self.completed = False

    def play(self, restart: bool = False) -> None:
        if restart:
            self.reset()
            return

        self.playing = True
        self.completed = False

    def pause(self) -> None:
        self.playing = False

    def stop(self) -> None:
        self.current_index = 0
        self.elapsed = 0.0
        self.playing = False
        self.completed = True

    def update(self, dt: float) -> str:
        if not self.playing or self.completed:
            return self.current_frame

        self.elapsed += dt

        while self.elapsed >= self.frame_duration and self.playing and not self.completed:
            self.elapsed -= self.frame_duration
            self._advance_frame()

        return self.current_frame

    def _advance_frame(self) -> None:
        next_index = self.current_index + 1

        if next_index < len(self.frames):
            self.current_index = next_index
            return

        if self.loop:
            self.current_index = 0
            return

        self.current_index = len(self.frames) - 1
        self.playing = False
        self.completed = True

        if self.on_complete:
            self.on_complete()


class SpriteAnimator:
    """Controls sprite animations for a GameObject.

    It updates the target object's image_path.
    """

    def __init__(self, target: Any | None = None):
        self.target = target
        self.animations: dict[str, SpriteAnimation] = {}
        self.current_name: str | None = None

    @property
    def current_animation(self) -> SpriteAnimation | None:
        if self.current_name is None:
            return None

        return self.animations.get(self.current_name)

    def set_target(self, target: Any) -> None:
        self.target = target

        animation = self.current_animation
        if animation is not None:
            self._set_target_frame(animation.current_frame)

    def add_animation(
        self,
        name: str,
        frames: list[str],
        fps: float = 8.0,
        loop: bool = True,
        on_complete: Callable[[], None] | None = None,
    ) -> SpriteAnimation:
        animation = SpriteAnimation(
            name=name,
            frames=frames,
            fps=fps,
            loop=loop,
            on_complete=on_complete,
        )

        self.animations[name] = animation

        if self.current_name is None:
            self.current_name = name
            self._set_target_frame(animation.current_frame)

        return animation

    def play(self, name: str, restart: bool = True) -> SpriteAnimation:
        if name not in self.animations:
            available = ", ".join(self.animations.keys())
            raise SpriteAnimationError(
                f"Unknown sprite animation '{name}'. Available animations: {available}"
            )

        self.current_name = name
        animation = self.animations[name]
        animation.play(restart=restart)
        self._set_target_frame(animation.current_frame)

        return animation

    def pause(self) -> None:
        animation = self.current_animation

        if animation is not None:
            animation.pause()

    def resume(self) -> None:
        animation = self.current_animation

        if animation is not None:
            animation.play(restart=False)

    def stop(self) -> None:
        animation = self.current_animation

        if animation is not None:
            animation.stop()
            self._set_target_frame(animation.current_frame)

    def update(self, dt: float) -> str | None:
        animation = self.current_animation

        if animation is None:
            return None

        frame = animation.update(dt)
        self._set_target_frame(frame)

        return frame

    def _set_target_frame(self, frame: str) -> None:
        if self.target is None:
            return

        if hasattr(self.target, "set_image"):
            self.target.set_image(frame)
        else:
            self.target.image_path = frame
