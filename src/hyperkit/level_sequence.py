"""Level sequencing helpers for content-driven HyperKit games."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .level import LevelData, LevelManager


class LevelSequenceError(Exception):
    """Base error for level sequence operations."""


@dataclass
class LevelSequence:
    """Ordered level-file progression helper."""

    levels: list[str]
    loop: bool = False
    current_index: int = 0

    def __post_init__(self) -> None:
        self.levels = [
            str(level).strip()
            for level in self.levels
        ]

        if not self.levels:
            raise LevelSequenceError(
                "LevelSequence requires at least one level."
            )

        if any(
            not level
            for level in self.levels
        ):
            raise LevelSequenceError(
                "LevelSequence level names must not be empty."
            )

        if not (
            0
            <= int(
                self.current_index
            )
            < len(
                self.levels
            )
        ):
            raise LevelSequenceError(
                "current_index is outside the level sequence."
            )

        self.current_index = int(
            self.current_index
        )

    @classmethod
    def from_iterable(
        cls,
        levels: Iterable[str],
        *,
        loop: bool = False,
    ) -> "LevelSequence":
        return cls(
            levels=list(
                levels
            ),
            loop=loop,
        )

    @property
    def current(
        self,
    ) -> str:
        return self.levels[
            self.current_index
        ]

    @property
    def is_first(
        self,
    ) -> bool:
        return self.current_index == 0

    @property
    def is_last(
        self,
    ) -> bool:
        return (
            self.current_index
            == len(
                self.levels
            )
            - 1
        )

    @property
    def progress(
        self,
    ) -> tuple[int, int]:
        return (
            self.current_index + 1,
            len(
                self.levels
            ),
        )

    def set_index(
        self,
        index: int,
    ) -> str:
        index = int(
            index
        )

        if not (
            0
            <= index
            < len(
                self.levels
            )
        ):
            raise LevelSequenceError(
                "Level index is outside the sequence."
            )

        self.current_index = index
        return self.current

    def next(
        self,
    ) -> str | None:
        if not self.is_last:
            self.current_index += 1
            return self.current

        if self.loop:
            self.current_index = 0
            return self.current

        return None

    def previous(
        self,
    ) -> str | None:
        if not self.is_first:
            self.current_index -= 1
            return self.current

        if self.loop:
            self.current_index = (
                len(
                    self.levels
                )
                - 1
            )
            return self.current

        return None

    def reset(
        self,
    ) -> "LevelSequence":
        self.current_index = 0
        return self

    def load_current(
        self,
        manager: LevelManager,
    ) -> LevelData:
        if not isinstance(
            manager,
            LevelManager,
        ):
            raise LevelSequenceError(
                "manager must be a LevelManager."
            )

        return manager.load(
            self.current
        )

    def advance_and_load(
        self,
        manager: LevelManager,
    ) -> LevelData | None:
        next_level = self.next()

        if next_level is None:
            return None

        return manager.load(
            next_level
        )
