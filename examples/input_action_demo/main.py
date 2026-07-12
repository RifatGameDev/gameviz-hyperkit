from hyperkit import Game, GameObject, InputActionMap, Scene, TextLabel


class InputActionDemo(Scene):
    """Shows tap, area tap, and swipe action mapping."""

    def start(self):
        self.actions = InputActionMap()

        self.player = self.add(
            GameObject(
                x=310,
                y=620,
                width=100,
                height=100,
                color=(0.2, 0.75, 1.0, 1),
                name="player",
            )
        )

        self.attack_button = self.add(
            GameObject(
                x=190,
                y=420,
                width=340,
                height=110,
                color=(0.2, 0.45, 0.9, 1),
                name="attack_button",
            )
        )

        self.add(
            TextLabel(
                x=90,
                y=1180,
                text="Input Action Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=180,
                y=455,
                text="Attack Area",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=60,
                y=1080,
                text="Tap screen, tap button, or swipe left/right.",
                font_size=25,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.actions.map_tap("jump", self.jump)
        self.actions.map_area(
            "attack",
            x=self.attack_button.x,
            y=self.attack_button.y,
            width=self.attack_button.width,
            height=self.attack_button.height,
            callback=self.attack,
        )
        self.actions.map_swipe(
            "move_left", direction="left", callback=self.move_left)
        self.actions.map_swipe(
            "move_right", direction="right", callback=self.move_right)

        self.start_game()

    def jump(self, event):
        self.player.y += 70
        self.message.set_text("Action: jump")

    def attack(self, event):
        self.attack_button.color = (1.0, 0.45, 0.25, 1)
        self.message.set_text("Action: attack")

    def move_left(self, event):
        self.player.x -= 80
        self.message.set_text("Action: move_left")

    def move_right(self, event):
        self.player.x += 80
        self.message.set_text("Action: move_right")

    def on_tap(self, x, y):
        self.actions.handle_tap(x, y)

    def on_swipe(self, start, end, direction):
        self.actions.handle_swipe(start, end, direction)


if __name__ == "__main__":
    Game(title="Input Action Demo", width=720, height=1280).set_scene(
        InputActionDemo()
    ).run()
