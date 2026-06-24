from random import randint

from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel


class SimplePhysicsScene(Scene):
    """Simple Physics game template.

    Goal:
    - Tap/click to launch the ball upward.
    - Gravity pulls the ball down.
    - Ball bounces on walls and floor.
    - Collect coins to score.
    - Reach target score to win.
    - Tap after game over/win to restart.
    """

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280

        self.gravity = -1600
        self.bounce_factor = 0.75
        self.jump_force = 850
        self.target_score = 10

        self.score = ScoreManager(high_score_key="simple_physics_high_score")

        self.ball = self.add(
            GameObject(
                x=320,
                y=450,
                width=80,
                height=80,
                vx=180,
                vy=0,
                color=(0.25, 0.75, 1.0, 1),
                shape="circle",
                name="physics_ball",
            )
        )

        self.floor = self.add(
            GameObject(
                x=0,
                y=70,
                width=720,
                height=35,
                color=(0.25, 0.9, 0.35, 1),
                name="floor",
            )
        )

        self.coin = self.add(
            GameObject(
                x=randint(80, 560),
                y=randint(350, 980),
                width=55,
                height=55,
                color=(1.0, 0.85, 0.15, 1),
                shape="circle",
                name="coin",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=70,
                y=1180,
                text="Simple Physics",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=30,
                y=1125,
                text="Score: 0",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.best_label = self.add(
            TextLabel(
                x=30,
                y=1085,
                text=f"Best: {self.score.high_score}",
                font_size=26,
                color=(0.8, 0.9, 1, 1),
            )
        )

        self.message_label = self.add(
            TextLabel(
                x=90,
                y=1010,
                text="Tap to launch. Collect coins!",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.start_game()
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

        self.ball.vy = self.jump_force

        if x < self.ball.x:
            self.ball.vx = -260
        elif x > self.ball.x + self.ball.width:
            self.ball.vx = 260

        self.message_label.set_text("")

    def update(self, dt):
        if not self.is_playing():
            return

        self.ball.vy += self.gravity * dt

        super().update(dt)

        self.handle_wall_bounce()
        self.handle_floor_bounce()
        self.handle_coin_collection()

    def handle_wall_bounce(self):
        if self.ball.x <= 0:
            self.ball.x = 0
            self.ball.vx = abs(self.ball.vx)

        if self.ball.x + self.ball.width >= self.screen_width:
            self.ball.x = self.screen_width - self.ball.width
            self.ball.vx = -abs(self.ball.vx)

        if self.ball.y + self.ball.height >= self.screen_height:
            self.ball.y = self.screen_height - self.ball.height
            self.ball.vy = -abs(self.ball.vy) * self.bounce_factor

    def handle_floor_bounce(self):
        floor_top = self.floor.y + self.floor.height

        if self.ball.y <= floor_top:
            self.ball.y = floor_top
            self.ball.vy = abs(self.ball.vy) * self.bounce_factor

            if abs(self.ball.vy) < 120:
                self.ball.vy = 0

    def handle_coin_collection(self):
        if self.ball.collides_with(self.coin):
            self.score.add(1)
            self.update_labels()
            self.move_coin()

            if self.score.value >= self.target_score:
                self.win_game()

    def move_coin(self):
        self.coin.x = randint(80, 560)
        self.coin.y = randint(280, 1000)

    def win_game(self):
        self.end_game()
        self.ball.vx = 0
        self.ball.vy = 0
        self.ball.color = (0.2, 1.0, 0.45, 1)
        self.message_label.set_text("You won! Tap anywhere to restart.")

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Simple Physics", width=720, height=1280).set_scene(
        SimplePhysicsScene()).run()
