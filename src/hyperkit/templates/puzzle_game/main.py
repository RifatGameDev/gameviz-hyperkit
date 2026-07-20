from __future__ import annotations

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


class PuzzleGameScene(Scene):
    def start(self):
        self.grid_size = 3
        self.tile_size = 150
        self.tile_gap = 20
        self.grid_start_x = 105
        self.grid_start_y = 380
        self.score_goal = 9
        self.active_tile_index = 0
        self.game_over = False

        self.assets = AssetManager()
        self.score = ScoreManager(high_score_key="puzzle_game_high_score")
        self.camera_shake = CameraShake(self)
        self.particles = ParticleEmitter(self)
        self.bounds_manager = BoundsManager()
        self.screen_bounds = ScreenBounds(width=720, height=1280)
        self.input_actions = InputActionMap()

        self.tiles = []

        self.background = self.add(
            GameObject(
                x=0,
                y=0,
                width=720,
                height=1280,
                color=(0.08, 0.09, 0.14, 1),
                shape="rect",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=45,
                y=1180,
                text="Puzzle Game",
                font_size=44,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.help_label = self.add(
            TextLabel(
                x=45,
                y=1125,
                text="Tap the glowing tile. Follow the pattern and reach the goal.",
                font_size=22,
                color=(0.82, 0.9, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=45,
                y=1045,
                text="Score: 0",
                font_size=34,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.high_score_label = self.add(
            TextLabel(
                x=45,
                y=995,
                text=f"High Score: {self.score.high_score}",
                font_size=26,
                color=(0.95, 0.82, 0.3, 1),
            )
        )

        self.progress_label = self.add(
            TextLabel(
                x=45,
                y=920,
                text=f"Goal Progress: 0 / {self.score_goal}",
                font_size=24,
                color=(0.78, 0.92, 1, 1),
            )
        )

        self.progress_bar = ProgressBar(
            scene=self,
            x=45,
            y=875,
            width=630,
            height=30,
            value=0,
            max_value=self.score_goal,
        )

        self._create_grid()

        self.status_label = self.add(
            TextLabel(
                x=45,
                y=120,
                text="Ready. Tap the glowing tile!",
                font_size=26,
                color=(0.8, 1, 0.85, 1),
            )
        )

        self._highlight_active_tile()
        self.start_game()

    def _create_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile = self.add(
                    GameObject(
                        x=self.grid_start_x + col *
                        (self.tile_size + self.tile_gap),
                        y=self.grid_start_y + row *
                        (self.tile_size + self.tile_gap),
                        width=self.tile_size,
                        height=self.tile_size,
                        color=(0.18, 0.22, 0.34, 1),
                        shape="rect",
                        image_path=None,
                    )
                )
                self.tiles.append(tile)

    def update(self, dt):
        self.camera_shake.update(dt)
        self.particles.update(dt)
        super().update(dt)

    def on_tap(self, x, y):
        if self.game_over:
            self._restart()
            return

        tapped_index = self._find_tapped_tile(x, y)

        if tapped_index is None:
            self.status_label.set_text("Tap inside the puzzle grid.")
            return

        if tapped_index == self.active_tile_index:
            self._handle_correct_tap()
        else:
            self._handle_wrong_tap()

    def _find_tapped_tile(self, x, y):
        for index, tile in enumerate(self.tiles):
            inside_x = tile.x <= x <= tile.x + tile.width
            inside_y = tile.y <= y <= tile.y + tile.height

            if inside_x and inside_y:
                return index

        return None

    def _handle_correct_tap(self):
        self.score.add(1)

        current_score = self.score.value
        progress_value = min(current_score, self.score_goal)

        self.score_label.set_text(f"Score: {current_score}")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.progress_label.set_text(
            f"Goal Progress: {progress_value} / {self.score_goal}"
        )
        self.progress_bar.set_value(progress_value)

        active_tile = self.tiles[self.active_tile_index]

        self.particles.burst(
            x=active_tile.x + active_tile.width / 2,
            y=active_tile.y + active_tile.height / 2,
            count=10,
        )

        if current_score >= self.score_goal:
            self.status_label.set_text(
                "Puzzle complete! Tap again for a new run.")
            self._set_win_state()
            return

        self.active_tile_index = (self.active_tile_index + 4) % len(self.tiles)
        self._highlight_active_tile()
        self.status_label.set_text("Correct! Follow the next glowing tile.")

    def _handle_wrong_tap(self):
        self.game_over = True
        self.camera_shake.shake(intensity=16, duration=0.35)
        self.status_label.set_text("Wrong tile. Tap to restart.")

        for tile in self.tiles:
            tile.color = (0.55, 0.12, 0.16, 1)

    def _highlight_active_tile(self):
        for index, tile in enumerate(self.tiles):
            if index == self.active_tile_index:
                tile.color = (0.25, 0.85, 1.0, 1)
            else:
                tile.color = (0.18, 0.22, 0.34, 1)

    def _set_win_state(self):
        self.game_over = True
        self.camera_shake.shake(intensity=8, duration=0.2)

        for tile in self.tiles:
            tile.color = (0.25, 1.0, 0.48, 1)

    def _restart(self):
        self.game_over = False
        self.active_tile_index = 0

        self.score.reset()
        self.score_label.set_text("Score: 0")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.progress_label.set_text(f"Goal Progress: 0 / {self.score_goal}")
        self.progress_bar.set_value(0)
        self.status_label.set_text("Ready. Tap the glowing tile!")

        self._highlight_active_tile()


if __name__ == "__main__":
    Game(
        title="HyperKit Puzzle Game",
        width=720,
        height=1280,
    ).set_scene(PuzzleGameScene()).run()
