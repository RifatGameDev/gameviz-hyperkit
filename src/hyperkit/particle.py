from __future__ import annotations

from dataclasses import dataclass
from random import uniform
from typing import Any

from .object import GameObject


@dataclass
class ParticleConfig:
    count: int = 20
    min_speed: float = 120
    max_speed: float = 420
    min_size: float = 8
    max_size: float = 22
    lifetime: float = 0.6
    gravity: float = -500
    color: tuple[float, float, float, float] = (1.0, 0.85, 0.2, 1)
    shape: str = "circle"


class Particle:
    def __init__(
        self,
        obj: GameObject,
        lifetime: float,
        gravity: float = -500,
        fade: bool = True,
    ) -> None:
        self.obj = obj
        self.lifetime = lifetime
        self.remaining = lifetime
        self.gravity = gravity
        self.fade = fade
        self.start_alpha = obj.color[3] if len(obj.color) >= 4 else 1.0

    @property
    def alive(self) -> bool:
        return self.remaining > 0 and self.obj.active

    def update(self, dt: float) -> bool:
        if not self.alive:
            self.obj.active = False
            self.obj.visible = False
            return False

        self.remaining -= dt

        self.obj.vy += self.gravity * dt
        self.obj.x += self.obj.vx * dt
        self.obj.y += self.obj.vy * dt

        if self.fade and self.lifetime > 0:
            alpha = max(0.0, self.start_alpha *
                        (self.remaining / self.lifetime))
            r, g, b, _ = self.obj.color
            self.obj.color = (r, g, b, alpha)

        if self.remaining <= 0:
            self.obj.active = False
            self.obj.visible = False
            return False

        return True


class ParticleEmitter:
    """Simple particle emitter for HyperKit scenes.

    The emitter creates GameObject particles and adds them to a scene.
    """

    def __init__(self, scene: Any):
        self.scene = scene
        self.particles: list[Particle] = []

    def burst(
        self,
        x: float,
        y: float,
        count: int = 20,
        color: tuple[float, float, float, float] = (1.0, 0.85, 0.2, 1),
        min_speed: float = 120,
        max_speed: float = 420,
        min_size: float = 8,
        max_size: float = 22,
        lifetime: float = 0.6,
        gravity: float = -500,
        shape: str = "circle",
        fade: bool = True,
    ) -> list[Particle]:
        created: list[Particle] = []

        for _ in range(count):
            size = uniform(min_size, max_size)

            obj = GameObject(
                x=x - size / 2,
                y=y - size / 2,
                width=size,
                height=size,
                vx=uniform(-max_speed, max_speed),
                vy=uniform(min_speed, max_speed),
                color=color,
                shape=shape,
                name="particle",
            )

            self.scene.add(obj)

            particle = Particle(
                obj=obj,
                lifetime=lifetime,
                gravity=gravity,
                fade=fade,
            )

            self.particles.append(particle)
            created.append(particle)

        return created

    def emit_config(self, x: float, y: float, config: ParticleConfig) -> list[Particle]:
        return self.burst(
            x=x,
            y=y,
            count=config.count,
            color=config.color,
            min_speed=config.min_speed,
            max_speed=config.max_speed,
            min_size=config.min_size,
            max_size=config.max_size,
            lifetime=config.lifetime,
            gravity=config.gravity,
            shape=config.shape,
        )

    def update(self, dt: float) -> None:
        self.particles = [
            particle
            for particle in self.particles
            if particle.update(dt)
        ]

    def clear(self) -> None:
        for particle in self.particles:
            particle.obj.active = False
            particle.obj.visible = False

        self.particles.clear()
