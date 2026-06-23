from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel


class TapCounterScene(Scene):
    """Tap Counter game template.

    Goal:
    - Tap/click anywhere to move the ball.
    - Each tap increases score.
    - Reach target score to finish the round.
    - Tap again after game over to restart.
    """

    def start(self):
        self.target_score = 20
        self.score = ScoreManager(high_score_key="tap_counter_high_score")

        self.player = self.add(
            GameObject(
                x=300,
                y=520,
                width=120,
                height=120,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
                name="tap_ball",
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=30,
                y=1180,
                text="Score: 0",
                font_size=32,
                color=(1, 1, 1, 1),
            )
        )

        self.best_label = self.add(
            TextLabel(
                x=30,
                y=1135,
                text=f"Best: {self.score.high_score}",
                font_size=28,
                color=(0.8, 0.9, 1, 1),
            )
        )

        self.message_label = self.add(
            TextLabel(
                x=120,
                y=1020,
                text=f"Tap the circle! Target: {self.target_score}",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.start_game()
        self.update_labels()

    def reset_round(self):
        self.score.reset_score()
        self.player.x = 300
        self.player.y = 520
        self.player.color = (0.2, 0.75, 1.0, 1)
        self.start_game()
        self.message_label.set_text(
            f"Tap the circle! Target: {self.target_score}")
        self.update_labels()

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        if not self.is_playing():
            return

        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2

        self.score.add(1)
        self.update_labels()

        if self.score.value >= self.target_score:
            self.player.color = (0.2, 1.0, 0.45, 1)
            self.end_game()
            self.message_label.set_text("Game Over! Tap anywhere to restart.")


if __name__ == "__main__":
    Game(title="Tap Counter", width=720, height=1280).set_scene(
        TapCounterScene()).run()
