from __future__ import annotations

from typing import Optional, Tuple, Union

from .environment import (
    RuntimeEnvironment,
    detect_runtime_environment,
)
from .input import TouchTracker
from .layout import CanvasScaler
from .mobile import (
    DisplayOrientation,
    MobileDisplayProfile,
    MobileViewport,
    SafeAreaInsets,
)
from .performance import (
    FrameTimeController,
    PerformanceProfile,
)
from .scene import Scene


ColorValue = Tuple[
    float,
    float,
    float,
    float,
]


class Game:
    """Kivy-backed HyperKit game runner.

    HyperKit renders against a virtual resolution and scales the game
    to the available desktop or mobile viewport.
    """

    def __init__(
        self,
        title: str = "HyperKit Game",
        width: int = 720,
        height: int = 1280,
        fps: int = 60,
        background_color: ColorValue = (
            0.08,
            0.08,
            0.1,
            1.0,
        ),
        *,
        orientation: Union[
            str,
            DisplayOrientation,
        ] = DisplayOrientation.AUTO,
        fullscreen: Optional[
            bool
        ] = None,
        safe_area: Optional[
            SafeAreaInsets
        ] = None,
        use_safe_area: bool = True,
        performance_profile: Optional[
            PerformanceProfile
        ] = None,
        touch_move_min_distance: float = 0.0,
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(
                "Game width and height "
                "must be greater than zero."
            )

        if fps <= 0:
            raise ValueError(
                "Game fps must be "
                "greater than zero."
            )

        self.title = title

        if performance_profile is None:
            performance_profile = (
                PerformanceProfile(
                    target_fps=int(
                        fps
                    ),
                    fixed_step=(
                        1.0
                        / int(
                            fps
                        )
                    ),
                )
            )

        if not isinstance(
            performance_profile,
            PerformanceProfile,
        ):
            raise TypeError(
                "performance_profile must be "
                "a PerformanceProfile instance."
            )

        self.performance_profile = (
            performance_profile
        )
        self.fps = (
            performance_profile
            .target_fps
        )
        self.frame_time = (
            FrameTimeController(
                performance_profile
            )
        )

        if touch_move_min_distance < 0:
            raise ValueError(
                "touch_move_min_distance "
                "cannot be negative."
            )

        self.touch_move_min_distance = float(
            touch_move_min_distance
        )

        self.background_color = (
            background_color
        )

        self.environment: (
            RuntimeEnvironment
        ) = detect_runtime_environment()

        self.display_profile = (
            MobileDisplayProfile(
                virtual_width=int(
                    width
                ),
                virtual_height=int(
                    height
                ),
                orientation=orientation,
                fullscreen=fullscreen,
                use_safe_area=(
                    use_safe_area
                ),
                safe_area=(
                    safe_area
                    if safe_area
                    is not None
                    else SafeAreaInsets()
                ),
            )
        )

        (
            self.width,
            self.height,
        ) = (
            self.display_profile
            .virtual_size
        )

        self.scene: Optional[
            Scene
        ] = None

        self._app = None
        self._widget = None
        self._paused = False
        self._backgrounded = False
        self._stopped = False

    @property
    def is_paused(
        self,
    ) -> bool:
        return self._paused

    @property
    def is_backgrounded(
        self,
    ) -> bool:
        return self._backgrounded

    @property
    def is_stopped(
        self,
    ) -> bool:
        return self._stopped

    @property
    def is_mobile(
        self,
    ) -> bool:
        return (
            self.environment
            .is_mobile
        )

    def performance_stats(
        self,
    ) -> dict[str, float | int]:
        return {
            "target_fps": (
                self.performance_profile
                .target_fps
            ),
            "frame_count": (
                self.frame_time
                .frame_count
            ),
            "hitch_count": (
                self.frame_time
                .hitch_count
            ),
            "clamped_time": (
                self.frame_time
                .clamped_time
            ),
            "last_raw_dt": (
                self.frame_time
                .last_raw_dt
            ),
            "last_dt": (
                self.frame_time
                .last_dt
            ),
        }

    @property
    def fullscreen(
        self,
    ) -> bool:
        return (
            self.display_profile
            .resolve_fullscreen(
                is_mobile=(
                    self.is_mobile
                )
            )
        )

    def update_safe_area(
        self,
        safe_area: SafeAreaInsets,
    ) -> "Game":
        self.display_profile = (
            self.display_profile
            .with_safe_area(
                safe_area
            )
        )

        return self

    def set_scene(
        self,
        scene: Scene,
    ) -> "Game":
        self.scene = scene

        scene.bind_game(
            self
        )

        return self

    def change_scene(
        self,
        scene: Scene,
    ) -> "Game":
        previous_scene = (
            self.scene
        )

        if (
            previous_scene is not None
            and previous_scene is not scene
        ):
            stop_hook = getattr(
                previous_scene,
                "on_stop",
                None,
            )

            if callable(
                stop_hook
            ):
                stop_hook()

            release = getattr(
                previous_scene,
                "release_resources",
                None,
            )

            if callable(
                release
            ):
                release()

            if hasattr(
                previous_scene,
                "started",
            ):
                previous_scene.started = False

        self.scene = scene

        scene.bind_game(
            self
        )

        if not scene.started:
            scene.started = True
            scene.start()

        return self

    def _call_scene_hook(
        self,
        name: str,
    ) -> None:
        if self.scene is None:
            return

        callback = getattr(
            self.scene,
            name,
            None,
        )

        if callable(
            callback
        ):
            callback()

    def _cancel_active_touches(
        self,
    ) -> int:
        widget = self._widget

        if widget is None:
            return 0

        tracker = getattr(
            widget,
            "touch_tracker",
            None,
        )

        if tracker is None:
            return 0

        cancel_all = getattr(
            tracker,
            "cancel_all",
            None,
        )

        if not callable(
            cancel_all
        ):
            return 0

        result = cancel_all()

        return (
            int(result)
            if result is not None
            else 0
        )

    def pause(
        self,
    ) -> None:
        if (
            self._paused
            or self._stopped
        ):
            return

        self._paused = True
        self._cancel_active_touches()

        self._call_scene_hook(
            "on_pause"
        )

    def background(
        self,
    ) -> None:
        if (
            self._backgrounded
            or self._stopped
        ):
            return

        self._backgrounded = True
        self._paused = True
        self._cancel_active_touches()

        self._call_scene_hook(
            "on_background"
        )

    def resume(
        self,
    ) -> None:
        if self._stopped:
            return

        was_suspended = (
            self._paused
            or self._backgrounded
        )

        self._paused = False
        self._backgrounded = False

        if was_suspended:
            self._call_scene_hook(
                "on_resume"
            )

    def stop(
        self,
    ) -> None:
        if self._stopped:
            return

        self._stopped = True
        self._paused = True
        self._backgrounded = False
        self._cancel_active_touches()

        self._call_scene_hook(
            "on_stop"
        )

        if self.scene is not None:
            release = getattr(
                self.scene,
                "release_resources",
                None,
            )

            if callable(
                release
            ):
                release()

    def run(
        self,
    ) -> None:
        if self.scene is None:
            raise RuntimeError(
                "No scene set. "
                "Use Game(...).set_scene("
                "MyScene()).run()."
            )

        try:
            from kivy.app import App
            from kivy.clock import Clock

            from kivy.core.text import (
                Label as CoreLabel,
            )

            from kivy.core.window import (
                Window,
            )

            from kivy.graphics import (
                Color,
                Ellipse,
                Rectangle,
            )

            from kivy.uix.widget import (
                Widget,
            )

        except ImportError as exc:
            raise RuntimeError(
                "Kivy is required to run "
                "HyperKit games. Install with: "
                "pip install kivy"
            ) from exc

        game = self

        class HyperKitWidget(
            Widget
        ):
            def __init__(
                self,
                **kwargs,
            ):
                super().__init__(
                    **kwargs
                )

                self.scaler = (
                    CanvasScaler(
                        virtual_width=(
                            game.width
                        ),
                        virtual_height=(
                            game.height
                        ),
                        actual_width=(
                            game.width
                        ),
                        actual_height=(
                            game.height
                        ),
                    )
                )

                self.touch_tracker = (
                    TouchTracker(
                        move_min_distance=(
                            game
                            .touch_move_min_distance
                        )
                    )
                )

                self.viewport = (
                    MobileViewport(
                        x=0.0,
                        y=0.0,
                        width=float(
                            game.width
                        ),
                        height=float(
                            game.height
                        ),
                    )
                )

                if (
                    game.scene
                    and not
                    game.scene.started
                ):
                    game.scene.started = (
                        True
                    )

                    game.scene.start()

                Clock.schedule_interval(
                    self._tick,
                    1.0
                    / max(
                        1,
                        game.fps,
                    ),
                )

            def _update_scaler(
                self,
            ):
                width = max(
                    1.0,
                    float(
                        self.width
                    ),
                )

                height = max(
                    1.0,
                    float(
                        self.height
                    ),
                )

                self.viewport = (
                    game.display_profile
                    .resolve_viewport(
                        width,
                        height,
                    )
                )

                self.scaler.update_actual_size(
                    self.viewport.width,
                    self.viewport.height,
                )

            def _to_screen_x(
                self,
                value,
            ):
                return (
                    self.viewport.x
                    + self.scaler
                    .to_screen_x(
                        value
                    )
                )

            def _to_screen_y(
                self,
                value,
            ):
                return (
                    self.viewport.y
                    + self.scaler
                    .to_screen_y(
                        value
                    )
                )

            def _to_screen_rect(
                self,
                x,
                y,
                width,
                height,
            ):
                (
                    sx,
                    sy,
                    sw,
                    sh,
                ) = (
                    self.scaler
                    .to_screen_rect(
                        x,
                        y,
                        width,
                        height,
                    )
                )

                return (
                    self.viewport.x + sx,
                    self.viewport.y + sy,
                    sw,
                    sh,
                )

            def _to_virtual_point(
                self,
                x,
                y,
            ):
                local_x = (
                    float(x)
                    - self.viewport.x
                )

                local_y = (
                    float(y)
                    - self.viewport.y
                )

                return (
                    self.scaler
                    .to_virtual_point(
                        local_x,
                        local_y,
                    )
                )

            def _camera_offset(
                self,
            ):
                if not game.scene:
                    return (
                        0.0,
                        0.0,
                    )

                shake_x = float(
                    getattr(
                        game.scene,
                        "camera_offset_x",
                        0.0,
                    )
                )

                shake_y = float(
                    getattr(
                        game.scene,
                        "camera_offset_y",
                        0.0,
                    )
                )

                follow_x = float(
                    getattr(
                        game.scene,
                        "camera_follow_offset_x",
                        0.0,
                    )
                )

                follow_y = float(
                    getattr(
                        game.scene,
                        "camera_follow_offset_y",
                        0.0,
                    )
                )

                return (
                    shake_x
                    + follow_x,
                    shake_y
                    + follow_y,
                )

            def _draw_background(
                self,
            ):
                Color(
                    *game.background_color
                )

                Rectangle(
                    pos=(0, 0),
                    size=self.size,
                )

            def _draw_text(
                self,
                obj,
            ):
                font_size = max(
                    1,
                    int(
                        getattr(
                            obj,
                            "font_size",
                            28,
                        )
                        * self.scaler.scale
                    ),
                )

                label = CoreLabel(
                    text=str(
                        getattr(
                            obj,
                            "text",
                            "",
                        )
                    ),
                    font_size=font_size,
                    bold=bool(
                        getattr(
                            obj,
                            "bold",
                            False,
                        )
                    ),
                )

                label.refresh()

                (
                    camera_x,
                    camera_y,
                ) = (
                    self._camera_offset()
                )

                screen_x = (
                    self._to_screen_x(
                        obj.x
                        + camera_x
                    )
                )

                screen_y = (
                    self._to_screen_y(
                        obj.y
                        + camera_y
                    )
                )

                Color(
                    *obj.color
                )

                Rectangle(
                    texture=(
                        label.texture
                    ),
                    pos=(
                        screen_x,
                        screen_y,
                    ),
                    size=(
                        label.texture.size
                    ),
                )

            def _draw_button_text(
                self,
                obj,
            ):
                text = str(
                    getattr(
                        obj,
                        "text",
                        "",
                    )
                )

                if not text:
                    return

                font_size = max(
                    1,
                    int(
                        getattr(
                            obj,
                            "font_size",
                            24,
                        )
                        * self.scaler.scale
                    ),
                )

                label = CoreLabel(
                    text=text,
                    font_size=font_size,
                    bold=bool(
                        getattr(
                            obj,
                            "bold",
                            False,
                        )
                    ),
                )

                label.refresh()

                (
                    camera_x,
                    camera_y,
                ) = (
                    self._camera_offset()
                )

                (
                    sx,
                    sy,
                    sw,
                    sh,
                ) = (
                    self._to_screen_rect(
                        obj.x
                        + camera_x,
                        obj.y
                        + camera_y,
                        obj.width,
                        obj.height,
                    )
                )

                text_x = (
                    sx
                    + (
                        sw
                        - label.texture
                        .size[0]
                    )
                    / 2
                )

                text_y = (
                    sy
                    + (
                        sh
                        - label.texture
                        .size[1]
                    )
                    / 2
                )

                Color(
                    *getattr(
                        obj,
                        "text_color",
                        (
                            1,
                            1,
                            1,
                            1,
                        ),
                    )
                )

                Rectangle(
                    texture=(
                        label.texture
                    ),
                    pos=(
                        text_x,
                        text_y,
                    ),
                    size=(
                        label.texture.size
                    ),
                )

            def _tick(
                self,
                dt,
            ):
                self._update_scaler()

                if (
                    game.scene
                    and not
                    game.is_paused
                    and not
                    game.is_backgrounded
                ):
                    safe_dt = (
                        game.frame_time
                        .normalize(
                            dt
                        )
                    )

                    game.scene.update(
                        safe_dt
                    )

                self._redraw()

            def _redraw(
                self,
            ):
                self.canvas.clear()
                self._update_scaler()

                with self.canvas:
                    self._draw_background()

                    if not game.scene:
                        return

                    (
                        camera_x,
                        camera_y,
                    ) = (
                        self._camera_offset()
                    )

                    for obj in (
                        game.scene.objects
                    ):
                        if (
                            not obj.visible
                            or not obj.active
                        ):
                            continue

                        if (
                            obj.shape
                            == "text"
                        ):
                            self._draw_text(
                                obj
                            )

                            continue

                        (
                            sx,
                            sy,
                            sw,
                            sh,
                        ) = (
                            self._to_screen_rect(
                                obj.x
                                + camera_x,
                                obj.y
                                + camera_y,
                                obj.width,
                                obj.height,
                            )
                        )

                        if (
                            hasattr(
                                obj,
                                "has_image",
                            )
                            and obj.has_image()
                        ):
                            Color(
                                1,
                                1,
                                1,
                                1,
                            )

                            Rectangle(
                                source=str(
                                    obj.image_path
                                ),
                                pos=(
                                    sx,
                                    sy,
                                ),
                                size=(
                                    sw,
                                    sh,
                                ),
                            )

                        else:
                            Color(
                                *obj.color
                            )

                            if (
                                obj.shape
                                == "circle"
                            ):
                                Ellipse(
                                    pos=(
                                        sx,
                                        sy,
                                    ),
                                    size=(
                                        sw,
                                        sh,
                                    ),
                                )

                            else:
                                Rectangle(
                                    pos=(
                                        sx,
                                        sy,
                                    ),
                                    size=(
                                        sw,
                                        sh,
                                    ),
                                )

                        if hasattr(
                            obj,
                            "text",
                        ):
                            self._draw_button_text(
                                obj
                            )

                    game.scene.draw(
                        self.canvas
                    )

            def _pointer_id(
                self,
                touch,
            ):
                return getattr(
                    touch,
                    "uid",
                    0,
                )

            def on_touch_down(
                self,
                touch,
            ):
                self._update_scaler()

                if not self.viewport.contains(
                    touch.x,
                    touch.y,
                ):
                    return False

                (
                    vx,
                    vy,
                ) = (
                    self._to_virtual_point(
                        touch.x,
                        touch.y,
                    )
                )

                self.touch_tracker.touch_down(
                    vx,
                    vy,
                    pointer_id=(
                        self._pointer_id(
                            touch
                        )
                    ),
                )

                if game.scene:
                    game.scene.on_touch_down(
                        vx,
                        vy,
                    )

                return True

            def on_touch_move(
                self,
                touch,
            ):
                (
                    vx,
                    vy,
                ) = (
                    self._to_virtual_point(
                        touch.x,
                        touch.y,
                    )
                )

                move_event = (
                    self.touch_tracker
                    .touch_move(
                        vx,
                        vy,
                        pointer_id=(
                            self._pointer_id(
                                touch
                            )
                        ),
                    )
                )

                if move_event is None:
                    return True

                if game.scene:
                    game.scene.on_touch_move(
                        vx,
                        vy,
                    )

                return True

            def on_touch_up(
                self,
                touch,
            ):
                (
                    vx,
                    vy,
                ) = (
                    self._to_virtual_point(
                        touch.x,
                        touch.y,
                    )
                )

                gesture = (
                    self.touch_tracker
                    .touch_up(
                        vx,
                        vy,
                        pointer_id=(
                            self._pointer_id(
                                touch
                            )
                        ),
                    )
                )

                if (
                    game.scene
                    and gesture is not None
                ):
                    game.scene.on_touch_up(
                        vx,
                        vy,
                    )

                    if (
                        gesture.kind
                        == "tap"
                    ):
                        handled = (
                            game.scene
                            .dispatch_tap(
                                vx,
                                vy,
                            )
                        )

                        if not handled:
                            game.scene.on_tap(
                                vx,
                                vy,
                            )

                    elif (
                        gesture.kind
                        == "swipe"
                        and gesture.direction
                    ):
                        game.scene.on_swipe(
                            gesture.start,
                            gesture.end,
                            gesture.direction,
                        )

                return True

        class HyperKitKivyApp(
            App
        ):
            def build(
                self,
            ):
                self.title = (
                    game.title
                )

                if (
                    game.environment
                    .is_desktop
                ):
                    Window.size = (
                        game.width,
                        game.height,
                    )

                    Window.fullscreen = (
                        game.fullscreen
                    )

                widget = (
                    HyperKitWidget()
                )
                game._widget = widget

                return widget

            def on_pause(
                self,
            ):
                game.pause()

                return True

            def on_resume(
                self,
            ):
                game.resume()

            def on_stop(
                self,
            ):
                game.stop()

        self._app = (
            HyperKitKivyApp()
        )

        self._app.run()
