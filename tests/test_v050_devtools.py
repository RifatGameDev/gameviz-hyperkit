import math

import pytest

from hyperkit import (
    DebugOverlay,
    RuntimeDiagnostics,
    Scene,
)


def test_runtime_diagnostics_tracks_stable_fps():
    diagnostics = RuntimeDiagnostics(
        target_fps=60,
        sample_window=60,
    )

    for _ in range(60):
        diagnostics.update(
            1 / 60
        )

    snapshot = diagnostics.snapshot()

    assert snapshot.frame_count == 60
    assert math.isclose(
        snapshot.fps,
        60.0,
        rel_tol=0.02,
    )
    assert math.isclose(
        snapshot.frame_ms,
        1000 / 60,
        rel_tol=0.02,
    )
    assert snapshot.dropped_frames == 0


def test_runtime_diagnostics_counts_slow_frames():
    diagnostics = RuntimeDiagnostics(
        target_fps=60
    )

    diagnostics.update(
        0.05
    )

    assert (
        diagnostics.snapshot()
        .dropped_frames
        == 1
    )


def test_runtime_diagnostics_rejects_invalid_values():
    with pytest.raises(
        ValueError
    ):
        RuntimeDiagnostics(
            target_fps=0
        )

    with pytest.raises(
        ValueError
    ):
        RuntimeDiagnostics(
            sample_window=0
        )

    diagnostics = RuntimeDiagnostics()

    with pytest.raises(
        ValueError
    ):
        diagnostics.update(
            -0.1
        )


def test_runtime_diagnostics_reset_is_chainable():
    diagnostics = RuntimeDiagnostics()
    diagnostics.update(
        1 / 30
    )

    assert (
        diagnostics.reset()
        is diagnostics
    )

    snapshot = diagnostics.snapshot()

    assert snapshot.frame_count == 0
    assert snapshot.elapsed_seconds == 0
    assert snapshot.dropped_frames == 0


def test_debug_overlay_updates_and_toggles():
    scene = Scene()
    overlay = DebugOverlay(
        scene,
        visible=True,
    )

    snapshot = overlay.update(
        1 / 60
    )

    assert snapshot.frame_count == 1
    assert "FPS:" in overlay.label.text
    assert overlay.label.visible is True

    assert overlay.toggle() is False
    assert overlay.label.visible is False

    assert overlay.toggle() is True
    assert overlay.label.visible is True
