from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .object import GameObject


class SceneTransitionError(Exception):
    """Base error for scene transition helpers."""


@dataclass
class SceneTransition:
    """Simple fade transition helper for HyperKit scenes."""

    scene: Any
    color: tuple[
        float,
        float,
        float,
    ] = (
        0,
        0,
        0,
    )

    def __post_init__(
        self,
    ) -> None:
        if len(
            self.color
        ) != 3:
            raise SceneTransitionError(
                "SceneTransition color must contain RGB values."
            )

        self.color = tuple(
            max(
                0.0,
                min(
                    1.0,
                    float(value),
                ),
            )
            for value in self.color
        )

        self.overlay: GameObject | None = None
        self.mode: str = "idle"
        self.duration: float = 0.0
        self.elapsed: float = 0.0
        self.from_alpha: float = 0.0
        self.to_alpha: float = 0.0
        self.on_complete: Callable[
            [],
            None,
        ] | None = None

        self._ensure_overlay()

    @property
    def alpha(
        self,
    ) -> float:
        if self.overlay is None:
            return 0.0

        return float(
            self.overlay.color[
                3
            ]
        )

    @property
    def progress(
        self,
    ) -> float:
        if self.mode == "idle":
            return 1.0

        if self.duration <= 0:
            return 1.0

        return max(
            0.0,
            min(
                self.elapsed
                / self.duration,
                1.0,
            ),
        )

    def _scene_size(
        self,
    ) -> tuple[
        float,
        float,
    ]:
        game = getattr(
            self.scene,
            "game",
            None,
        )

        if game is not None:
            return (
                float(
                    getattr(
                        game,
                        "width",
                        720,
                    )
                ),
                float(
                    getattr(
                        game,
                        "height",
                        1280,
                    )
                ),
            )

        return (
            720.0,
            1280.0,
        )

    def _ensure_overlay(
        self,
    ) -> GameObject:
        if self.overlay is not None:
            return self.overlay

        width, height = (
            self._scene_size()
        )

        self.overlay = GameObject(
            x=0,
            y=0,
            width=width,
            height=height,
            color=(
                self.color[
                    0
                ],
                self.color[
                    1
                ],
                self.color[
                    2
                ],
                0.0,
            ),
            shape="rect",
            name="scene_transition_overlay",
        )

        self.scene.add(
            self.overlay
        )
        self._move_overlay_to_top()

        return self.overlay

    def _move_overlay_to_top(
        self,
    ) -> None:
        if self.overlay is None:
            return

        objects = getattr(
            self.scene,
            "objects",
            None,
        )

        if objects is None:
            return

        if self.overlay in objects:
            objects.remove(
                self.overlay
            )
            objects.append(
                self.overlay
            )

    def _set_alpha(
        self,
        alpha: float,
    ) -> None:
        overlay = (
            self._ensure_overlay()
        )

        alpha = max(
            0.0,
            min(
                1.0,
                float(
                    alpha
                ),
            ),
        )

        r, g, b = self.color

        overlay.color = (
            r,
            g,
            b,
            alpha,
        )
        overlay.visible = (
            alpha > 0
        )
        overlay.active = True

        self._move_overlay_to_top()

    def fade_in(
        self,
        duration: float = 0.4,
        on_complete: Callable[
            [],
            None,
        ] | None = None,
    ) -> "SceneTransition":
        """Fade from the transition color to transparent."""

        return self._start(
            mode="fade_in",
            from_alpha=1.0,
            to_alpha=0.0,
            duration=duration,
            on_complete=on_complete,
        )

    def fade_out(
        self,
        duration: float = 0.4,
        on_complete: Callable[
            [],
            None,
        ] | None = None,
    ) -> "SceneTransition":
        """Fade from transparent to the transition color."""

        return self._start(
            mode="fade_out",
            from_alpha=0.0,
            to_alpha=1.0,
            duration=duration,
            on_complete=on_complete,
        )

    def fade_to_scene(
        self,
        next_scene: Any,
        duration: float = 0.4,
    ) -> "SceneTransition":
        """Fade out, then switch to another scene."""

        game = getattr(
            self.scene,
            "game",
            None,
        )

        if game is None:
            raise SceneTransitionError(
                "SceneTransition.fade_to_scene requires "
                "a scene bound to a Game."
            )

        if not hasattr(
            game,
            "change_scene",
        ):
            raise SceneTransitionError(
                "Game.change_scene() is required "
                "for scene transitions."
            )

        def change_scene_after_fade(
        ) -> None:
            game.change_scene(
                next_scene
            )

        return self.fade_out(
            duration=duration,
            on_complete=change_scene_after_fade,
        )

    def _start(
        self,
        mode: str,
        from_alpha: float,
        to_alpha: float,
        duration: float,
        on_complete: Callable[
            [],
            None,
        ] | None = None,
    ) -> "SceneTransition":
        duration = float(
            duration
        )

        if duration < 0:
            raise SceneTransitionError(
                "Transition duration must be non-negative."
            )

        self.mode = mode
        self.duration = duration
        self.elapsed = 0.0
        self.from_alpha = float(
            from_alpha
        )
        self.to_alpha = float(
            to_alpha
        )
        self.on_complete = (
            on_complete
        )

        if duration == 0:
            callback = (
                self.on_complete
            )
            self._set_alpha(
                self.to_alpha
            )
            self.mode = "idle"
            self.on_complete = None

            if (
                self.overlay is not None
                and self.to_alpha <= 0
            ):
                self.overlay.visible = False

            if callback is not None:
                callback()

            return self

        self._set_alpha(
            self.from_alpha
        )

        return self

    def update(
        self,
        dt: float,
    ) -> None:
        dt = float(
            dt
        )

        if dt < 0:
            raise SceneTransitionError(
                "Transition dt must be non-negative."
            )

        if self.mode == "idle":
            return

        self.elapsed += dt

        progress = (
            self.progress
        )

        alpha = (
            self.from_alpha
            + (
                self.to_alpha
                - self.from_alpha
            )
            * progress
        )

        self._set_alpha(
            alpha
        )

        if progress >= 1.0:
            callback = (
                self.on_complete
            )

            self.mode = "idle"
            self.on_complete = None

            if (
                self.overlay is not None
                and self.to_alpha <= 0
            ):
                self.overlay.visible = False

            if callback is not None:
                callback()

    def is_running(
        self,
    ) -> bool:
        return (
            self.mode
            != "idle"
        )

    def stop(
        self,
    ) -> None:
        self.mode = "idle"
        self.elapsed = 0.0
        self.duration = 0.0
        self.on_complete = None
        self._set_alpha(
            0.0
        )

        if self.overlay is not None:
            self.overlay.visible = False
