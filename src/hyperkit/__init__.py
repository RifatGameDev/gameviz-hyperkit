"""GameViz HyperKit.

A lightweight Python SDK for mobile-ready 2D hypercasual game prototypes.
"""

from .collision import circle_intersects_circle, rect_intersects_rect, rect_intersects_circle
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
from .sprite import SpriteAnimation, SpriteAnimationError, SpriteAnimator
from .particle import Particle, ParticleConfig, ParticleEmitter
from .camera import CameraShake
from .transition import SceneTransition, SceneTransitionError
from .timers import Cooldown, Timer, TimerError, TimerManager
from .input_actions import InputActionBinding, InputActionEvent, InputActionMap
from .level import LevelData, LevelError, LevelLoader, LevelManager, load_level
from .camera_follow import CameraFollow

try:  # Kivy may not be available in headless test environments.
    from .app import Game
except Exception:  # pragma: no cover
    Game = None  # type: ignore

__all__ = [
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
]

__version__ = "0.1.0"
