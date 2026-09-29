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
    """Resolve Android's writable app-private storage directory."""

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

        if app_path.name.lower() == "app":
            return app_path.parent

        return app_path

    return Path.cwd()


def _get_default_save_root(app_name: str) -> Path:
    """Return the platform-appropriate default save directory."""

    android_root = _get_android_private_root()

    if android_root is not None:
        return android_root / f".{app_name}"

    return Path.home() / f".{app_name}"


class SaveManager:
    """JSON persistence for settings, scores, and local game progress.

    Desktop default:
        ~/.<app_name>/save.json

    Android default:
        <app-private-files>/.<app_name>/save.json

    A custom root always takes precedence over automatic
    platform-specific storage selection.
    """

    def __init__(
        self,
        app_name: str = "hyperkit_game",
        filename: str = "save.json",
        root: str | Path | None = None,
    ) -> None:
        app_name = str(app_name).strip()
        filename = str(filename).strip()

        if not app_name:
            raise ValueError(
                "app_name must not be empty"
            )

        if not filename:
            raise ValueError(
                "filename must not be empty"
            )

        if root is not None:
            base = Path(root)
        else:
            base = _get_default_save_root(
                app_name
            )

        base.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.app_name = app_name
        self.filename = filename
        self.path = base / filename
        self.data: dict[str, Any] = {}

        self.load()

    @property
    def exists(self) -> bool:
        """Return whether the save file currently exists."""

        return self.path.is_file()

    def load(self) -> dict[str, Any]:
        """Load existing JSON save data.

        Invalid JSON is treated as an empty save rather than preventing
        the game from starting.
        """

        if not self.path.exists():
            self.data = {}
            return self.data

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

    def reload(self) -> dict[str, Any]:
        """Reload the current save file from disk."""

        return self.load()

    def save(self) -> None:
        """Atomically write the current save data to disk."""

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        content = json.dumps(
            self.data,
            indent=2,
            ensure_ascii=False,
        )

        temporary = self.path.with_name(
            f".{self.path.name}.tmp"
        )

        try:
            temporary.write_text(
                content,
                encoding="utf-8",
            )
            temporary.replace(
                self.path
            )
        finally:
            if temporary.exists():
                temporary.unlink()

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

    def has(self, key: str) -> bool:
        """Return whether a key exists in the save data."""

        return key in self.data

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

    def update(
        self,
        values: Mapping[str, Any],
        auto_save: bool = True,
    ) -> None:
        """Update multiple save values in one operation."""

        self.data.update(
            dict(values)
        )

        if auto_save:
            self.save()

    def delete(
        self,
        key: str,
        auto_save: bool = True,
    ) -> bool:
        """Delete a saved key and report whether it existed."""

        if key not in self.data:
            return False

        del self.data[key]

        if auto_save:
            self.save()

        return True

    def snapshot(self) -> dict[str, Any]:
        """Return a shallow copy of the current save data."""

        return dict(
            self.data
        )

    def reset(self) -> None:
        """Clear all saved data and persist the empty save."""

        self.data = {}
        self.save()
