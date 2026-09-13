"""Runtime environment detection for GameViz HyperKit."""

from __future__ import annotations

import os
import platform
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional


class PlatformKind(str, Enum):
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    ANDROID = "android"
    UNKNOWN = "unknown"


def detect_wsl(
    *,
    environ: Optional[
        Mapping[str, str]
    ] = None,
    release_name: Optional[
        str
    ] = None,
) -> bool:
    """Return whether Linux is running inside WSL."""

    if environ is None:
        environ = os.environ

    if (
        "WSL_DISTRO_NAME" in environ
        or "WSL_INTEROP" in environ
    ):
        return True

    if release_name is None:
        release_name = (
            platform.release()
        )

    normalized_release = (
        release_name
        .strip()
        .lower()
    )

    return (
        "microsoft"
        in normalized_release
        or "wsl"
        in normalized_release
    )


@dataclass(frozen=True)
class RuntimeEnvironment:
    platform: PlatformKind
    python_version: str
    python_implementation: str
    executable: str

    machine: str = ""
    system: str = ""
    release: str = ""
    is_wsl: bool = False

    @property
    def is_android(
        self,
    ) -> bool:
        return (
            self.platform
            == PlatformKind.ANDROID
        )

    @property
    def is_mobile(
        self,
    ) -> bool:
        return self.is_android

    @property
    def is_windows(
        self,
    ) -> bool:
        return (
            self.platform
            == PlatformKind.WINDOWS
        )

    @property
    def is_linux(
        self,
    ) -> bool:
        return (
            self.platform
            == PlatformKind.LINUX
        )

    @property
    def is_macos(
        self,
    ) -> bool:
        return (
            self.platform
            == PlatformKind.MACOS
        )

    @property
    def is_desktop(
        self,
    ) -> bool:
        return self.platform in {
            PlatformKind.WINDOWS,
            PlatformKind.MACOS,
            PlatformKind.LINUX,
        }

    @property
    def device_family(
        self,
    ) -> str:
        if self.is_mobile:
            return "mobile"

        if self.is_desktop:
            return "desktop"

        return "unknown"

    def to_dict(
        self,
    ) -> dict[str, object]:
        """Stable HyperKit 0.2 environment dictionary."""

        return {
            "platform": (
                self.platform.value
            ),
            "python_version": (
                self.python_version
            ),
            "python_implementation": (
                self.python_implementation
            ),
            "executable": self.executable,
            "is_android": self.is_android,
            "is_mobile": self.is_mobile,
            "is_desktop": self.is_desktop,
        }

    def to_extended_dict(
        self,
    ) -> dict[str, object]:
        """Extended environment information for Phase 73."""

        data = self.to_dict()

        data.update(
            {
                "machine": self.machine,
                "system": self.system,
                "release": self.release,
                "is_wsl": self.is_wsl,
                "device_family": (
                    self.device_family
                ),
            }
        )

        return data


def detect_platform(
    *,
    environ: Optional[
        Mapping[str, str]
    ] = None,
    platform_name: Optional[
        str
    ] = None,
    system_name: Optional[
        str
    ] = None,
) -> PlatformKind:
    if environ is None:
        environ = os.environ

    if (
        "ANDROID_ARGUMENT"
        in environ
        or "P4A_BOOTSTRAP"
        in environ
    ):
        return PlatformKind.ANDROID

    if platform_name is None:
        platform_name = (
            sys.platform
        )

    normalized_platform = (
        platform_name
        .strip()
        .lower()
    )

    if normalized_platform.startswith(
        "android"
    ):
        return PlatformKind.ANDROID

    if normalized_platform.startswith(
        "win"
    ):
        return PlatformKind.WINDOWS

    if (
        normalized_platform
        == "darwin"
    ):
        return PlatformKind.MACOS

    if normalized_platform.startswith(
        "linux"
    ):
        return PlatformKind.LINUX

    if system_name is None:
        system_name = (
            platform.system()
        )

    normalized_system = (
        system_name
        .strip()
        .lower()
    )

    if normalized_system == "windows":
        return PlatformKind.WINDOWS

    if normalized_system == "darwin":
        return PlatformKind.MACOS

    if normalized_system == "linux":
        return PlatformKind.LINUX

    if normalized_system == "android":
        return PlatformKind.ANDROID

    return PlatformKind.UNKNOWN


def detect_runtime_environment(
) -> RuntimeEnvironment:
    platform_kind = (
        detect_platform()
    )

    release_name = (
        platform.release()
    )

    return RuntimeEnvironment(
        platform=platform_kind,
        python_version=(
            platform.python_version()
        ),
        python_implementation=(
            platform.python_implementation()
        ),
        executable=sys.executable,
        machine=platform.machine(),
        system=platform.system(),
        release=release_name,
        is_wsl=(
            platform_kind
            == PlatformKind.LINUX
            and detect_wsl(
                release_name=(
                    release_name
                )
            )
        ),
    )
