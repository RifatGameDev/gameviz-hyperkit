"""GameViz HyperKit.

A lightweight Python SDK for mobile-ready 2D hypercasual game prototypes.
"""

from .errors import (
    HyperKitCompatibilityError,
    HyperKitConfigurationError,
    HyperKitError,
    HyperKitRuntimeError,
    HyperKitValidationError,
)

from .compatibility import (
    API_VERSION,
    get_api_version,
    is_api_compatible,
    require_api_version,
)

from .config import SDKConfig

from .runtime import (
    RuntimeState,
    SDKContext,
    create_context,
    get_default_context,
    reset_default_context,
    set_default_context,
)

from .collision import (
    circle_intersects_circle,
    rect_intersects_circle,
    rect_intersects_rect,
)

from .geometry import Circle, Rect, Vector2
from .input import TouchEvent, TouchGesture, TouchTracker
from .object import GameObject
from .physics import apply_gravity, clamp, move_towards
from .save import SaveManager
from .scene import Scene
from .score import ScoreManager
from .ui import Button, TextLabel
from .state import GameState, StateMachine
from .layout import CanvasScaler

from .assets import (
    AssetError,
    AssetManager,
    AssetNotFoundError,
    UnsupportedAssetTypeError,
    load_audio,
    load_csv,
    load_font,
    load_image,
    load_json,
    load_text,
)

from .audio import (
    AudioError,
    AudioLoadError,
    AudioManager,
    play_music,
    play_sound,
    stop_music,
)

from .animation import (
    AnimationManager,
    ColorTween,
    Tween,
    ease_in_out_quad,
    ease_in_quad,
    ease_out_quad,
    linear,
)

from .sprite import (
    SpriteAnimation,
    SpriteAnimationError,
    SpriteAnimator,
)

from .particle import (
    Particle,
    ParticleConfig,
    ParticleEmitter,
)

from .camera import CameraShake

from .transition import (
    SceneTransition,
    SceneTransitionError,
)

from .timers import (
    Cooldown,
    Timer,
    TimerError,
    TimerManager,
)

from .input_actions import (
    InputActionBinding,
    InputActionEvent,
    InputActionMap,
)

from .level import (
    LevelData,
    LevelError,
    LevelLoader,
    LevelManager,
    load_level,
)

from .camera_follow import CameraFollow

from .bounds import (
    Bounds,
    BoundsManager,
    ScreenBounds,
    WorldBounds,
)

from .progress import (
    ProgressBar,
    ProgressBarError,
)

from .health import (
    HealthCheck,
    HealthReport,
    format_health_report,
    generate_health_report,
)

from .release import (
    ReleaseCheck,
    ReleaseReport,
    format_release_report,
    generate_release_report,
)

from .audit import (
    PreReleaseAuditCheck,
    PreReleaseAuditReport,
    format_pre_release_audit_report,
    generate_pre_release_audit_report,
)

from .template_validation import (
    TemplateValidationCheck,
    TemplateValidationReport,
    format_template_validation_report,
    generate_template_validation_report,
)

from .generated_project_validation import (
    GeneratedProjectValidationCheck,
    GeneratedProjectValidationReport,
    POLISHED_TEMPLATES,
    format_generated_project_validation_report,
    generate_generated_project_validation_report,
)

from .release_evidence import (
    ALLOWED_QA_STATUSES,
    PASSING_QA_STATUSES,
    TEMPLATE_DISPLAY_NAMES,
    ReleaseEvidenceCheck,
    ReleaseEvidenceReport,
    format_release_evidence_report,
    generate_release_evidence_report,
    run_release_evidence_validation,
)

from .project_config import (
    PROJECT_CONFIG_FILENAME,
    PROJECT_CONFIG_SCHEMA_VERSION,
    ProjectConfig,
    find_project_config,
    load_project_config,
)

from .deprecation import (
    HyperKitDeprecationWarning,
    build_deprecation_message,
    deprecated,
    warn_deprecated,
)

from .environment import (
    PlatformKind,
    RuntimeEnvironment,
    detect_platform,
    detect_runtime_environment,
)

from .logging import (
    configure_logging,
    get_logger,
    log_event,
)

from .lifecycle import (
    run_game,
    start_runtime,
    stop_runtime,
)

from .api_contract import (
    REQUIRED_PUBLIC_API,
    get_missing_public_api,
    validate_public_api,
)


try:  # Kivy may not be available in headless test environments.
    from .app import Game
except Exception:  # pragma: no cover
    Game = None  # type: ignore


__all__ = [
    "API_VERSION",
    "SDKConfig",
    "RuntimeState",
    "SDKContext",
    "create_context",
    "get_default_context",
    "set_default_context",
    "reset_default_context",
    "HyperKitError",
    "HyperKitConfigurationError",
    "HyperKitCompatibilityError",
    "HyperKitRuntimeError",
    "HyperKitValidationError",
    "get_api_version",
    "is_api_compatible",
    "require_api_version",
    "Button",
    "TextLabel",
    "Circle",
    "Game",
    "GameObject",
    "Rect",
    "SaveManager",
    "Scene",
    "ScoreManager",
    "TouchEvent",
    "TouchGesture",
    "TouchTracker",
    "Vector2",
    "apply_gravity",
    "circle_intersects_circle",
    "clamp",
    "move_towards",
    "rect_intersects_circle",
    "rect_intersects_rect",
    "GameState",
    "StateMachine",
    "CanvasScaler",
    "AssetError",
    "AssetManager",
    "AssetNotFoundError",
    "UnsupportedAssetTypeError",
    "load_audio",
    "load_csv",
    "load_font",
    "load_image",
    "load_json",
    "load_text",
    "AudioError",
    "AudioLoadError",
    "AudioManager",
    "play_music",
    "play_sound",
    "stop_music",
    "AnimationManager",
    "ColorTween",
    "Tween",
    "ease_in_out_quad",
    "ease_in_quad",
    "ease_out_quad",
    "linear",
    "SpriteAnimation",
    "SpriteAnimationError",
    "SpriteAnimator",
    "Particle",
    "ParticleConfig",
    "ParticleEmitter",
    "CameraShake",
    "SceneTransition",
    "SceneTransitionError",
    "Cooldown",
    "Timer",
    "TimerError",
    "TimerManager",
    "InputActionBinding",
    "InputActionEvent",
    "InputActionMap",
    "LevelData",
    "LevelError",
    "LevelLoader",
    "LevelManager",
    "load_level",
    "CameraFollow",
    "Bounds",
    "BoundsManager",
    "ScreenBounds",
    "WorldBounds",
    "ProgressBar",
    "ProgressBarError",
    "HealthCheck",
    "HealthReport",
    "format_health_report",
    "generate_health_report",
    "ReleaseCheck",
    "ReleaseReport",
    "format_release_report",
    "generate_release_report",
    "PreReleaseAuditCheck",
    "PreReleaseAuditReport",
    "format_pre_release_audit_report",
    "generate_pre_release_audit_report",
    "TemplateValidationCheck",
    "TemplateValidationReport",
    "format_template_validation_report",
    "generate_template_validation_report",
    "GeneratedProjectValidationCheck",
    "GeneratedProjectValidationReport",
    "POLISHED_TEMPLATES",
    "format_generated_project_validation_report",
    "generate_generated_project_validation_report",
    "ALLOWED_QA_STATUSES",
    "PASSING_QA_STATUSES",
    "TEMPLATE_DISPLAY_NAMES",
    "ReleaseEvidenceCheck",
    "ReleaseEvidenceReport",
    "format_release_evidence_report",
    "generate_release_evidence_report",
    "run_release_evidence_validation",
    "PROJECT_CONFIG_FILENAME",
    "PROJECT_CONFIG_SCHEMA_VERSION",
    "ProjectConfig",
    "find_project_config",
    "load_project_config",
    "HyperKitDeprecationWarning",
    "build_deprecation_message",
    "deprecated",
    "warn_deprecated",
    "PlatformKind",
    "RuntimeEnvironment",
    "detect_platform",
    "detect_runtime_environment",
    "configure_logging",
    "get_logger",
    "log_event",
    "start_runtime",
    "stop_runtime",
    "run_game",
    "REQUIRED_PUBLIC_API",
    "get_missing_public_api",
    "validate_public_api",
]


__version__ = "0.2.0.dev0"
