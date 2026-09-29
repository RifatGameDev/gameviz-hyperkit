from pathlib import Path

import pytest

from hyperkit import (
    LevelSequence,
    LevelSequenceError,
    LevelManager,
)


def create_levels(
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

    for index in (
        1,
        2,
        3,
    ):
        (
            data
            / f"level_{index}.json"
        ).write_text(
            (
                "{"
                f'"name": "Level {index}",'
                '"objects": []'
                "}"
            ),
            encoding="utf-8",
        )


def test_level_sequence_progression_and_reset():
    sequence = LevelSequence(
        [
            "level_1.json",
            "level_2.json",
            "level_3.json",
        ]
    )

    assert sequence.current == "level_1.json"
    assert sequence.progress == (
        1,
        3,
    )
    assert sequence.next() == "level_2.json"
    assert sequence.next() == "level_3.json"
    assert sequence.next() is None
    assert sequence.previous() == "level_2.json"
    assert sequence.reset() is sequence
    assert sequence.current == "level_1.json"


def test_level_sequence_can_loop():
    sequence = LevelSequence(
        [
            "one.json",
            "two.json",
        ],
        loop=True,
    )

    sequence.next()

    assert sequence.next() == "one.json"
    assert sequence.previous() == "two.json"


def test_level_sequence_loads_current_level(
    tmp_path: Path,
):
    create_levels(
        tmp_path
    )

    manager = LevelManager(
        project_path=tmp_path
    )
    sequence = LevelSequence(
        [
            "level_1.json",
            "level_2.json",
        ]
    )

    first = sequence.load_current(
        manager
    )
    second = sequence.advance_and_load(
        manager
    )

    assert first.name == "Level 1"
    assert second is not None
    assert second.name == "Level 2"
    assert manager.current_level is second


def test_level_sequence_rejects_invalid_configuration():
    with pytest.raises(
        LevelSequenceError
    ):
        LevelSequence(
            []
        )

    with pytest.raises(
        LevelSequenceError
    ):
        LevelSequence(
            [
                "one.json",
            ],
            current_index=2,
        )
