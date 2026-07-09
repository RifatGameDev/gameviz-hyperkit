from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .object import GameObject


class SceneTransitionError(Exception):
    """Base error for scene transition helpers."""


@dataclass
class SceneTransition:
    """Simple fade transition helper for HyperKit scenes.

    Usage:
        self.transition = SceneTransition(self)
        self.transition.fade_in()

    In update:
        self.transition.update(dt)
    """

    scene: Any
    color: tuple[float, float, float] = (0, 0, 0)

    def __post_init__(self) -> None:
        self.overlay: GameObject | None = None
        self.mode: str = "idle"
        self.duration: float = 0.0
        self.elapsed: float = 0.0
        self.from_alpha: float = 0.0
        self.to_alpha: float = 0.0
        self.on_complete: Callable[[], None] | None = None
        self._ensure_overlay()

    def _scene_size(self) -> tuple[float, float]:
        game = getattr(self.scene, "game", None)

        if game is not None:
            return float(getattr(game, "width", 720)), float(getattr(game, "height", 1280))

        return 720.0, 1280.0

    def _ensure_overlay(self) -> GameObject:
        if self.overlay is not None:
            return self.overlay

        width, height = self._scene_size()

        self.overlay = GameObject(
            x=0,
            y=0,
            width=width,
            height=height,
            color=(self.color[0], self.color[1], self.color[2], 0.0),
            shape="rectangle",
            name="scene_transition_overlay",
        )

        self.scene.add(self.overlay)
        self._move_overlay_to_top()

        return self.overlay

    def _move_overlay_to_top(self) -> None:
        if self.overlay is None:
            return

        objects = getattr(self.scene, "objects", None)

        if objects is None:
            return

        if self.overlay in objects:
            objects.remove(self.overlay)
            objects.append(self.overlay)

    def _set_alpha(self, alpha: float) -> None:
        overlay = self._ensure_overlay()

        alpha = max(0.0, min(1.0, float(alpha)))
        r, g, b = self.color

        overlay.color = (r, g, b, alpha)
        overlay.visible = alpha > 0
        overlay.active = True

        self._move_overlay_to_top()

    def fade_in(
        self,
        duration: float = 0.4,
        on_complete: Callable[[], None] | None = None,
    ) -> None:
        """Fade from black to transparent."""
        self._start(
            mode="fade_in",
            from_alpha=1.0,
            to_alpha=0.0,
            duration=duration,
            on_complete=on_complete,
        )

    def fade_out(
        self,
        duration: float = 0.4,
        on_complete: Callable[[], None] | None = None,
    ) -> None:
        """Fade from transparent to black."""
        self._start(
            mode="fade_out",
            from_alpha=0.0,
            to_alpha=1.0,
            duration=duration,
            on_complete=on_complete,
        )

    def fade_to_scene(self, next_scene: Any, duration: float = 0.4) -> None:
        """Fade out, then switch to another scene."""
        game = getattr(self.scene, "game", None)

        if game is None:
            raise SceneTransitionError(
                "SceneTransition.fade_to_scene requires a scene bound to a Game.")

        if not hasattr(game, "change_scene"):
            raise SceneTransitionError(
                "Game.change_scene() is required for scene transitions.")

        def change_scene_after_fade() -> None:
            game.change_scene(next_scene)

        self.fade_out(duration=duration, on_complete=change_scene_after_fade)

    def _start(
        self,
        mode: str,
        from_alpha: float,
        to_alpha: float,
        duration: float,
        on_complete: Callable[[], None] | None = None,
    ) -> None:
        if duration <= 0:
            self._set_alpha(to_alpha)
            if on_complete:
                on_complete()
            return

        self.mode = mode
        self.duration = float(duration)
        self.elapsed = 0.0
        self.from_alpha = float(from_alpha)
        self.to_alpha = float(to_alpha)
        self.on_complete = on_complete

        self._set_alpha(self.from_alpha)

    def update(self, dt: float) -> None:
        if self.mode == "idle":
            return

        self.elapsed += dt

        progress = min(self.elapsed / self.duration, 1.0)
        alpha = self.from_alpha + (self.to_alpha - self.from_alpha) * progress

        self._set_alpha(alpha)

        if progress >= 1.0:
            callback = self.on_complete

            self.mode = "idle"
            self.on_complete = None

            if self.overlay is not None and self.to_alpha <= 0:
                self.overlay.visible = False

            if callback:
                callback()

    def is_running(self) -> bool:
        return self.mode != "idle"

    def stop(self) -> None:
        self.mode = "idle"
        self.on_complete = None
        self._set_alpha(0.0)

        if self.overlay is not None:
            self.overlay.visible = False
