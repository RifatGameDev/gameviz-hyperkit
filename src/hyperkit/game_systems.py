"""Reusable game-session, progression, ads, and analytics systems."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from time import monotonic
from typing import Any
from uuid import uuid4

from .ads import (
    AdProvider,
    AdResult,
    AdType,
    AdsService,
)
from .analytics import (
    AnalyticsProvider,
    AnalyticsService,
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

    def __post_init__(self) -> None:
        self.session_id = str(self.session_id).strip()
        self.started_at = float(self.started_at)

        if not self.session_id:
            raise ValueError(
                "session_id must not be empty."
            )

        if self.ended_at is not None:
            self.ended_at = float(self.ended_at)

        self.pause_count = int(self.pause_count)
        self.resume_count = int(self.resume_count)

        if self.pause_count < 0:
            raise ValueError(
                "pause_count cannot be negative."
            )

        if self.resume_count < 0:
            raise ValueError(
                "resume_count cannot be negative."
            )

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

    @property
    def active(self) -> bool:
        return (
            self.current is not None
            and not self.current.ended
        )

    @property
    def session_id(self) -> str | None:
        if self.current is None:
            return None

        return self.current.session_id

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
                "No active game session. Start a session first."
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

    def reset(
        self,
        *,
        level: int = 1,
        xp: int = 0,
        coins: int = 0,
    ) -> "ProgressionTracker":
        replacement = ProgressionTracker(
            level=level,
            xp=xp,
            coins=coins,
        )

        self.level = replacement.level
        self.xp = replacement.xp
        self.coins = replacement.coins
        return self

    def as_dict(self) -> dict[str, int]:
        return {
            "level": self.level,
            "xp": self.xp,
            "coins": self.coins,
        }


class GameSystems:
    """Coordinates session, progression, ads, and analytics."""

    SERVICE_NAME = "game_systems"

    def __init__(
        self,
        *,
        analytics: AnalyticsService | AnalyticsProvider | None = None,
        ads: AdsService | AdProvider | None = None,
        session: SessionTracker | None = None,
        progression: ProgressionTracker | None = None,
    ) -> None:
        if isinstance(
            analytics,
            AnalyticsService,
        ):
            self.analytics = analytics
        else:
            self.analytics = AnalyticsService(
                analytics
            )

        if isinstance(
            ads,
            AdsService,
        ):
            self.ads = ads
        else:
            self.ads = AdsService(
                ads
            )

        self.session = (
            session
            or SessionTracker()
        )

        self.progression = (
            progression
            or ProgressionTracker()
        )

        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    def initialize(self) -> "GameSystems":
        if self._initialized:
            return self

        self.analytics.initialize()
        self.ads.initialize()

        self._initialized = True
        return self

    def attach(
        self,
        context: SDKContext,
        *,
        replace: bool = False,
    ) -> "GameSystems":
        if not isinstance(
            context,
            SDKContext,
        ):
            raise HyperKitRuntimeError(
                "context must be an SDKContext instance."
            )

        context.register_service(
            self.SERVICE_NAME,
            self,
            replace=replace,
        )

        context.register_service(
            AnalyticsService.SERVICE_NAME,
            self.analytics,
            replace=replace,
        )

        context.register_service(
            AdsService.SERVICE_NAME,
            self.ads,
            replace=replace,
        )

        return self

    def on_runtime_start(self) -> None:
        self.initialize()

        session = self.session.start()

        self.analytics.track(
            "session_start",
            session_id=session.session_id,
        )

    def on_runtime_pause(self) -> None:
        if not self.session.active:
            return

        self.session.pause()
        self.analytics.track(
            "session_pause"
        )

    def on_runtime_background(self) -> None:
        if not self.session.active:
            return

        self.session.background()
        self.analytics.track(
            "session_background"
        )

    def on_runtime_resume(self) -> None:
        if not self.session.active:
            return

        self.session.resume()
        self.analytics.track(
            "session_resume"
        )

    def on_runtime_stop(self) -> None:
        if (
            self.session.current is None
            or self.session.current.ended
        ):
            return

        session = self.session.end()

        self.analytics.track(
            "session_end",
            session_id=session.session_id,
            duration=self.session.duration,
        )

        self.analytics.flush()

    def game_start(
        self,
        **properties: Any,
    ) -> None:
        self.analytics.game_start(
            **properties
        )

    def game_over(
        self,
        *,
        score: int | None = None,
        high_score: int | None = None,
        reason: str | None = None,
        **properties: Any,
    ) -> None:
        self.analytics.game_over(
            score=score,
            high_score=high_score,
            reason=reason,
            **properties,
        )

    def level_start(
        self,
        level: int | None = None,
        **properties: Any,
    ) -> None:
        resolved_level = (
            self.progression.level
            if level is None
            else int(level)
        )

        if resolved_level < 1:
            raise ValueError(
                "level must be at least 1."
            )

        self.analytics.level_start(
            resolved_level,
            **properties,
        )

    def level_complete(
        self,
        level: int | None = None,
        *,
        score: int | None = None,
        duration: float | None = None,
        **properties: Any,
    ) -> None:
        resolved_level = (
            self.progression.level
            if level is None
            else int(level)
        )

        if resolved_level < 1:
            raise ValueError(
                "level must be at least 1."
            )

        self.analytics.level_complete(
            resolved_level,
            score=score,
            duration=duration,
            **properties,
        )

    def record_score(
        self,
        score: int,
        *,
        high_score: int | None = None,
        **properties: Any,
    ) -> None:
        self.analytics.score(
            score,
            high_score=high_score,
            **properties,
        )

    def record_progression(
        self,
        **properties: Any,
    ) -> None:
        payload = dict(properties)
        payload.update(
            self.progression.as_dict()
        )

        self.analytics.progression(
            **payload
        )

    def add_coins(
        self,
        amount: int,
        *,
        track: bool = True,
    ) -> int:
        value = self.progression.add_coins(
            amount
        )

        if track:
            self.record_progression()

        return value

    def spend_coins(
        self,
        amount: int,
        *,
        track: bool = True,
    ) -> bool:
        spent = self.progression.spend_coins(
            amount
        )

        if spent and track:
            self.record_progression()

        return spent

    def add_xp(
        self,
        amount: int,
        *,
        track: bool = True,
    ) -> int:
        value = self.progression.add_xp(
            amount
        )

        if track:
            self.record_progression()

        return value

    def advance_level(
        self,
        amount: int = 1,
        *,
        track: bool = True,
    ) -> int:
        value = self.progression.advance_level(
            amount
        )

        if track:
            self.record_progression()

        return value

    def ads_available(
        self,
        ad_type: AdType | str,
        placement: str | None = None,
    ) -> bool:
        return self.ads.is_available(
            ad_type,
            placement,
        )

    def show_banner(
        self,
        placement: str | None = None,
    ) -> AdResult:
        return self.ads.show_banner(
            placement
        )

    def hide_banner(
        self,
        placement: str | None = None,
    ) -> AdResult:
        return self.ads.hide_banner(
            placement
        )

    def show_interstitial(
        self,
        placement: str | None = None,
    ) -> AdResult:
        return self.ads.show_interstitial(
            placement
        )

    def show_rewarded(
        self,
        placement: str | None = None,
        *,
        on_reward: Callable[[], None] | None = None,
    ) -> AdResult:
        return self.ads.show_rewarded(
            placement,
            on_reward=on_reward,
        )


__all__ = [
    "GameSession",
    "GameSystems",
    "ProgressionTracker",
    "SessionState",
    "SessionTracker",
]
