import pytest

from hyperkit import Circle, Rect, Vector2


def test_vector2_arithmetic():
    a = Vector2(
        3,
        4,
    )
    b = Vector2(
        1,
        2,
    )

    assert a + b == Vector2(
        4,
        6,
    )
    assert a - b == Vector2(
        2,
        2,
    )
    assert a * 2 == Vector2(
        6,
        8,
    )
    assert 2 * a == Vector2(
        6,
        8,
    )
    assert a / 2 == Vector2(
        1.5,
        2,
    )
    assert -a == Vector2(
        -3,
        -4,
    )


def test_vector2_length_and_normalized():
    value = Vector2(
        3,
        4,
    )

    assert value.length_squared == 25
    assert value.length == 5
    assert value.normalized().length == pytest.approx(
        1.0
    )


def test_zero_vector_normalizes_safely():
    assert Vector2().normalized() == Vector2()


def test_vector2_dot_distance_and_lerp():
    a = Vector2(
        0,
        0,
    )
    b = Vector2(
        6,
        8,
    )

    assert a.distance_to(
        b
    ) == 10
    assert Vector2(
        1,
        2,
    ).dot(
        Vector2(
            3,
            4,
        )
    ) == 11

    assert a.lerp(
        b,
        0.5,
    ) == Vector2(
        3,
        4,
    )


def test_vector2_lerp_clamps_amount():
    start = Vector2(
        1,
        2,
    )
    end = Vector2(
        5,
        6,
    )

    assert start.lerp(
        end,
        -1,
    ) == start
    assert start.lerp(
        end,
        2,
    ) == end


def test_vector2_divide_by_zero_is_rejected():
    with pytest.raises(
        ZeroDivisionError
    ):
        Vector2(
            1,
            2,
        ) / 0


def test_rect_geometry_helpers():
    rect = Rect(
        10,
        20,
        30,
        40,
    )

    assert rect.center == Vector2(
        25,
        40,
    )
    assert rect.size == Vector2(
        30,
        40,
    )
    assert rect.area == 1200
    assert rect.translated(
        Vector2(
            5,
            -10,
        )
    ) == Rect(
        15,
        10,
        30,
        40,
    )


def test_circle_geometry_helpers():
    circle = Circle(
        5,
        6,
        10,
    )

    assert circle.center == Vector2(
        5,
        6,
    )
    assert circle.diameter == 20
    assert circle.contains(
        5,
        6,
    )
    assert not circle.contains(
        30,
        30,
    )
    assert circle.translated(
        Vector2(
            2,
            3,
        )
    ) == Circle(
        7,
        9,
        10,
    )
