"""Runtime environment detection for GameViz HyperKit."""

from __future__ import annotations

import os
import platform
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional


class PlatformKind(str, Enum):
    """Platforms recognized by HyperKit."""

    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    ANDROID = "android"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RuntimeEnvironment:
    """Information about the current HyperKit runtime environment."""

    platform: PlatformKind
    python_version: str
    python_implementation: str
    executable: str

    @property
    def is_android(self) -> bool:
        """Return whether HyperKit is running on Android."""

        return self.platform == PlatformKind.ANDROID

    @property
    def is_mobile(self) -> bool:
        """Return whether HyperKit is running on a mobile platform."""

        return self.is_android

    @property
    def is_desktop(self) -> bool:
        """Return whether HyperKit is running on a desktop platform."""

        return self.platform in {
            PlatformKind.WINDOWS,
            PlatformKind.MACOS,
            PlatformKind.LINUX,
        }

    def to_dict(self) -> dict[str, object]:
        """Return runtime information as a dictionary."""

        return {
            "platform": self.platform.value,
            "python_version": self.python_version,
            "python_implementation": self.python_implementation,
            "executable": self.executable,
            "is_android": self.is_android,
            "is_mobile": self.is_mobile,
            "is_desktop": self.is_desktop,
        }


def detect_platform(
    *,
    environ: Optional[Mapping[str, str]] = None,
    platform_name: Optional[str] = None,
    system_name: Optional[str] = None,
) -> PlatformKind:
    """Detect the current runtime platform.

    Optional arguments exist mainly to make detection deterministic
    during automated tests.
    """

    if environ is None:
        environ = os.environ

    if (
        "ANDROID_ARGUMENT" in environ
        or "P4A_BOOTSTRAP" in environ
    ):
        return PlatformKind.ANDROID

    if platform_name is None:
        platform_name = sys.platform

    normalized_platform = platform_name.strip().lower()

    if normalized_platform.startswith("android"):
        return PlatformKind.ANDROID

    if normalized_platform.startswith("win"):
        return PlatformKind.WINDOWS

    if normalized_platform == "darwin":
        return PlatformKind.MACOS

    if normalized_platform.startswith("linux"):
        return PlatformKind.LINUX

    if system_name is None:
        system_name = platform.system()

    normalized_system = system_name.strip().lower()

    if normalized_system == "windows":
        return PlatformKind.WINDOWS

    if normalized_system == "darwin":
        return PlatformKind.MACOS

    if normalized_system == "linux":
        return PlatformKind.LINUX

    if normalized_system == "android":
        return PlatformKind.ANDROID

    return PlatformKind.UNKNOWN


def detect_runtime_environment() -> RuntimeEnvironment:
    """Return information about the current runtime."""

    return RuntimeEnvironment(
        platform=detect_platform(),
        python_version=platform.python_version(),
        python_implementation=platform.python_implementation(),
        executable=sys.executable,
    )
