"""Frozen public API contract for GameViz HyperKit 1.0."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping
from typing import Optional

from .errors import HyperKitCompatibilityError


FROZEN_API_VERSION = "1.0"
FROZEN_API_EXPORT_COUNT = 256
FROZEN_API_FINGERPRINT = (
    "80bdc58a8590797b01faa0305ec3aac2"
    "2ed81ea17fc98b8d9a02ec211fa70d75"
)

FROZEN_PUBLIC_API = frozenset(
    {
        "ADMOB_APPLICATION_ID_META_DATA",
        "ADMOB_SAMPLE_APP_ID",
        "ADMOB_SDK_DEPENDENCY",
        "ADMOB_TEST_BANNER_ID",
        "ADMOB_TEST_INTERSTITIAL_ID",
        "ADMOB_TEST_PLACEMENTS",
        "ADMOB_TEST_REWARDED_ID",
        "ALLOWED_QA_STATUSES",
        "API_VERSION",
        "AdConfig",
        "AdMobAndroidBridge",
        "AdMobAndroidProvider",
        "AdProvider",
        "AdResult",
        "AdStatus",
        "AdType",
        "AdsService",
        "AnalyticsEvent",
        "AnalyticsProvider",
        "AnalyticsResult",
        "AnalyticsService",
        "AndroidAdBridge",
        "AndroidAdBuildRequirements",
        "AndroidAdProvider",
        "AndroidAnalyticsBridge",
        "AndroidAnalyticsBuildRequirements",
        "AndroidAnalyticsProvider",
        "AnimationManager",
        "AssetError",
        "AssetManager",
        "AssetNotFoundError",
        "AudioError",
        "AudioLoadError",
        "AudioManager",
        "BodyType",
        "Bounds",
        "BoundsManager",
        "Button",
        "COMPLETE_GAME_TEMPLATES",
        "CameraFollow",
        "CameraShake",
        "CanvasScaler",
        "Circle",
        "CleanInstallResult",
        "CollisionManifold",
        "ColorTween",
        "CompleteGameCheck",
        "CompleteGameReport",
        "ContentError",
        "ContentItem",
        "ContentManager",
        "ContentManifest",
        "Cooldown",
        "DEFAULT_ANDROID_AD_PERMISSIONS",
        "DEFAULT_ANDROID_ANALYTICS_PERMISSIONS",
        "DebugOverlay",
        "DisplayOrientation",
        "DistributionArtifact",
        "DistributionCheck",
        "DistributionReport",
        "FIREBASE_ANALYTICS_DEPENDENCY",
        "FIREBASE_ANALYTICS_JAVA_SOURCE",
        "FROZEN_API_VERSION",
        "FROZEN_PUBLIC_API",
        "FirebaseAnalyticsAndroidBridge",
        "FirebaseAnalyticsAndroidProvider",
        "FirebaseAnalyticsConfig",
        "FixedStepClock",
        "FrameTimeController",
        "Game",
        "GameObject",
        "GameSession",
        "GameState",
        "GameSystems",
        "GeneratedProjectValidationCheck",
        "GeneratedProjectValidationReport",
        "HealthCheck",
        "HealthReport",
        "HyperKitCompatibilityError",
        "HyperKitConfigurationError",
        "HyperKitDeprecationWarning",
        "HyperKitError",
        "HyperKitRuntimeError",
        "HyperKitValidationError",
        "InputActionBinding",
        "InputActionEvent",
        "InputActionMap",
        "LevelData",
        "LevelError",
        "LevelLoader",
        "LevelManager",
        "LevelSequence",
        "LevelSequenceError",
        "MobileDisplayProfile",
        "MobileViewport",
        "MockAdProvider",
        "MockAnalyticsProvider",
        "MockAndroidAdBridge",
        "MockAndroidAnalyticsBridge",
        "NoOpAdProvider",
        "NoOpAnalyticsProvider",
        "ObjectPool",
        "ObjectPoolError",
        "PASSING_QA_STATUSES",
        "POLISHED_TEMPLATES",
        "PROJECT_CONFIG_FILENAME",
        "PROJECT_CONFIG_SCHEMA_VERSION",
        "Particle",
        "ParticleConfig",
        "ParticleEmitter",
        "PerformanceMode",
        "PerformanceProfile",
        "PhysicsBody",
        "PhysicsCollision",
        "PhysicsMaterial",
        "PhysicsWorld",
        "PlatformKind",
        "PreReleaseAuditCheck",
        "PreReleaseAuditReport",
        "Prefab",
        "PrefabError",
        "PrefabLibrary",
        "ProgressBar",
        "ProgressBarError",
        "ProgressionTracker",
        "ProjectConfig",
        "REQUIRED_PUBLIC_API",
        "Rect",
        "ReleaseBuildError",
        "ReleaseCheck",
        "ReleaseEvidenceCheck",
        "ReleaseEvidenceReport",
        "ReleaseReport",
        "RuntimeDiagnostics",
        "RuntimeEnvironment",
        "RuntimeSnapshot",
        "RuntimeState",
        "SDKConfig",
        "SDKContext",
        "SafeAreaInsets",
        "SaveManager",
        "Scene",
        "SceneTransition",
        "SceneTransitionError",
        "ScoreManager",
        "ScreenBounds",
        "SessionState",
        "SessionTracker",
        "SpriteAnimation",
        "SpriteAnimationError",
        "SpriteAnimator",
        "StateMachine",
        "TEMPLATE_DISPLAY_NAMES",
        "TemplateValidationCheck",
        "TemplateValidationReport",
        "TextLabel",
        "Timer",
        "TimerError",
        "TimerManager",
        "TouchEvent",
        "TouchGesture",
        "TouchTracker",
        "Tween",
        "UnsupportedAssetTypeError",
        "Vector2",
        "WorldBounds",
        "apply_drag",
        "apply_gravity",
        "background_runtime",
        "build_deprecation_message",
        "circle_collision",
        "circle_intersects_circle",
        "circle_intersects_rect",
        "circle_rect_collision",
        "clamp",
        "collision_manifold",
        "configure_admob_android_project",
        "configure_firebase_analytics_android_project",
        "configure_logging",
        "create_admob_config",
        "create_context",
        "deprecated",
        "detect_platform",
        "detect_runtime_environment",
        "detect_wsl",
        "discover_distribution_artifacts",
        "ease_in_out_quad",
        "ease_in_quad",
        "ease_out_quad",
        "find_project_config",
        "format_clean_install_result",
        "format_complete_game_report",
        "format_distribution_report",
        "format_generated_project_validation_report",
        "format_health_report",
        "format_pre_release_audit_report",
        "format_release_evidence_report",
        "format_release_report",
        "format_template_validation_report",
        "generate_complete_game_report",
        "generate_distribution_report",
        "generate_generated_project_validation_report",
        "generate_health_report",
        "generate_pre_release_audit_report",
        "generate_release_evidence_report",
        "generate_release_report",
        "generate_template_validation_report",
        "get_api_fingerprint",
        "get_api_version",
        "get_default_context",
        "get_logger",
        "get_missing_public_api",
        "get_unexpected_public_api",
        "intersects",
        "is_api_compatible",
        "linear",
        "load_audio",
        "load_csv",
        "load_firebase_analytics_config",
        "load_font",
        "load_image",
        "load_json",
        "load_level",
        "load_project_config",
        "load_text",
        "log_event",
        "move_towards",
        "normalize_orientation",
        "pause_runtime",
        "play_music",
        "play_sound",
        "point_in_circle",
        "read_project_version",
        "rect_circle_collision",
        "rect_collision",
        "rect_intersects_circle",
        "rect_intersects_rect",
        "reflect_velocity",
        "require_api_version",
        "reset_default_context",
        "resume_runtime",
        "run_clean_install_verification",
        "run_complete_game_validation",
        "run_game",
        "run_release_evidence_validation",
        "set_default_context",
        "sha256_file",
        "start_runtime",
        "stop_music",
        "stop_runtime",
        "validate_frozen_public_api",
        "validate_public_api",
        "validate_publish_target",
        "warn_deprecated",
        "write_checksum_manifest",
        "write_release_manifest",
    }
)

# Backward-compatible name used by earlier contract validation code.
# At the v0.9 public-beta stage, the required API is the complete frozen
# surface intended for HyperKit 1.0.
REQUIRED_PUBLIC_API = FROZEN_PUBLIC_API


def get_missing_public_api(
    namespace: Mapping[str, object],
) -> tuple[str, ...]:
    """Return frozen public API names missing from a namespace."""

    missing = (
        FROZEN_PUBLIC_API
        - set(namespace)
    )

    return tuple(
        sorted(missing)
    )


def get_unexpected_public_api(
    names: Iterable[str],
) -> tuple[str, ...]:
    """Return exported names that are not part of the frozen 1.0 API."""

    unexpected = (
        set(names)
        - FROZEN_PUBLIC_API
    )

    return tuple(
        sorted(unexpected)
    )


def get_api_fingerprint(
    names: Optional[
        Iterable[str]
    ] = None,
) -> str:
    """Return a deterministic SHA-256 fingerprint for an API name set."""

    values = (
        FROZEN_PUBLIC_API
        if names is None
        else frozenset(
            str(name)
            for name in names
        )
    )

    payload = "\n".join(
        sorted(
            values
        )
    ).encode(
        "utf-8"
    )

    return hashlib.sha256(
        payload
    ).hexdigest()


def validate_public_api(
    namespace: Optional[
        Mapping[str, object]
    ] = None,
) -> None:
    """Validate that every frozen HyperKit 1.0 API name exists."""

    if namespace is None:
        import hyperkit

        namespace = vars(
            hyperkit
        )

    missing = get_missing_public_api(
        namespace
    )

    if missing:
        names = ", ".join(
            missing
        )

        raise HyperKitCompatibilityError(
            "HyperKit frozen public API "
            f"is missing: {names}."
        )


def validate_frozen_public_api(
    exported_names: Optional[
        Iterable[str]
    ] = None,
) -> None:
    """Require an exact match with the frozen HyperKit 1.0 export set."""

    if exported_names is None:
        import hyperkit

        exported_names = (
            hyperkit.__all__
        )

    exported = tuple(
        exported_names
    )
    exported_set = set(
        exported
    )

    missing = tuple(
        sorted(
            FROZEN_PUBLIC_API
            - exported_set
        )
    )

    unexpected = (
        get_unexpected_public_api(
            exported
        )
    )

    duplicates = tuple(
        sorted(
            {
                name
                for name in exported_set
                if exported.count(
                    name
                )
                > 1
            }
        )
    )

    fingerprint = get_api_fingerprint(
        exported
    )

    count_matches = (
        len(
            exported_set
        )
        == FROZEN_API_EXPORT_COUNT
    )

    fingerprint_matches = (
        fingerprint
        == FROZEN_API_FINGERPRINT
    )

    if (
        not missing
        and not unexpected
        and not duplicates
        and count_matches
        and fingerprint_matches
    ):
        return

    details: list[str] = []

    if missing:
        details.append(
            "missing="
            + ", ".join(
                missing
            )
        )

    if unexpected:
        details.append(
            "unexpected="
            + ", ".join(
                unexpected
            )
        )

    if duplicates:
        details.append(
            "duplicates="
            + ", ".join(
                duplicates
            )
        )

    if not count_matches:
        details.append(
            "export_count="
            f"{len(exported_set)} "
            "(expected "
            f"{FROZEN_API_EXPORT_COUNT})"
        )

    if not fingerprint_matches:
        details.append(
            "fingerprint="
            f"{fingerprint} "
            "(expected "
            f"{FROZEN_API_FINGERPRINT})"
        )

    raise HyperKitCompatibilityError(
        "HyperKit frozen public API mismatch: "
        + "; ".join(
            details
        )
        + "."
    )
