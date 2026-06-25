from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel


class ScoreHighScoreDemo(Scene):
    """Tap the coin to increase score and save high score."""

    def start(self):
        self.score = ScoreManager(high_score_key="example_score_highscore")

        self.coin = self.add(
            GameObject(
                x=300,
                y=520,
                width=100,
                height=100,
                color=(1.0, 0.85, 0.15, 1),
                shape="circle",
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=40,
                y=1180,
                text="Score: 0",
                font_size=32,
                color=(1, 1, 1, 1),
            )
        )

        self.best_label = self.add(
            TextLabel(
                x=40,
                y=1135,
                text=f"Best: {self.score.high_score}",
                font_size=28,
                color=(0.8, 0.9, 1, 1),
            )
        )

        self.start_game()
        self.update_labels()

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")

    def on_tap(self, x, y):
        if self.coin.x <= x <= self.coin.x + self.coin.width and self.coin.y <= y <= self.coin.y + self.coin.height:
            self.score.add(1)
            self.update_labels()


if __name__ == "__main__":
    Game(title="Score Demo", width=720, height=1280).set_scene(
        ScoreHighScoreDemo()).run()
