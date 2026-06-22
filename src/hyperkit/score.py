from __future__ import annotations

from .save import SaveManager


class ScoreManager:
    """Score and high-score helper."""

    def __init__(self, save: SaveManager | None = None, high_score_key: str = "high_score") -> None:
        self.score = 0
        self.high_score_key = high_score_key
        self.save = save or SaveManager()

    @property
    def high_score(self) -> int:
        return int(self.save.get(self.high_score_key, 0))

    def add(self, amount: int = 1) -> int:
        self.score += amount
        if self.score > self.high_score:
            self.save.set(self.high_score_key, self.score)
        return self.score

    def reset_score(self) -> None:
        self.score = 0

    def reset_high_score(self) -> None:
        self.save.set(self.high_score_key, 0)
