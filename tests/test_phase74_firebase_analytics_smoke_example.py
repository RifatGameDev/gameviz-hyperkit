from __future__ import annotations

import ast
from pathlib import Path


def _example_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "phase74_firebase_analytics_smoke"
        / "main.py"
    )


def test_phase74_firebase_analytics_smoke_example_has_valid_python():
    path = _example_path()

    content = path.read_text(
        encoding="utf-8",
    )

    ast.parse(
        content,
        filename=str(path),
    )


def test_phase74_firebase_analytics_smoke_example_uses_real_provider():
    content = (
        _example_path()
        .read_text(
            encoding="utf-8",
        )
    )

    assert (
        "FirebaseAnalyticsAndroidProvider"
        in content
    )

    assert (
        "from_google_services_json"
        in content
    )

    assert (
        "org.gameviz.phase74analyticssmoke"
        in content
    )

    assert (
        "game_start"
        in content
    )

    assert (
        "hyperkit_smoke_tap"
        in content
    )

    assert (
        "level_complete"
        in content
    )
