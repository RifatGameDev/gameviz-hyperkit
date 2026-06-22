from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SaveManager:
    """Simple JSON save manager for scores, settings, and local progress."""

    def __init__(self, app_name: str = "hyperkit_game", filename: str = "save.json", root: str | Path | None = None) -> None:
        base = Path(root) if root else Path.home() / f".{app_name}"
        base.mkdir(parents=True, exist_ok=True)
        self.path = base / filename
        self.data: dict[str, Any] = {}
        self.load()

    def load(self) -> dict[str, Any]:
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.data = {}
        return self.data

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any, auto_save: bool = True) -> None:
        self.data[key] = value
        if auto_save:
            self.save()

    def reset(self) -> None:
        self.data = {}
        self.save()
