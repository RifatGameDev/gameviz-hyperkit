from __future__ import annotations

from hyperkit import (
    AssetManager,
    BodyType,
    BoundsManager,
    CameraShake,
    Cooldown,
    Game,
    GameObject,
    InputActionMap,
    ParticleEmitter,
    PhysicsMaterial,
    PhysicsWorld,
    ProgressBar,
    Scene,
    ScoreManager,
    ScreenBounds,
    TextLabel,
)


PLAYER_LAYER = 1
WORLD_LAYER = 2
TARGET_LAYER = 4


class SimplePhysicsScene(Scene):
    def start(self):
        self.gravity = -1400
        self.jump_force = 720
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

        self.left_wall = self.add(
            GameObject(
                x=25,
                y=0,
                width=20,
                height=1280,
                visible=False,
            )
        )
        self.right_wall = self.add(
            GameObject(
                x=675,
                y=0,
                width=20,
                height=1280,
                visible=False,
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

        self.physics = PhysicsWorld(
            gravity_y=self.gravity,
        )
        bounce_material = PhysicsMaterial(
            restitution=self.bounce_strength,
            friction=0.0,
        )

        self.ball_body = self.physics.add_body(
            self.ball,
            body_type=BodyType.DYNAMIC,
            material=bounce_material,
            layer=PLAYER_LAYER,
            mask=WORLD_LAYER | TARGET_LAYER,
            on_collision=self._on_ball_collision,
            on_trigger=self._on_ball_trigger,
        )
        self.ball_body.set_velocity(180, 0)

        self.floor_body = self.physics.add_body(
            self.floor,
            body_type=BodyType.STATIC,
            material=bounce_material,
            layer=WORLD_LAYER,
            mask=PLAYER_LAYER,
        )
        self.left_wall_body = self.physics.add_body(
            self.left_wall,
            body_type=BodyType.STATIC,
            material=bounce_material,
            layer=WORLD_LAYER,
            mask=PLAYER_LAYER,
        )
        self.right_wall_body = self.physics.add_body(
            self.right_wall,
            body_type=BodyType.STATIC,
            material=bounce_material,
            layer=WORLD_LAYER,
            mask=PLAYER_LAYER,
        )
        self.target_body = self.physics.add_body(
            self.target,
            body_type=BodyType.STATIC,
            is_trigger=True,
            layer=TARGET_LAYER,
            mask=PLAYER_LAYER,
        )

        self.start_game()

    def update(self, dt):
        if not self.is_playing():
            return

        if not self.game_over:
            self.physics.step(dt)
            self._sync_ball_label()
            self._check_out_of_bounds()

        self.camera_shake.update(dt)
        self.particles.update(dt)

    def on_tap(self, x, y):
        if self.game_over:
            self._restart()
            return

        self.ball_body.set_velocity(
            self.ball.vx,
            self.jump_force,
        )
        self.status_label.set_text("Force applied!")
        self.camera_shake.shake(intensity=4, duration=0.08)

        self.particles.burst(
            x=self.ball.x + self.ball.width / 2,
            y=self.ball.y + self.ball.height / 2,
            count=8,
        )

    def _on_ball_collision(self, other, _manifold):
        if other is self.floor_body:
            self._add_score()
            self.camera_shake.shake(
                intensity=7,
                duration=0.1,
            )

    def _on_ball_trigger(self, other, _manifold):
        if other is not self.target_body:
            return

        self._move_target()
        self._add_score()
        self.status_label.set_text(
            "Target hit! HyperKit physics handled the trigger."
        )

    def _sync_ball_label(self):
        self.ball_label.x = self.ball.x + 28
        self.ball_label.y = self.ball.y + 30

    def _check_out_of_bounds(self):
        if self.ball.y > 1300:
            self._set_game_over(
                "Ball escaped upward. Tap to restart."
            )

    def _add_score(self):
        self.score.add(1)

        current_score = self.score.value
        progress_value = min(
            current_score,
            self.score_goal,
        )

        self.score_label.set_text(
            f"Score: {current_score}"
        )
        self.high_score_label.set_text(
            f"High Score: {self.score.high_score}"
        )
        self.progress_label.set_text(
            f"Goal Progress: {progress_value} / {self.score_goal}"
        )
        self.progress_bar.set_value(
            progress_value
        )

        if current_score >= self.score_goal:
            self.status_label.set_text(
                "Goal reached! Keep bouncing for a new high score."
            )
            self.ball.color = (
                0.25,
                1.0,
                0.48,
                1,
            )

    def _move_target(self):
        next_x = (
            120
            + (self.score.value * 85) % 460
        )
        next_y = (
            450
            + (self.score.value * 65) % 360
        )

        self.target.x = next_x
        self.target.y = next_y
        self.target_label.x = (
            self.target.x + 24
        )
        self.target_label.y = (
            self.target.y + 28
        )

        self.particles.burst(
            x=self.target.x + self.target.width / 2,
            y=self.target.y + self.target.height / 2,
            count=12,
        )

    def _set_game_over(self, message: str):
        self.game_over = True
        self.ball.color = (
            1,
            0.25,
            0.25,
            1,
        )
        self.status_label.set_text(message)
        self.camera_shake.shake(
            intensity=16,
            duration=0.35,
        )

    def _restart(self):
        self.game_over = False
        self.ball.x = 300
        self.ball.y = 680
        self.ball.color = (
            0.2,
            0.75,
            1.0,
            1,
        )
        self.ball_body.set_velocity(
            180,
            0,
        )
        self._sync_ball_label()

        self.target.x = 500
        self.target.y = 700
        self.target_label.x = (
            self.target.x + 24
        )
        self.target_label.y = (
            self.target.y + 28
        )

        self.score.reset()
        self.score_label.set_text(
            "Score: 0"
        )
        self.high_score_label.set_text(
            f"High Score: {self.score.high_score}"
        )
        self.progress_label.set_text(
            f"Goal Progress: 0 / {self.score_goal}"
        )
        self.progress_bar.set_value(0)
        self.status_label.set_text(
            "Ready. Tap to apply force!"
        )


if __name__ == "__main__":
    Game(
        title="HyperKit Simple Physics",
        width=720,
        height=1280,
    ).set_scene(
        SimplePhysicsScene()
    ).run()
