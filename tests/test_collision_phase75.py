from hyperkit.collision import (
    CollisionManifold,
    circle_collision,
    circle_intersects_circle,
    circle_intersects_rect,
    collision_manifold,
    intersects,
    point_in_circle,
    rect_circle_collision,
    rect_collision,
    rect_intersects_circle,
    rect_intersects_rect,
)
from hyperkit.geometry import Circle, Rect, Vector2


def test_existing_boolean_collision_helpers_remain_compatible():
    assert rect_intersects_rect(
        Rect(0, 0, 10, 10),
        Rect(5, 5, 10, 10),
    )
    assert circle_intersects_circle(
        Circle(0, 0, 5),
        Circle(8, 0, 5),
    )
    assert rect_intersects_circle(
        Rect(0, 0, 10, 10),
        Circle(5, 5, 2),
    )
    assert circle_intersects_rect(
        Circle(5, 5, 2),
        Rect(0, 0, 10, 10),
    )


def test_rect_collision_reports_normal_and_penetration():
    result = rect_collision(
        Rect(0, 0, 10, 10),
        Rect(8, 0, 10, 10),
    )

    assert result.colliding is True
    assert result.normal == Vector2(1.0, 0.0)
    assert result.penetration == 2


def test_rect_collision_treats_touching_edges_as_collision():
    result = rect_collision(
        Rect(0, 0, 10, 10),
        Rect(10, 0, 10, 10),
    )

    assert result.colliding is True
    assert result.penetration == 0


def test_circle_collision_reports_normal_and_penetration():
    result = circle_collision(
        Circle(0, 0, 5),
        Circle(8, 0, 5),
    )

    assert result.colliding is True
    assert result.normal == Vector2(1.0, 0.0)
    assert result.penetration == 2


def test_rect_circle_collision_reports_external_overlap():
    result = rect_circle_collision(
        Rect(0, 0, 10, 10),
        Circle(11, 5, 2),
    )

    assert result.colliding is True
    assert result.normal == Vector2(1.0, 0.0)
    assert result.penetration == 1


def test_rect_circle_collision_handles_circle_center_inside_rect():
    result = rect_circle_collision(
        Rect(0, 0, 10, 10),
        Circle(5, 5, 2),
    )

    assert result.colliding is True
    assert result.penetration == 7


def test_point_in_circle_and_generic_dispatch():
    circle = Circle(5, 5, 3)
    rect = Rect(0, 0, 5, 5)

    assert point_in_circle(5, 5, circle)
    assert intersects(rect, circle)

    result = collision_manifold(rect, circle)

    assert isinstance(
        result,
        CollisionManifold,
    )
    assert result.colliding is True


def test_inverted_manifold_reverses_normal():
    result = CollisionManifold(
        True,
        Vector2(1, -1),
        3,
    ).inverted()

    assert result.normal == Vector2(-1, 1)
    assert result.penetration == 3
