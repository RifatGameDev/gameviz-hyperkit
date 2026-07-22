from __future__ import annotations

from hyperkit import (
    AssetManager,
    BoundsManager,
    CameraShake,
    Cooldown,
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


class SimplePhysicsScene(Scene):
    def start(self):
        self.gravity = -1400
        self.jump_force = 720
        self.ball_velocity_y = 0
        self.ball_velocity_x = 180
        self.bounce_strength = 0.72
        self.floor_y = 190
        self.score_goal = 10
        self.game_over = False

        self.assets = AssetManager()
        self.score = ScoreManager(high_score_key="simple_physics_high_score")
        self.camera_shake = CameraShake(self)
        self.particles = ParticleEmitter(self)
        self.bounds_manager = BoundsManager()
        self.screen_bounds = ScreenBounds(width=720, height=1280)
        self.input_actions = InputActionMap()
        self.force_cooldown = Cooldown(0.15)

        self.background = self.add(
            GameObject(
                x=0,
                y=0,
                width=720,
                height=1280,
                color=(0.07, 0.09, 0.14, 1),
                shape="rect",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=45,
                y=1180,
                text="Simple Physics",
                font_size=44,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.help_label = self.add(
            TextLabel(
                x=45,
                y=1125,
                text="Tap to push the ball upward. Keep it bouncing.",
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

        self.floor = self.add(
            GameObject(
                x=45,
                y=self.floor_y - 25,
                width=630,
                height=35,
                color=(0.22, 0.28, 0.4, 1),
                shape="rect",
            )
        )

        self.ball = self.add(
            GameObject(
                x=300,
                y=680,
                width=90,
                height=90,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
                image_path=None,
            )
        )

        self.ball_label = self.add(
            TextLabel(
                x=self.ball.x + 28,
                y=self.ball.y + 30,
                text="B",
                font_size=28,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.target = self.add(
            GameObject(
                x=500,
                y=700,
                width=85,
                height=85,
                color=(0.25, 1.0, 0.48, 1),
                shape="circle",
            )
        )

        self.target_label = self.add(
            TextLabel(
                x=self.target.x + 24,
                y=self.target.y + 28,
                text="+",
                font_size=34,
                color=(0.05, 0.08, 0.12, 1),
                bold=True,
            )
        )

        self.status_label = self.add(
            TextLabel(
                x=45,
                y=90,
                text="Ready. Tap to apply force!",
                font_size=26,
                color=(0.8, 1, 0.85, 1),
            )
        )

        self.start_game()

    def update(self, dt):
        if not self.game_over:
            self._update_ball(dt)
            self._check_floor_bounce()
            self._check_wall_bounce()
            self._check_target_hit()
            self._check_out_of_bounds()

        self.camera_shake.update(dt)
        self.particles.update(dt)
        super().update(dt)

    def on_tap(self, x, y):
        if self.game_over:
            self._restart()
            return

        self.ball_velocity_y = self.jump_force
        self.status_label.set_text("Force applied!")
        self.camera_shake.shake(intensity=4, duration=0.08)

        self.particles.burst(
            x=self.ball.x + self.ball.width / 2,
            y=self.ball.y + self.ball.height / 2,
            count=8,
        )

    def _update_ball(self, dt):
        self.ball_velocity_y += self.gravity * dt
        self.ball.x += self.ball_velocity_x * dt
        self.ball.y += self.ball_velocity_y * dt

        self.ball_label.x = self.ball.x + 28
        self.ball_label.y = self.ball.y + 30

    def _check_floor_bounce(self):
        if self.ball.y <= self.floor_y:
            self.ball.y = self.floor_y
            self.ball_velocity_y = abs(
                self.ball_velocity_y) * self.bounce_strength
            self._add_score()
            self.camera_shake.shake(intensity=7, duration=0.1)

    def _check_wall_bounce(self):
        if self.ball.x <= 45:
            self.ball.x = 45
            self.ball_velocity_x = abs(self.ball_velocity_x)

        if self.ball.x + self.ball.width >= 675:
            self.ball.x = 675 - self.ball.width
            self.ball_velocity_x = -abs(self.ball_velocity_x)

    def _check_target_hit(self):
        overlaps_x = (
            self.ball.x < self.target.x + self.target.width
            and self.ball.x + self.ball.width > self.target.x
        )

        overlaps_y = (
            self.ball.y < self.target.y + self.target.height
            and self.ball.y + self.ball.height > self.target.y
        )

        if overlaps_x and overlaps_y:
            self._move_target()
            self._add_score()
            self.status_label.set_text("Target hit! Nice physics control.")

    def _check_out_of_bounds(self):
        if self.ball.y > 1300:
            self._set_game_over("Ball escaped upward. Tap to restart.")

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
                "Goal reached! Keep bouncing for a new high score.")
            self.ball.color = (0.25, 1.0, 0.48, 1)

    def _move_target(self):
        next_x = 120 + (self.score.value * 85) % 460
        next_y = 450 + (self.score.value * 65) % 360

        self.target.x = next_x
        self.target.y = next_y
        self.target_label.x = self.target.x + 24
        self.target_label.y = self.target.y + 28

        self.particles.burst(
            x=self.target.x + self.target.width / 2,
            y=self.target.y + self.target.height / 2,
            count=12,
        )

    def _set_game_over(self, message: str):
        self.game_over = True
        self.ball.color = (1, 0.25, 0.25, 1)
        self.status_label.set_text(message)
        self.camera_shake.shake(intensity=16, duration=0.35)

    def _restart(self):
        self.game_over = False
        self.ball.x = 300
        self.ball.y = 680
        self.ball.color = (0.2, 0.75, 1.0, 1)

        self.ball_velocity_y = 0
        self.ball_velocity_x = 180

        self.target.x = 500
        self.target.y = 700
        self.target_label.x = self.target.x + 24
        self.target_label.y = self.target.y + 28

        self.score.reset()
        self.score_label.set_text("Score: 0")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.progress_label.set_text(f"Goal Progress: 0 / {self.score_goal}")
        self.progress_bar.set_value(0)
        self.status_label.set_text("Ready. Tap to apply force!")


if __name__ == "__main__":
    Game(
        title="HyperKit Simple Physics",
        width=720,
        height=1280,
    ).set_scene(SimplePhysicsScene()).run()
