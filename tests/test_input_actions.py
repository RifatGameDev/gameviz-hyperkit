import pytest

from hyperkit import InputActionMap


def test_input_action_map_handles_tap():
    called = {"action": None}

    actions = InputActionMap()
    actions.map_tap(
        "jump", callback=lambda event: called.update(action=event.action))

    event = actions.handle_tap(100, 200)

    assert event is not None
    assert event.action == "jump"
    assert event.x == 100
    assert event.y == 200
    assert called["action"] == "jump"


def test_input_action_map_handles_area_tap():
    called = {"value": False}

    actions = InputActionMap()
    actions.map_area(
        "attack",
        x=100,
        y=100,
        width=200,
        height=100,
        callback=lambda event: called.update(value=True),
    )

    event = actions.handle_tap(150, 150)

    assert event is not None
    assert event.action == "attack"
    assert called["value"] is True


def test_input_action_map_ignores_tap_outside_area():
    actions = InputActionMap()
    actions.map_area("attack", x=100, y=100, width=200, height=100)

    event = actions.handle_tap(20, 20)

    assert event is None


def test_input_action_map_handles_swipe_direction():
    called = {"direction": None}

    actions = InputActionMap()
    actions.map_swipe(
        "move_left",
        direction="left",
        callback=lambda event: called.update(direction=event.direction),
    )

    event = actions.handle_swipe((300, 300), (100, 300), "left")

    assert event is not None
    assert event.action == "move_left"
    assert event.direction == "left"
    assert called["direction"] == "left"


def test_input_action_map_ignores_wrong_swipe_direction():
    actions = InputActionMap()
    actions.map_swipe("move_left", direction="left")

    event = actions.handle_swipe((100, 300), (300, 300), "right")

    assert event is None


def test_disable_action_prevents_trigger():
    actions = InputActionMap()
    actions.map_tap("jump")
    actions.disable_action("jump")

    event = actions.handle_tap(100, 200)

    assert event is None


def test_enable_action_allows_trigger_again():
    actions = InputActionMap()
    actions.map_tap("jump")

    actions.disable_action("jump")
    actions.enable_action("jump")

    event = actions.handle_tap(100, 200)

    assert event is not None
    assert event.action == "jump"


def test_remove_action_deletes_bindings():
    actions = InputActionMap()
    actions.map_tap("jump")
    actions.remove_action("jump")

    assert actions.actions() == []
    assert actions.handle_tap(100, 200) is None


def test_latest_binding_has_priority():
    actions = InputActionMap()
    actions.map_tap("first")
    actions.map_tap("second")

    event = actions.handle_tap(100, 200)

    assert event is not None
    assert event.action == "second"



def test_input_action_rejects_empty_action_name():
    actions = InputActionMap()

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        actions.map_tap("   ")


def test_area_binding_rejects_non_positive_size():
    actions = InputActionMap()

    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        actions.map_area(
            "attack",
            x=0,
            y=0,
            width=0,
            height=100,
        )


def test_swipe_direction_is_normalized():
    actions = InputActionMap()
    actions.map_swipe(
        "move_left",
        direction=" LEFT ",
    )

    event = actions.handle_swipe(
        (300, 300),
        (100, 300),
        "left",
    )

    assert event is not None
    assert event.direction == "left"


def test_action_map_can_be_disabled_and_reenabled():
    actions = InputActionMap()
    actions.map_tap("jump")

    assert actions.set_enabled(False) is actions
    assert actions.handle_tap(10, 10) is None

    actions.set_enabled(True)

    assert actions.handle_tap(10, 10) is not None


def test_has_action_and_bindings_for():
    actions = InputActionMap()
    first = actions.map_tap("jump")
    second = actions.map_area(
        "jump",
        x=0,
        y=0,
        width=100,
        height=100,
    )

    assert actions.has_action("jump")
    assert actions.bindings_for("jump") == [
        first,
        second,
    ]


def test_enable_disable_action_report_binding_count():
    actions = InputActionMap()
    actions.map_tap("jump")
    actions.map_area(
        "jump",
        x=0,
        y=0,
        width=100,
        height=100,
    )

    assert actions.disable_action("jump") == 2
    assert actions.enable_action("jump") == 2


def test_remove_action_reports_removed_binding_count():
    actions = InputActionMap()
    actions.map_tap("jump")
    actions.map_area(
        "jump",
        x=0,
        y=0,
        width=100,
        height=100,
    )

    assert actions.remove_action("jump") == 2
    assert actions.remove_action("jump") == 0


def test_clear_is_chainable_and_resets_last_event():
    actions = InputActionMap()
    actions.map_tap("jump")
    actions.handle_tap(10, 10)

    assert actions.last_event is not None

    result = actions.clear()

    assert result is actions
    assert actions.bindings == []
    assert actions.last_event is None
