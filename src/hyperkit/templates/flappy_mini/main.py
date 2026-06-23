from random import randint

from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel, apply_gravity


class FlappyMiniScene(Scene):
    """Flappy Mini game template.

    Goal:
    - Tap/click to jump.
    - Avoid pipes.
    - Score increases when passing pipes.
    - Game over when hitting pipe or screen boundary.
    - Tap again after game over to restart.
    """

    def start(self):
        self.gravity = -1800
        self.jump_force = 680
        self.pipe_speed = -260
        self.gap_size = 280
        self.screen_width = 720
        self.screen_height = 1280

        self.score = ScoreManager(high_score_key="flappy_mini_high_score")

        self.player = self.add(
            GameObject(
                x=120,
                y=640,
                width=64,
                height=64,
                color=(1.0, 0.85, 0.2, 1),
                shape="circle",
                name="player",
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
                y=1040,
                text="Tap to fly. Avoid pipes!",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.top_pipe = None
        self.bottom_pipe = None

        self.spawn_pipe()
        self.start_game()
        self.update_labels()

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")

    def spawn_pipe(self):
        gap_center_y = randint(360, 900)

        self.top_pipe = self.add(
            GameObject(
                x=760,
                y=gap_center_y + self.gap_size / 2,
                width=95,
                height=1280,
                vx=self.pipe_speed,
                color=(0.1, 0.8, 0.25, 1),
                name="top_pipe",
            )
        )

        self.bottom_pipe = self.add(
            GameObject(
                x=760,
                y=gap_center_y - self.gap_size / 2 - 1280,
                width=95,
                height=1280,
                vx=self.pipe_speed,
                color=(0.1, 0.8, 0.25, 1),
                name="bottom_pipe",
            )
        )

        self.top_pipe.data["scored"] = False

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        if not self.is_playing():
            return

        self.player.vy = self.jump_force
        self.message_label.set_text("")

    def update(self, dt):
        if not self.is_playing():
            return

        self.player.vy = apply_gravity(self.player.vy, self.gravity, dt)

        super().update(dt)

        self.check_score()
        self.check_pipe_reset()
        self.check_game_over()

    def check_score(self):
        if self.top_pipe is None:
            return

        pipe_passed_player = self.top_pipe.x + self.top_pipe.width < self.player.x

        if pipe_passed_player and not self.top_pipe.data.get("scored", False):
            self.top_pipe.data["scored"] = True
            self.score.add(1)
            self.update_labels()

    def check_pipe_reset(self):
        if self.top_pipe is None or self.bottom_pipe is None:
            return

        if self.top_pipe.x < -140:
            self.remove(self.top_pipe)
            self.remove(self.bottom_pipe)
            self.spawn_pipe()

    def check_game_over(self):
        if self.top_pipe is None or self.bottom_pipe is None:
            return

        out_of_screen = self.player.y < 0 or self.player.y + \
            self.player.height > self.screen_height
        hit_pipe = self.player.collides_with(
            self.top_pipe) or self.player.collides_with(self.bottom_pipe)

        if out_of_screen or hit_pipe:
            self.game_over()

    def game_over(self):
        self.end_game()

        self.player.vy = 0
        self.player.color = (1.0, 0.25, 0.25, 1)

        if self.top_pipe:
            self.top_pipe.vx = 0

        if self.bottom_pipe:
            self.bottom_pipe.vx = 0

        self.update_labels()
        self.message_label.set_text("Game Over! Tap anywhere to restart.")

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Flappy Mini", width=720, height=1280).set_scene(
        FlappyMiniScene()).run()
