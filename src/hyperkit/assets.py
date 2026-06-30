from __future__ import annotations

import csv
import json
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

    def __init__(self, project_path: str | Path = ".", assets_folder: str = "assets"):
        self.project_path = Path(project_path).resolve()
        self.assets_path = (self.project_path / assets_folder).resolve()

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

        if not path.exists():
            raise AssetNotFoundError(f"Asset not found: {path}")

        return path

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

    def load_json(self, filename: str | Path) -> Any:
        """Load JSON data from assets/data."""
        path = self._resolve_asset(
            "data", filename, JSON_EXTENSIONS, "JSON data")

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def load_csv(self, filename: str | Path) -> list[dict[str, str]]:
        """Load CSV data from assets/data."""
        path = self._resolve_asset(
            "data", filename, CSV_EXTENSIONS, "CSV data")

        with path.open("r", encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))

    def load_text(self, filename: str | Path) -> str:
        """Load text data from assets/data."""
        path = self._resolve_asset(
            "data", filename, TEXT_EXTENSIONS, "text data")
        return path.read_text(encoding="utf-8")

    def list_assets(self, folder: str, extensions: set[str]) -> list[str]:
        folder_path = self.assets_path / folder

        if not folder_path.exists():
            return []

        results = []

        for path in folder_path.iterdir():
            if path.is_file() and path.suffix.lower() in extensions:
                relative_path = path.relative_to(self.assets_path)
                results.append(str(relative_path).replace("\\", "/"))

        return sorted(results)

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
