"""Reusable data-driven prefab helpers for HyperKit."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .assets import AssetManager
from .level import LevelManager
from .object import GameObject


class PrefabError(Exception):
    """Base error for HyperKit prefabs."""


@dataclass(frozen=True)
class Prefab:
    """Reusable GameObject definition."""

    name: str
    object_data: dict[
        str,
        Any,
    ]
    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        name = str(
            self.name
        ).strip()

        if not name:
            raise PrefabError(
                "Prefab name must not be empty."
            )

        if not isinstance(
            self.object_data,
            dict,
        ):
            raise PrefabError(
                "Prefab object data must be an object."
            )

        if not isinstance(
            self.metadata,
            dict,
        ):
            raise PrefabError(
                "Prefab metadata must be an object."
            )

        object.__setattr__(
            self,
            "name",
            name,
        )
        object.__setattr__(
            self,
            "object_data",
            dict(
                self.object_data
            ),
        )
        object.__setattr__(
            self,
            "metadata",
            dict(
                self.metadata
            ),
        )


class PrefabLibrary:
    """Load reusable GameObject definitions from JSON."""

    def __init__(
        self,
        project_path: str | Path = ".",
        assets: AssetManager | None = None,
        level_manager: LevelManager | None = None,
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
        self.level_manager = (
            level_manager
            or LevelManager(
                project_path=self.project_path,
                assets=self.assets,
            )
        )
        self.prefabs: dict[
            str,
            Prefab,
        ] = {}

    @property
    def names(
        self,
    ) -> list[str]:
        return sorted(
            self.prefabs
        )

    def register(
        self,
        prefab: Prefab,
        *,
        replace: bool = False,
    ) -> Prefab:
        if not isinstance(
            prefab,
            Prefab,
        ):
            raise PrefabError(
                "prefab must be a Prefab instance."
            )

        if (
            prefab.name in self.prefabs
            and not replace
        ):
            raise PrefabError(
                "Prefab already registered: "
                f"{prefab.name}"
            )

        self.prefabs[
            prefab.name
        ] = prefab

        return prefab

    def load(
        self,
        filename: str | Path,
        *,
        replace: bool = False,
    ) -> list[Prefab]:
        data = self.assets.load_json(
            filename
        )

        if not isinstance(
            data,
            dict,
        ):
            raise PrefabError(
                "Prefab file must contain an object."
            )

        raw_prefabs = data.get(
            "prefabs",
            {},
        )

        if not isinstance(
            raw_prefabs,
            dict,
        ):
            raise PrefabError(
                "Prefab file field 'prefabs' must be an object."
            )

        loaded: list[Prefab] = []

        for name, raw in raw_prefabs.items():
            if not isinstance(
                raw,
                dict,
            ):
                raise PrefabError(
                    "Prefab definition must be an object: "
                    f"{name}"
                )

            prefab = Prefab(
                name=name,
                object_data=raw.get(
                    "object",
                    raw.get(
                        "object_data",
                        {},
                    ),
                ),
                metadata=raw.get(
                    "metadata",
                    {},
                ),
            )

            self.register(
                prefab,
                replace=replace,
            )
            loaded.append(
                prefab
            )

        return loaded

    def get(
        self,
        name: str,
    ) -> Prefab | None:
        return self.prefabs.get(
            str(
                name
            ).strip()
        )

    def require(
        self,
        name: str,
    ) -> Prefab:
        key = str(
            name
        ).strip()
        prefab = self.prefabs.get(
            key
        )

        if prefab is None:
            raise PrefabError(
                "Unknown prefab: "
                f"{key}"
            )

        return prefab

    def create(
        self,
        name: str,
        **overrides: Any,
    ) -> GameObject:
        prefab = self.require(
            name
        )
        data = dict(
            prefab.object_data
        )

        if "data" in data:
            nested = data.get(
                "data"
            )

            if isinstance(
                nested,
                dict,
            ):
                data[
                    "data"
                ] = dict(
                    nested
                )

        override_data = overrides.pop(
            "data",
            None,
        )

        data.update(
            overrides
        )

        if override_data is not None:
            if not isinstance(
                override_data,
                dict,
            ):
                raise PrefabError(
                    "Prefab data override must be an object."
                )

            merged = dict(
                data.get(
                    "data",
                    {},
                )
            )
            merged.update(
                override_data
            )
            data[
                "data"
            ] = merged

        return (
            self.level_manager
            .create_object(
                data
            )
        )

    def add_to_scene(
        self,
        scene: Any,
        name: str,
        **overrides: Any,
    ) -> GameObject:
        if not hasattr(
            scene,
            "add",
        ):
            raise PrefabError(
                "Scene must provide an add() method."
            )

        obj = self.create(
            name,
            **overrides,
        )

        return scene.add(
            obj
        )

    def remove(
        self,
        name: str,
    ) -> bool:
        return (
            self.prefabs.pop(
                str(
                    name
                ).strip(),
                None,
            )
            is not None
        )

    def clear(
        self,
    ) -> int:
        count = len(
            self.prefabs
        )
        self.prefabs.clear()
        return count
