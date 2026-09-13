"""Android build, artifact, device, and deployment tooling.

This module provides the lower-level Android toolchain used by
GameViz HyperKit Phase 73.

Windows Android compilation is performed through WSL. Projects are
staged inside the Linux filesystem before Buildozer runs, then APK/AAB
artifacts are copied back to the original project bin directory.
"""

from __future__ import annotations

import platform
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)


DEFAULT_ANDROID_ACTIVITY = (
    "org.kivy.android.PythonActivity"
)

ANDROID_ARTIFACT_SUFFIXES = (
    ".apk",
    ".aab",
)


class AndroidToolchainError(
    RuntimeError
):
    """Raised when an Android toolchain operation cannot continue."""


@dataclass(frozen=True)
class AndroidArtifact:
    """Android build artifact discovered in a project."""

    path: Path
    kind: str
    size_bytes: int
    modified_time: float

    @property
    def name(
        self,
    ) -> str:
        return self.path.name


@dataclass(frozen=True)
class AndroidDevice:
    """ADB-connected Android device."""

    serial: str
    state: str

    model: Optional[
        str
    ] = None

    product: Optional[
        str
    ] = None

    device: Optional[
        str
    ] = None

    transport_id: Optional[
        str
    ] = None

    properties: Tuple[
        Tuple[str, str],
        ...,
    ] = ()

    @property
    def is_online(
        self,
    ) -> bool:
        return (
            self.state
            == "device"
        )


@dataclass(frozen=True)
class AndroidBuildResult:
    """Result of an Android Buildozer build."""

    strategy: str
    mode: str
    returncode: int
    artifacts: Tuple[
        AndroidArtifact,
        ...,
    ]

    project_path: Path
    staged_workspace: Optional[
        str
    ] = None

    @property
    def succeeded(
        self,
    ) -> bool:
        return (
            self.returncode == 0
            and bool(
                self.artifacts
            )
        )


def _artifact_kind(
    path: Path,
) -> str:
    suffix = (
        path.suffix.lower()
    )

    if suffix == ".apk":
        return "apk"

    if suffix == ".aab":
        return "aab"

    return (
        suffix.lstrip(".")
        or "unknown"
    )


def find_android_artifacts(
    project_path: Union[
        str,
        Path,
    ] = ".",
) -> Tuple[
    AndroidArtifact,
    ...,
]:
    """Find APK and AAB files under the project's bin directory."""

    root = Path(
        project_path
    ).resolve()

    bin_path = (
        root
        / "bin"
    )

    if not bin_path.exists():
        return ()

    artifacts: List[
        AndroidArtifact
    ] = []

    for path in (
        bin_path.rglob("*")
    ):
        if not path.is_file():
            continue

        if (
            path.suffix.lower()
            not in
            ANDROID_ARTIFACT_SUFFIXES
        ):
            continue

        stat = path.stat()

        artifacts.append(
            AndroidArtifact(
                path=path.resolve(),
                kind=(
                    _artifact_kind(
                        path
                    )
                ),
                size_bytes=(
                    stat.st_size
                ),
                modified_time=(
                    stat.st_mtime
                ),
            )
        )

    artifacts.sort(
        key=lambda item: (
            item.modified_time
        ),
        reverse=True,
    )

    return tuple(
        artifacts
    )


def select_android_artifact(
    project_path: Union[
        str,
        Path,
    ] = ".",
    *,
    artifact: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
    prefer_kind: str = "apk",
) -> AndroidArtifact:
    """Select an explicit or most-recent Android artifact."""

    if artifact is not None:
        path = Path(
            artifact
        ).resolve()

        if not path.is_file():
            raise AndroidToolchainError(
                "Android artifact does not exist: "
                f"{path}"
            )

        if (
            path.suffix.lower()
            not in
            ANDROID_ARTIFACT_SUFFIXES
        ):
            raise AndroidToolchainError(
                "Android artifact must be "
                "an APK or AAB file."
            )

        stat = path.stat()

        return AndroidArtifact(
            path=path,
            kind=(
                _artifact_kind(
                    path
                )
            ),
            size_bytes=stat.st_size,
            modified_time=(
                stat.st_mtime
            ),
        )

    artifacts = (
        find_android_artifacts(
            project_path
        )
    )

    if not artifacts:
        raise AndroidToolchainError(
            "No Android APK or AAB "
            "artifacts were found. "
            "Run an Android build first."
        )

    normalized_preference = (
        prefer_kind
        .strip()
        .lower()
    )

    for item in artifacts:
        if (
            item.kind
            == normalized_preference
        ):
            return item

    return artifacts[0]


def parse_adb_devices(
    output: str,
) -> Tuple[
    AndroidDevice,
    ...,
]:
    """Parse `adb devices -l` output."""

    devices: List[
        AndroidDevice
    ] = []

    for raw_line in (
        output.splitlines()
    ):
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith(
            "List of devices"
        ):
            continue

        if line.startswith("*"):
            continue

        parts = line.split()

        if len(parts) < 2:
            continue

        serial = parts[0]
        state = parts[1]

        properties: Dict[
            str,
            str,
        ] = {}

        for item in parts[2:]:
            if ":" not in item:
                continue

            key, value = (
                item.split(
                    ":",
                    1,
                )
            )

            properties[
                key
            ] = value

        devices.append(
            AndroidDevice(
                serial=serial,
                state=state,
                model=(
                    properties.get(
                        "model"
                    )
                ),
                product=(
                    properties.get(
                        "product"
                    )
                ),
                device=(
                    properties.get(
                        "device"
                    )
                ),
                transport_id=(
                    properties.get(
                        "transport_id"
                    )
                ),
                properties=tuple(
                    sorted(
                        properties.items()
                    )
                ),
            )
        )

    return tuple(
        devices
    )


def resolve_adb_executable(
    adb_path: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
) -> str:
    if adb_path is not None:
        path = Path(
            adb_path
        )

        if not path.exists():
            raise AndroidToolchainError(
                "ADB executable was "
                "not found: "
                f"{path}"
            )

        return str(
            path
        )

    discovered = (
        shutil.which(
            "adb"
        )
    )

    if not discovered:
        raise AndroidToolchainError(
            "ADB was not found on PATH. "
            "Install Android Platform Tools "
            "or add adb to PATH."
        )

    return discovered


def list_android_devices(
    *,
    adb_path: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
) -> Tuple[
    AndroidDevice,
    ...,
]:
    adb = (
        resolve_adb_executable(
            adb_path
        )
    )

    result = subprocess.run(
        [
            adb,
            "devices",
            "-l",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise AndroidToolchainError(
            "ADB device query failed: "
            f"{result.stderr.strip()}"
        )

    return parse_adb_devices(
        result.stdout
    )


def select_android_device(
    devices: Sequence[
        AndroidDevice
    ],
    *,
    serial: Optional[
        str
    ] = None,
) -> AndroidDevice:
    """Resolve the target ADB device."""

    if serial:
        for device in devices:
            if (
                device.serial
                == serial
            ):
                if not (
                    device.is_online
                ):
                    raise AndroidToolchainError(
                        f"Android device "
                        f"'{serial}' is "
                        f"not ready: "
                        f"{device.state}"
                    )

                return device

        raise AndroidToolchainError(
            "Android device was "
            "not found: "
            f"{serial}"
        )

    online = [
        device
        for device in devices
        if device.is_online
    ]

    if not online:
        raise AndroidToolchainError(
            "No authorized Android "
            "device is connected."
        )

    if len(online) > 1:
        names = ", ".join(
            device.serial
            for device in online
        )

        raise AndroidToolchainError(
            "Multiple Android devices "
            "are connected. "
            "Specify --serial. "
            f"Devices: {names}"
        )

    return online[0]


def read_android_package_id(
    project_path: Union[
        str,
        Path,
    ] = ".",
) -> str:
    """Read application ID from buildozer.spec."""

    root = Path(
        project_path
    ).resolve()

    spec = (
        root
        / "buildozer.spec"
    )

    if not spec.is_file():
        raise AndroidToolchainError(
            "buildozer.spec was "
            "not found: "
            f"{spec}"
        )

    package_name: Optional[
        str
    ] = None

    package_domain: Optional[
        str
    ] = None

    in_app_section = False

    for raw_line in (
        spec.read_text(
            encoding="utf-8"
        ).splitlines()
    ):
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if (
            line.startswith("[")
            and line.endswith("]")
        ):
            in_app_section = (
                line.lower()
                == "[app]"
            )

            continue

        if not in_app_section:
            continue

        if "=" not in line:
            continue

        key, value = (
            line.split(
                "=",
                1,
            )
        )

        key = (
            key.strip().lower()
        )

        value = (
            value.strip()
        )

        if (
            key
            == "package.name"
        ):
            package_name = value

        elif (
            key
            == "package.domain"
        ):
            package_domain = value

    if not package_name:
        raise AndroidToolchainError(
            "buildozer.spec is missing "
            "package.name."
        )

    if not package_domain:
        raise AndroidToolchainError(
            "buildozer.spec is missing "
            "package.domain."
        )

    return (
        f"{package_domain}."
        f"{package_name}"
    )


def _adb_target_args(
    adb: str,
    device: AndroidDevice,
) -> List[str]:
    return [
        adb,
        "-s",
        device.serial,
    ]


def install_android_artifact(
    artifact: AndroidArtifact,
    *,
    serial: Optional[
        str
    ] = None,
    adb_path: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
    replace: bool = True,
) -> AndroidDevice:
    """Install an APK onto a connected Android device."""

    if artifact.kind != "apk":
        raise AndroidToolchainError(
            "ADB installation requires "
            "an APK artifact."
        )

    adb = (
        resolve_adb_executable(
            adb_path
        )
    )

    devices = (
        list_android_devices(
            adb_path=adb
        )
    )

    device = (
        select_android_device(
            devices,
            serial=serial,
        )
    )

    command = (
        _adb_target_args(
            adb,
            device,
        )
    )

    command.append(
        "install"
    )

    if replace:
        command.append(
            "-r"
        )

    command.append(
        str(
            artifact.path
        )
    )

    result = subprocess.run(
        command,
        check=False,
    )

    if result.returncode != 0:
        raise AndroidToolchainError(
            "ADB installation failed "
            f"for device "
            f"{device.serial}."
        )

    return device


def launch_android_app(
    package_id: str,
    *,
    serial: Optional[
        str
    ] = None,
    activity: str = (
        DEFAULT_ANDROID_ACTIVITY
    ),
    adb_path: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
) -> AndroidDevice:
    """Launch a HyperKit Android application."""

    normalized_package = (
        package_id.strip()
    )

    normalized_activity = (
        activity.strip()
    )

    if not normalized_package:
        raise AndroidToolchainError(
            "Android package ID "
            "cannot be empty."
        )

    if not normalized_activity:
        raise AndroidToolchainError(
            "Android activity "
            "cannot be empty."
        )

    adb = (
        resolve_adb_executable(
            adb_path
        )
    )

    devices = (
        list_android_devices(
            adb_path=adb
        )
    )

    device = (
        select_android_device(
            devices,
            serial=serial,
        )
    )

    component = (
        f"{normalized_package}/"
        f"{normalized_activity}"
    )

    command = (
        _adb_target_args(
            adb,
            device,
        )
        + [
            "shell",
            "am",
            "start",
            "-n",
            component,
        ]
    )

    result = subprocess.run(
        command,
        check=False,
    )

    if result.returncode != 0:
        raise AndroidToolchainError(
            "Failed to launch "
            f"{normalized_package} "
            f"on device "
            f"{device.serial}."
        )

    return device


def deploy_android_artifact(
    project_path: Union[
        str,
        Path,
    ] = ".",
    *,
    artifact: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
    serial: Optional[
        str
    ] = None,
    package_id: Optional[
        str
    ] = None,
    activity: str = (
        DEFAULT_ANDROID_ACTIVITY
    ),
    adb_path: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
) -> Tuple[
    AndroidArtifact,
    AndroidDevice,
]:
    """Install and launch a project's most recent APK."""

    selected = (
        select_android_artifact(
            project_path,
            artifact=artifact,
            prefer_kind="apk",
        )
    )

    device = (
        install_android_artifact(
            selected,
            serial=serial,
            adb_path=adb_path,
        )
    )

    resolved_package = (
        package_id
        or read_android_package_id(
            project_path
        )
    )

    launch_android_app(
        resolved_package,
        serial=device.serial,
        activity=activity,
        adb_path=adb_path,
    )

    return (
        selected,
        device,
    )


def resolve_wsl_executable(
    executable: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
) -> str:
    if executable is not None:
        path = Path(
            executable
        )

        if not path.exists():
            raise AndroidToolchainError(
                "WSL executable was "
                "not found: "
                f"{path}"
            )

        return str(
            path
        )

    discovered = (
        shutil.which(
            "wsl"
        )
        or shutil.which(
            "wsl.exe"
        )
    )

    if not discovered:
        raise AndroidToolchainError(
            "WSL was not found. "
            "Install WSL 2 and a "
            "Linux distribution."
        )

    return discovered


def _wsl_prefix(
    executable: str,
    distro: Optional[
        str
    ],
) -> List[str]:
    command = [
        executable,
    ]

    if distro:
        command.extend(
            [
                "-d",
                distro,
            ]
        )

    return command


def windows_path_to_wsl(
    path: Union[
        str,
        Path,
    ],
    *,
    wsl_executable: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
    distro: Optional[
        str
    ] = None,
) -> str:
    """Convert a Windows path using WSL's own wslpath utility."""

    executable = (
        resolve_wsl_executable(
            wsl_executable
        )
    )

    command = (
        _wsl_prefix(
            executable,
            distro,
        )
        + [
            "wslpath",
            "-a",
            "-u",
            str(
                Path(path).resolve()
            ),
        ]
    )

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise AndroidToolchainError(
            "Could not convert "
            "Windows path to WSL path: "
            f"{result.stderr.strip()}"
        )

    converted = (
        result.stdout.strip()
    )

    if not converted:
        raise AndroidToolchainError(
            "WSL returned an empty "
            "path conversion result."
        )

    return converted


def wsl_has_command(
    name: str,
    *,
    wsl_executable: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
    distro: Optional[
        str
    ] = None,
) -> bool:
    executable = (
        resolve_wsl_executable(
            wsl_executable
        )
    )

    command = (
        _wsl_prefix(
            executable,
            distro,
        )
        + [
            "bash",
            "-lc",
            (
                "command -v "
                f"{shlex.quote(name)} "
                ">/dev/null 2>&1"
            ),
        ]
    )

    result = subprocess.run(
        command,
        check=False,
    )

    return (
        result.returncode
        == 0
    )


def _workspace_name(
    project_path: Path,
) -> str:
    value = "".join(
        character
        if (
            character.isalnum()
            or character
            in {
                "-",
                "_",
            }
        )
        else "_"
        for character
        in project_path.name
    )

    return (
        value
        or "hyperkit-game"
    )


def build_android_with_wsl(
    project_path: Union[
        str,
        Path,
    ] = ".",
    *,
    mode: str = "debug",
    distro: Optional[
        str
    ] = None,
    wsl_executable: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
    sdk_source: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
) -> AndroidBuildResult:
    """Build Android through WSL using a Linux-side staging directory."""

    normalized_mode = (
        mode.strip().lower()
    )

    if normalized_mode not in {
        "debug",
        "release",
    }:
        raise AndroidToolchainError(
            "Android build mode must "
            "be 'debug' or 'release'."
        )

    project = Path(
        project_path
    ).resolve()

    if not project.is_dir():
        raise AndroidToolchainError(
            "Project directory does "
            "not exist: "
            f"{project}"
        )

    spec = (
        project
        / "buildozer.spec"
    )

    if not spec.is_file():
        raise AndroidToolchainError(
            "buildozer.spec was not "
            "found. Run "
            "'hyperkit init-android' first."
        )

    executable = (
        resolve_wsl_executable(
            wsl_executable
        )
    )

    if not wsl_has_command(
        "buildozer",
        wsl_executable=executable,
        distro=distro,
    ):
        raise AndroidToolchainError(
            "Buildozer is not installed "
            "inside the selected WSL "
            "Linux environment."
        )

    if sdk_source is None:
        sdk_source = (
            Path(__file__)
            .resolve()
            .parent
        )

    sdk_path = Path(
        sdk_source
    ).resolve()

    if not (
        sdk_path
        / "__init__.py"
    ).is_file():
        raise AndroidToolchainError(
            "HyperKit SDK source "
            "directory is invalid: "
            f"{sdk_path}"
        )

    wsl_project = (
        windows_path_to_wsl(
            project,
            wsl_executable=executable,
            distro=distro,
        )
    )

    wsl_sdk = (
        windows_path_to_wsl(
            sdk_path,
            wsl_executable=executable,
            distro=distro,
        )
    )

    name = (
        _workspace_name(
            project
        )
    )

    workspace = (
        "$HOME/.hyperkit/"
        f"builds/{name}"
    )

    quoted_source = (
        shlex.quote(
            wsl_project
        )
    )

    quoted_sdk = (
        shlex.quote(
            wsl_sdk
        )
    )

    script = "\n".join(
        [
            "set -e",
            (
                "SRC="
                f"{quoted_source}"
            ),
            (
                "SDK="
                f"{quoted_sdk}"
            ),
            (
                'WORK="'
                f"{workspace}"
                '"'
            ),
            'rm -rf "$WORK"',
            'mkdir -p "$WORK"',
            'cp -a "$SRC"/. "$WORK"/',
            (
                'rm -rf '
                '"$WORK/.git" '
                '"$WORK/.buildozer" '
                '"$WORK/build" '
                '"$WORK/dist" '
                '"$WORK/bin" '
                '"$WORK/hyperkit"'
            ),
            (
                'cp -a "$SDK" '
                '"$WORK/hyperkit"'
            ),
            (
                "sed -i "
                "'s/,gameviz-hyperkit//g; "
                "s/gameviz-hyperkit,//g; "
                "s/gameviz-hyperkit//g' "
                '"$WORK/buildozer.spec"'
            ),
            'cd "$WORK"',
            (
                "buildozer android "
                f"{normalized_mode}"
            ),
            'mkdir -p "$SRC/bin"',
            (
                'find "$WORK/bin" '
                "-maxdepth 1 "
                "-type f "
                "\\( "
                "-name '*.apk' "
                "-o "
                "-name '*.aab' "
                "\\) "
                "-exec cp -f {} "
                '"$SRC/bin/" \\;'
            ),
        ]
    )

    command = (
        _wsl_prefix(
            executable,
            distro,
        )
        + [
            "bash",
            "-lc",
            script,
        ]
    )

    result = subprocess.run(
        command,
        check=False,
    )

    artifacts = (
        find_android_artifacts(
            project
        )
    )

    if (
        result.returncode == 0
        and not artifacts
    ):
        raise AndroidToolchainError(
            "Buildozer completed but "
            "no APK or AAB was copied "
            "back to the project bin "
            "directory."
        )

    return AndroidBuildResult(
        strategy="wsl",
        mode=normalized_mode,
        returncode=(
            result.returncode
        ),
        artifacts=artifacts,
        project_path=project,
        staged_workspace=(
            workspace
        ),
    )


def build_android_local(
    project_path: Union[
        str,
        Path,
    ] = ".",
    *,
    mode: str = "debug",
    buildozer_executable: Optional[
        Union[
            str,
            Path,
        ]
    ] = None,
) -> AndroidBuildResult:
    """Run Buildozer directly on Linux/macOS."""

    normalized_mode = (
        mode.strip().lower()
    )

    if normalized_mode not in {
        "debug",
        "release",
    }:
        raise AndroidToolchainError(
            "Android build mode must "
            "be 'debug' or 'release'."
        )

    project = Path(
        project_path
    ).resolve()

    if not project.is_dir():
        raise AndroidToolchainError(
            "Project directory does "
            "not exist: "
            f"{project}"
        )

    spec = (
        project
        / "buildozer.spec"
    )

    if not spec.is_file():
        raise AndroidToolchainError(
            "buildozer.spec was not "
            "found. Run "
            "'hyperkit init-android' first."
        )

    if buildozer_executable:
        buildozer = str(
            buildozer_executable
        )

    else:
        buildozer = (
            shutil.which(
                "buildozer"
            )
        )

    if not buildozer:
        raise AndroidToolchainError(
            "Buildozer was not found "
            "on PATH."
        )

    result = subprocess.run(
        [
            buildozer,
            "android",
            normalized_mode,
        ],
        cwd=project,
        check=False,
    )

    artifacts = (
        find_android_artifacts(
            project
        )
    )

    return AndroidBuildResult(
        strategy="local",
        mode=normalized_mode,
        returncode=(
            result.returncode
        ),
        artifacts=artifacts,
        project_path=project,
    )


def build_android(
    project_path: Union[
        str,
        Path,
    ] = ".",
    *,
    mode: str = "debug",
    distro: Optional[
        str
    ] = None,
) -> AndroidBuildResult:
    """Build Android using the appropriate host strategy."""

    host = (
        platform.system()
        .strip()
        .lower()
    )

    if host == "windows":
        return (
            build_android_with_wsl(
                project_path,
                mode=mode,
                distro=distro,
            )
        )

    if host in {
        "linux",
        "darwin",
    }:
        return (
            build_android_local(
                project_path,
                mode=mode,
            )
        )

    raise AndroidToolchainError(
        "Android builds are not "
        "supported on host platform: "
        f"{platform.system()}"
    )
