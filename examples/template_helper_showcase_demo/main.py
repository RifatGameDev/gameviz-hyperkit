from pathlib import Path
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


def ensure_assets(project_path: Path) -> None:
    images_path = project_path / "assets" / "images"
    images_path.mkdir(parents=True, exist_ok=True)

    player_path = images_path / "showcase_player.png"

    if not player_path.exists():
        save_demo_png(player_path, (80, 170, 255, 255))


class TemplateHelperShowcaseDemo(Scene):
    """Shows helper systems that templates can use."""

    def start(self):
        project_path = Path(__file__).parent
        ensure_assets(project_path)

        self.assets = AssetManager(project_path=project_path)
        self.particles = ParticleEmitter(self)
        self.camera_shake = CameraShake(self)
        self.bounds = BoundsManager(
            screen=ScreenBounds(width=720, height=1280))
        self.actions = InputActionMap()

        self.score = 0
        self.target_score = 10

        self.player = self.add(
            GameObject(
                x=300,
                y=560,
                width=130,
                height=130,
                image_path=self.assets.load_image("showcase_player.png"),
                name="showcase_player",
            )
        )

        self.add(
            TextLabel(
                x=60,
                y=1180,
                text="Template Helper Showcase",
                font_size=32,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.progress = ProgressBar(
            scene=self,
            x=60,
            y=1085,
            width=600,
            height=34,
            value=0,
            max_value=self.target_score,
            fill_color=(0.25, 0.75, 1.0, 1),
            text_format="Score: {value:.0f}/{max_value:.0f}",
            name="showcase_progress",
        )

        self.message = self.add(
            TextLabel(
                x=70,
                y=1005,
                text="Tap anywhere to test helpers.",
                font_size=26,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.actions.map_tap("score", callback=self.score_action)

        self.start_game()

    def score_action(self, event):
        x = float(event.x or 0)
        y = float(event.y or 0)

        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2
        self.bounds.keep_on_screen(self.player)

        self.score += 1
        self.progress.set_value(self.score)

        self.particles.burst(x=x, y=y, count=18)
        self.camera_shake.shake(intensity=6, duration=0.08)

        if self.score >= self.target_score:
            self.message.set_text("Target complete! Helper systems working.")
            self.camera_shake.shake(intensity=18, duration=0.25)
            self.score = 0
            self.progress.set_value(0)
        else:
            self.message.set_text("Tap feedback created!")

    def on_tap(self, x, y):
        self.actions.handle_tap(x, y)

    def update(self, dt):
        self.particles.update(dt)
        self.camera_shake.update(dt)
        super().update(dt)


if __name__ == "__main__":
    Game(title="Template Helper Showcase", width=720, height=1280).set_scene(
        TemplateHelperShowcaseDemo()
    ).run()
