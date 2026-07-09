from hyperkit import Cooldown, Game, GameObject, Scene, TextLabel, Timer


class TimerCooldownDemo(Scene):
    """Shows Timer and Cooldown helpers."""

    def start(self):
        self.score = 0

        self.auto_timer = Timer(
            duration=1.0,
            repeat=True,
            on_complete=self.add_auto_score,
        )

        self.tap_cooldown = Cooldown(duration=1.5)

        self.button = self.add(
            GameObject(
                x=190,
                y=520,
                width=340,
                height=120,
                color=(0.2, 0.45, 0.9, 1),
                name="cooldown_button",
            )
        )

        self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Timer & Cooldown Demo",
                font_size=34,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=80,
                y=1080,
                text="Score: 0",
                font_size=32,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.timer_label = self.add(
            TextLabel(
                x=80,
                y=1020,
                text="Auto score every 1 second",
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.add(
            TextLabel(
                x=215,
                y=560,
                text="Tap +5 Score",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.cooldown_label = self.add(
            TextLabel(
                x=80,
                y=450,
                text="Button ready",
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.start_game()

    def add_auto_score(self):
        self.score += 1
        self.update_score_label()

    def update_score_label(self):
        self.score_label.set_text(f"Score: {self.score}")

    def point_inside_button(self, x, y):
        return (
            self.button.x <= x <= self.button.x + self.button.width
            and self.button.y <= y <= self.button.y + self.button.height
        )

    def on_tap(self, x, y):
        if not self.point_inside_button(x, y):
            return

        if self.tap_cooldown.use():
            self.score += 5
            self.update_score_label()
            self.cooldown_label.set_text("Used! Wait for cooldown...")
            self.button.color = (0.6, 0.2, 0.2, 1)
        else:
            self.cooldown_label.set_text(
                f"Cooldown: {self.tap_cooldown.remaining:.1f}s"
            )

    def update(self, dt):
        self.auto_timer.update(dt)
        self.tap_cooldown.update(dt)

        if self.tap_cooldown.ready:
            self.button.color = (0.2, 0.45, 0.9, 1)
            self.cooldown_label.set_text("Button ready")
        else:
            self.cooldown_label.set_text(
                f"Cooldown: {self.tap_cooldown.remaining:.1f}s"
            )

        super().update(dt)


if __name__ == "__main__":
    Game(title="Timer Cooldown Demo", width=720, height=1280).set_scene(
        TimerCooldownDemo()
    ).run()
