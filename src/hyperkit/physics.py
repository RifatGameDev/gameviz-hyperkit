from __future__ import annotations


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def move_towards(current: float, target: float, max_delta: float) -> float:
    if abs(target - current) <= max_delta:
        return target
    return current + max_delta if target > current else current - max_delta


def apply_gravity(velocity_y: float, gravity: float, dt: float) -> float:
    return velocity_y + gravity * dt
