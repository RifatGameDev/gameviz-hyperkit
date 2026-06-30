from pathlib import Path

from hyperkit import AssetManager, Game, Scene, TextLabel


class AssetLoadingDemo(Scene):
    """Shows how to load JSON data from the assets folder."""

    def start(self):
        assets = AssetManager(project_path=Path(__file__).parent)
        level_data = assets.load_json("level.json")

        self.add(
            TextLabel(
                x=60,
                y=1180,
                text="Asset Loading Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=60,
                y=1100,
                text=f"Level: {level_data['level_name']}",
                font_size=30,
                color=(0.8, 0.9, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=60,
                y=1040,
                text=f"Target Score: {level_data['target_score']}",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.add(
            TextLabel(
                x=60,
                y=980,
                text=level_data["message"],
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.start_game()


if __name__ == "__main__":
    Game(title="Asset Loading Demo", width=720, height=1280).set_scene(
        AssetLoadingDemo()
    ).run()
