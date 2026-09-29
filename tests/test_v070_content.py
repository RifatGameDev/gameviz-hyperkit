from pathlib import Path

import pytest

from hyperkit import (
    ContentError,
    ContentItem,
    ContentManager,
    ContentManifest,
)


def create_content_project(
    root: Path,
) -> None:
    (
        root
        / "assets"
        / "images"
    ).mkdir(
        parents=True
    )
    (
        root
        / "assets"
        / "audio"
    ).mkdir()
    (
        root
        / "assets"
        / "fonts"
    ).mkdir()
    (
        root
        / "assets"
        / "data"
    ).mkdir()

    (
        root
        / "assets"
        / "images"
        / "hero.png"
    ).write_bytes(
        b"fake"
    )

    (
        root
        / "assets"
        / "data"
        / "questions.json"
    ).write_text(
        '{"questions": [1, 2, 3]}',
        encoding="utf-8",
    )

    (
        root
        / "assets"
        / "data"
        / "content.json"
    ).write_text(
        """
{
  "name": "Demo Content",
  "version": "1",
  "items": [
    {
      "id": "hero",
      "kind": "image",
      "asset": "hero.png",
      "tags": ["player", "Character"],
      "data": {"role": "main"}
    },
    {
      "id": "questions",
      "kind": "json",
      "asset": "questions.json",
      "tags": ["quiz"]
    },
    {
      "id": "difficulty",
      "kind": "config",
      "data": {"speed": 3}
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )


def test_content_manifest_validates_duplicate_ids():
    with pytest.raises(
        ContentError,
        match="Duplicate",
    ):
        ContentManifest(
            name="Demo",
            items=(
                ContentItem(
                    "same",
                    "config",
                ),
                ContentItem(
                    "same",
                    "config",
                ),
            ),
        )


def test_content_manager_loads_and_queries_manifest(
    tmp_path: Path,
):
    create_content_project(
        tmp_path
    )
    manager = ContentManager(
        project_path=tmp_path
    )

    manifest = manager.load(
        "content.json"
    )

    assert manifest.name == "Demo Content"
    assert manager.loaded
    assert manager.content_ids == [
        "difficulty",
        "hero",
        "questions",
    ]
    assert (
        manager.require(
            "hero"
        ).data[
            "role"
        ]
        == "main"
    )
    assert [
        item.content_id
        for item in manager.find_by_tag(
            "CHARACTER"
        )
    ] == [
        "hero"
    ]
    assert [
        item.content_id
        for item in manager.find_by_kind(
            "json"
        )
    ] == [
        "questions"
    ]


def test_content_manager_loads_assets_and_inline_data(
    tmp_path: Path,
):
    create_content_project(
        tmp_path
    )
    manager = ContentManager(
        project_path=tmp_path
    )
    manager.load(
        "content.json"
    )

    assert manager.resolve_asset(
        "hero"
    ).endswith(
        "hero.png"
    )

    assert manager.load_item(
        "questions"
    ) == {
        "questions": [
            1,
            2,
            3,
        ]
    }

    assert manager.load_item(
        "difficulty"
    ) == {
        "speed": 3
    }

    assert manager.validate_assets() == []


def test_content_manager_reports_missing_assets(
    tmp_path: Path,
):
    create_content_project(
        tmp_path
    )
    manager = ContentManager(
        project_path=tmp_path
    )
    manager.set_manifest(
        ContentManifest(
            name="Broken",
            items=(
                ContentItem(
                    "missing",
                    "image",
                    "missing.png",
                ),
            ),
        )
    )

    issues = manager.validate_assets()

    assert len(
        issues
    ) == 1
    assert "missing" in issues[0]


def test_content_manager_require_rejects_unknown_id():
    manager = ContentManager()

    with pytest.raises(
        ContentError,
        match="Unknown content id",
    ):
        manager.require(
            "missing"
        )


def test_content_manager_unload_clears_state():
    manager = ContentManager()
    manager.set_manifest(
        ContentManifest(
            name="Demo",
            items=(
                ContentItem(
                    "config",
                    "config",
                    data={
                        "value": 1
                    },
                ),
            ),
        )
    )

    manager.unload()

    assert not manager.loaded
    assert manager.content_ids == []
