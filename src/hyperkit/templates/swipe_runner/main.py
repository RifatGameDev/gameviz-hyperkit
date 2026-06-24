from random import choice, randint

from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel


class SwipeRunnerScene(Scene):
    """Swipe Runner game template.

    Goal:
    - Swipe left/right to change lanes.
    - Avoid incoming obstacles.
    - Score increases while surviving.
    - Game gets faster over time.
    - Tap after game over to restart.
    """

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280

        self.lanes = [160, 330, 500]
        self.current_lane = 1

        self.obstacles = []
        self.spawn_timer = 0.0
        self.spawn_interval = 1.1
        self.score_timer = 0.0

        self.base_speed = -420
        self.current_speed = self.base_speed
        self.max_speed = -850

        self.score = ScoreManager(high_score_key="swipe_runner_high_score")

        self.player = self.add(
            GameObject(
                x=self.lanes[self.current_lane],
                y=150,
                width=90,
                height=90,
                color=(0.2, 0.75, 1.0, 1),
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
                x=115,
                y=1040,
                text="Swipe left/right to avoid obstacles!",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.start_game()
        self.update_labels()

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")

    def move_to_lane(self):
        self.player.x = self.lanes[self.current_lane]

    def on_swipe(self, start, end, direction):
        if not self.is_playing():
            return

        if direction == "left":
            self.current_lane = max(0, self.current_lane - 1)
        elif direction == "right":
            self.current_lane = min(len(self.lanes) - 1, self.current_lane + 1)

        self.move_to_lane()
        self.message_label.set_text("")

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()

    def spawn_obstacle(self):
        lane_index = randint(0, len(self.lanes) - 1)

        obstacle = self.add(
            GameObject(
                x=self.lanes[lane_index],
                y=self.screen_height + 120,
                width=95,
                height=95,
                vy=self.current_speed,
                color=choice(
                    [
                        (1.0, 0.25, 0.25, 1),
                        (1.0, 0.45, 0.15, 1),
                        (0.9, 0.1, 0.45, 1),
                    ]
                ),
                name="obstacle",
            )
        )

        self.obstacles.append(obstacle)

    def update_score(self, dt):
        self.score_timer += dt

        if self.score_timer >= 0.25:
            self.score_timer = 0
            self.score.add(1)
            self.update_labels()

    def increase_difficulty(self):
        if self.current_speed > self.max_speed:
            self.current_speed -= 0.35

        self.spawn_interval = max(0.55, self.spawn_interval - 0.0007)

    def update_obstacles(self):
        for obstacle in list(self.obstacles):
            if obstacle.y < -150:
                self.obstacles.remove(obstacle)
                self.remove(obstacle)

    def check_collision(self):
        for obstacle in self.obstacles:
            if self.player.collides_with(obstacle):
                self.game_over()
                return

    def update(self, dt):
        if not self.is_playing():
            return

        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_obstacle()

        self.update_score(dt)
        self.increase_difficulty()

        super().update(dt)

        self.update_obstacles()
        self.check_collision()

    def game_over(self):
        self.end_game()

        self.player.color = (1.0, 0.25, 0.25, 1)

        for obstacle in self.obstacles:
            obstacle.vy = 0

        self.update_labels()
        self.message_label.set_text("Game Over! Tap anywhere to restart.")

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Swipe Runner", width=720, height=1280).set_scene(
        SwipeRunnerScene()).run()
