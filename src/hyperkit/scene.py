from __future__ import annotations

from typing import Iterable

from .object import GameObject
from .state import GameState, StateMachine


class Scene:
    """Base class for game scenes.

    Override start, update, draw, on_tap, on_swipe, on_touch_down, on_touch_move,
    and on_touch_up in your game-specific scenes.
    """

    def __init__(self) -> None:
        self.game = None
        self.objects: list[GameObject] = []
        self.started = False
        self.state_machine = StateMachine(GameState.PLAYING)

    def bind_game(self, game: object) -> None:
        self.game = game

    @property
    def state(self) -> str:
        return self.state_machine.value

    def set_state(self, state: GameState | str) -> None:
        self.state_machine.set(state)

    def is_state(self, state: GameState | str) -> bool:
        return self.state_machine.is_state(state)

    def is_menu(self) -> bool:
        return self.is_state(GameState.MENU)

    def is_playing(self) -> bool:
        return self.is_state(GameState.PLAYING)

    def is_paused(self) -> bool:
        return self.is_state(GameState.PAUSED)

    def is_game_over(self) -> bool:
        return self.is_state(GameState.GAME_OVER)

    def start_game(self) -> None:
        self.state_machine.start()

    def pause_game(self) -> None:
        self.state_machine.pause()

    def resume_game(self) -> None:
        self.state_machine.resume()

    def end_game(self) -> None:
        self.state_machine.game_over()

    def show_menu(self) -> None:
        self.state_machine.menu()

    def reset_game_state(self) -> None:
        self.state_machine.reset(GameState.PLAYING)

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
        if not self.is_playing():
            return

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
