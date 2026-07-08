from hyperkit import AnimationManager, Game, GameObject, Scene, TextLabel


class AnimationDemo(Scene):
    """Shows movement, resize, color, loop, and yoyo animation."""

    def start(self):
        self.animations = AnimationManager()

        self.player = self.add(
            GameObject(
                x=300,
                y=560,
                width=110,
                height=110,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
                name="animated_player",
            )
        )

        self.add(
            TextLabel(
                x=70,
                y=1180,
                text="Animation Demo",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=60,
                y=1110,
                text="Tap anywhere to animate the circle.",
                font_size=28,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.animations.resize_to(
            self.player,
            width=140,
            height=140,
            duration=0.6,
            easing="ease_in_out_quad",
            loop=True,
            yoyo=True,
        )

        self.animations.color_to(
            self.player,
            color=(1.0, 0.45, 0.25, 1),
            duration=1.0,
            easing="ease_in_out_quad",
            loop=True,
            yoyo=True,
        )

        self.start_game()

    def on_tap(self, x, y):
        target_x = x - self.player.width / 2
        target_y = y - self.player.height / 2

        self.animations.stop(self.player, "x")
        self.animations.stop(self.player, "y")

        self.animations.move_to(
            self.player,
            x=target_x,
            y=target_y,
            duration=0.35,
            easing="ease_out_quad",
        )

        self.message.set_text("Moving with animation!")

    def update(self, dt):
        self.animations.update(dt)
        super().update(dt)


if __name__ == "__main__":
    Game(title="Animation Demo", width=720,
         height=1280).set_scene(AnimationDemo()).run()
