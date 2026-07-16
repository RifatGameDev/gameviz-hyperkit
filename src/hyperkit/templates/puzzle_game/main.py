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

    colors = {
        "tile_blue.png": (70, 170, 255, 255),
        "tile_gold.png": (255, 210, 60, 255),
        "tile_green.png": (70, 220, 120, 255),
    }

    for filename, color in colors.items():
        path = images_path / filename
        if not path.exists():
            save_demo_png(path, color)


class PuzzleGameScene(Scene):
    """Modern puzzle template using HyperKit helpers."""

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280
        self.target_matches = 6

        project_path = Path(__file__).parent
        ensure_template_assets(project_path)

        self.assets = AssetManager(project_path=project_path)
        self.score = ScoreManager(high_score_key="puzzle_game_high_score")
        self.particles = ParticleEmitter(self)
        self.camera_shake = CameraShake(self)
        self.bounds = BoundsManager(
            screen=ScreenBounds(width=self.screen_width,
                                height=self.screen_height)
        )
        self.actions = InputActionMap()

        self.selected_tile = None
        self.tiles = []
        self.tile_images = [
            self.assets.load_image("tile_blue.png"),
            self.assets.load_image("tile_gold.png"),
            self.assets.load_image("tile_green.png"),
        ]

        self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Puzzle Game",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=50,
                y=1125,
                text="Matches: 0",
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
            max_value=self.target_matches,
            fill_color=(0.25, 0.75, 1.0, 1),
            text_format="Matches: {value:.0f}/{max_value:.0f}",
            name="puzzle_progress",
        )

        self.message_label = self.add(
            TextLabel(
                x=70,
                y=940,
                text="Tap matching tiles.",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.create_tiles()
        self.start_game()
        self.update_labels()

    def create_tiles(self):
        start_x = 110
        start_y = 360
        size = 120
        gap = 35

        values = [0, 0, 1, 1, 2, 2]
        random.shuffle(values)

        for index, value in enumerate(values):
            row = index // 3
            col = index % 3

            tile = self.add(
                GameObject(
                    x=start_x + col * (size + gap),
                    y=start_y + row * (size + gap),
                    width=size,
                    height=size,
                    image_path=self.tile_images[value],
                    name=f"tile_{index}",
                )
            )
            tile.data["value"] = value
            tile.data["matched"] = False

            self.tiles.append(tile)

            self.actions.map_area(
                action=f"select_tile_{index}",
                x=tile.x,
                y=tile.y,
                width=tile.width,
                height=tile.height,
                callback=self.select_tile,
                data={"tile_index": index},
            )

    def update_labels(self):
        self.score_label.set_text(f"Matches: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")
        self.progress_bar.set_value(self.score.value)

    def select_tile(self, event):
        if not self.is_playing():
            return

        tile_index = event.data["tile_index"]
        tile = self.tiles[tile_index]

        if tile.data.get("matched"):
            self.message_label.set_text("Already matched.")
            return

        if self.selected_tile is None:
            self.selected_tile = tile
            tile.width = 135
            tile.height = 135
            self.bounds.keep_on_screen(tile)
            self.message_label.set_text("Select another tile.")
            return

        first = self.selected_tile
        second = tile

        first.width = 120
        first.height = 120

        if first is second:
            self.selected_tile = None
            self.message_label.set_text("Choose a different tile.")
            return

        if first.data["value"] == second.data["value"]:
            first.data["matched"] = True
            second.data["matched"] = True
            first.color = (0.5, 1.0, 0.5, 1)
            second.color = (0.5, 1.0, 0.5, 1)

            self.score.add(1)
            self.update_labels()
            self.message_label.set_text("Match found!")

            self.camera_shake.shake(intensity=6, duration=0.08)
            self.particles.burst(
                x=second.x + second.width / 2,
                y=second.y + second.height / 2,
                count=18,
                color=(0.2, 1.0, 0.45, 1),
                lifetime=0.45,
            )

            if self.score.value >= self.target_matches // 2:
                self.complete_round()
        else:
            self.message_label.set_text("Not a match.")
            self.camera_shake.shake(intensity=10, duration=0.12)

        self.selected_tile = None

    def complete_round(self):
        self.end_game()
        self.message_label.set_text("Puzzle complete! Tap to restart.")
        self.camera_shake.shake(intensity=18, duration=0.25)

        self.particles.burst(
            x=360,
            y=640,
            count=40,
            color=(1.0, 0.85, 0.2, 1),
            lifetime=0.8,
        )

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        event = self.actions.handle_tap(x, y)

        if event is None:
            self.message_label.set_text("Tap a tile.")

    def update(self, dt):
        self.particles.update(dt)
        self.camera_shake.update(dt)
        super().update(dt)

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Puzzle Game", width=720, height=1280).set_scene(
        PuzzleGameScene()
    ).run()
