from __future__ import annotations

from .save import SaveManager


class ScoreManager:
    """Score and high-score helper for HyperKit games.

    Example:
        score = ScoreManager()
        score.add(1)
        score.save_high_score()
    """

    def __init__(
        self,
        save: SaveManager | None = None,
        high_score_key: str = "high_score",
        initial_score: int = 0,
        auto_save_high_score: bool = True,
    ) -> None:
        self.score = int(initial_score)
        self.high_score_key = high_score_key
        self.save = save or SaveManager()
        self.auto_save_high_score = auto_save_high_score

    @property
    def value(self) -> int:
        """Current score value."""
        return self.score

    @property
    def high_score(self) -> int:
        """Saved high score value."""
        return int(self.save.get(self.high_score_key, 0))

    def add(self, amount: int = 1) -> int:
        """Add score and update high score if needed."""
        self.score += int(amount)

        if self.auto_save_high_score:
            self.save_high_score()

        return self.score

    def subtract(self, amount: int = 1, minimum: int | None = 0) -> int:
        """Subtract score.

        By default, score will not go below 0.
        Set minimum=None if negative score is allowed.
        """
        self.score -= int(amount)

        if minimum is not None:
            self.score = max(int(minimum), self.score)

        return self.score

    def set_score(self, value: int) -> int:
        """Set current score directly."""
        self.score = int(value)

        if self.auto_save_high_score:
            self.save_high_score()

        return self.score

    def reset_score(self) -> None:
        """Reset only the current score."""
        self.score = 0

    def reset(self) -> None:
        """Alias for reset_score."""
        self.reset_score()

    def save_high_score(self) -> bool:
        """Save current score as high score if it is greater.

        Returns:
            True if a new high score was saved, otherwise False.
        """
        if self.score > self.high_score:
            self.save.set(self.high_score_key, self.score)
            return True

        return False

    def reset_high_score(self) -> None:
        """Reset saved high score."""
        self.save.set(self.high_score_key, 0)

    def is_new_high_score(self) -> bool:
        """Return True if current score is greater than saved high score."""
        return self.score > self.high_score

    def as_dict(self) -> dict[str, int]:
        """Return score data as a dictionary."""
        return {
            "score": self.score,
            "high_score": self.high_score,
        }
