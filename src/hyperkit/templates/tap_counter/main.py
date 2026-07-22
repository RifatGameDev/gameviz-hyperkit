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


class TapCounterScene(Scene):
    def start(self):
        self.tap_goal = 30

        self.assets = AssetManager()
        self.score = ScoreManager(high_score_key="tap_counter_high_score")
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
                color=(0.08, 0.1, 0.16, 1),
                shape="rect",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=45,
                y=1180,
                text="Tap Counter",
                font_size=44,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.help_label = self.add(
            TextLabel(
                x=45,
                y=1125,
                text="Tap anywhere to move the target and increase your score.",
                font_size=22,
                color=(0.82, 0.86, 0.95, 1),
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
                y=915,
                text=f"Goal Progress: 0 / {self.tap_goal}",
                font_size=24,
                color=(0.78, 0.92, 1, 1),
            )
        )

        self.progress_bar = ProgressBar(
            scene=self,
            x=45,
            y=870,
            width=630,
            height=32,
            value=0,
            max_value=self.tap_goal,
        )

        self.target = self.add(
            GameObject(
                x=300,
                y=520,
                width=120,
                height=120,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
                image_path=None,
            )
        )

        self.target_label = self.add(
            TextLabel(
                x=285,
                y=560,
                text="TAP",
                font_size=28,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.status_label = self.add(
            TextLabel(
                x=45,
                y=120,
                text="Ready. Start tapping!",
                font_size=26,
                color=(0.8, 1, 0.85, 1),
            )
        )

        self.start_game()

    def update(self, dt):
        self.camera_shake.update(dt)
        self.particles.update(dt)
        super().update(dt)

    def on_tap(self, x, y):
        self.score.add(1)

        self.target.x = x - self.target.width / 2
        self.target.y = y - self.target.height / 2
        self.screen_bounds.clamp_object(self.target)

        self.target_label.x = self.target.x + 35
        self.target_label.y = self.target.y + 40

        current_score = self.score.value
        progress_value = min(current_score, self.tap_goal)

        self.score_label.set_text(f"Score: {current_score}")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.progress_label.set_text(
            f"Goal Progress: {progress_value} / {self.tap_goal}"
        )
        self.progress_bar.set_value(progress_value)

        self.camera_shake.shake(intensity=8, duration=0.15)
        self.particles.burst(
            x=self.target.x + self.target.width / 2,
            y=self.target.y + self.target.height / 2,
            count=10,
        )

        if current_score >= self.tap_goal:
            self.status_label.set_text(
                "Goal reached! Keep tapping for a new high score.")
            self.target.color = (0.3, 1.0, 0.55, 1)
        elif current_score >= self.tap_goal // 2:
            self.status_label.set_text("Nice progress. You are halfway there!")
            self.target.color = (1.0, 0.65, 0.2, 1)
        else:
            self.status_label.set_text("Good tap! Keep going.")
            self.target.color = (0.2, 0.75, 1.0, 1)


if __name__ == "__main__":
    Game(
        title="HyperKit Tap Counter",
        width=720,
        height=1280,
    ).set_scene(TapCounterScene()).run()
