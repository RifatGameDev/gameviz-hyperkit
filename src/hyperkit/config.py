"""Core SDK configuration for GameViz HyperKit."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import HyperKitConfigurationError


VALID_LOG_LEVELS = {
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
}


@dataclass
class SDKConfig:
    """Global SDK configuration.

    This intentionally remains small during the 0.2 development cycle.
    Additional runtime, mobile, Android, analytics, and advertising
    configuration can build on top of this foundation later.
    """

    debug: bool = False
    strict: bool = True
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        self._validate_boolean("debug", self.debug)
        self._validate_boolean("strict", self.strict)

        if not isinstance(self.log_level, str):
            raise HyperKitConfigurationError(
                "log_level must be a string."
            )

        normalized_level = self.log_level.strip().upper()

        if normalized_level not in VALID_LOG_LEVELS:
            valid = ", ".join(sorted(VALID_LOG_LEVELS))
            raise HyperKitConfigurationError(
                f"Unsupported log level '{self.log_level}'. "
                f"Expected one of: {valid}."
            )

        self.log_level = normalized_level

    @staticmethod
    def _validate_boolean(name: str, value: object) -> None:
        if type(value) is not bool:
            raise HyperKitConfigurationError(
                f"{name} must be a boolean value."
            )

    def to_dict(self) -> dict[str, object]:
        """Return a serializable representation of the configuration."""

        return {
            "debug": self.debug,
            "strict": self.strict,
            "log_level": self.log_level,
        }
