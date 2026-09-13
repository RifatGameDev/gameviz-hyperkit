"""Core exception hierarchy for GameViz HyperKit.

All new SDK-level exceptions should inherit from HyperKitError.
This gives applications one stable exception type that can be used
to catch errors originating from HyperKit while still allowing more
specific exception handling when needed.
"""


class HyperKitError(Exception):
    """Base exception for all HyperKit SDK-level errors."""


class HyperKitConfigurationError(HyperKitError):
    """Raised when HyperKit configuration is invalid."""


class HyperKitCompatibilityError(HyperKitError):
    """Raised when an incompatible HyperKit API is requested."""


class HyperKitRuntimeError(HyperKitError):
    """Raised when the HyperKit runtime cannot continue safely."""


class HyperKitValidationError(HyperKitError):
    """Raised when SDK or project validation fails."""
