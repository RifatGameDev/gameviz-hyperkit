from pathlib import Path

import pytest

from hyperkit import (
    AssetManager,
    AssetNotFoundError,
    UnsupportedAssetTypeError,
)


def create_asset_folders(project_path: Path):
    (project_path / "assets" / "images").mkdir(parents=True)
    (project_path / "assets" / "audio").mkdir(parents=True)
    (project_path / "assets" / "fonts").mkdir(parents=True)
    (project_path / "assets" / "data").mkdir(parents=True)


def test_load_json_reads_data_file(tmp_path: Path):
    create_asset_folders(tmp_path)

    data_path = tmp_path / "assets" / "data" / "level.json"
    data_path.write_text(
        '{"level": 1, "name": "Demo Level"}', encoding="utf-8")

    assets = AssetManager(project_path=tmp_path)

    data = assets.load_json("level.json")

    assert data["level"] == 1
    assert data["name"] == "Demo Level"


def test_load_csv_reads_data_file(tmp_path: Path):
    create_asset_folders(tmp_path)

    csv_path = tmp_path / "assets" / "data" / "items.csv"
    csv_path.write_text("name,score\ncoin,10\ngem,50\n", encoding="utf-8")

    assets = AssetManager(project_path=tmp_path)

    rows = assets.load_csv("items.csv")

    assert rows[0]["name"] == "coin"
    assert rows[0]["score"] == "10"
    assert rows[1]["name"] == "gem"


def test_load_text_reads_data_file(tmp_path: Path):
    create_asset_folders(tmp_path)

    text_path = tmp_path / "assets" / "data" / "message.txt"
    text_path.write_text("Hello HyperKit", encoding="utf-8")

    assets = AssetManager(project_path=tmp_path)

    assert assets.load_text("message.txt") == "Hello HyperKit"


def test_load_image_returns_image_path(tmp_path: Path):
    create_asset_folders(tmp_path)

    image_path = tmp_path / "assets" / "images" / "player.png"
    image_path.write_bytes(b"fake image bytes")

    assets = AssetManager(project_path=tmp_path)

    loaded_path = assets.load_image("player.png")

    assert loaded_path.endswith("player.png")


def test_missing_asset_raises_clear_error(tmp_path: Path):
    create_asset_folders(tmp_path)

    assets = AssetManager(project_path=tmp_path)

    with pytest.raises(AssetNotFoundError):
        assets.load_image("missing.png")


def test_fbx_asset_is_rejected_with_clear_error(tmp_path: Path):
    create_asset_folders(tmp_path)

    fbx_path = tmp_path / "assets" / "images" / "character.fbx"
    fbx_path.write_text("fake fbx source", encoding="utf-8")

    assets = AssetManager(project_path=tmp_path)

    with pytest.raises(UnsupportedAssetTypeError, match="FBX"):
        assets.load_image("character.fbx")


def test_list_assets_returns_relative_paths(tmp_path: Path):
    create_asset_folders(tmp_path)

    (tmp_path / "assets" / "images" / "player.png").write_bytes(b"fake")
    (tmp_path / "assets" / "images" / "enemy.webp").write_bytes(b"fake")

    assets = AssetManager(project_path=tmp_path)

    assert assets.list_images() == ["images/enemy.webp", "images/player.png"]
