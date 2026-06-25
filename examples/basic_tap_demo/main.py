from hyperkit import Game, GameObject, Scene, TextLabel


class BasicTapDemo(Scene):
    """Basic custom HyperKit example.

    Tap/click anywhere to move the blue circle.
    """

    def start(self):
        self.player = self.add(
            GameObject(
                x=300,
                y=520,
                width=110,
                height=110,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
            )
        )

        self.label = self.add(
            TextLabel(
                x=40,
                y=1180,
                text="Tap anywhere to move the circle",
                font_size=28,
                color=(1, 1, 1, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2


if __name__ == "__main__":
    Game(title="Basic Tap Demo", width=720,
         height=1280).set_scene(BasicTapDemo()).run()
