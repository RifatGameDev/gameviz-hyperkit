from pathlib import Path
import struct
import zlib

from hyperkit import AssetManager, Game, GameObject, Scene, SpriteAnimator, TextLabel


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


def create_demo_frames(images_path: Path) -> None:
    images_path.mkdir(parents=True, exist_ok=True)

    frames = [
        ("player_1.png", (255, 80, 80, 255)),
        ("player_2.png", (80, 255, 120, 255)),
        ("player_3.png", (80, 150, 255, 255)),
    ]

    for filename, color in frames:
        frame_path = images_path / filename

        if not frame_path.exists():
            save_demo_png(frame_path, color)


class SpriteAnimationDemo(Scene):
    """Shows frame-based sprite animation using SpriteAnimator."""

    def start(self):
        project_path = Path(__file__).parent
        create_demo_frames(project_path / "assets" / "images")

        assets = AssetManager(project_path=project_path)

        frames = [
            assets.load_image("player_1.png"),
            assets.load_image("player_2.png"),
            assets.load_image("player_3.png"),
        ]

        self.player = self.add(
            GameObject(
                x=300,
                y=560,
                width=150,
                height=150,
                image_path=frames[0],
                name="sprite_player",
            )
        )

        self.sprite = SpriteAnimator(self.player)
        self.sprite.add_animation("idle", frames=frames, fps=4, loop=True)
        self.sprite.play("idle")

        self.add(
            TextLabel(
                x=60,
                y=1180,
                text="Sprite Animation Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=60,
                y=1110,
                text="Tap anywhere to move the animated sprite.",
                font_size=27,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2
        self.message.set_text("Sprite moved!")

    def update(self, dt):
        self.sprite.update(dt)
        super().update(dt)


if __name__ == "__main__":
    Game(title="Sprite Animation Demo", width=720, height=1280).set_scene(
        SpriteAnimationDemo()
    ).run()
