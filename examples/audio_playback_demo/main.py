from pathlib import Path

from hyperkit import AssetManager, AudioManager, Game, GameObject, Scene, TextLabel


class AudioPlaybackDemo(Scene):
    """Shows how to play a sound effect using AudioManager."""

    def start(self):
        self.assets = AssetManager(project_path=Path(__file__).parent)
        self.audio = AudioManager()

        self.click_sound = self.assets.load_audio("click.wav")

        self.button = self.add(
            GameObject(
                x=210,
                y=520,
                width=300,
                height=120,
                color=(0.2, 0.45, 0.9, 1),
                name="sound_button",
            )
        )

        self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Audio Playback Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=150,
                y=560,
                text="Tap to Play Sound",
                font_size=28,
                color=(1, 1, 1, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=80,
                y=460,
                text="Tap the button to play click.wav",
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        if (
            self.button.x <= x <= self.button.x + self.button.width
            and self.button.y <= y <= self.button.y + self.button.height
        ):
            self.audio.play_sound(self.click_sound)
            self.message.set_text("Sound played!")


if __name__ == "__main__":
    Game(title="Audio Playback Demo", width=720, height=1280).set_scene(
        AudioPlaybackDemo()
    ).run()
