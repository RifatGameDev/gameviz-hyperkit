from hyperkit import CameraFollow, Game, GameObject, Scene, TextLabel


class CameraFollowDemo(Scene):
    """Shows simple camera follow behavior."""

    def start(self):
        self.player = self.add(
            GameObject(
                x=300,
                y=600,
                width=90,
                height=90,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
                name="player",
            )
        )

        # Add world objects so camera movement is visible.
        for i in range(8):
            self.add(
                GameObject(
                    x=120 + i * 220,
                    y=420 + (i % 2) * 220,
                    width=90,
                    height=90,
                    color=(1.0, 0.85, 0.2, 1),
                    shape="circle",
                    name=f"coin_{i}",
                )
            )

        self.add(
            GameObject(
                x=-200,
                y=300,
                width=2000,
                height=40,
                color=(0.25, 0.9, 0.35, 1),
                name="ground",
            )
        )

        self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Camera Follow Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=70,
                y=1110,
                text="Tap left/right side to move player.",
                font_size=27,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.camera_follow = CameraFollow(
            scene=self,
            target=self.player,
            screen_width=720,
            screen_height=1280,
            smoothness=6.0,
        )
        self.camera_follow.snap_to_target()

        self.start_game()

    def on_tap(self, x, y):
        if x < 360:
            self.player.x -= 160
            self.message.set_text("Move left")
        else:
            self.player.x += 160
            self.message.set_text("Move right")

    def update(self, dt):
        self.camera_follow.update(dt)
        super().update(dt)


if __name__ == "__main__":
    Game(title="Camera Follow Demo", width=720, height=1280).set_scene(
        CameraFollowDemo()
    ).run()
