from __future__ import annotations

import ast
from pathlib import Path


def test_phase74_admob_smoke_example_has_valid_python():
    path = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "phase74_admob_smoke"
        / "main.py"
    )

    content = path.read_text(
        encoding="utf-8",
    )

    ast.parse(
        content,
        filename=str(path),
    )


def test_phase74_admob_smoke_example_uses_test_provider_flow():
    path = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "phase74_admob_smoke"
        / "main.py"
    )

    content = path.read_text(
        encoding="utf-8",
    )

    assert "AdMobAndroidProvider" in content
    assert 'show_banner(' in content
    assert 'show_interstitial(' in content
    assert 'show_rewarded(' in content
    assert 'on_reward=' in content
