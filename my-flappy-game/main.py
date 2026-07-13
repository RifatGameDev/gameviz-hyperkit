from pathlib import Path
import random
import struct
import zlib

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


def save_demo_png(path: Path, color: tuple[int, int, int, int]) -> None:
    """Create a small colored PNG using only Python standard library."""
    width = 32
    height = 32

    raw = b"".join(b"\x00" + bytes(color) * width for _ in range(height))
    compressed = zlib.compress(raw)

    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + chunk_type
            + data
            + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
        )

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB",
                 width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", compressed)
    png += chunk(b"IEND", b"")

    path.write_bytes(png)


def ensure_template_assets(project_path: Path) -> None:
    images_path = project_path / "assets" / "images"
    images_path.mkdir(parents=True, exist_ok=True)

    bird_path = images_path / "bird.png"
    pipe_path = images_path / "pipe.png"

    if not bird_path.exists():
        save_demo_png(bird_path, (255, 215, 60, 255))

    if not pipe_path.exists():
        save_demo_png(pipe_path, (70, 220, 100, 255))


def rects_overlap(a: GameObject, b: GameObject) -> bool:
    return not (
        a.x + a.width < b.x
        or a.x > b.x + b.width
        or a.y + a.height < b.y
        or a.y > b.y + b.height
    )


class FlappyMiniScene(Scene):
    """Modern Flappy Mini template using HyperKit helpers."""

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280
        self.target_score = 10

        project_path = Path(__file__).parent
        ensure_template_assets(project_path)

        self.assets = AssetManager(project_path=project_path)
        self.score = ScoreManager(high_score_key="flappy_mini_high_score")
        self.particles = ParticleEmitter(self)
        self.camera_shake = CameraShake(self)
        self.bounds = BoundsManager(
            screen=ScreenBounds(width=self.screen_width,
                                height=self.screen_height)
        )
        self.actions = InputActionMap()

        self.gravity = -1800
        self.flap_power = 620
        self.bird_velocity = 0
        self.pipe_speed = 240
        self.pipe_gap = 300
        self.pipe_width = 110
        self.pipe_scored = False

        self.bird = self.add(
            GameObject(
                x=150,
                y=640,
                width=90,
                height=90,
                image_path=self.assets.load_image("bird.png"),
                name="bird",
            )
        )

        self.bottom_pipe = self.add(
            GameObject(
                x=760,
                y=0,
                width=self.pipe_width,
                height=420,
                image_path=self.assets.load_image("pipe.png"),
                name="bottom_pipe",
            )
        )

        self.top_pipe = self.add(
            GameObject(
                x=760,
                y=860,
                width=self.pipe_width,
                height=420,
                image_path=self.assets.load_image("pipe.png"),
                name="top_pipe",
            )
        )

        self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Flappy Mini",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=50,
                y=1125,
                text="Score: 0",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.best_label = self.add(
            TextLabel(
                x=50,
                y=1085,
                text=f"Best: {self.score.high_score}",
                font_size=26,
                color=(0.8, 0.9, 1, 1),
            )
        )

        self.progress_bar = ProgressBar(
            scene=self,
            x=60,
            y=1015,
            width=600,
            height=32,
            value=0,
            max_value=self.target_score,
            fill_color=(0.25, 0.75, 1.0, 1),
            text_format="Target: {value:.0f}/{max_value:.0f}",
            name="flappy_progress",
        )

        self.message_label = self.add(
            TextLabel(
                x=70,
                y=940,
                text="Tap to flap!",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.actions.map_tap("flap", callback=self.flap)

        self.reset_pipes()
        self.start_game()
        self.update_labels()

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")
        self.progress_bar.set_value(self.score.value)

    def reset_pipes(self):
        gap_center = random.randint(430, 850)

        bottom_height = gap_center - self.pipe_gap / 2
        top_y = gap_center + self.pipe_gap / 2
        top_height = self.screen_height - top_y

        self.bottom_pipe.x = 760
        self.bottom_pipe.y = 0
        self.bottom_pipe.height = max(120, bottom_height)

        self.top_pipe.x = 760
        self.top_pipe.y = top_y
        self.top_pipe.height = max(120, top_height)

        self.pipe_scored = False

    def flap(self, event):
        if not self.is_playing():
            return

        self.bird_velocity = self.flap_power
        self.message_label.set_text("Flap!")

        self.particles.burst(
            x=self.bird.x,
            y=self.bird.y + self.bird.height / 2,
            count=8,
            color=(1.0, 0.85, 0.2, 1),
            lifetime=0.3,
            gravity=-200,
        )

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        self.actions.handle_tap(x, y)

    def update(self, dt):
        if self.is_playing():
            self.bird_velocity += self.gravity * dt
            self.bird.y += self.bird_velocity * dt

            self.bottom_pipe.x -= self.pipe_speed * dt
            self.top_pipe.x -= self.pipe_speed * dt

            if self.bottom_pipe.x + self.bottom_pipe.width < 0:
                self.reset_pipes()

            if not self.pipe_scored and self.bottom_pipe.x + self.bottom_pipe.width < self.bird.x:
                self.pipe_scored = True
                self.score.add(1)
                self.update_labels()
                self.message_label.set_text("Point!")
                self.camera_shake.shake(intensity=4, duration=0.06)

                self.particles.burst(
                    x=self.bird.x + self.bird.width / 2,
                    y=self.bird.y + self.bird.height / 2,
                    count=14,
                    color=(0.2, 1.0, 0.45, 1),
                    lifetime=0.45,
                    gravity=-300,
                )

            if (
                self.bounds.is_outside_screen(self.bird)
                or rects_overlap(self.bird, self.bottom_pipe)
                or rects_overlap(self.bird, self.top_pipe)
            ):
                self.game_over()

            if self.score.value >= self.target_score:
                self.complete_round()

        self.particles.update(dt)
        self.camera_shake.update(dt)
        super().update(dt)

    def game_over(self):
        self.end_game()
        self.camera_shake.shake(intensity=18, duration=0.25)
        self.message_label.set_text("Game Over! Tap to restart.")

        self.particles.burst(
            x=self.bird.x + self.bird.width / 2,
            y=self.bird.y + self.bird.height / 2,
            count=28,
            color=(1.0, 0.25, 0.25, 1),
            lifetime=0.7,
        )

    def complete_round(self):
        self.end_game()
        self.camera_shake.shake(intensity=18, duration=0.25)
        self.message_label.set_text("Target reached! Tap to restart.")

        self.particles.burst(
            x=self.bird.x + self.bird.width / 2,
            y=self.bird.y + self.bird.height / 2,
            count=36,
            color=(0.2, 1.0, 0.45, 1),
            lifetime=0.8,
        )

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Flappy Mini", width=720, height=1280).set_scene(
        FlappyMiniScene()
    ).run()
