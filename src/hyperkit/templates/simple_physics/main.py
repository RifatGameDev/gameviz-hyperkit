from pathlib import Path
import struct
import zlib

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
    ScreenBounds,
    TextLabel,
)


def save_demo_png(path: Path, color: tuple[int, int, int, int]) -> None:
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

    ball_path = images_path / "physics_ball.png"

    if not ball_path.exists():
        save_demo_png(ball_path, (70, 180, 255, 255))


class SimplePhysicsScene(Scene):
    """Modern simple physics template using HyperKit helpers."""

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280

        project_path = Path(__file__).parent
        ensure_template_assets(project_path)

        self.assets = AssetManager(project_path=project_path)
        self.particles = ParticleEmitter(self)
        self.camera_shake = CameraShake(self)
        self.bounds = BoundsManager(
            screen=ScreenBounds(width=self.screen_width,
                                height=self.screen_height)
        )
        self.actions = InputActionMap()
        self.launch_cooldown = Cooldown(duration=0.4)

        self.gravity = -1200
        self.energy = 100

        self.ball = self.add(
            GameObject(
                x=310,
                y=760,
                width=100,
                height=100,
                vx=260,
                vy=0,
                image_path=self.assets.load_image("physics_ball.png"),
                shape="circle",
                name="physics_ball",
            )
        )

        self.ground = self.add(
            GameObject(
                x=0,
                y=240,
                width=720,
                height=50,
                color=(0.25, 0.9, 0.35, 1),
                name="ground",
            )
        )

        self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Simple Physics",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.energy_bar = ProgressBar(
            scene=self,
            x=60,
            y=1090,
            width=600,
            height=32,
            value=self.energy,
            max_value=100,
            fill_color=(0.25, 0.75, 1.0, 1),
            text_format="Energy: {value:.0f}/{max_value:.0f}",
            name="physics_energy",
        )

        self.message_label = self.add(
            TextLabel(
                x=60,
                y=1015,
                text="Tap to launch the ball upward.",
                font_size=26,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.actions.map_tap("launch", callback=self.launch_ball)

        self.start_game()

    def launch_ball(self, event):
        if not self.launch_cooldown.use():
            self.message_label.set_text(
                f"Cooldown: {self.launch_cooldown.remaining:.1f}s"
            )
            return

        x = float(event.x or self.ball.x)
        y = float(event.y or self.ball.y)

        self.ball.x = x - self.ball.width / 2
        self.bounds.keep_on_screen(self.ball)

        self.ball.vy = 780
        self.energy = max(0, self.energy - 10)
        self.energy_bar.set_value(self.energy)

        self.message_label.set_text("Launch!")
        self.camera_shake.shake(intensity=6, duration=0.08)

        self.particles.burst(
            x=self.ball.x + self.ball.width / 2,
            y=self.ball.y,
            count=18,
            color=(1.0, 0.85, 0.2, 1),
            lifetime=0.45,
            gravity=-300,
        )

    def on_tap(self, x, y):
        self.actions.handle_tap(x, y)

    def update(self, dt):
        self.ball.vy += self.gravity * dt
        self.ball.x += self.ball.vx * dt
        self.ball.y += self.ball.vy * dt

        if self.ball.y <= self.ground.y + self.ground.height:
            self.ball.y = self.ground.y + self.ground.height
            self.ball.vy = abs(self.ball.vy) * 0.65

            if self.ball.vy > 80:
                self.camera_shake.shake(intensity=7, duration=0.08)
                self.particles.burst(
                    x=self.ball.x + self.ball.width / 2,
                    y=self.ball.y,
                    count=10,
                    color=(0.8, 0.8, 0.8, 1),
                    lifetime=0.3,
                    gravity=-200,
                )

        self.bounds.bounce_on_screen(self.ball, bounce=1.0)

        self.launch_cooldown.update(dt)
        self.particles.update(dt)
        self.camera_shake.update(dt)

        if self.energy < 100:
            self.energy = min(100, self.energy + 8 * dt)
            self.energy_bar.set_value(self.energy)

        super().update(dt)


if __name__ == "__main__":
    Game(title="Simple Physics", width=720, height=1280).set_scene(
        SimplePhysicsScene()
    ).run()
