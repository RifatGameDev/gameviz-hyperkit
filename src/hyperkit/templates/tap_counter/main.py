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

    player_path = images_path / "player.png"
    coin_path = images_path / "coin.png"

    if not player_path.exists():
        save_demo_png(player_path, (60, 190, 255, 255))

    if not coin_path.exists():
        save_demo_png(coin_path, (255, 215, 40, 255))


class TapCounterScene(Scene):
    """Modern tap counter template using HyperKit helpers."""

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280
        self.target_score = 20

        project_path = Path(__file__).parent
        ensure_template_assets(project_path)

        self.assets = AssetManager(project_path=project_path)
        self.score = ScoreManager(high_score_key="tap_counter_high_score")
        self.particles = ParticleEmitter(self)
        self.camera_shake = CameraShake(self)
        self.bounds = BoundsManager(
            screen=ScreenBounds(width=self.screen_width,
                                height=self.screen_height)
        )
        self.actions = InputActionMap()

        self.player = self.add(
            GameObject(
                x=300,
                y=560,
                width=120,
                height=120,
                image_path=self.assets.load_image("player.png"),
                name="player",
            )
        )

        self.coin = self.add(
            GameObject(
                x=305,
                y=760,
                width=90,
                height=90,
                image_path=self.assets.load_image("coin.png"),
                name="coin",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Tap Counter",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=40,
                y=1125,
                text="Score: 0",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.best_label = self.add(
            TextLabel(
                x=40,
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
            text_format="Progress: {value:.0f}/{max_value:.0f}",
            name="tap_progress",
        )

        self.message_label = self.add(
            TextLabel(
                x=70,
                y=940,
                text="Tap anywhere to score!",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.actions.map_tap("tap_score", callback=self.handle_tap_score)

        self.start_game()
        self.update_labels()

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")
        self.progress_bar.set_value(self.score.value)

    def handle_tap_score(self, event):
        if not self.is_playing():
            return

        x = float(event.x or 0)
        y = float(event.y or 0)

        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2
        self.bounds.keep_on_screen(self.player)

        self.coin.x = self.player.x + 15
        self.coin.y = self.player.y + 150
        self.bounds.keep_on_screen(self.coin)

        self.score.add(1)
        self.update_labels()

        self.particles.burst(
            x=x,
            y=y,
            count=14,
            color=(1.0, 0.85, 0.2, 1),
            lifetime=0.45,
        )

        self.camera_shake.shake(intensity=5, duration=0.08)

        if self.score.value >= self.target_score:
            self.complete_round()
        else:
            self.message_label.set_text("Nice tap! Keep going.")

    def complete_round(self):
        self.end_game()
        self.camera_shake.shake(intensity=18, duration=0.25)
        self.message_label.set_text("Target reached! Tap to restart.")

        self.particles.burst(
            x=self.player.x + self.player.width / 2,
            y=self.player.y + self.player.height / 2,
            count=35,
            color=(0.2, 1.0, 0.45, 1),
            lifetime=0.8,
        )

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        self.actions.handle_tap(x, y)

    def update(self, dt):
        self.particles.update(dt)
        self.camera_shake.update(dt)
        super().update(dt)

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Tap Counter", width=720, height=1280).set_scene(
        TapCounterScene()).run()
