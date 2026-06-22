from hyperkit import TouchTracker


def test_tap_detection():
    tracker = TouchTracker()
    tracker.touch_down(10, 10, timestamp=0.0)
    gesture = tracker.touch_up(12, 11, timestamp=0.1)
    assert gesture is not None
    assert gesture.kind == "tap"


def test_swipe_detection():
    tracker = TouchTracker()
    tracker.touch_down(10, 10, timestamp=0.0)
    gesture = tracker.touch_up(200, 10, timestamp=0.3)
    assert gesture is not None
    assert gesture.kind == "swipe"
    assert gesture.direction == "right"
