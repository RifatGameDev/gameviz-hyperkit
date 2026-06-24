from hyperkit import CanvasScaler


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
    assert scaler.to_screen_rect(100, 200, 50, 80) == (50, 100, 25, 40)


def test_canvas_scaler_converts_screen_to_virtual():
    scaler = CanvasScaler(
        virtual_width=720,
        virtual_height=1280,
        actual_width=360,
        actual_height=640,
    )

    assert scaler.to_virtual_point(50, 100) == (100, 200)


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
    assert scaler.to_screen_x(0) == 140
    assert scaler.to_virtual_point(140, 0) == (0, 0)
