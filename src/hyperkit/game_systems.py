"""Reusable game-session and progression systems for GameViz HyperKit."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from time import monotonic
from typing import Any
from uuid import uuid4

from .analytics import (
    AnalyticsEvent,
    AnalyticsProvider,
    NoOpAnalyticsProvider,
)
from .errors import HyperKitRuntimeError
from .runtime import SDKContext


class SessionState(str, Enum):
    """Lifecycle states for one gameplay session."""

    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    BACKGROUND = "background"
    ENDED = "ended"


@dataclass
class GameSession:
    """One tracked gameplay session."""

    session_id: str
    started_at: float
    state: SessionState = SessionState.RUNNING
    ended_at: float | None = None
    pause_count: int = 0
    resume_count: int = 0

    @property
    def ended(self) -> bool:
        return self.state == SessionState.ENDED


class SessionTracker:
    """Track gameplay session lifecycle without platform dependencies."""

    def __init__(
        self,
        *,
        time_fn: Callable[[], float] = monotonic,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._time_fn = time_fn
        self._id_factory = id_factory or (
            lambda: uuid4().hex
        )
        self.current: GameSession | None = None

    def start(self) -> GameSession:
        if (
            self.current is not None
            and not self.current.ended
        ):
            return self.current

        self.current = GameSession(
            session_id=str(self._id_factory()),
            started_at=float(self._time_fn()),
        )

        return self.current

    def _require_active(self) -> GameSession:
        if self.current is None or self.current.ended:
            raise HyperKitRuntimeError(
                "No active game session. "
                "Start a session first."
            )

        return self.current

    def pause(self) -> GameSession:
        session = self._require_active()

        if session.state == SessionState.PAUSED:
            return session

        if session.state not in {
            SessionState.RUNNING,
            SessionState.BACKGROUND,
        }:
            raise HyperKitRuntimeError(
                "Game session cannot be paused "
                f"from state '{session.state.value}'."
            )

        session.state = SessionState.PAUSED
        session.pause_count += 1
        return session

    def background(self) -> GameSession:
        session = self._require_active()

        if session.state == SessionState.BACKGROUND:
            return session

        if session.state not in {
            SessionState.RUNNING,
            SessionState.PAUSED,
        }:
            raise HyperKitRuntimeError(
                "Game session cannot enter background "
                f"from state '{session.state.value}'."
            )

        session.state = SessionState.BACKGROUND
        return session

    def resume(self) -> GameSession:
        session = self._require_active()

        if session.state == SessionState.RUNNING:
            return session

        if session.state not in {
            SessionState.PAUSED,
            SessionState.BACKGROUND,
        }:
            raise HyperKitRuntimeError(
                "Game session cannot resume "
                f"from state '{session.state.value}'."
            )

        session.state = SessionState.RUNNING
        session.resume_count += 1
        return session

    def end(self) -> GameSession:
        session = self._require_active()

        session.state = SessionState.ENDED
        session.ended_at = float(self._time_fn())
        return session

    @property
    def duration(self) -> float:
        if self.current is None:
            raise HyperKitRuntimeError(
                "No game session has been started."
            )

        session = self.current

        end = (
            session.ended_at
            if session.ended_at is not None
            else float(self._time_fn())
        )

        return max(
            0.0,
            end - session.started_at,
        )


@dataclass
class ProgressionTracker:
    """Small reusable progression state for casual games."""

    level: int = 1
    xp: int = 0
    coins: int = 0

    def __post_init__(self) -> None:
        if self.level < 1:
            raise ValueError("level must be at least 1.")

        if self.xp < 0:
            raise ValueError("xp cannot be negative.")

        if self.coins < 0:
            raise ValueError("coins cannot be negative.")

    def add_xp(self, amount: int) -> int:
        amount = int(amount)
        if amount < 0:
            raise ValueError("xp amount cannot be negative.")

        self.xp += amount
        return self.xp

    def add_coins(self, amount: int) -> int:
        amount = int(amount)
        if amount < 0:
            raise ValueError("coin amount cannot be negative.")

        self.coins += amount
        return self.coins

    def spend_coins(self, amount: int) -> bool:
        amount = int(amount)
        if amount < 0:
            raise ValueError("coin amount cannot be negative.")

        if amount > self.coins:
            return False

        self.coins -= amount
        return True

    def advance_level(self, amount: int = 1) -> int:
        amount = int(amount)
        if amount < 1:
            raise ValueError("level amount must be at least 1.")

        self.level += amount
        return self.level

    def as_dict(self) -> dict[str, int]:
        return {
            "level": self.level,
            "xp": self.xp,
            "coins": self.coins,
        }


class GameSystems:
    """Coordinates session, progression, and analytics hooks."""

    SERVICE_NAME = "game_systems"

    def __init__(
        self,
        *,
        analytics: AnalyticsProvider | None = None,
        session: SessionTracker | None = None,
        progression: ProgressionTracker | None = None,
    ) -> None:
        self.analytics = (
            analytics
            if analytics is not None
            else NoOpAnalyticsProvider()
        )
        self.session = session or SessionTracker()
        self.progression = progression or ProgressionTracker()
        self._initialized = False

    def initialize(self) -> "GameSystems":
        if not self._initialized:
            self.analytics.initialize()
            self._initialized = True

        return self

    def attach(
        self,
        context: SDKContext,
        *,
        replace: bool = False,
    ) -> "GameSystems":
        if not isinstance(context, SDKContext):
            raise HyperKitRuntimeError(
                "context must be an SDKContext instance."
            )

        context.register_service(
            self.SERVICE_NAME,
            self,
            replace=replace,
        )

        return self

    def _track(
        self,
        name: str,
        **properties: Any,
    ) -> None:
        self.initialize()

        self.analytics.track_event(
            AnalyticsEvent(
                name=name,
                properties=properties,
            )
        )

    def on_runtime_start(self) -> None:
        session = self.session.start()

        self._track(
            "session_start",
            session_id=session.session_id,
        )

    def on_runtime_pause(self) -> None:
        if self.session.current is None:
            return

        self.session.pause()
        self._track("session_pause")

    def on_runtime_background(self) -> None:
        if self.session.current is None:
            return

        self.session.background()
        self._track("session_background")

    def on_runtime_resume(self) -> None:
        if self.session.current is None:
            return

        self.session.resume()
        self._track("session_resume")

    def on_runtime_stop(self) -> None:
        if (
            self.session.current is None
            or self.session.current.ended
        ):
            return

        session = self.session.end()

        self._track(
            "session_end",
            session_id=session.session_id,
            duration=self.session.duration,
        )

        self.analytics.flush()

    def record_score(
        self,
        score: int,
        *,
        high_score: int | None = None,
    ) -> None:
        properties: dict[str, int] = {
            "score": int(score),
        }

        if high_score is not None:
            properties["high_score"] = int(high_score)

        self._track(
            "score_recorded",
            **properties,
        )

    def record_progression(self) -> None:
        self._track(
            "progression_updated",
            **self.progression.as_dict(),
        )


__all__ = [
    "GameSession",
    "GameSystems",
    "ProgressionTracker",
    "SessionState",
    "SessionTracker",
]
