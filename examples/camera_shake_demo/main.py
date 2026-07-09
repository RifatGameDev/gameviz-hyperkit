from hyperkit import CameraShake, Game, GameObject, Scene, TextLabel


class CameraShakeDemo(Scene):
    """Shows simple camera shake effect."""

    def start(self):
        self.camera_shake = CameraShake(self)

        self.box = self.add(
            GameObject(
                x=260,
                y=540,
                width=200,
                height=200,
                color=(1.0, 0.45, 0.25, 1),
                name="shake_box",
            )
        )

        self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Camera Shake Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=80,
                y=1110,
                text="Tap anywhere to shake the screen.",
                font_size=27,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=120,
                y=460,
                text="Ready",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.camera_shake.shake(intensity=22, duration=0.35)
        self.message.set_text("Shake!")

    def update(self, dt):
        self.camera_shake.update(dt)
        super().update(dt)


if __name__ == "__main__":
    Game(title="Camera Shake Demo", width=720, height=1280).set_scene(
        CameraShakeDemo()
    ).run()
