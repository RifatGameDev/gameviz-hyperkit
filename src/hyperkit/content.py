"""Content manifest and content lookup helpers for HyperKit."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .assets import AssetManager


class ContentError(Exception):
    """Base error for HyperKit content management."""


@dataclass(frozen=True)
class ContentItem:
    """One named content entry from a content manifest."""

    content_id: str
    kind: str
    asset: str | None = None
    tags: tuple[str, ...] = ()
    data: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        content_id = str(
            self.content_id
        ).strip()
        kind = str(
            self.kind
        ).strip().lower()

        if not content_id:
            raise ContentError(
                "Content item id must not be empty."
            )

        if not kind:
            raise ContentError(
                "Content item kind must not be empty."
            )

        normalized_tags = tuple(
            dict.fromkeys(
                str(tag).strip().lower()
                for tag in self.tags
                if str(tag).strip()
            )
        )

        if self.asset is not None:
            asset = str(
                self.asset
            ).strip()

            if not asset:
                asset = None
        else:
            asset = None

        if not isinstance(
            self.data,
            dict,
        ):
            raise ContentError(
                "Content item data must be an object."
            )

        object.__setattr__(
            self,
            "content_id",
            content_id,
        )
        object.__setattr__(
            self,
            "kind",
            kind,
        )
        object.__setattr__(
            self,
            "asset",
            asset,
        )
        object.__setattr__(
            self,
            "tags",
            normalized_tags,
        )
        object.__setattr__(
            self,
            "data",
            dict(
                self.data
            ),
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ContentItem":
        if not isinstance(
            data,
            dict,
        ):
            raise ContentError(
                "Content item must be an object."
            )

        raw_tags = data.get(
            "tags",
            (),
        )

        if not isinstance(
            raw_tags,
            (list, tuple),
        ):
            raise ContentError(
                "Content item tags must be a list."
            )

        return cls(
            content_id=data.get(
                "id",
                "",
            ),
            kind=data.get(
                "kind",
                "",
            ),
            asset=data.get(
                "asset",
            ),
            tags=tuple(
                raw_tags
            ),
            data=data.get(
                "data",
                {},
            ),
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        return {
            "id": self.content_id,
            "kind": self.kind,
            "asset": self.asset,
            "tags": list(
                self.tags
            ),
            "data": dict(
                self.data
            ),
        }


@dataclass(frozen=True)
class ContentManifest:
    """Validated collection of content items."""

    name: str
    version: str = "1"
    items: tuple[
        ContentItem,
        ...
    ] = ()

    def __post_init__(self) -> None:
        name = str(
            self.name
        ).strip()
        version = str(
            self.version
        ).strip()

        if not name:
            raise ContentError(
                "Content manifest name must not be empty."
            )

        if not version:
            raise ContentError(
                "Content manifest version must not be empty."
            )

        seen: set[str] = set()

        for item in self.items:
            if not isinstance(
                item,
                ContentItem,
            ):
                raise ContentError(
                    "Content manifest items must be ContentItem instances."
                )

            if item.content_id in seen:
                raise ContentError(
                    "Duplicate content id: "
                    f"{item.content_id}"
                )

            seen.add(
                item.content_id
            )

        object.__setattr__(
            self,
            "name",
            name,
        )
        object.__setattr__(
            self,
            "version",
            version,
        )
        object.__setattr__(
            self,
            "items",
            tuple(
                self.items
            ),
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ContentManifest":
        if not isinstance(
            data,
            dict,
        ):
            raise ContentError(
                "Content manifest must be an object."
            )

        raw_items = data.get(
            "items",
            [],
        )

        if not isinstance(
            raw_items,
            list,
        ):
            raise ContentError(
                "Content manifest items must be a list."
            )

        return cls(
            name=data.get(
                "name",
                "HyperKit Content",
            ),
            version=data.get(
                "version",
                "1",
            ),
            items=tuple(
                ContentItem.from_dict(
                    item
                )
                for item in raw_items
            ),
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "items": [
                item.to_dict()
                for item in self.items
            ],
        }


class ContentManager:
    """Load and query content-driven game data."""

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
        self.manifest: (
            ContentManifest
            | None
        ) = None
        self._items: dict[
            str,
            ContentItem,
        ] = {}

    @property
    def loaded(
        self,
    ) -> bool:
        return (
            self.manifest
            is not None
        )

    @property
    def content_ids(
        self,
    ) -> list[str]:
        return sorted(
            self._items
        )

    def load(
        self,
        filename: str | Path,
    ) -> ContentManifest:
        data = self.assets.load_json(
            filename
        )

        manifest = (
            ContentManifest.from_dict(
                data
            )
        )

        self.set_manifest(
            manifest
        )

        return manifest

    def set_manifest(
        self,
        manifest: ContentManifest,
    ) -> "ContentManager":
        if not isinstance(
            manifest,
            ContentManifest,
        ):
            raise ContentError(
                "manifest must be a ContentManifest."
            )

        self.manifest = manifest
        self._items = {
            item.content_id: item
            for item in manifest.items
        }

        return self

    def unload(
        self,
    ) -> None:
        self.manifest = None
        self._items.clear()

    def get(
        self,
        content_id: str,
        default: Any = None,
    ) -> ContentItem | Any:
        return self._items.get(
            str(
                content_id
            ).strip(),
            default,
        )

    def require(
        self,
        content_id: str,
    ) -> ContentItem:
        key = str(
            content_id
        ).strip()

        item = self._items.get(
            key
        )

        if item is None:
            raise ContentError(
                "Unknown content id: "
                f"{key}"
            )

        return item

    def find_by_kind(
        self,
        kind: str,
    ) -> list[ContentItem]:
        normalized = str(
            kind
        ).strip().lower()

        return [
            item
            for item in self._items.values()
            if item.kind == normalized
        ]

    def find_by_tag(
        self,
        tag: str,
    ) -> list[ContentItem]:
        normalized = str(
            tag
        ).strip().lower()

        return [
            item
            for item in self._items.values()
            if normalized in item.tags
        ]

    def resolve_asset(
        self,
        content_id: str,
    ) -> str:
        item = self.require(
            content_id
        )

        if item.asset is None:
            raise ContentError(
                "Content item has no asset: "
                f"{item.content_id}"
            )

        loaders = {
            "image": self.assets.load_image,
            "audio": self.assets.load_audio,
            "font": self.assets.load_font,
        }

        loader = loaders.get(
            item.kind
        )

        if loader is None:
            raise ContentError(
                "Content asset resolution supports "
                "image, audio, and font items. "
                f"Got: {item.kind}"
            )

        return loader(
            item.asset
        )

    def validate_assets(
        self,
    ) -> list[str]:
        issues: list[str] = []

        for item in self._items.values():
            if item.asset is None:
                continue

            if item.kind not in {
                "image",
                "audio",
                "font",
            }:
                continue

            try:
                self.resolve_asset(
                    item.content_id
                )
            except Exception as exc:
                issues.append(
                    f"{item.content_id}: {exc}"
                )

        return issues

    def iter_items(
        self,
    ) -> Iterable[ContentItem]:
        return iter(
            self._items.values()
        )
