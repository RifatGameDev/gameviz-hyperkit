import pytest

from hyperkit import Cooldown, Timer, TimerError, TimerManager


def test_timer_requires_positive_duration():
    with pytest.raises(TimerError):
        Timer(0)


def test_timer_completes_after_duration():
    completed = {"value": False}

    timer = Timer(1.0, on_complete=lambda: completed.update(value=True))

    fired = timer.update(1.0)

    assert fired is True
    assert completed["value"] is True
    assert timer.completed
    assert not timer.active


def test_timer_does_not_complete_early():
    timer = Timer(1.0)

    fired = timer.update(0.5)

    assert fired is False
    assert not timer.completed
    assert timer.remaining == 0.5


def test_repeating_timer_stays_active():
    count = {"value": 0}

    timer = Timer(1.0, repeat=True, on_complete=lambda: count.update(
        value=count["value"] + 1))

    timer.update(1.0)

    assert count["value"] == 1
    assert timer.active
    assert not timer.completed


def test_timer_pause_and_resume():
    timer = Timer(1.0)

    timer.pause()
    timer.update(1.0)

    assert not timer.completed

    timer.resume()
    timer.update(1.0)

    assert timer.completed


def test_timer_restart_resets_timer():
    timer = Timer(1.0)

    timer.update(1.0)
    assert timer.completed

    timer.restart()

    assert timer.elapsed == 0.0
    assert not timer.completed
    assert timer.active


def test_cooldown_starts_ready_by_default():
    cooldown = Cooldown(1.0)

    assert cooldown.ready


def test_cooldown_use_resets_progress():
    cooldown = Cooldown(1.0)

    assert cooldown.use() is True
    assert not cooldown.ready
    assert cooldown.remaining == 1.0


def test_cooldown_blocks_until_ready():
    cooldown = Cooldown(1.0)

    assert cooldown.use() is True
    assert cooldown.use() is False

    cooldown.update(0.5)

    assert cooldown.use() is False

    cooldown.update(0.5)

    assert cooldown.use() is True


def test_cooldown_finish_makes_ready():
    cooldown = Cooldown(1.0, start_ready=False)

    assert not cooldown.ready

    cooldown.finish()

    assert cooldown.ready


def test_timer_manager_after_removes_completed_timer():
    count = {"value": 0}

    manager = TimerManager()
    manager.after(1.0, lambda: count.update(value=count["value"] + 1))

    manager.update(1.0)

    assert count["value"] == 1
    assert manager.timers == []


def test_timer_manager_every_keeps_repeating_timer():
    count = {"value": 0}

    manager = TimerManager()
    manager.every(1.0, lambda: count.update(value=count["value"] + 1))

    manager.update(1.0)
    manager.update(1.0)

    assert count["value"] == 2
    assert len(manager.timers) == 1


def test_timer_manager_clear_stops_all_timers():
    manager = TimerManager()

    manager.after(1.0, lambda: None)
    manager.every(1.0, lambda: None)

    manager.clear()

    assert manager.timers == []



def test_repeating_timer_fires_multiple_intervals_from_large_dt():
    count = {"value": 0}

    timer = Timer(
        1.0,
        repeat=True,
        on_complete=lambda: count.update(
            value=count["value"] + 1
        ),
    )

    assert timer.update(2.5) is True
    assert count["value"] == 2
    assert timer.times_fired == 2
    assert timer.elapsed == pytest.approx(0.5)


def test_timer_rejects_negative_dt():
    timer = Timer(1.0)

    with pytest.raises(
        TimerError,
        match="dt",
    ):
        timer.update(-0.1)


def test_cooldown_rejects_negative_dt():
    cooldown = Cooldown(1.0)

    with pytest.raises(
        TimerError,
        match="dt",
    ):
        cooldown.update(-0.1)


def test_timer_lifecycle_methods_are_chainable():
    timer = Timer(
        1.0,
        auto_start=False,
    )

    assert timer.start() is timer
    assert timer.pause() is timer
    assert timer.resume() is timer
    assert timer.stop() is timer
    assert timer.reset() is timer


def test_timer_manager_can_remove_timer():
    manager = TimerManager()
    timer = manager.after(
        1.0,
        lambda: None,
    )

    assert manager.remove(timer) is True
    assert timer.completed
    assert manager.timers == []
    assert manager.remove(timer) is False


def test_timer_manager_pause_and_resume_all():
    manager = TimerManager()
    first = manager.after(
        1.0,
        lambda: None,
    )
    second = manager.every(
        1.0,
        lambda: None,
    )

    manager.pause_all()

    assert not first.active
    assert not second.active

    manager.resume_all()

    assert first.active
    assert second.active


def test_timer_manager_rejects_negative_dt():
    manager = TimerManager()

    with pytest.raises(
        TimerError,
        match="dt",
    ):
        manager.update(-0.1)
