from __future__ import annotations

from typing import Optional

from .input import TouchTracker
from .layout import CanvasScaler
from .scene import Scene


class Game:
    """Kivy-backed HyperKit game runner.

    HyperKit uses a virtual resolution. The default is 720x1280.
    The game is automatically scaled to fit the real screen/window size.
    """

    def __init__(
        self,
        title: str = "HyperKit Game",
        width: int = 720,
        height: int = 1280,
        fps: int = 60,
        background_color: tuple[float, float,
                                float, float] = (0.08, 0.08, 0.1, 1),
    ) -> None:
        self.title = title
        self.width = width
        self.height = height
        self.fps = fps
        self.background_color = background_color
        self.scene: Optional[Scene] = None
        self._app = None

    def set_scene(self, scene: Scene) -> "Game":
        self.scene = scene
        scene.bind_game(self)
        return self

    def run(self) -> None:
        if self.scene is None:
            raise RuntimeError(
                "No scene set. Use Game(...).set_scene(MyScene()).run().")

        try:
            from kivy.app import App
            from kivy.clock import Clock
            from kivy.core.text import Label as CoreLabel
            from kivy.core.window import Window
            from kivy.graphics import Color, Ellipse, Rectangle
            from kivy.uix.widget import Widget
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "Kivy is required to run HyperKit games. Install with: pip install kivy"
            ) from exc

        game = self

        class HyperKitWidget(Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.scaler = CanvasScaler(
                    virtual_width=game.width,
                    virtual_height=game.height,
                    actual_width=game.width,
                    actual_height=game.height,
                )

                self.touch_tracker = TouchTracker()

                if game.scene and not game.scene.started:
                    game.scene.started = True
                    game.scene.start()

                Clock.schedule_interval(self._tick, 1.0 / max(1, game.fps))

            def _update_scaler(self):
                self.scaler.update_actual_size(self.width, self.height)

            def _draw_background(self):
                Color(*game.background_color)
                Rectangle(pos=(0, 0), size=self.size)

                # Optional subtle content area overlay.
                # This helps when the window aspect ratio does not match the virtual canvas.
                Color(0, 0, 0, 0)
                Rectangle(
                    pos=(self.scaler.offset_x, self.scaler.offset_y),
                    size=(self.scaler.content_width,
                          self.scaler.content_height),
                )

            def _draw_text(self, obj):
                font_size = max(
                    1, int(getattr(obj, "font_size", 28) * self.scaler.scale))

                label = CoreLabel(
                    text=str(getattr(obj, "text", "")),
                    font_size=font_size,
                    bold=bool(getattr(obj, "bold", False)),
                )
                label.refresh()

                screen_x = self.scaler.to_screen_x(obj.x)
                screen_y = self.scaler.to_screen_y(obj.y)

                Color(*obj.color)
                Rectangle(
                    texture=label.texture,
                    pos=(screen_x, screen_y),
                    size=label.texture.size,
                )

            def _draw_button_text(self, obj):
                text = str(getattr(obj, "text", ""))
                if not text:
                    return

                font_size = max(
                    1, int(getattr(obj, "font_size", 24) * self.scaler.scale))

                label = CoreLabel(
                    text=text,
                    font_size=font_size,
                    bold=bool(getattr(obj, "bold", False)),
                )
                label.refresh()

                sx, sy, sw, sh = self.scaler.to_screen_rect(
                    obj.x, obj.y, obj.width, obj.height)

                text_x = sx + (sw - label.texture.size[0]) / 2
                text_y = sy + (sh - label.texture.size[1]) / 2

                Color(1, 1, 1, 1)
                Rectangle(
                    texture=label.texture,
                    pos=(text_x, text_y),
                    size=label.texture.size,
                )

            def _tick(self, dt):
                self._update_scaler()

                if game.scene:
                    game.scene.update(dt)

                self._redraw()

            def _redraw(self):
                self.canvas.clear()
                self._update_scaler()

                with self.canvas:
                    self._draw_background()

                    if not game.scene:
                        return

                    for obj in game.scene.objects:
                        if not obj.visible or not obj.active:
                            continue

                        if obj.shape == "text":
                            self._draw_text(obj)
                            continue

                        sx, sy, sw, sh = self.scaler.to_screen_rect(
                            obj.x,
                            obj.y,
                            obj.width,
                            obj.height,
                        )

                        Color(*obj.color)

                        if obj.shape == "circle":
                            Ellipse(pos=(sx, sy), size=(sw, sh))
                        else:
                            Rectangle(pos=(sx, sy), size=(sw, sh))

                        if hasattr(obj, "text"):
                            self._draw_button_text(obj)

                    game.scene.draw(self.canvas)

            def on_touch_down(self, touch):
                vx, vy = self.scaler.to_virtual_point(touch.x, touch.y)

                self.touch_tracker.touch_down(vx, vy)

                if game.scene:
                    game.scene.on_touch_down(vx, vy)

                return True

            def on_touch_move(self, touch):
                vx, vy = self.scaler.to_virtual_point(touch.x, touch.y)

                if game.scene:
                    game.scene.on_touch_move(vx, vy)

                return True

            def on_touch_up(self, touch):
                vx, vy = self.scaler.to_virtual_point(touch.x, touch.y)

                gesture = self.touch_tracker.touch_up(vx, vy)

                if game.scene:
                    game.scene.on_touch_up(vx, vy)

                    if gesture and gesture.kind == "tap":
                        game.scene.on_tap(vx, vy)
                    elif gesture and gesture.kind == "swipe" and gesture.direction:
                        game.scene.on_swipe(
                            gesture.start, gesture.end, gesture.direction)

                return True

        class HyperKitKivyApp(App):
            def build(self):
                self.title = game.title
                Window.size = (game.width, game.height)
                return HyperKitWidget()

        self._app = HyperKitKivyApp()
        self._app.run()
