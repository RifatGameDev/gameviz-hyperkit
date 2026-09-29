from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .assets import AssetManager
from .object import GameObject


class LevelError(Exception):
    """Base error for HyperKit level loading."""


def _normalize_color(
    value: Any,
    *,
    field_name: str,
) -> tuple[float, float, float, float]:
    if not isinstance(
        value,
        (list, tuple),
    ):
        raise LevelError(
            f"{field_name} must contain 4 numeric values."
        )

    if len(value) != 4:
        raise LevelError(
            f"{field_name} must have 4 values: r, g, b, a."
        )

    try:
        components = tuple(
            float(component)
            for component in value
        )
    except (
        TypeError,
        ValueError,
    ) as exc:
        raise LevelError(
            f"{field_name} must contain numeric values."
        ) from exc

    return tuple(
        max(
            0.0,
            min(
                1.0,
                component,
            ),
        )
        for component in components
    )


def _normalize_shape(
    value: Any,
) -> str:
    shape = str(
        value
    ).strip().lower()

    if shape == "rectangle":
        shape = "rect"

    if shape not in {
        "rect",
        "circle",
    }:
        raise LevelError(
            "Level object shape must be 'rect', 'rectangle', or 'circle'."
        )

    return shape


@dataclass
class LevelData:
    """Structured level data loaded from JSON."""

    name: str = "Untitled Level"
    width: int = 720
    height: int = 1280
    background_color: tuple[
        float,
        float,
        float,
        float,
    ] | None = None
    objects: list[
        dict[str, Any]
    ] = field(
        default_factory=list
    )
    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "LevelData":
        if not isinstance(
            data,
            dict,
        ):
            raise LevelError(
                "Level data must be a JSON object."
            )

        name = str(
            data.get(
                "name",
                "Untitled Level",
            )
        ).strip()

        if not name:
            name = "Untitled Level"

        try:
            width = int(
                data.get(
                    "width",
                    720,
                )
            )
            height = int(
                data.get(
                    "height",
                    1280,
                )
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise LevelError(
                "Level width and height must be integers."
            ) from exc

        if width <= 0:
            raise LevelError(
                "Level width must be greater than 0."
            )

        if height <= 0:
            raise LevelError(
                "Level height must be greater than 0."
            )

        objects = data.get(
            "objects",
            [],
        )

        if not isinstance(
            objects,
            list,
        ):
            raise LevelError(
                "Level data field 'objects' must be a list."
            )

        normalized_objects: list[
            dict[str, Any]
        ] = []

        for index, obj in enumerate(
            objects
        ):
            if not isinstance(
                obj,
                dict,
            ):
                raise LevelError(
                    "Level object at index "
                    f"{index} must be a JSON object."
                )

            normalized_objects.append(
                dict(
                    obj
                )
            )

        metadata = data.get(
            "metadata",
            {},
        )

        if not isinstance(
            metadata,
            dict,
        ):
            raise LevelError(
                "Level data field 'metadata' must be a JSON object."
            )

        background_color = data.get(
            "background_color"
        )

        if background_color is not None:
            background_color = (
                _normalize_color(
                    background_color,
                    field_name="background_color",
                )
            )

        return cls(
            name=name,
            width=width,
            height=height,
            background_color=background_color,
            objects=normalized_objects,
            metadata=dict(
                metadata
            ),
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "background_color": (
                list(
                    self.background_color
                )
                if self.background_color
                is not None
                else None
            ),
            "objects": [
                dict(
                    obj
                )
                for obj in self.objects
            ],
            "metadata": dict(
                self.metadata
            ),
        }

    def find_object(
        self,
        name: str,
    ) -> dict[
        str,
        Any,
    ] | None:
        for obj in self.objects:
            if obj.get(
                "name"
            ) == name:
                return obj

        return None

    def objects_by_type(
        self,
        object_type: str,
    ) -> list[
        dict[
            str,
            Any,
        ]
    ]:
        return [
            obj
            for obj in self.objects
            if obj.get(
                "type"
            ) == object_type
        ]


class LevelLoader:
    """Load level JSON files from assets/data."""

    def __init__(
        self,
        project_path: str | Path = ".",
        assets: AssetManager | None = None,
    ) -> None:
        self.project_path = Path(
            project_path
        ).resolve()

        self.assets = (
            assets
            or AssetManager(
                project_path=self.project_path
            )
        )

    def load(
        self,
        filename: str | Path,
    ) -> LevelData:
        data = self.assets.load_json(
            filename
        )

        return LevelData.from_dict(
            data
        )


class LevelManager:
    """High-level helper for loading levels and creating GameObjects."""

    def __init__(
        self,
        project_path: str | Path = ".",
        assets: AssetManager | None = None,
    ) -> None:
        self.project_path = Path(
            project_path
        ).resolve()

        self.assets = (
            assets
            or AssetManager(
                project_path=self.project_path
            )
        )

        self.loader = LevelLoader(
            project_path=self.project_path,
            assets=self.assets,
        )

        self.current_level: (
            LevelData
            | None
        ) = None

    @property
    def has_level(
        self,
    ) -> bool:
        return (
            self.current_level
            is not None
        )

    def load(
        self,
        filename: str | Path,
    ) -> LevelData:
        self.current_level = (
            self.loader.load(
                filename
            )
        )

        return self.current_level

    def unload(
        self,
    ) -> None:
        self.current_level = None

    def create_object(
        self,
        data: dict[str, Any],
    ) -> GameObject:
        if not isinstance(
            data,
            dict,
        ):
            raise LevelError(
                "Level object data must be a JSON object."
            )

        try:
            width = float(
                data.get(
                    "width",
                    50,
                )
            )
            height = float(
                data.get(
                    "height",
                    50,
                )
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise LevelError(
                "Level object width and height must be numeric."
            ) from exc

        if width <= 0:
            raise LevelError(
                "Level object width must be greater than 0."
            )

        if height <= 0:
            raise LevelError(
                "Level object height must be greater than 0."
            )

        color = _normalize_color(
            data.get(
                "color",
                (
                    1,
                    1,
                    1,
                    1,
                ),
            ),
            field_name="Level object color",
        )

        shape = _normalize_shape(
            data.get(
                "shape",
                "rect",
            )
        )

        image_path = data.get(
            "image_path"
        )

        if (
            image_path is None
            and data.get(
                "image"
            )
        ):
            image_path = (
                self.assets.load_image(
                    str(
                        data[
                            "image"
                        ]
                    )
                )
            )

        object_data = data.get(
            "data",
            {},
        )

        if not isinstance(
            object_data,
            dict,
        ):
            raise LevelError(
                "Level object field 'data' must be a JSON object."
            )

        try:
            obj = GameObject(
                x=float(
                    data.get(
                        "x",
                        0,
                    )
                ),
                y=float(
                    data.get(
                        "y",
                        0,
                    )
                ),
                width=width,
                height=height,
                vx=float(
                    data.get(
                        "vx",
                        0,
                    )
                ),
                vy=float(
                    data.get(
                        "vy",
                        0,
                    )
                ),
                color=color,
                shape=shape,
                name=str(
                    data.get(
                        "name",
                        "level_object",
                    )
                ),
                image_path=(
                    str(
                        image_path
                    )
                    if image_path
                    is not None
                    else None
                ),
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise LevelError(
                "Level object position and velocity must be numeric."
            ) from exc

        obj.data.update(
            dict(
                object_data
            )
        )

        obj.data[
            "type"
        ] = data.get(
            "type",
            "object",
        )

        return obj

    def create_objects(
        self,
        level: LevelData | None = None,
    ) -> list[
        GameObject
    ]:
        level_data = (
            level
            or self.current_level
        )

        if level_data is None:
            raise LevelError(
                "No level loaded. "
                "Call load('level.json') first."
            )

        return [
            self.create_object(
                obj_data
            )
            for obj_data
            in level_data.objects
        ]

    def add_to_scene(
        self,
        scene: Any,
        level: LevelData | None = None,
    ) -> list[
        GameObject
    ]:
        if not hasattr(
            scene,
            "add",
        ):
            raise LevelError(
                "Scene must provide an add() method."
            )

        objects = self.create_objects(
            level
        )

        for obj in objects:
            scene.add(
                obj
            )

        return objects


def load_level(
    filename: str | Path,
    project_path: str | Path = ".",
) -> LevelData:
    return LevelLoader(
        project_path=project_path
    ).load(
        filename
    )
