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

    player_path = images_path / "runner_player.png"
    coin_path = images_path / "runner_coin.png"
    hazard_path = images_path / "runner_hazard.png"

    if not player_path.exists():
        save_demo_png(player_path, (80, 180, 255, 255))

    if not coin_path.exists():
        save_demo_png(coin_path, (255, 215, 40, 255))

    if not hazard_path.exists():
        save_demo_png(hazard_path, (255, 70, 70, 255))


def rects_overlap(a: GameObject, b: GameObject) -> bool:
    return not (
        a.x + a.width < b.x
        or a.x > b.x + b.width
        or a.y + a.height < b.y
        or a.y > b.y + b.height
    )


class SwipeRunnerScene(Scene):
    """Modern swipe runner template using HyperKit helpers."""

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280
        self.target_distance = 100

        project_path = Path(__file__).parent
        ensure_template_assets(project_path)

        self.assets = AssetManager(project_path=project_path)
        self.score = ScoreManager(high_score_key="swipe_runner_high_score")
        self.particles = ParticleEmitter(self)
        self.camera_shake = CameraShake(self)
        self.bounds = BoundsManager(
            screen=ScreenBounds(width=self.screen_width,
                                height=self.screen_height)
        )
        self.actions = InputActionMap()

        self.lanes = [150, 315, 480]
        self.current_lane = 1
        self.runner_speed = 360
        self.distance = 0

        self.player = self.add(
            GameObject(
                x=self.lanes[self.current_lane],
                y=230,
                width=90,
                height=90,
                image_path=self.assets.load_image("runner_player.png"),
                name="runner_player",
            )
        )

        self.coin = self.add(
            GameObject(
                x=self.lanes[0],
                y=1220,
                width=70,
                height=70,
                image_path=self.assets.load_image("runner_coin.png"),
                name="coin",
            )
        )

        self.hazard = self.add(
            GameObject(
                x=self.lanes[2],
                y=1500,
                width=95,
                height=95,
                image_path=self.assets.load_image("runner_hazard.png"),
                name="hazard",
            )
        )

        self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Swipe Runner",
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
            max_value=self.target_distance,
            fill_color=(0.25, 0.75, 1.0, 1),
            text_format="Distance: {value:.0f}/{max_value:.0f}",
            name="runner_progress",
        )

        self.message_label = self.add(
            TextLabel(
                x=60,
                y=940,
                text="Swipe left/right or tap sides to move.",
                font_size=26,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.actions.map_swipe(
            "move_left", direction="left", callback=self.move_left)
        self.actions.map_swipe(
            "move_right", direction="right", callback=self.move_right)

        self.reset_item(self.coin, force_kind="coin", y=1220)
        self.reset_item(self.hazard, force_kind="hazard", y=1500)

        self.start_game()
        self.update_labels()

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")
        self.progress_bar.set_value(self.distance)

    def lane_x(self, lane_index: int) -> float:
        return self.lanes[lane_index]

    def move_left(self, event=None):
        if not self.is_playing():
            return

        self.current_lane = max(0, self.current_lane - 1)
        self.player.x = self.lane_x(self.current_lane)
        self.message_label.set_text("Move left")

    def move_right(self, event=None):
        if not self.is_playing():
            return

        self.current_lane = min(len(self.lanes) - 1, self.current_lane + 1)
        self.player.x = self.lane_x(self.current_lane)
        self.message_label.set_text("Move right")

    def reset_item(self, obj: GameObject, force_kind: str | None = None, y: float | None = None):
        lane = random.randint(0, len(self.lanes) - 1)
        obj.x = self.lane_x(lane)
        obj.y = y if y is not None else random.randint(1280, 1650)

        kind = force_kind or random.choice(["coin", "hazard"])
        obj.data["kind"] = kind

        if kind == "coin":
            obj.image_path = self.assets.load_image("runner_coin.png")
            obj.width = 70
            obj.height = 70
            obj.name = "coin"
        else:
            obj.image_path = self.assets.load_image("runner_hazard.png")
            obj.width = 95
            obj.height = 95
            obj.name = "hazard"

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        if x < self.screen_width / 2:
            self.move_left()
        else:
            self.move_right()

    def on_swipe(self, start, end, direction):
        if self.is_game_over():
            return

        self.actions.handle_swipe(start, end, direction)

    def update(self, dt):
        if self.is_playing():
            self.distance += 18 * dt
            self.distance = min(self.distance, self.target_distance)

            self.coin.y -= self.runner_speed * dt
            self.hazard.y -= self.runner_speed * dt

            if self.coin.y + self.coin.height < 0:
                self.reset_item(self.coin, force_kind="coin")

            if self.hazard.y + self.hazard.height < 0:
                self.reset_item(self.hazard, force_kind="hazard")

            if rects_overlap(self.player, self.coin):
                self.collect_coin()

            if rects_overlap(self.player, self.hazard):
                self.hit_hazard()

            if self.distance >= self.target_distance:
                self.complete_round()

            self.update_labels()

        self.particles.update(dt)
        self.camera_shake.update(dt)
        super().update(dt)

    def collect_coin(self):
        self.score.add(1)
        self.message_label.set_text("Coin collected!")

        self.particles.burst(
            x=self.coin.x + self.coin.width / 2,
            y=self.coin.y + self.coin.height / 2,
            count=18,
            color=(1.0, 0.85, 0.2, 1),
            lifetime=0.45,
        )

        self.camera_shake.shake(intensity=5, duration=0.08)
        self.reset_item(self.coin, force_kind="coin")

    def hit_hazard(self):
        self.end_game()
        self.camera_shake.shake(intensity=18, duration=0.25)
        self.message_label.set_text("Hit hazard! Tap to restart.")

        self.particles.burst(
            x=self.player.x + self.player.width / 2,
            y=self.player.y + self.player.height / 2,
            count=30,
            color=(1.0, 0.25, 0.25, 1),
            lifetime=0.7,
        )

    def complete_round(self):
        self.end_game()
        self.camera_shake.shake(intensity=18, duration=0.25)
        self.message_label.set_text("Distance complete! Tap to restart.")

        self.particles.burst(
            x=self.player.x + self.player.width / 2,
            y=self.player.y + self.player.height / 2,
            count=36,
            color=(0.2, 1.0, 0.45, 1),
            lifetime=0.8,
        )

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Swipe Runner", width=720, height=1280).set_scene(
        SwipeRunnerScene()
    ).run()
