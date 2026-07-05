from pathlib import Path

from hyperkit import AssetManager, Game, GameObject, Scene, TextLabel


class ImageRenderingDemo(Scene):
    """Shows how to render an image using GameObject."""

    def start(self):
        assets = AssetManager(project_path=Path(__file__).parent)

        self.player = self.add(
            GameObject(
                x=300,
                y=560,
                width=140,
                height=140,
                image_path=assets.load_image("player.png"),
                name="image_player",
            )
        )

        self.add(
            TextLabel(
                x=60,
                y=1180,
                text="Image Rendering Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=60,
                y=1110,
                text="Tap anywhere to move the image.",
                font_size=28,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2


if __name__ == "__main__":
    Game(title="Image Rendering Demo", width=720, height=1280).set_scene(
        ImageRenderingDemo()
    ).run()
