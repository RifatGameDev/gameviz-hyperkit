from hyperkit import Game, GameObject, ProgressBar, Scene, TextLabel


class ProgressBarDemo(Scene):
    """Shows health and XP progress bars."""

    def start(self):
        self.health = 100
        self.xp = 0

        self.add(
            TextLabel(
                x=90,
                y=1180,
                text="Progress Bar Demo",
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.health_bar = ProgressBar(
            scene=self,
            x=60,
            y=1090,
            width=600,
            height=35,
            value=self.health,
            max_value=100,
            fill_color=(0.2, 0.9, 0.35, 1),
            text_format="Health: {value:.0f}/{max_value:.0f}",
            name="health_bar",
        )

        self.xp_bar = ProgressBar(
            scene=self,
            x=60,
            y=1025,
            width=600,
            height=30,
            value=self.xp,
            max_value=100,
            fill_color=(0.25, 0.55, 1.0, 1),
            text_format="XP: {value:.0f}%",
            name="xp_bar",
        )

        self.damage_button = self.add(
            GameObject(
                x=90,
                y=500,
                width=240,
                height=110,
                color=(1.0, 0.25, 0.25, 1),
                name="damage_button",
            )
        )

        self.heal_button = self.add(
            GameObject(
                x=390,
                y=500,
                width=240,
                height=110,
                color=(0.2, 0.8, 0.35, 1),
                name="heal_button",
            )
        )

        self.add(
            TextLabel(
                x=135,
                y=540,
                text="Damage",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=455,
                y=540,
                text="Heal",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=70,
                y=430,
                text="Tap red for damage, green for heal. XP grows every tap.",
                font_size=24,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.start_game()

    def point_inside(self, obj, x, y):
        return obj.x <= x <= obj.x + obj.width and obj.y <= y <= obj.y + obj.height

    def on_tap(self, x, y):
        if self.point_inside(self.damage_button, x, y):
            self.health -= 15
            self.message.set_text("Damage taken!")
        elif self.point_inside(self.heal_button, x, y):
            self.health += 10
            self.message.set_text("Health restored!")
        else:
            self.message.set_text("Tap a button.")

        self.xp += 10

        if self.xp >= 100:
            self.xp = 0
            self.message.set_text("XP bar completed and reset!")

        self.health_bar.set_value(self.health)
        self.xp_bar.set_value(self.xp)


if __name__ == "__main__":
    Game(title="Progress Bar Demo", width=720, height=1280).set_scene(
        ProgressBarDemo()
    ).run()
