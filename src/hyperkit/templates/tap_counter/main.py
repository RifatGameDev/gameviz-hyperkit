from hyperkit import Game, GameObject, Scene, ScoreManager


class TapCounterScene(Scene):
    def start(self):
        self.score = ScoreManager()
        self.player = self.add(
            GameObject(
                x=320,
                y=560,
                width=120,
                height=120,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
                name="tap_ball",
            )
        )

    def on_tap(self, x, y):
        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2
        self.score.add(1)
        print(f"Score: {self.score.score} | Best: {self.score.high_score}")


if __name__ == "__main__":
    Game(title="Tap Counter", width=720, height=1280).set_scene(TapCounterScene()).run()
