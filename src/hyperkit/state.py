from __future__ import annotations

from enum import Enum


class GameState(str, Enum):
    """Common game states for HyperKit games."""

    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class StateMachine:
    """Small helper for managing game state."""

    def __init__(self, initial_state: GameState | str = GameState.PLAYING) -> None:
        self._state = self._normalize(initial_state)

    @staticmethod
    def _normalize(state: GameState | str) -> GameState:
        if isinstance(state, GameState):
            return state

        try:
            return GameState(state)
        except ValueError as exc:
            allowed = ", ".join(s.value for s in GameState)
            raise ValueError(
                f"Invalid game state '{state}'. Allowed states: {allowed}") from exc

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def value(self) -> str:
        return self._state.value

    def set(self, state: GameState | str) -> None:
        self._state = self._normalize(state)

    def is_state(self, state: GameState | str) -> bool:
        return self._state == self._normalize(state)

    def start(self) -> None:
        self.set(GameState.PLAYING)

    def pause(self) -> None:
        self.set(GameState.PAUSED)

    def resume(self) -> None:
        self.set(GameState.PLAYING)

    def game_over(self) -> None:
        self.set(GameState.GAME_OVER)

    def menu(self) -> None:
        self.set(GameState.MENU)

    def reset(self, state: GameState | str = GameState.PLAYING) -> None:
        self.set(state)
