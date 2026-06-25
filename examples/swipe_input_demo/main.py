from hyperkit import Game, GameObject, Scene, TextLabel


class SwipeInputDemo(Scene):
    """Swipe left/right to move between lanes."""

    def start(self):
        self.lanes = [160, 330, 500]
        self.current_lane = 1

        self.player = self.add(
            GameObject(
                x=self.lanes[self.current_lane],
                y=420,
                width=95,
                height=95,
                color=(0.2, 0.75, 1.0, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=70,
                y=1180,
                text="Swipe left or right",
                font_size=32,
                color=(1, 1, 1, 1),
            )
        )

        self.start_game()

    def on_swipe(self, start, end, direction):
        if direction == "left":
            self.current_lane = max(0, self.current_lane - 1)
        elif direction == "right":
            self.current_lane = min(len(self.lanes) - 1, self.current_lane + 1)

        self.player.x = self.lanes[self.current_lane]
        self.message.set_text(f"Swipe: {direction}")


if __name__ == "__main__":
    Game(title="Swipe Input Demo", width=720,
         height=1280).set_scene(SwipeInputDemo()).run()
