from hyperkit import Game, GameObject, ParticleEmitter, Scene, TextLabel


class ParticleDemo(Scene):
    """Shows simple particle burst effects."""

    def start(self):
        self.particles = ParticleEmitter(self)

        self.button = self.add(
            GameObject(
                x=210,
                y=520,
                width=300,
                height=120,
                color=(0.2, 0.45, 0.9, 1),
                name="particle_button",
            )
        )

        self.add(
            TextLabel(
                x=90,
                y=1180,
                text="Particle Demo",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.add(
            TextLabel(
                x=165,
                y=560,
                text="Tap for Burst",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.message = self.add(
            TextLabel(
                x=70,
                y=460,
                text="Tap anywhere to create particles.",
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.particles.burst(
            x=x,
            y=y,
            count=24,
            color=(1.0, 0.85, 0.2, 1),
            lifetime=0.7,
        )

        self.message.set_text("Particle burst created!")

    def update(self, dt):
        self.particles.update(dt)
        super().update(dt)


if __name__ == "__main__":
    Game(title="Particle Demo", width=720,
         height=1280).set_scene(ParticleDemo()).run()
