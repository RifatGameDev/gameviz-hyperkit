import pytest

from hyperkit import GameObject, SpriteAnimation, SpriteAnimationError, SpriteAnimator


def test_sprite_animation_requires_frames():
    with pytest.raises(SpriteAnimationError):
        SpriteAnimation(name="empty", frames=[])


def test_sprite_animation_requires_positive_fps():
    with pytest.raises(SpriteAnimationError):
        SpriteAnimation(name="bad", frames=["a.png"], fps=0)


def test_sprite_animation_starts_with_first_frame():
    animation = SpriteAnimation(
        name="idle", frames=["idle_1.png", "idle_2.png"])

    assert animation.current_frame == "idle_1.png"


def test_sprite_animation_advances_frame_by_fps():
    animation = SpriteAnimation(
        name="run",
        frames=["run_1.png", "run_2.png", "run_3.png"],
        fps=2,
        loop=True,
    )

    animation.update(0.5)

    assert animation.current_frame == "run_2.png"

    animation.update(0.5)

    assert animation.current_frame == "run_3.png"


def test_sprite_animation_loops_to_first_frame():
    animation = SpriteAnimation(
        name="run",
        frames=["run_1.png", "run_2.png"],
        fps=2,
        loop=True,
    )

    animation.update(0.5)
    animation.update(0.5)

    assert animation.current_frame == "run_1.png"
    assert animation.playing


def test_sprite_animation_non_loop_stops_at_last_frame():
    animation = SpriteAnimation(
        name="attack",
        frames=["attack_1.png", "attack_2.png"],
        fps=2,
        loop=False,
    )

    animation.update(0.5)
    animation.update(0.5)

    assert animation.current_frame == "attack_2.png"
    assert animation.completed
    assert not animation.playing


def test_sprite_animator_sets_first_frame_on_target():
    obj = GameObject()
    animator = SpriteAnimator(obj)

    animator.add_animation(
        "idle",
        frames=["idle_1.png", "idle_2.png"],
        fps=2,
        loop=True,
    )

    assert obj.image_path == "idle_1.png"


def test_sprite_animator_updates_target_image_path():
    obj = GameObject()
    animator = SpriteAnimator(obj)

    animator.add_animation(
        "run",
        frames=["run_1.png", "run_2.png"],
        fps=2,
        loop=True,
    )

    animator.update(0.5)

    assert obj.image_path == "run_2.png"


def test_sprite_animator_can_switch_animation():
    obj = GameObject()
    animator = SpriteAnimator(obj)

    animator.add_animation("idle", frames=["idle_1.png"], fps=2)
    animator.add_animation("jump", frames=["jump_1.png", "jump_2.png"], fps=2)

    animator.play("jump")

    assert obj.image_path == "jump_1.png"
    assert animator.current_name == "jump"


def test_sprite_animator_rejects_unknown_animation():
    obj = GameObject()
    animator = SpriteAnimator(obj)

    animator.add_animation("idle", frames=["idle_1.png"], fps=2)

    with pytest.raises(SpriteAnimationError):
        animator.play("missing")



def test_sprite_animation_rejects_empty_name():
    with pytest.raises(
        SpriteAnimationError,
        match="name",
    ):
        SpriteAnimation(
            name=" ",
            frames=["a.png"],
        )


def test_sprite_animation_rejects_empty_frame_path():
    with pytest.raises(
        SpriteAnimationError,
        match="frames",
    ):
        SpriteAnimation(
            name="idle",
            frames=["a.png", " "],
        )


def test_sprite_animation_rejects_negative_dt():
    animation = SpriteAnimation(
        name="idle",
        frames=["a.png"],
    )

    with pytest.raises(
        SpriteAnimationError,
        match="dt",
    ):
        animation.update(-0.1)


def test_sprite_animation_lifecycle_methods_are_chainable():
    animation = SpriteAnimation(
        name="idle",
        frames=["a.png", "b.png"],
    )

    assert animation.pause() is animation
    assert animation.play() is animation
    assert animation.stop() is animation
    assert animation.reset() is animation


def test_sprite_animator_reports_animation_names():
    animator = SpriteAnimator()
    animator.add_animation(
        "run",
        ["run.png"],
    )
    animator.add_animation(
        "idle",
        ["idle.png"],
    )

    assert animator.animation_names == [
        "idle",
        "run",
    ]


def test_sprite_animator_set_target_is_chainable():
    animator = SpriteAnimator()
    animator.add_animation(
        "idle",
        ["idle.png"],
    )
    obj = GameObject()

    assert animator.set_target(obj) is animator
    assert obj.image_path == "idle.png"


def test_sprite_animator_pause_resume_stop_report_result():
    animator = SpriteAnimator()

    assert animator.pause() is False
    assert animator.resume() is False
    assert animator.stop() is False

    animator.add_animation(
        "idle",
        ["idle.png"],
    )

    assert animator.pause() is True
    assert animator.resume() is True
    assert animator.stop() is True


def test_sprite_animator_can_remove_current_animation():
    obj = GameObject()
    animator = SpriteAnimator(obj)
    animator.add_animation(
        "idle",
        ["idle.png"],
    )
    animator.add_animation(
        "run",
        ["run.png"],
    )

    assert animator.remove_animation(
        "idle"
    ) is True
    assert animator.current_name == "run"
    assert obj.image_path == "run.png"
    assert animator.remove_animation(
        "missing"
    ) is False


def test_sprite_animator_clear_reports_count():
    animator = SpriteAnimator()
    animator.add_animation(
        "idle",
        ["idle.png"],
    )
    animator.add_animation(
        "run",
        ["run.png"],
    )

    assert animator.clear() == 2
    assert animator.animation_names == []
    assert animator.current_name is None


def test_sprite_animator_rejects_negative_dt():
    animator = SpriteAnimator()

    with pytest.raises(
        SpriteAnimationError,
        match="dt",
    ):
        animator.update(-0.1)
