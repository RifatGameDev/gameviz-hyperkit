from random import randint

from hyperkit import Game, GameObject, Scene, ScoreManager, apply_gravity


class FlappyMiniScene(Scene):
    def start(self):
        self.score = ScoreManager()
        self.gravity = -1800
        self.jump_force = 650
        self.pipe_speed = -250
        self.player = self.add(
            GameObject(x=120, y=650, width=64, height=64, color=(1, 0.85, 0.2, 1), shape="circle", name="player")
        )
        self.spawn_pipe()

    def spawn_pipe(self):
        gap_y = randint(360, 880)
        gap_size = 260
        self.top_pipe = self.add(
            GameObject(x=760, y=gap_y + gap_size / 2, width=90, height=1280, color=(0.1, 0.8, 0.25, 1), name="top_pipe")
        )
        self.bottom_pipe = self.add(
            GameObject(x=760, y=-1280 + gap_y - gap_size / 2, width=90, height=1280, color=(0.1, 0.8, 0.25, 1), name="bottom_pipe")
        )
        self.top_pipe.vx = self.pipe_speed
        self.bottom_pipe.vx = self.pipe_speed

    def on_tap(self, x, y):
        self.player.vy = self.jump_force

    def update(self, dt):
        self.player.vy = apply_gravity(self.player.vy, self.gravity, dt)
        super().update(dt)

        if self.top_pipe.x < -120:
            self.remove(self.top_pipe)
            self.remove(self.bottom_pipe)
            self.spawn_pipe()
            self.score.add(1)
            print(f"Score: {self.score.score} | Best: {self.score.high_score}")

        if self.player.y < 0 or self.player.y > 1280:
            self.reset_game()

        if self.player.collides_with(self.top_pipe) or self.player.collides_with(self.bottom_pipe):
            self.reset_game()

    def reset_game(self):
        print("Game over")
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Flappy Mini", width=720, height=1280).set_scene(FlappyMiniScene()).run()
