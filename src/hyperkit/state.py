from __future__ import annotations

from enum import Enum
from typing import Callable


class GameState(str, Enum):
    """Common game states for HyperKit games."""

    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


StateChangeCallback = Callable[
    [GameState, GameState],
    None,
]


class StateMachine:
    """Small helper for managing game state."""

    def __init__(
        self,
        initial_state: GameState | str = GameState.PLAYING,
        on_change: StateChangeCallback | None = None,
    ) -> None:
        self._state = self._normalize(
            initial_state
        )
        self._previous_state: GameState | None = None
        self.on_change = on_change

    @staticmethod
    def _normalize(
        state: GameState | str,
    ) -> GameState:
        if isinstance(
            state,
            GameState,
        ):
            return state

        try:
            return GameState(
                state
            )
        except ValueError as exc:
            allowed = ", ".join(
                item.value
                for item in GameState
            )
            raise ValueError(
                f"Invalid game state '{state}'. "
                f"Allowed states: {allowed}"
            ) from exc

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def previous_state(
        self,
    ) -> GameState | None:
        return self._previous_state

    @property
    def value(self) -> str:
        return self._state.value

    def set(
        self,
        state: GameState | str,
    ) -> bool:
        """Set the state and return whether it actually changed."""

        next_state = self._normalize(
            state
        )

        if next_state == self._state:
            return False

        previous = self._state
        self._previous_state = previous
        self._state = next_state

        if self.on_change is not None:
            self.on_change(
                previous,
                next_state,
            )

        return True

    def is_state(
        self,
        state: GameState | str,
    ) -> bool:
        return (
            self._state
            == self._normalize(
                state
            )
        )

    def start(self) -> bool:
        return self.set(
            GameState.PLAYING
        )

    def pause(self) -> bool:
        return self.set(
            GameState.PAUSED
        )

    def resume(self) -> bool:
        return self.set(
            GameState.PLAYING
        )

    def game_over(self) -> bool:
        return self.set(
            GameState.GAME_OVER
        )

    def menu(self) -> bool:
        return self.set(
            GameState.MENU
        )

    def reset(
        self,
        state: GameState | str = GameState.PLAYING,
    ) -> bool:
        return self.set(
            state
        )
