from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping, Optional


ANDROID_PRIVATE_ENV = "ANDROID_PRIVATE"
ANDROID_ARGUMENT_ENV = "ANDROID_ARGUMENT"
ANDROID_APP_PATH_ENV = "ANDROID_APP_PATH"
P4A_BOOTSTRAP_ENV = "P4A_BOOTSTRAP"


def _is_android_runtime(
    environ: Optional[Mapping[str, str]] = None,
) -> bool:
    """Return True when running inside a python-for-android app."""

    env = os.environ if environ is None else environ

    return any(
        bool(env.get(key))
        for key in (
            ANDROID_PRIVATE_ENV,
            ANDROID_ARGUMENT_ENV,
            ANDROID_APP_PATH_ENV,
            P4A_BOOTSTRAP_ENV,
        )
    )


def _get_android_private_root(
    environ: Optional[Mapping[str, str]] = None,
) -> Optional[Path]:
    """Resolve Android's writable app-private storage directory.

    python-for-android exposes ANDROID_PRIVATE as the application's
    internal files directory. This is the preferred location for
    persistent HyperKit save data on Android.

    Older or unusual python-for-android environments may not expose
    ANDROID_PRIVATE. In that case, ANDROID_ARGUMENT or ANDROID_APP_PATH
    is used as a fallback.
    """

    env = os.environ if environ is None else environ

    private_path = env.get(ANDROID_PRIVATE_ENV)

    if private_path:
        return Path(private_path)

    if not _is_android_runtime(env):
        return None

    app_path_value = (
        env.get(ANDROID_ARGUMENT_ENV)
        or env.get(ANDROID_APP_PATH_ENV)
    )

    if app_path_value:
        app_path = Path(app_path_value)

        # Modern python-for-android commonly points these variables to:
        #
        # /data/user/0/<package>/files/app
        #
        # Save data belongs beside "app", inside the package's private
        # files directory, not inside Android's protected /data root.
        if app_path.name.lower() == "app":
            return app_path.parent

        return app_path

    # Last-resort Android fallback. python-for-android normally changes
    # the current working directory to the application's private app
    # directory before executing main.py.
    return Path.cwd()


def _get_default_save_root(app_name: str) -> Path:
    """Return the platform-appropriate default save directory."""

    android_root = _get_android_private_root()

    if android_root is not None:
        return android_root / f".{app_name}"

    return Path.home() / f".{app_name}"


class SaveManager:
    """Simple JSON save manager for scores, settings, and local progress.

    Desktop default:
        ~/.<app_name>/save.json

    Android default:
        <app-private-files>/.<app_name>/save.json

    A custom ``root`` always takes precedence over automatic
    platform-specific storage selection.
    """

    def __init__(
        self,
        app_name: str = "hyperkit_game",
        filename: str = "save.json",
        root: str | Path | None = None,
    ) -> None:
        if root:
            base = Path(root)
        else:
            base = _get_default_save_root(app_name)

        base.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.path = base / filename
        self.data: dict[str, Any] = {}

        self.load()

    def load(self) -> dict[str, Any]:
        """Load existing JSON save data.

        Invalid JSON is treated as an empty save rather than preventing
        the game from starting.
        """

        if self.path.exists():
            try:
                loaded = json.loads(
                    self.path.read_text(
                        encoding="utf-8",
                    )
                )

                if isinstance(loaded, dict):
                    self.data = loaded
                else:
                    self.data = {}

            except (
                json.JSONDecodeError,
                UnicodeDecodeError,
            ):
                self.data = {}

        return self.data

    def save(self) -> None:
        """Write the current save data to disk."""

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.path.write_text(
            json.dumps(
                self.data,
                indent=2,
            ),
            encoding="utf-8",
        )

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Return a saved value."""

        return self.data.get(
            key,
            default,
        )

    def set(
        self,
        key: str,
        value: Any,
        auto_save: bool = True,
    ) -> None:
        """Set a save value and optionally persist immediately."""

        self.data[key] = value

        if auto_save:
            self.save()

    def reset(self) -> None:
        """Clear all saved data and persist the empty save."""

        self.data = {}
        self.save()
