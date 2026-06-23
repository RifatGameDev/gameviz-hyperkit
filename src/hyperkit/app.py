from __future__ import annotations

from typing import Optional

from .input import TouchTracker
from .scene import Scene


class Game:
    """Kivy-backed HyperKit game runner.

    This class keeps the public API small while using Kivy internally for
    desktop/mobile windows, drawing, and touch events.
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
                self.touch_tracker = TouchTracker()
                if game.scene and not game.scene.started:
                    game.scene.started = True
                    game.scene.start()
                Clock.schedule_interval(self._tick, 1.0 / max(1, game.fps))

            def _draw_text(self, obj):
                label = CoreLabel(
                    text=str(getattr(obj, "text", "")),
                    font_size=int(getattr(obj, "font_size", 28)),
                    bold=bool(getattr(obj, "bold", False)),
                )
                label.refresh()

                Color(*obj.color)
                Rectangle(
                    texture=label.texture,
                    pos=(obj.x, obj.y),
                    size=label.texture.size,
                )

            def _draw_button_text(self, obj):
                text = str(getattr(obj, "text", ""))
                if not text:
                    return

                label = CoreLabel(
                    text=text,
                    font_size=int(getattr(obj, "font_size", 24)),
                    bold=bool(getattr(obj, "bold", False)),
                )
                label.refresh()

                text_x = obj.x + (obj.width - label.texture.size[0]) / 2
                text_y = obj.y + (obj.height - label.texture.size[1]) / 2

                Color(1, 1, 1, 1)
                Rectangle(
                    texture=label.texture,
                    pos=(text_x, text_y),
                    size=label.texture.size,
                )

            def _tick(self, dt):
                if game.scene:
                    game.scene.update(dt)
                self._redraw()

            def _redraw(self):
                self.canvas.clear()
                with self.canvas:
                    Color(*game.background_color)
                    Rectangle(pos=(0, 0), size=self.size)

                    if not game.scene:
                        return

                    for obj in game.scene.objects:
                        if not obj.visible or not obj.active:
                            continue

                        if obj.shape == "text":
                            self._draw_text(obj)
                            continue

                        Color(*obj.color)
                        if obj.shape == "circle":
                            Ellipse(pos=(obj.x, obj.y), size=(
                                obj.width, obj.height))
                        else:
                            Rectangle(pos=(obj.x, obj.y), size=(
                                obj.width, obj.height))

                        if hasattr(obj, "text"):
                            self._draw_button_text(obj)

                    game.scene.draw(self.canvas)

            def on_touch_down(self, touch):
                self.touch_tracker.touch_down(touch.x, touch.y)
                if game.scene:
                    game.scene.on_touch_down(touch.x, touch.y)
                return True

            def on_touch_move(self, touch):
                if game.scene:
                    game.scene.on_touch_move(touch.x, touch.y)
                return True

            def on_touch_up(self, touch):
                gesture = self.touch_tracker.touch_up(touch.x, touch.y)
                if game.scene:
                    game.scene.on_touch_up(touch.x, touch.y)
                    if gesture and gesture.kind == "tap":
                        game.scene.on_tap(touch.x, touch.y)
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
