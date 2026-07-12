from pathlib import Path

import pytest

from hyperkit import LevelData, LevelError, LevelManager, load_level


def create_level_file(project_path: Path):
    data_folder = project_path / "assets" / "data"
    data_folder.mkdir(parents=True)

    level_json = """
{
  "name": "Test Level",
  "width": 720,
  "height": 1280,
  "background_color": [0.1, 0.1, 0.15, 1.0],
  "metadata": {
    "difficulty": "easy"
  },
  "objects": [
    {
      "name": "player",
      "type": "spawn",
      "x": 300,
      "y": 500,
      "width": 100,
      "height": 100,
      "shape": "circle",
      "color": [0.2, 0.75, 1.0, 1.0]
    },
    {
      "name": "coin",
      "type": "collectible",
      "x": 420,
      "y": 650,
      "width": 60,
      "height": 60,
      "shape": "circle",
      "color": [1.0, 0.85, 0.2, 1.0],
      "data": {
        "score": 10
      }
    }
  ]
}
"""
    (data_folder / "level_1.json").write_text(level_json, encoding="utf-8")


def test_level_data_from_dict():
    level = LevelData.from_dict(
        {
            "name": "Demo",
            "objects": [
                {"name": "player", "type": "spawn"},
                {"name": "coin", "type": "collectible"},
            ],
        }
    )

    assert level.name == "Demo"
    assert level.find_object("player")["type"] == "spawn"
    assert len(level.objects_by_type("collectible")) == 1


def test_level_data_rejects_invalid_objects():
    with pytest.raises(LevelError):
        LevelData.from_dict({"objects": "not a list"})


def test_load_level_reads_json_file(tmp_path: Path):
    create_level_file(tmp_path)

    level = load_level("level_1.json", project_path=tmp_path)

    assert level.name == "Test Level"
    assert level.width == 720
    assert level.height == 1280
    assert level.background_color == (0.1, 0.1, 0.15, 1.0)
    assert level.metadata["difficulty"] == "easy"
    assert len(level.objects) == 2


def test_level_manager_creates_game_objects(tmp_path: Path):
    create_level_file(tmp_path)

    manager = LevelManager(project_path=tmp_path)
    level = manager.load("level_1.json")
    objects = manager.create_objects(level)

    assert len(objects) == 2

    player = objects[0]
    coin = objects[1]

    assert player.name == "player"
    assert player.x == 300
    assert player.y == 500
    assert player.shape == "circle"
    assert player.color == (0.2, 0.75, 1.0, 1.0)
    assert player.data["type"] == "spawn"

    assert coin.name == "coin"
    assert coin.data["type"] == "collectible"
    assert coin.data["score"] == 10


def test_level_manager_requires_loaded_level(tmp_path: Path):
    manager = LevelManager(project_path=tmp_path)

    with pytest.raises(LevelError):
        manager.create_objects()


class DummyScene:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        return obj


def test_level_manager_adds_objects_to_scene(tmp_path: Path):
    create_level_file(tmp_path)

    manager = LevelManager(project_path=tmp_path)
    level = manager.load("level_1.json")

    scene = DummyScene()
    objects = manager.add_to_scene(scene, level)

    assert len(objects) == 2
    assert len(scene.objects) == 2
