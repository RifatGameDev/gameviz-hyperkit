from hyperkit import Circle, Rect, circle_intersects_circle, rect_intersects_circle, rect_intersects_rect


def test_rect_intersects_rect():
    assert rect_intersects_rect(Rect(0, 0, 10, 10), Rect(5, 5, 10, 10))
    assert not rect_intersects_rect(Rect(0, 0, 10, 10), Rect(20, 20, 5, 5))


def test_circle_intersects_circle():
    assert circle_intersects_circle(Circle(0, 0, 5), Circle(8, 0, 5))
    assert not circle_intersects_circle(Circle(0, 0, 5), Circle(20, 0, 5))


def test_rect_intersects_circle():
    assert rect_intersects_circle(Rect(0, 0, 10, 10), Circle(5, 5, 2))
    assert not rect_intersects_circle(Rect(0, 0, 10, 10), Circle(50, 50, 2))
