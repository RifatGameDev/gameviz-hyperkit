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
