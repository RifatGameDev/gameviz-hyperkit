from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
AUDIO_EXTENSIONS = {".wav", ".mp3", ".ogg"}
FONT_EXTENSIONS = {".ttf", ".otf"}
JSON_EXTENSIONS = {".json"}
CSV_EXTENSIONS = {".csv"}
TEXT_EXTENSIONS = {".txt"}

UNSUPPORTED_SOURCE_EXTENSIONS = {
    ".fbx": "FBX is a 3D source asset format. Export it as PNG frames or a sprite sheet before using it in HyperKit.",
    ".blend": "Blender files are source files. Export the needed game asset as PNG, audio, font, JSON, CSV, or TXT.",
    ".obj": "OBJ is a 3D model format. HyperKit currently supports 2D assets only.",
    ".glb": "GLB is a 3D model format. HyperKit currently supports 2D assets only.",
    ".gltf": "GLTF is a 3D model format. HyperKit currently supports 2D assets only.",
}


class AssetError(Exception):
    """Base error for HyperKit asset loading."""


class AssetNotFoundError(AssetError, FileNotFoundError):
    """Raised when an asset file is missing."""


class UnsupportedAssetTypeError(AssetError, ValueError):
    """Raised when an asset file type is not supported."""


class AssetManager:
    """Helper class for loading assets from a HyperKit project.

    Default project structure:

    assets/
    ├── images/
    ├── audio/
    ├── fonts/
    └── data/
    """

    def __init__(
        self,
        project_path: str | Path = ".",
        assets_folder: str = "assets",
    ):
        assets_folder = str(assets_folder).strip()

        if not assets_folder:
            raise AssetError(
                "assets_folder must not be empty."
            )

        self.project_path = Path(project_path).resolve()
        self.assets_path = (
            self.project_path
            / assets_folder
        ).resolve()
        self._cache: dict[
            tuple[str, str],
            Any,
        ] = {}

    def _candidate_path(self, folder: str, filename: str | Path) -> Path:
        raw_path = Path(filename)

        if raw_path.is_absolute():
            return raw_path.resolve()

        parts = raw_path.parts

        if parts and parts[0] == self.assets_path.name:
            return (self.project_path / raw_path).resolve()

        if parts and parts[0] == folder:
            return (self.assets_path / raw_path).resolve()

        return (self.assets_path / folder / raw_path).resolve()

    def _ensure_inside_assets_folder(self, path: Path) -> None:
        try:
            path.relative_to(self.assets_path)
        except ValueError as exc:
            raise AssetError(
                f"Asset path must be inside the assets folder: {self.assets_path}"
            ) from exc

    def _validate_extension(self, path: Path, allowed_extensions: set[str], asset_type: str) -> None:
        extension = path.suffix.lower()

        if extension in UNSUPPORTED_SOURCE_EXTENSIONS:
            raise UnsupportedAssetTypeError(
                f"Unsupported asset type '{extension}' for {asset_type}. "
                f"{UNSUPPORTED_SOURCE_EXTENSIONS[extension]}"
            )

        if extension not in allowed_extensions:
            allowed = ", ".join(sorted(allowed_extensions))
            raise UnsupportedAssetTypeError(
                f"Unsupported {asset_type} file type '{extension}'. "
                f"Supported types: {allowed}"
            )

    def _resolve_asset(
        self,
        folder: str,
        filename: str | Path,
        allowed_extensions: set[str],
        asset_type: str,
    ) -> Path:
        path = self._candidate_path(folder, filename)
        self._ensure_inside_assets_folder(path)
        self._validate_extension(path, allowed_extensions, asset_type)

        if not path.exists() or not path.is_file():
            raise AssetNotFoundError(
                f"Asset not found: {path}"
            )

        return path

    @property
    def cache_size(
        self,
    ) -> int:
        return len(
            self._cache
        )

    def clear_cache(
        self,
    ) -> int:
        count = len(
            self._cache
        )
        self._cache.clear()
        return count

    def _cache_key(
        self,
        asset_type: str,
        filename: str | Path,
    ) -> tuple[str, str]:
        return (
            str(
                asset_type
            ),
            str(
                filename
            ),
        )

    def load_image(self, filename: str | Path) -> str:
        """Return image file path from assets/images."""
        path = self._resolve_asset(
            "images", filename, IMAGE_EXTENSIONS, "image")
        return str(path)

    def load_audio(self, filename: str | Path) -> str:
        """Return audio file path from assets/audio."""
        path = self._resolve_asset(
            "audio", filename, AUDIO_EXTENSIONS, "audio")
        return str(path)

    def load_font(self, filename: str | Path) -> str:
        """Return font file path from assets/fonts."""
        path = self._resolve_asset("fonts", filename, FONT_EXTENSIONS, "font")
        return str(path)

    def load_json(
        self,
        filename: str | Path,
        *,
        cached: bool = False,
    ) -> Any:
        """Load JSON data from assets/data."""
        key = self._cache_key(
            "json",
            filename,
        )

        if cached and key in self._cache:
            return deepcopy(
                self._cache[
                    key
                ]
            )

        path = self._resolve_asset(
            "data", filename, JSON_EXTENSIONS, "JSON data")

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if cached:
            self._cache[
                key
            ] = deepcopy(
                data
            )

        return data

    def load_csv(
        self,
        filename: str | Path,
        *,
        cached: bool = False,
    ) -> list[dict[str, str]]:
        """Load CSV data from assets/data."""
        key = self._cache_key(
            "csv",
            filename,
        )

        if cached and key in self._cache:
            return deepcopy(
                self._cache[
                    key
                ]
            )

        path = self._resolve_asset(
            "data", filename, CSV_EXTENSIONS, "CSV data")

        with path.open("r", encoding="utf-8", newline="") as file:
            rows = list(
                csv.DictReader(
                    file
                )
            )

        if cached:
            self._cache[
                key
            ] = deepcopy(
                rows
            )

        return rows

    def load_text(
        self,
        filename: str | Path,
        *,
        cached: bool = False,
    ) -> str:
        """Load text data from assets/data."""
        key = self._cache_key(
            "text",
            filename,
        )

        if cached and key in self._cache:
            return str(
                self._cache[
                    key
                ]
            )

        path = self._resolve_asset(
            "data", filename, TEXT_EXTENSIONS, "text data")
        content = path.read_text(
            encoding="utf-8"
        )

        if cached:
            self._cache[
                key
            ] = content

        return content

    def exists(
        self,
        folder: str,
        filename: str | Path,
        extensions: set[str],
        asset_type: str = "asset",
    ) -> bool:
        """Return whether a valid asset exists without raising."""

        try:
            self._resolve_asset(
                folder,
                filename,
                extensions,
                asset_type,
            )
        except AssetError:
            return False

        return True

    def list_assets(
        self,
        folder: str,
        extensions: set[str],
        recursive: bool = False,
    ) -> list[str]:
        folder = str(folder).strip()

        if not folder:
            raise AssetError(
                "Asset folder must not be empty."
            )

        folder_path = (
            self.assets_path
            / folder
        ).resolve()

        self._ensure_inside_assets_folder(
            folder_path
        )

        if not folder_path.exists():
            return []

        if not folder_path.is_dir():
            raise AssetError(
                f"Asset folder is not a directory: {folder_path}"
            )

        normalized_extensions = {
            str(extension).lower()
            for extension in extensions
        }

        iterator = (
            folder_path.rglob("*")
            if recursive
            else folder_path.iterdir()
        )

        results = []

        for path in iterator:
            if (
                path.is_file()
                and path.suffix.lower()
                in normalized_extensions
            ):
                relative_path = (
                    path.relative_to(
                        self.assets_path
                    )
                )
                results.append(
                    relative_path.as_posix()
                )

        return sorted(results)

    def preload_data(
        self,
        filenames: list[
            str | Path
        ],
    ) -> dict[str, Any]:
        loaded: dict[
            str,
            Any,
        ] = {}

        for filename in filenames:
            path = Path(
                filename
            )
            extension = (
                path.suffix
                .lower()
            )

            key = str(
                filename
            )

            if extension in JSON_EXTENSIONS:
                loaded[key] = self.load_json(
                    filename,
                    cached=True,
                )
            elif extension in CSV_EXTENSIONS:
                loaded[key] = self.load_csv(
                    filename,
                    cached=True,
                )
            elif extension in TEXT_EXTENSIONS:
                loaded[key] = self.load_text(
                    filename,
                    cached=True,
                )
            else:
                raise UnsupportedAssetTypeError(
                    "preload_data supports JSON, CSV, and TXT files."
                )

        return loaded

    def list_images(self) -> list[str]:
        return self.list_assets("images", IMAGE_EXTENSIONS)

    def list_audio(self) -> list[str]:
        return self.list_assets("audio", AUDIO_EXTENSIONS)

    def list_fonts(self) -> list[str]:
        return self.list_assets("fonts", FONT_EXTENSIONS)

    def list_data(self) -> list[str]:
        return self.list_assets(
            "data",
            JSON_EXTENSIONS | CSV_EXTENSIONS | TEXT_EXTENSIONS,
        )


def load_image(filename: str | Path) -> str:
    return AssetManager().load_image(filename)


def load_audio(filename: str | Path) -> str:
    return AssetManager().load_audio(filename)


def load_font(filename: str | Path) -> str:
    return AssetManager().load_font(filename)


def load_json(filename: str | Path) -> Any:
    return AssetManager().load_json(filename)


def load_csv(filename: str | Path) -> list[dict[str, str]]:
    return AssetManager().load_csv(filename)


def load_text(filename: str | Path) -> str:
    return AssetManager().load_text(filename)
