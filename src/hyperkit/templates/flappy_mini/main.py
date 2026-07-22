from __future__ import annotations
import random

from hyperkit import (
    AssetManager,
    BoundsManager,
    CameraShake,
    Game,
    GameObject,
    InputActionMap,
    ParticleEmitter,
    ProgressBar,
    Scene,
    ScoreManager,
    ScreenBounds,
    TextLabel,
)


class FlappyMiniScene(Scene):
    def start(self):
        self.gravity = -1450
        self.jump_force = 520
        self.bird_velocity = 0
        self.pipe_speed = 260
        self.pipe_gap = 320
        self.pipe_min_gap_center = 390
        self.pipe_max_gap_center = 760
        self.score_goal = 10
        self.game_over = False

        self.assets = AssetManager()
        self.score = ScoreManager(high_score_key="flappy_mini_high_score")
        self.camera_shake = CameraShake(self)
        self.particles = ParticleEmitter(self)
        self.bounds_manager = BoundsManager()
        self.screen_bounds = ScreenBounds(width=720, height=1280)
        self.input_actions = InputActionMap()

        self.background = self.add(
            GameObject(
                x=0,
                y=0,
                width=720,
                height=1280,
                color=(0.08, 0.14, 0.2, 1),
                shape="rect",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=45,
                y=1180,
                text="Flappy Mini",
                font_size=44,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.help_label = self.add(
            TextLabel(
                x=45,
                y=1125,
                text="Tap to jump. Stay inside the screen and pass the pipes.",
                font_size=22,
                color=(0.82, 0.9, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=45,
                y=1045,
                text="Score: 0",
                font_size=34,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.high_score_label = self.add(
            TextLabel(
                x=45,
                y=995,
                text=f"High Score: {self.score.high_score}",
                font_size=26,
                color=(0.95, 0.82, 0.3, 1),
            )
        )

        self.progress_label = self.add(
            TextLabel(
                x=45,
                y=920,
                text=f"Goal Progress: 0 / {self.score_goal}",
                font_size=24,
                color=(0.78, 0.92, 1, 1),
            )
        )

        self.progress_bar = ProgressBar(
            scene=self,
            x=45,
            y=875,
            width=630,
            height=30,
            value=0,
            max_value=self.score_goal,
        )

        self.bird = self.add(
            GameObject(
                x=170,
                y=610,
                width=72,
                height=72,
                color=(1.0, 0.82, 0.22, 1),
                shape="circle",
                image_path=None,
            )
        )

        self.bird_label = self.add(
            TextLabel(
                x=178,
                y=630,
                text="B",
                font_size=28,
                color=(0.08, 0.1, 0.16, 1),
                bold=True,
            )
        )

        self.pipe_top = self.add(
            GameObject(
                x=760,
                y=780,
                width=110,
                height=500,
                color=(0.25, 0.9, 0.45, 1),
                shape="rect",
            )
        )

        self.pipe_bottom = self.add(
            GameObject(
                x=760,
                y=0,
                width=110,
                height=420,
                color=(0.25, 0.9, 0.45, 1),
                shape="rect",
            )
        )

        self._randomize_pipe_gap()

        self.status_label = self.add(
            TextLabel(
                x=45,
                y=120,
                text="Ready. Tap to flap!",
                font_size=26,
                color=(0.8, 1, 0.85, 1),
            )
        )

        self.start_game()

    def update(self, dt):
        if not self.game_over:
            self._update_bird(dt)
            self._update_pipes(dt)
            self._check_collisions()

        self.camera_shake.update(dt)
        self.particles.update(dt)
        super().update(dt)

    def on_tap(self, x, y):
        if self.game_over:
            self._restart()
            return

        self.bird_velocity = self.jump_force
        self.status_label.set_text("Flap!")
        self.camera_shake.shake(intensity=4, duration=0.08)

        self.particles.burst(
            x=self.bird.x + self.bird.width / 2,
            y=self.bird.y + self.bird.height / 2,
            count=8,
        )

    def _update_bird(self, dt):
        self.bird_velocity += self.gravity * dt
        self.bird.y += self.bird_velocity * dt
        self.bird_label.x = self.bird.x + 22
        self.bird_label.y = self.bird.y + 20

    def _update_pipes(self, dt):
        self.pipe_top.x -= self.pipe_speed * dt
        self.pipe_bottom.x -= self.pipe_speed * dt

        if self.pipe_top.x < -130:
            self._reset_pipes()
            self._add_score()

    def _reset_pipes(self):
        self.pipe_top.x = 760
        self.pipe_bottom.x = 760
        self._randomize_pipe_gap()

    def _randomize_pipe_gap(self):
        gap_center = random.randint(
            self.pipe_min_gap_center,
            self.pipe_max_gap_center,
        )

        half_gap = self.pipe_gap / 2

        bottom_height = gap_center - half_gap
        top_y = gap_center + half_gap

        self.pipe_bottom.y = 0
        self.pipe_bottom.height = bottom_height

        self.pipe_top.y = top_y
        self.pipe_top.height = 1280 - top_y

    def _add_score(self):
        self.score.add(1)

        current_score = self.score.value
        progress_value = min(current_score, self.score_goal)

        self.score_label.set_text(f"Score: {current_score}")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.progress_label.set_text(
            f"Goal Progress: {progress_value} / {self.score_goal}"
        )
        self.progress_bar.set_value(progress_value)

        if current_score >= self.score_goal:
            self.status_label.set_text(
                "Goal reached! Keep flying for a new high score.")
        else:
            self.status_label.set_text("Nice! Pipe passed.")

    def _check_collisions(self):
        hit_ground = self.bird.y <= 0
        hit_ceiling = self.bird.y + self.bird.height >= 1280

        overlaps_pipe_x = (
            self.bird.x + self.bird.width > self.pipe_top.x
            and self.bird.x < self.pipe_top.x + self.pipe_top.width
        )

        hits_top_pipe = overlaps_pipe_x and (
            self.bird.y + self.bird.height > self.pipe_top.y
        )
        hits_bottom_pipe = overlaps_pipe_x and (
            self.bird.y < self.pipe_bottom.y + self.pipe_bottom.height
        )

        if hit_ground or hit_ceiling or hits_top_pipe or hits_bottom_pipe:
            self._set_game_over()

    def _set_game_over(self):
        self.game_over = True
        self.bird.color = (1, 0.25, 0.25, 1)
        self.status_label.set_text("Game over. Tap to restart.")
        self.camera_shake.shake(intensity=16, duration=0.35)

    def _restart(self):
        self.game_over = False
        self.bird.x = 170
        self.bird.y = 610
        self.bird_velocity = 0
        self.bird.color = (1.0, 0.82, 0.22, 1)

        self._reset_pipes()

        self.score.reset()
        self.score_label.set_text("Score: 0")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.progress_label.set_text(f"Goal Progress: 0 / {self.score_goal}")
        self.progress_bar.set_value(0)
        self.status_label.set_text("Ready. Tap to flap!")


if __name__ == "__main__":
    Game(
        title="HyperKit Flappy Mini",
        width=720,
        height=1280,
    ).set_scene(FlappyMiniScene()).run()
