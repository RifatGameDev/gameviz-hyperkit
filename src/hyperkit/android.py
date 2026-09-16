from __future__ import annotations

import platform
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple, Union


DEFAULT_PACKAGE_DOMAIN = "org.gameviz"
DEFAULT_APP_VERSION = "0.1.0"
DEFAULT_ORIENTATION = "portrait"

DEFAULT_ANDROID_API = 35
DEFAULT_ANDROID_MIN_API = 24
MIN_SUPPORTED_ANDROID_API = 24

DEFAULT_ANDROID_PYTHON_VERSION = "3.11.9"
DEFAULT_ANDROID_HOST_PYTHON_VERSION = "3.11.9"

DEFAULT_ACCEPT_SDK_LICENSE = True

DEFAULT_ANDROID_PERMISSIONS = (
    "VIBRATE",
)

# Phase 73 real-device validation was completed on ARM64.
#
# Additional architectures can still be supplied explicitly when
# generating a buildozer.spec, but ARM64 is the validated default.
DEFAULT_ANDROID_ARCHS = (
    "arm64-v8a",
)

DEFAULT_REQUIREMENTS = (
    f"python3=={DEFAULT_ANDROID_PYTHON_VERSION}",
    f"hostpython3=={DEFAULT_ANDROID_HOST_PYTHON_VERSION}",
    "kivy",
    "gameviz-hyperkit",
)

DEFAULT_SOURCE_INCLUDE_EXTS = (
    "py",
    "png",
    "jpg",
    "jpeg",
    "webp",
    "kv",
    "atlas",
    "json",
    "csv",
    "txt",
    "wav",
    "mp3",
    "ogg",
    "ttf",
    "otf",
)

SUPPORTED_ORIENTATIONS = (
    "portrait",
    "landscape",
    "sensor",
    "all",
)


def _clean_identifier(
    value: str,
    *,
    fallback: str,
) -> str:
    cleaned = "".join(
        ch.lower() if ch.isalnum() else "_"
        for ch in value.strip()
    ).strip("_")

    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")

    if not cleaned:
        cleaned = fallback

    if cleaned[0].isdigit():
        cleaned = f"game_{cleaned}"

    return cleaned


def normalized_package_name(title: str) -> str:
    """
    Return an Android-safe package name derived from a title.

    Example:
        "Tap Counter Game" -> "tap_counter_game"
    """

    return _clean_identifier(
        title,
        fallback="hyperkit_game",
    )


def normalized_package_domain(domain: str) -> str:
    """
    Normalize a dotted Android package domain.

    Example:
        "com.GameViz" -> "com.gameviz"
    """

    raw_segments = [
        segment
        for segment in domain.strip().split(".")
        if segment.strip()
    ]

    if not raw_segments:
        return DEFAULT_PACKAGE_DOMAIN

    segments = [
        _clean_identifier(
            segment,
            fallback="gameviz",
        )
        for segment in raw_segments
    ]

    if len(segments) == 1:
        segments.insert(
            0,
            "org",
        )

    return ".".join(segments)


def normalize_permissions(
    permissions: Iterable[str],
) -> Tuple[str, ...]:
    normalized = []
    seen = set()

    for permission in permissions:
        value = permission.strip().upper()

        if not value:
            continue

        if value in seen:
            continue

        seen.add(value)
        normalized.append(value)

    return tuple(normalized)


def normalize_archs(
    archs: Iterable[str],
) -> Tuple[str, ...]:
    normalized = []
    seen = set()

    for arch in archs:
        value = arch.strip()

        if not value:
            continue

        if value in seen:
            continue

        seen.add(value)
        normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True)
class AndroidBuildConfig:
    """
    Android application/build configuration used when generating
    buildozer.spec.

    The defaults represent the Android configuration validated during
    HyperKit Phase 73:

    - Android target API 35
    - Android minimum API 24
    - Python 3.11.9
    - hostpython 3.11.9
    - ARM64
    - automatic Android SDK license acceptance

    Individual projects may still override supported settings where
    appropriate.
    """

    title: str = "HyperKit Game"

    package_name: Optional[str] = None

    package_domain: str = DEFAULT_PACKAGE_DOMAIN

    version: str = DEFAULT_APP_VERSION

    requirements: Tuple[str, ...] = DEFAULT_REQUIREMENTS

    orientation: str = DEFAULT_ORIENTATION

    fullscreen: bool = False

    permissions: Tuple[str, ...] = DEFAULT_ANDROID_PERMISSIONS

    android_api: int = DEFAULT_ANDROID_API

    min_api: int = DEFAULT_ANDROID_MIN_API

    ndk: Optional[str] = None

    archs: Tuple[str, ...] = DEFAULT_ANDROID_ARCHS

    accept_sdk_license: bool = DEFAULT_ACCEPT_SDK_LICENSE

    source_include_exts: Tuple[str, ...] = (
        DEFAULT_SOURCE_INCLUDE_EXTS
    )

    def __post_init__(self) -> None:
        title = self.title.strip()

        if not title:
            raise ValueError(
                "Android app title cannot be empty."
            )

        package_name = (
            self.package_name
            or normalized_package_name(title)
        )

        package_name = normalized_package_name(
            package_name
        )

        package_domain = normalized_package_domain(
            self.package_domain
        )

        orientation = (
            self.orientation
            .strip()
            .lower()
        )

        if orientation not in SUPPORTED_ORIENTATIONS:
            available = ", ".join(
                SUPPORTED_ORIENTATIONS
            )

            raise ValueError(
                f"Unsupported Android orientation "
                f"'{self.orientation}'. "
                f"Choose one of: {available}."
            )

        if self.android_api <= 0:
            raise ValueError(
                "android_api must be greater than zero."
            )

        if self.min_api <= 0:
            raise ValueError(
                "min_api must be greater than zero."
            )

        if self.min_api < MIN_SUPPORTED_ANDROID_API:
            raise ValueError(
                "min_api must be at least "
                f"{MIN_SUPPORTED_ANDROID_API} "
                "for HyperKit Android builds."
            )

        if self.min_api > self.android_api:
            raise ValueError(
                "min_api cannot be greater than android_api."
            )

        requirements = tuple(
            item.strip()
            for item in self.requirements
            if item.strip()
        )

        if not requirements:
            raise ValueError(
                "At least one Android build requirement "
                "is required."
            )

        permissions = normalize_permissions(
            self.permissions
        )

        archs = normalize_archs(
            self.archs
        )

        if not archs:
            raise ValueError(
                "At least one Android architecture "
                "is required."
            )

        source_include_exts = tuple(
            item
            .strip()
            .lstrip(".")
            .lower()
            for item in self.source_include_exts
            if item.strip()
        )

        if not source_include_exts:
            raise ValueError(
                "At least one source file extension "
                "is required."
            )

        object.__setattr__(
            self,
            "title",
            title,
        )

        object.__setattr__(
            self,
            "package_name",
            package_name,
        )

        object.__setattr__(
            self,
            "package_domain",
            package_domain,
        )

        object.__setattr__(
            self,
            "orientation",
            orientation,
        )

        object.__setattr__(
            self,
            "requirements",
            requirements,
        )

        object.__setattr__(
            self,
            "permissions",
            permissions,
        )

        object.__setattr__(
            self,
            "archs",
            archs,
        )

        object.__setattr__(
            self,
            "source_include_exts",
            source_include_exts,
        )

        if self.ndk is not None:
            ndk = self.ndk.strip()

            object.__setattr__(
                self,
                "ndk",
                ndk or None,
            )


@dataclass(frozen=True)
class AndroidBuildEnvironment:
    """
    Information about the local Android build environment.
    """

    host_platform: str

    buildozer_path: Optional[str]

    java_path: Optional[str]

    adb_path: Optional[str]

    wsl_path: Optional[str]

    direct_android_build_supported: bool

    can_run_android_build: bool

    guidance: str


@dataclass(frozen=True)
class AndroidReadinessCheck:
    name: str

    passed: bool

    message: str

    required: bool = True


@dataclass(frozen=True)
class AndroidReadinessReport:
    root: Path

    environment: AndroidBuildEnvironment

    checks: Tuple[
        AndroidReadinessCheck,
        ...,
    ]

    @property
    def failed_required(
        self,
    ) -> Tuple[
        AndroidReadinessCheck,
        ...,
    ]:
        return tuple(
            check
            for check in self.checks
            if (
                check.required
                and not check.passed
            )
        )

    @property
    def passed(self) -> bool:
        return not self.failed_required


def detect_android_build_environment(
) -> AndroidBuildEnvironment:
    """
    Detect Android-related development tools and host support.

    HyperKit can generate Android configuration on every supported
    desktop platform.

    Native Buildozer compilation is expected to run on Linux/macOS.

    Windows development is supported through the HyperKit
    Windows-first workflow:

    - develop locally on Windows
    - generate Android configuration locally
    - compile the APK in GitHub Actions/Linux
    - download the APK to Windows
    - deploy to a physical Android device through ADB

    Local Linux or WSL is not required for that cloud-build workflow.
    """

    host_platform = (
        platform.system()
        or "Unknown"
    )

    normalized_host = (
        host_platform.lower()
    )

    buildozer_path = shutil.which(
        "buildozer"
    )

    java_path = shutil.which(
        "java"
    )

    adb_path = shutil.which(
        "adb"
    )

    # Keep WSL detection for backwards compatibility with the existing
    # environment-report structure, but HyperKit no longer recommends
    # WSL as the default Windows Android workflow.
    wsl_path = (
        shutil.which("wsl")
        or shutil.which("wsl.exe")
    )

    direct_supported = (
        normalized_host
        in {
            "linux",
            "darwin",
        }
    )

    can_run = (
        direct_supported
        and buildozer_path is not None
    )

    if normalized_host == "windows":
        guidance = (
            "Windows detected. HyperKit can generate Android "
            "configuration and deploy APKs through ADB on "
            "native Windows. Compile Android APKs with the "
            "HyperKit GitHub Actions/Linux cloud-build "
            "workflow; local Linux or WSL is not required."
        )

    elif (
        direct_supported
        and buildozer_path is None
    ):
        guidance = (
            "This host can run the Android toolchain, "
            "but Buildozer was not found. Install "
            "HyperKit's Android extra and required "
            "system packages first."
        )

    elif can_run:
        guidance = (
            "Android build environment is available."
        )

    else:
        guidance = (
            f"Android build support is not configured "
            f"for host platform '{host_platform}'."
        )

    return AndroidBuildEnvironment(
        host_platform=host_platform,
        buildozer_path=buildozer_path,
        java_path=java_path,
        adb_path=adb_path,
        wsl_path=wsl_path,
        direct_android_build_supported=(
            direct_supported
        ),
        can_run_android_build=can_run,
        guidance=guidance,
    )


def render_buildozer_spec(
    config: AndroidBuildConfig,
) -> str:
    permissions = ",".join(
        config.permissions
    )

    archs = ", ".join(
        config.archs
    )

    requirements = ",".join(
        config.requirements
    )

    include_exts = ",".join(
        config.source_include_exts
    )

    lines = [
        "[app]",
        f"title = {config.title}",
        (
            "package.name = "
            f"{config.package_name}"
        ),
        (
            "package.domain = "
            f"{config.package_domain}"
        ),
        "",
        "source.dir = .",
        (
            "source.include_exts = "
            f"{include_exts}"
        ),
        (
            "source.exclude_dirs = "
            ".git,.github,.venv,venv,"
            "build,dist,tests,__pycache__"
        ),
        "",
        f"version = {config.version}",
        (
            "requirements = "
            f"{requirements}"
        ),
        "",
        (
            "orientation = "
            f"{config.orientation}"
        ),
        (
            "fullscreen = "
            f"{1 if config.fullscreen else 0}"
        ),
        "",
    ]

    if permissions:
        lines.append(
            "android.permissions = "
            f"{permissions}"
        )

    lines.extend(
        [
            (
                "android.api = "
                f"{config.android_api}"
            ),
            (
                "android.minapi = "
                f"{config.min_api}"
            ),
            (
                "android.accept_sdk_license = "
                f"{config.accept_sdk_license}"
            ),
        ]
    )

    if config.ndk:
        lines.append(
            f"android.ndk = {config.ndk}"
        )

    lines.extend(
        [
            (
                "android.archs = "
                f"{archs}"
            ),
            "",
            "[buildozer]",
            "log_level = 2",
            "warn_on_root = 1",
            "",
        ]
    )

    return "\n".join(lines)


def create_buildozer_spec(
    path: Union[str, Path] = ".",
    title: str = "HyperKit Game",
    overwrite: bool = False,
    *,
    package_name: Optional[str] = None,
    package_domain: str = (
        DEFAULT_PACKAGE_DOMAIN
    ),
    version: str = DEFAULT_APP_VERSION,
    orientation: str = DEFAULT_ORIENTATION,
    fullscreen: bool = False,
    permissions: Optional[
        Sequence[str]
    ] = None,
    android_api: int = DEFAULT_ANDROID_API,
    min_api: int = DEFAULT_ANDROID_MIN_API,
    ndk: Optional[str] = None,
    archs: Optional[
        Sequence[str]
    ] = None,
    requirements: Optional[
        Sequence[str]
    ] = None,
    accept_sdk_license: bool = (
        DEFAULT_ACCEPT_SDK_LICENSE
    ),
) -> Path:
    """
    Create buildozer.spec for a HyperKit project.

    Existing files are preserved unless overwrite=True.

    Defaults match the Android configuration validated during
    HyperKit Phase 73 real-device testing.
    """

    root = Path(path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Project path does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Project path is not a directory: {root}"
        )

    spec_path = (
        root
        / "buildozer.spec"
    )

    if (
        spec_path.exists()
        and not overwrite
    ):
        return spec_path

    config = AndroidBuildConfig(
        title=title,
        package_name=package_name,
        package_domain=package_domain,
        version=version,
        requirements=tuple(
            requirements
            or DEFAULT_REQUIREMENTS
        ),
        orientation=orientation,
        fullscreen=fullscreen,
        permissions=tuple(
            DEFAULT_ANDROID_PERMISSIONS
            if permissions is None
            else permissions
        ),
        android_api=android_api,
        min_api=min_api,
        ndk=ndk,
        archs=tuple(
            archs
            or DEFAULT_ANDROID_ARCHS
        ),
        accept_sdk_license=(
            accept_sdk_license
        ),
    )

    spec_path.write_text(
        render_buildozer_spec(config),
        encoding="utf-8",
    )

    return spec_path


def generate_android_readiness_report(
    path: Union[str, Path] = ".",
    *,
    require_build_tools: bool = False,
) -> AndroidReadinessReport:
    root = Path(path).resolve()

    environment = (
        detect_android_build_environment()
    )

    checks = [
        AndroidReadinessCheck(
            name="Project directory",
            passed=(
                root.exists()
                and root.is_dir()
            ),
            message=(
                f"Found project directory: {root}"
                if (
                    root.exists()
                    and root.is_dir()
                )
                else (
                    "Project directory not found: "
                    f"{root}"
                )
            ),
        ),

        AndroidReadinessCheck(
            name="Main entry point",
            passed=(
                root
                / "main.py"
            ).is_file(),
            message=(
                "Found main.py"
                if (
                    root
                    / "main.py"
                ).is_file()
                else "Missing main.py"
            ),
        ),

        AndroidReadinessCheck(
            name=(
                "HyperKit project metadata"
            ),
            passed=(
                root
                / "hyperkit.toml"
            ).is_file(),
            message=(
                "Found hyperkit.toml"
                if (
                    root
                    / "hyperkit.toml"
                ).is_file()
                else "Missing hyperkit.toml"
            ),
        ),

        AndroidReadinessCheck(
            name="Buildozer configuration",
            passed=(
                root
                / "buildozer.spec"
            ).is_file(),
            message=(
                "Found buildozer.spec"
                if (
                    root
                    / "buildozer.spec"
                ).is_file()
                else (
                    "Missing buildozer.spec; "
                    "run 'hyperkit init-android'."
                )
            ),
        ),

        AndroidReadinessCheck(
            name="Host platform",
            passed=(
                environment
                .direct_android_build_supported
            ),
            message=environment.guidance,
            required=require_build_tools,
        ),

        AndroidReadinessCheck(
            name="Buildozer executable",
            passed=(
                environment.buildozer_path
                is not None
            ),
            message=(
                "Found Buildozer: "
                f"{environment.buildozer_path}"
                if environment.buildozer_path
                else (
                    "Buildozer executable "
                    "not found."
                )
            ),
            required=require_build_tools,
        ),

        AndroidReadinessCheck(
            name="Java runtime",
            passed=(
                environment.java_path
                is not None
            ),
            message=(
                "Found Java: "
                f"{environment.java_path}"
                if environment.java_path
                else (
                    "Java executable "
                    "not found on PATH."
                )
            ),
            required=False,
        ),

        AndroidReadinessCheck(
            name="ADB",
            passed=(
                environment.adb_path
                is not None
            ),
            message=(
                "Found ADB: "
                f"{environment.adb_path}"
                if environment.adb_path
                else (
                    "ADB not found on PATH; "
                    "device deployment will "
                    "need Android platform tools."
                )
            ),
            required=False,
        ),
    ]

    return AndroidReadinessReport(
        root=root,
        environment=environment,
        checks=tuple(checks),
    )


def format_android_readiness_report(
    report: AndroidReadinessReport,
) -> str:
    lines = [
        "HyperKit Android Readiness",
        "==========================",
        f"Project: {report.root}",
        (
            "Host: "
            f"{report.environment.host_platform}"
        ),
        "",
    ]

    for check in report.checks:
        if check.passed:
            marker = "PASS"

        elif check.required:
            marker = "FAIL"

        else:
            marker = "WARN"

        lines.append(
            f"[{marker}] "
            f"{check.name}: "
            f"{check.message}"
        )

    lines.extend(
        [
            "",
            (
                "Android readiness: "
                f"{'PASS' if report.passed else 'FAIL'}"
            ),
        ]
    )

    if not (
        report.environment
        .can_run_android_build
    ):
        lines.append(
            report.environment.guidance
        )

    return "\n".join(lines)
