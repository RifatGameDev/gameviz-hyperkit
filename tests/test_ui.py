from hyperkit import Button, Scene, TextLabel


def test_text_label_defaults_to_text_shape():
    label = TextLabel(
        text="Score: 10",
        font_size=32,
    )

    assert label.shape == "text"
    assert label.text == "Score: 10"
    assert label.font_size == 32


def test_text_label_set_text():
    label = TextLabel(
        text="Old"
    )

    result = label.set_text(
        "New"
    )

    assert label.text == "New"
    assert result is label


def test_button_click_calls_handler():
    clicked = {
        "value": False,
    }

    def on_click():
        clicked["value"] = True

    button = Button(
        text="Restart",
        on_click=on_click,
    )

    assert button.click() is True
    assert clicked["value"] is True


def test_disabled_button_does_not_call_handler():
    clicked = {
        "count": 0,
    }

    def on_click():
        clicked["count"] += 1

    button = Button(
        on_click=on_click,
        enabled=False,
    )

    assert button.click() is False
    assert clicked["count"] == 0


def test_button_hit_test_respects_interaction_state():
    button = Button(
        x=10,
        y=20,
        width=100,
        height=50,
    )

    assert button.hit_test(
        20,
        30,
    )

    button.visible = False

    assert not button.hit_test(
        20,
        30,
    )


def test_scene_dispatch_tap_clicks_topmost_button():
    clicked: list[str] = []
    scene = Scene()

    scene.add(
        Button(
            x=0,
            y=0,
            width=100,
            height=100,
            on_click=lambda: clicked.append(
                "bottom"
            ),
        )
    )
    scene.add(
        Button(
            x=0,
            y=0,
            width=100,
            height=100,
            on_click=lambda: clicked.append(
                "top"
            ),
        )
    )

    assert scene.dispatch_tap(
        50,
        50,
    ) is True
    assert clicked == [
        "top",
    ]


def test_scene_dispatch_tap_falls_through_without_button():
    scene = Scene()

    assert scene.dispatch_tap(
        50,
        50,
    ) is False


def test_button_text_style_defaults_are_available():
    button = Button()

    assert button.font_size == 24
    assert button.bold is False
    assert button.text_color == (
        1.0,
        1.0,
        1.0,
        1.0,
    )
