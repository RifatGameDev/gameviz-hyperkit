from hyperkit import Game, GameObject, Scene, SceneTransition, TextLabel


class FirstScene(Scene):
    def start(self):
        self.transition = SceneTransition(self)
        self.transition.fade_in(duration=0.4)

        self.add(
            TextLabel(
                x=90,
                y=1180,
                text="Scene Transition Demo",
                font_size=34,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=110,
                y=1050,
                text="First Scene",
                font_size=38,
                bold=True,
                color=(0.9, 0.9, 1, 1),
            )
        )

        self.add(
            GameObject(
                x=260,
                y=560,
                width=200,
                height=200,
                color=(0.2, 0.6, 1.0, 1),
                name="first_scene_box",
            )
        )

        self.message = self.add(
            TextLabel(
                x=80,
                y=460,
                text="Tap anywhere to go to Second Scene",
                font_size=26,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.message.set_text("Changing scene...")
        self.transition.fade_to_scene(SecondScene(), duration=0.4)

    def update(self, dt):
        self.transition.update(dt)
        super().update(dt)


class SecondScene(Scene):
    def start(self):
        self.transition = SceneTransition(self)
        self.transition.fade_in(duration=0.4)

        self.add(
            TextLabel(
                x=90,
                y=1180,
                text="Scene Transition Demo",
                font_size=34,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=90,
                y=1050,
                text="Second Scene",
                font_size=38,
                bold=True,
                color=(0.9, 1, 0.9, 1),
            )
        )

        self.add(
            GameObject(
                x=260,
                y=560,
                width=200,
                height=200,
                color=(0.2, 1.0, 0.45, 1),
                name="second_scene_box",
            )
        )

        self.message = self.add(
            TextLabel(
                x=90,
                y=460,
                text="Tap anywhere to go back to First Scene",
                font_size=26,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.message.set_text("Changing scene...")
        self.transition.fade_to_scene(FirstScene(), duration=0.4)

    def update(self, dt):
        self.transition.update(dt)
        super().update(dt)


if __name__ == "__main__":
    Game(title="Scene Transition Demo", width=720, height=1280).set_scene(
        FirstScene()
    ).run()
