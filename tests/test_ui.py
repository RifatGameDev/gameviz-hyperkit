from hyperkit import Button, TextLabel


def test_text_label_defaults_to_text_shape():
    label = TextLabel(text="Score: 10", font_size=32)

    assert label.shape == "text"
    assert label.text == "Score: 10"
    assert label.font_size == 32


def test_text_label_set_text():
    label = TextLabel(text="Old")

    label.set_text("New")

    assert label.text == "New"


def test_button_click_calls_handler():
    clicked = {"value": False}

    def on_click():
        clicked["value"] = True

    button = Button(text="Restart", on_click=on_click)
    button.click()

    assert clicked["value"] is True
