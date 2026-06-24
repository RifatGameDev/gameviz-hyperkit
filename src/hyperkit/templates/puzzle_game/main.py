from random import choice

from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel


COLORS = [
    ("red", (1.0, 0.25, 0.25, 1)),
    ("green", (0.2, 0.8, 0.35, 1)),
    ("blue", (0.25, 0.55, 1.0, 1)),
    ("yellow", (1.0, 0.85, 0.2, 1)),
    ("purple", (0.7, 0.35, 1.0, 1)),
]


class PuzzleGameScene(Scene):
    """Simple color puzzle template.

    Goal:
    - Look at the target color.
    - Tap a tile with the matching color.
    - Correct taps increase score.
    - Wrong taps reduce score.
    - Reach target score to win.
    - Tap after game over to restart.
    """

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280

        self.target_score = 10
        self.tiles = []
        self.target_name = ""

        self.score = ScoreManager(high_score_key="puzzle_game_high_score")

        self.title_label = self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Color Puzzle",
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

        self.target_label = self.add(
            TextLabel(
                x=80,
                y=1000,
                text="Tap target color",
                font_size=32,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.message_label = self.add(
            TextLabel(
                x=90,
                y=930,
                text="Find the matching color tile!",
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.create_board()
        self.pick_target()
        self.start_game()
        self.update_labels()

    def create_board(self):
        self.tiles.clear()

        tile_size = 135
        gap = 25
        start_x = 120
        start_y = 430

        for row in range(3):
            for col in range(3):
                color_name, color_value = choice(COLORS)

                tile = self.add(
                    GameObject(
                        x=start_x + col * (tile_size + gap),
                        y=start_y + row * (tile_size + gap),
                        width=tile_size,
                        height=tile_size,
                        color=color_value,
                        name="puzzle_tile",
                    )
                )

                tile.data["color_name"] = color_name
                self.tiles.append(tile)

    def pick_target(self):
        target_tile = choice(self.tiles)
        self.target_name = target_tile.data["color_name"]
        self.target_label.set_text(f"Target: {self.target_name.upper()}")

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")

    def point_inside_tile(self, tile, x, y):
        return (
            tile.x <= x <= tile.x + tile.width
            and tile.y <= y <= tile.y + tile.height
        )

    def refresh_board(self):
        for tile in self.tiles:
            color_name, color_value = choice(COLORS)
            tile.color = color_value
            tile.data["color_name"] = color_name

        self.pick_target()

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        if not self.is_playing():
            return

        for tile in self.tiles:
            if self.point_inside_tile(tile, x, y):
                self.handle_tile_tap(tile)
                return

    def handle_tile_tap(self, tile):
        selected_color = tile.data["color_name"]

        if selected_color == self.target_name:
            self.score.add(1)
            self.message_label.set_text("Correct! Find the next color.")
            self.refresh_board()
        else:
            self.score.subtract(1)
            self.message_label.set_text(f"Wrong! That was {selected_color}.")

        self.update_labels()

        if self.score.value >= self.target_score:
            self.win_game()

    def win_game(self):
        self.end_game()
        self.message_label.set_text("You won! Tap anywhere to restart.")
        self.target_label.set_text("Puzzle Complete!")

        for tile in self.tiles:
            tile.color = (0.2, 1.0, 0.45, 1)

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Puzzle Game", width=720, height=1280).set_scene(
        PuzzleGameScene()).run()
