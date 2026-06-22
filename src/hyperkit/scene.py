from __future__ import annotations

from typing import Iterable

from .object import GameObject


class Scene:
    """Base class for game scenes.

    Override start, update, draw, on_tap, on_swipe, on_touch_down, on_touch_move,
    and on_touch_up in your game-specific scenes.
    """

    def __init__(self) -> None:
        self.game = None
        self.objects: list[GameObject] = []
        self.started = False

    def bind_game(self, game: object) -> None:
        self.game = game

    def add(self, obj: GameObject) -> GameObject:
        self.objects.append(obj)
        return obj

    def remove(self, obj: GameObject) -> None:
        if obj in self.objects:
            self.objects.remove(obj)

    def clear(self) -> None:
        self.objects.clear()

    def active_objects(self) -> Iterable[GameObject]:
        return (obj for obj in self.objects if obj.active)

    def start(self) -> None:
        pass

    def update(self, dt: float) -> None:
        for obj in self.active_objects():
            obj.update(dt)

    def draw(self, canvas: object) -> None:
        pass

    def on_tap(self, x: float, y: float) -> None:
        pass

    def on_swipe(self, start: tuple[float, float], end: tuple[float, float], direction: str) -> None:
        pass

    def on_touch_down(self, x: float, y: float) -> None:
        pass

    def on_touch_move(self, x: float, y: float) -> None:
        pass

    def on_touch_up(self, x: float, y: float) -> None:
        pass
