from hyperkit import BoundsManager, Game, GameObject, Scene, ScreenBounds, TextLabel


class BoundsDemo(Scene):
    """Shows screen bounds, bounce, clamp, and wrap behavior."""

    def start(self):
        self.bounds = BoundsManager(
            screen=ScreenBounds(width=720, height=1280),
        )

        self.ball = self.add(
            GameObject(
                x=300,
                y=600,
                width=90,
                height=90,
                vx=260,
                vy=220,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
                name="bouncing_ball",
            )
        )

        self.box = self.add(
            GameObject(
                x=80,
                y=420,
                width=100,
                height=100,
                vx=180,
                vy=0,
                color=(1.0, 0.85, 0.2, 1),
                name="wrapping_box",
            )
        )

        self.add(
            TextLabel(
                x=90,
                y=1180,
                text="Bounds Demo",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=60,
                y=1110,
                text="Blue ball bounces. Yellow box wraps.",
                font_size=26,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.add(
            TextLabel(
                x=60,
                y=1045,
                text="Tap anywhere: ball moves there but stays inside screen.",
                font_size=23,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.ball.x = x - self.ball.width / 2
        self.ball.y = y - self.ball.height / 2
        self.bounds.keep_on_screen(self.ball)
        self.message.set_text("Ball clamped inside screen!")

    def update(self, dt):
        super().update(dt)

        self.bounds.bounce_on_screen(self.ball, bounce=1.0)
        self.bounds.wrap_on_screen(self.box)


if __name__ == "__main__":
    Game(title="Bounds Demo", width=720,
         height=1280).set_scene(BoundsDemo()).run()
