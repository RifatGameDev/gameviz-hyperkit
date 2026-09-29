from pathlib import Path

import pytest

from hyperkit import (
    Prefab,
    PrefabError,
    PrefabLibrary,
)


def create_prefab_project(
    root: Path,
) -> None:
    data = (
        root
        / "assets"
        / "data"
    )
    data.mkdir(
        parents=True
    )

    (
        data
        / "prefabs.json"
    ).write_text(
        """
{
  "prefabs": {
    "coin": {
      "object": {
        "name": "coin",
        "type": "collectible",
        "x": 10,
        "y": 20,
        "width": 40,
        "height": 40,
        "shape": "circle",
        "color": [1, 0.8, 0.2, 1],
        "data": {
          "score": 10
        }
      },
      "metadata": {
        "category": "reward"
      }
    }
  }
}
""".strip(),
        encoding="utf-8",
    )


def test_prefab_library_loads_and_creates_objects(
    tmp_path: Path,
):
    create_prefab_project(
        tmp_path
    )

    library = PrefabLibrary(
        project_path=tmp_path
    )

    loaded = library.load(
        "prefabs.json"
    )

    assert len(
        loaded
    ) == 1
    assert library.names == [
        "coin"
    ]

    coin = library.create(
        "coin",
        x=200,
        data={
            "value": 2
        },
    )

    assert coin.name == "coin"
    assert coin.x == 200
    assert coin.y == 20
    assert coin.data[
        "score"
    ] == 10
    assert coin.data[
        "value"
    ] == 2
    assert coin.data[
        "type"
    ] == "collectible"


def test_prefab_library_rejects_duplicate_registration():
    library = PrefabLibrary()
    prefab = Prefab(
        name="enemy",
        object_data={},
    )

    library.register(
        prefab
    )

    with pytest.raises(
        PrefabError,
        match="already registered",
    ):
        library.register(
            prefab
        )


def test_prefab_library_can_replace_prefab():
    library = PrefabLibrary()

    library.register(
        Prefab(
            "enemy",
            {
                "width": 10,
            },
        )
    )

    library.register(
        Prefab(
            "enemy",
            {
                "width": 20,
            },
        ),
        replace=True,
    )

    assert (
        library.create(
            "enemy"
        ).width
        == 20
    )


def test_prefab_library_adds_to_scene():
    class Scene:
        def __init__(self):
            self.objects = []

        def add(self, obj):
            self.objects.append(
                obj
            )
            return obj

    library = PrefabLibrary()
    library.register(
        Prefab(
            "enemy",
            {
                "name": "enemy",
            },
        )
    )
    scene = Scene()

    obj = library.add_to_scene(
        scene,
        "enemy",
    )

    assert scene.objects == [
        obj
    ]


def test_prefab_library_remove_and_clear():
    library = PrefabLibrary()
    library.register(
        Prefab(
            "a",
            {},
        )
    )
    library.register(
        Prefab(
            "b",
            {},
        )
    )

    assert library.remove(
        "a"
    )
    assert not library.remove(
        "missing"
    )
    assert library.clear() == 1
    assert library.names == []
