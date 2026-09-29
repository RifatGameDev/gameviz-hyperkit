import pytest

from hyperkit import (
    SpriteAnimation,
    SpriteAnimationError,
)


def test_sprite_animation_from_pattern_builds_frames():
    animation = SpriteAnimation.from_pattern(
        name="run",
        pattern="run_{index:02d}.png",
        start=1,
        end=3,
        fps=12,
    )

    assert animation.frames == [
        "run_01.png",
        "run_02.png",
        "run_03.png",
    ]
    assert animation.fps == 12


def test_sprite_animation_from_pattern_rejects_bad_range():
    with pytest.raises(
        SpriteAnimationError
    ):
        SpriteAnimation.from_pattern(
            name="run",
            pattern="run_{index}.png",
            start=3,
            end=1,
        )


def test_sprite_animation_from_pattern_requires_index():
    with pytest.raises(
        SpriteAnimationError,
        match="index",
    ):
        SpriteAnimation.from_pattern(
            name="run",
            pattern="run.png",
            start=1,
            end=2,
        )
