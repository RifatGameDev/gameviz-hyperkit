from pathlib import Path

from hyperkit import AssetManager


def create_data(
    root: Path,
):
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
        / "config.json"
    ).write_text(
        '{"speed": 2}',
        encoding="utf-8",
    )
    (
        data
        / "items.csv"
    ).write_text(
        "name,value\ncoin,10\n",
        encoding="utf-8",
    )
    (
        data
        / "message.txt"
    ).write_text(
        "hello",
        encoding="utf-8",
    )


def test_asset_manager_cached_json_is_isolated(
    tmp_path: Path,
):
    create_data(
        tmp_path
    )
    assets = AssetManager(
        project_path=tmp_path
    )

    first = assets.load_json(
        "config.json",
        cached=True,
    )
    first[
        "speed"
    ] = 99

    second = assets.load_json(
        "config.json",
        cached=True,
    )

    assert second[
        "speed"
    ] == 2
    assert assets.cache_size == 1


def test_asset_manager_preloads_supported_data(
    tmp_path: Path,
):
    create_data(
        tmp_path
    )
    assets = AssetManager(
        project_path=tmp_path
    )

    loaded = assets.preload_data(
        [
            "config.json",
            "items.csv",
            "message.txt",
        ]
    )

    assert loaded[
        "config.json"
    ][
        "speed"
    ] == 2
    assert loaded[
        "items.csv"
    ][0][
        "name"
    ] == "coin"
    assert loaded[
        "message.txt"
    ] == "hello"
    assert assets.cache_size == 3
    assert assets.clear_cache() == 3
    assert assets.cache_size == 0
