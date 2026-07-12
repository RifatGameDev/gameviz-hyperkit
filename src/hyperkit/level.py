from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .assets import AssetManager
from .object import GameObject


class LevelError(Exception):
    """Base error for HyperKit level loading."""


@dataclass
class LevelData:
    """Structured level data loaded from JSON."""

    name: str = "Untitled Level"
    width: int = 720
    height: int = 1280
    background_color: tuple[float, float, float, float] | None = None
    objects: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LevelData":
        if not isinstance(data, dict):
            raise LevelError("Level data must be a JSON object.")

        objects = data.get("objects", [])

        if not isinstance(objects, list):
            raise LevelError("Level data field 'objects' must be a list.")

        background_color = data.get("background_color")

        if background_color is not None:
            background_color = tuple(float(value)
                                     for value in background_color)

            if len(background_color) != 4:
                raise LevelError(
                    "background_color must have 4 values: r, g, b, a.")

        return cls(
            name=str(data.get("name", "Untitled Level")),
            width=int(data.get("width", 720)),
            height=int(data.get("height", 1280)),
            background_color=background_color,
            objects=objects,
            metadata=dict(data.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "background_color": list(self.background_color)
            if self.background_color is not None
            else None,
            "objects": self.objects,
            "metadata": self.metadata,
        }

    def find_object(self, name: str) -> dict[str, Any] | None:
        for obj in self.objects:
            if obj.get("name") == name:
                return obj

        return None

    def objects_by_type(self, object_type: str) -> list[dict[str, Any]]:
        return [
            obj
            for obj in self.objects
            if obj.get("type") == object_type
        ]


class LevelLoader:
    """Load level JSON files from assets/data."""

    def __init__(
        self,
        project_path: str | Path = ".",
        assets: AssetManager | None = None,
    ) -> None:
        self.project_path = Path(project_path).resolve()
        self.assets = assets or AssetManager(project_path=self.project_path)

    def load(self, filename: str | Path) -> LevelData:
        data = self.assets.load_json(filename)
        return LevelData.from_dict(data)


class LevelManager:
    """High-level helper for loading levels and creating GameObjects."""

    def __init__(
        self,
        project_path: str | Path = ".",
        assets: AssetManager | None = None,
    ) -> None:
        self.project_path = Path(project_path).resolve()
        self.assets = assets or AssetManager(project_path=self.project_path)
        self.loader = LevelLoader(
            project_path=self.project_path, assets=self.assets)
        self.current_level: LevelData | None = None

    def load(self, filename: str | Path) -> LevelData:
        self.current_level = self.loader.load(filename)
        return self.current_level

    def create_object(self, data: dict[str, Any]) -> GameObject:
        color = data.get("color", (1, 1, 1, 1))

        if isinstance(color, list):
            color = tuple(float(value) for value in color)

        image_path = data.get("image_path")

        if image_path is None and data.get("image"):
            image_path = self.assets.load_image(str(data["image"]))

        obj = GameObject(
            x=float(data.get("x", 0)),
            y=float(data.get("y", 0)),
            width=float(data.get("width", 50)),
            height=float(data.get("height", 50)),
            vx=float(data.get("vx", 0)),
            vy=float(data.get("vy", 0)),
            color=color,
            shape=str(data.get("shape", "rectangle")),
            name=str(data.get("name", "level_object")),
            image_path=image_path,
        )

        obj.data.update(dict(data.get("data", {})))
        obj.data["type"] = data.get("type", "object")

        return obj

    def create_objects(self, level: LevelData | None = None) -> list[GameObject]:
        level_data = level or self.current_level

        if level_data is None:
            raise LevelError("No level loaded. Call load('level.json') first.")

        return [
            self.create_object(obj_data)
            for obj_data in level_data.objects
        ]

    def add_to_scene(self, scene: Any, level: LevelData | None = None) -> list[GameObject]:
        objects = self.create_objects(level)

        for obj in objects:
            scene.add(obj)

        return objects


def load_level(filename: str | Path, project_path: str | Path = ".") -> LevelData:
    return LevelLoader(project_path=project_path).load(filename)
