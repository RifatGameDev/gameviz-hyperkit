from pathlib import Path

from hyperkit import Game, LevelManager, Scene, TextLabel


class LevelLoadingDemo(Scene):
    """Shows how to load GameObjects from a JSON level file."""

    def start(self):
        self.levels = LevelManager(project_path=Path(__file__).parent)
        self.level = self.levels.load("level_1.json")

        self.loaded_objects = self.levels.add_to_scene(self, self.level)

        self.add(
            TextLabel(
                x=70,
                y=1180,
                text="Level Loading Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=70,
                y=1110,
                text=f"Loaded: {self.level.name}",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.add(
            TextLabel(
                x=70,
                y=1055,
                text=f"Objects: {len(self.loaded_objects)}",
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.add(
            TextLabel(
                x=70,
                y=1005,
                text="Tap anywhere to reload the level.",
                font_size=24,
                color=(0.8, 0.9, 1, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Level Loading Demo", width=720, height=1280).set_scene(
        LevelLoadingDemo()
    ).run()
