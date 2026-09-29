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
    fade: bool = True

    def __post_init__(self) -> None:
        self.count = int(self.count)
        self.min_speed = float(self.min_speed)
        self.max_speed = float(self.max_speed)
        self.min_size = float(self.min_size)
        self.max_size = float(self.max_size)
        self.lifetime = float(self.lifetime)
        self.gravity = float(self.gravity)

        if self.count < 0:
            raise ValueError("Particle count cannot be negative.")

        if self.min_speed < 0 or self.max_speed < self.min_speed:
            raise ValueError(
                "Particle speed range must satisfy 0 <= min_speed <= max_speed."
            )

        if self.min_size <= 0 or self.max_size < self.min_size:
            raise ValueError(
                "Particle size range must satisfy 0 < min_size <= max_size."
            )

        if self.lifetime <= 0:
            raise ValueError("Particle lifetime must be greater than 0.")


class Particle:
    def __init__(
        self,
        obj: GameObject,
        lifetime: float,
        gravity: float = -500,
        fade: bool = True,
    ) -> None:
        self.obj = obj
        self.lifetime = float(lifetime)

        if self.lifetime <= 0:
            raise ValueError("Particle lifetime must be greater than 0.")

        self.remaining = self.lifetime
        self.gravity = float(gravity)
        self.fade = bool(fade)
        self.start_alpha = obj.color[3] if len(obj.color) >= 4 else 1.0

    @property
    def alive(self) -> bool:
        return self.remaining > 0 and self.obj.active

    @property
    def age(self) -> float:
        return max(0.0, self.lifetime - self.remaining)

    @property
    def progress(self) -> float:
        return min(1.0, self.age / self.lifetime)

    def update(self, dt: float) -> bool:
        dt = float(dt)

        if dt < 0:
            raise ValueError("Particle dt must be non-negative.")

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
        if not hasattr(scene, "add"):
            raise ValueError(
                "ParticleEmitter scene must provide an add() method."
            )

        self.scene = scene
        self.particles: list[Particle] = []

    @property
    def active_count(self) -> int:
        return len(self.particles)

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
        config = ParticleConfig(
            count=count,
            min_speed=min_speed,
            max_speed=max_speed,
            min_size=min_size,
            max_size=max_size,
            lifetime=lifetime,
            gravity=gravity,
            color=color,
            shape=shape,
            fade=fade,
        )

        created: list[Particle] = []

        for _ in range(config.count):
            size = uniform(
                config.min_size,
                config.max_size,
            )

            obj = GameObject(
                x=x - size / 2,
                y=y - size / 2,
                width=size,
                height=size,
                vx=uniform(
                    -config.max_speed,
                    config.max_speed,
                ),
                vy=uniform(
                    config.min_speed,
                    config.max_speed,
                ),
                color=config.color,
                shape=config.shape,
                name="particle",
            )

            self.scene.add(obj)

            particle = Particle(
                obj=obj,
                lifetime=config.lifetime,
                gravity=config.gravity,
                fade=config.fade,
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
            fade=config.fade,
        )

    def update(self, dt: float) -> None:
        dt = float(dt)

        if dt < 0:
            raise ValueError("ParticleEmitter dt must be non-negative.")

        self.particles = [
            particle
            for particle in self.particles
            if particle.update(dt)
        ]

    def clear(self) -> int:
        count = len(self.particles)

        for particle in self.particles:
            particle.obj.active = False
            particle.obj.visible = False

        self.particles.clear()
        return count
