from __future__ import annotations

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


class SwipeRunnerScene(Scene):
    def start(self):
        self.lanes = [150, 320, 490]
        self.current_lane = 1
        self.runner_speed = 420
        self.score_goal = 15
        self.game_over = False

        self.assets = AssetManager()
        self.score = ScoreManager(high_score_key="swipe_runner_high_score")
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
                color=(0.07, 0.09, 0.14, 1),
                shape="rect",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=45,
                y=1180,
                text="Swipe Runner",
                font_size=44,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.help_label = self.add(
            TextLabel(
                x=45,
                y=1125,
                text="Swipe left or right to change lanes and avoid obstacles.",
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

        self._create_lane_markers()

        self.player = self.add(
            GameObject(
                x=self.lanes[self.current_lane],
                y=170,
                width=90,
                height=90,
                color=(0.2, 0.75, 1.0, 1),
                shape="rect",
                image_path=None,
            )
        )

        self.player_label = self.add(
            TextLabel(
                x=self.player.x + 22,
                y=self.player.y + 28,
                text="P",
                font_size=28,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.obstacle = self.add(
            GameObject(
                x=self.lanes[0],
                y=1320,
                width=95,
                height=95,
                color=(1.0, 0.28, 0.28, 1),
                shape="rect",
            )
        )

        self.status_label = self.add(
            TextLabel(
                x=45,
                y=90,
                text="Ready. Swipe to move!",
                font_size=26,
                color=(0.8, 1, 0.85, 1),
            )
        )

        self.start_game()

    def _create_lane_markers(self):
        for lane_x in self.lanes:
            self.add(
                GameObject(
                    x=lane_x + 42,
                    y=130,
                    width=6,
                    height=900,
                    color=(0.2, 0.24, 0.34, 1),
                    shape="rect",
                )
            )

    def update(self, dt):
        if not self.game_over:
            self._update_obstacle(dt)
            self._check_collision()

        self.camera_shake.update(dt)
        self.particles.update(dt)
        super().update(dt)

    def on_swipe(self, start, end, direction):
        if self.game_over:
            self._restart()
            return

        if direction == "left":
            self._move_lane(-1)
        elif direction == "right":
            self._move_lane(1)

    def on_tap(self, x, y):
        if self.game_over:
            self._restart()
        else:
            self.status_label.set_text("Swipe left or right to move lanes.")

    def _move_lane(self, direction: int):
        old_lane = self.current_lane
        self.current_lane = max(
            0, min(len(self.lanes) - 1, self.current_lane + direction))

        if self.current_lane == old_lane:
            self.status_label.set_text("Edge lane reached.")
            return

        self.player.x = self.lanes[self.current_lane]
        self.player_label.x = self.player.x + 22
        self.status_label.set_text("Lane changed!")

        self.camera_shake.shake(intensity=4, duration=0.08)
        self.particles.burst(
            x=self.player.x + self.player.width / 2,
            y=self.player.y + self.player.height / 2,
            count=8,
        )

    def _update_obstacle(self, dt):
        self.obstacle.y -= self.runner_speed * dt

        if self.obstacle.y < -120:
            self._reset_obstacle()
            self._add_score()

    def _reset_obstacle(self):
        next_lane_index = (self.score.value + 1) % len(self.lanes)
        self.obstacle.x = self.lanes[next_lane_index]
        self.obstacle.y = 1320

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
                "Goal reached! Keep running for a new high score.")
        else:
            self.status_label.set_text("Obstacle avoided!")

    def _check_collision(self):
        overlaps_x = (
            self.player.x < self.obstacle.x + self.obstacle.width
            and self.player.x + self.player.width > self.obstacle.x
        )

        overlaps_y = (
            self.player.y < self.obstacle.y + self.obstacle.height
            and self.player.y + self.player.height > self.obstacle.y
        )

        if overlaps_x and overlaps_y:
            self._set_game_over()

    def _set_game_over(self):
        self.game_over = True
        self.player.color = (1, 0.25, 0.25, 1)
        self.status_label.set_text("Game over. Tap or swipe to restart.")
        self.camera_shake.shake(intensity=18, duration=0.35)

    def _restart(self):
        self.game_over = False
        self.current_lane = 1

        self.player.x = self.lanes[self.current_lane]
        self.player.y = 170
        self.player.color = (0.2, 0.75, 1.0, 1)
        self.player_label.x = self.player.x + 22
        self.player_label.y = self.player.y + 28

        self.obstacle.x = self.lanes[0]
        self.obstacle.y = 1320

        self.score.reset()
        self.score_label.set_text("Score: 0")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.progress_label.set_text(f"Goal Progress: 0 / {self.score_goal}")
        self.progress_bar.set_value(0)
        self.status_label.set_text("Ready. Swipe to move!")


if __name__ == "__main__":
    Game(
        title="HyperKit Swipe Runner",
        width=720,
        height=1280,
    ).set_scene(SwipeRunnerScene()).run()
