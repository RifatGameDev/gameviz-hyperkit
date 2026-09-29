import pytest

from hyperkit import CanvasScaler, Rect


def test_canvas_scaler_keeps_aspect_ratio_for_same_size():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=720,
        actual_height=1280,
    )

    assert scaler.scale == 1
    assert scaler.offset_x == 0
    assert scaler.offset_y == 0


def test_canvas_scaler_scales_down():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=360,
        actual_height=640,
    )

    assert scaler.scale == 0.5
    assert scaler.to_screen_rect(
        100,
        200,
        50,
        80,
    ) == (
        50,
        100,
        25,
        40,
    )


def test_canvas_scaler_converts_screen_to_virtual():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=360,
        actual_height=640,
    )

    assert scaler.to_virtual_point(
        50,
        100,
    ) == (
        100,
        200,
    )


def test_canvas_scaler_handles_wide_window_with_offset():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=1000,
        actual_height=1280,
    )

    assert scaler.scale == 1
    assert scaler.offset_x == 140
    assert scaler.offset_y == 0
    assert scaler.to_screen_x(
        0
    ) == 140
    assert scaler.to_virtual_point(
        140,
        0,
    ) == (
        0,
        0,
    )


def test_canvas_scaler_exposes_content_rect():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=1000,
        actual_height=1280,
    )

    assert scaler.content_rect == Rect(
        140,
        0,
        720,
        1280,
    )


def test_canvas_scaler_screen_point_round_trip():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=360,
        actual_height=640,
    )

    screen = scaler.to_screen_point(
        100,
        200,
    )

    assert scaler.to_virtual_point(
        *screen
    ) == (
        100,
        200,
    )


def test_canvas_scaler_virtual_rect_round_trip():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=360,
        actual_height=640,
    )

    screen_rect = scaler.to_screen_rect(
        100,
        200,
        50,
        80,
    )

    assert scaler.to_virtual_rect(
        *screen_rect
    ) == (
        100,
        200,
        50,
        80,
    )


def test_canvas_scaler_detects_letterbox_area():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=1000,
        actual_height=1280,
    )

    assert scaler.contains_screen_point(
        140,
        100,
    )
    assert scaler.contains_screen_point(
        860,
        100,
    )
    assert not scaler.contains_screen_point(
        100,
        100,
    )


def test_canvas_scaler_update_size_is_chainable_and_safe():
    scaler = CanvasScaler()

    result = scaler.update_actual_size(
        0,
        -10,
    )

    assert result is scaler
    assert scaler.actual_width == 1
    assert scaler.actual_height == 1


def test_canvas_scaler_rejects_invalid_virtual_size():
    with pytest.raises(
        ValueError,
        match="virtual_width",
    ):
        CanvasScaler(
            virtual_width=0,
        )

    with pytest.raises(
        ValueError,
        match="virtual_height",
    ):
        CanvasScaler(
            virtual_height=0,
        )
