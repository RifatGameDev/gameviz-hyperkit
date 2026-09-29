# HyperKit v0.6 — Mobile Production Runtime + Performance

HyperKit v0.6 hardens the runtime for real mobile game loops.

## Scope

The v0.6 milestone focuses on:

- frame-time protection
- fixed-step simulation support
- mobile performance profiles
- lifecycle reliability
- runtime service lifecycle propagation
- scene/resource cleanup
- touch-noise filtering
- Android/mobile runtime guidance

## Performance Profiles

HyperKit provides three common presets:

- `battery`
- `balanced`
- `performance`

Example:

```python
from hyperkit import Game, PerformanceProfile

profile = PerformanceProfile.from_mode("battery")

game = Game(
    title="My Game",
    performance_profile=profile,
)
```

When a performance profile is supplied to `Game`, the profile controls
the target FPS.

## Frame Hitch Protection

`FrameTimeController` clamps unusually large frame deltas before they
reach game-scene updates.

This protects physics, movement, timers, and other frame-dependent systems
from large jumps after stalls, app switching, debugger pauses, or device
load spikes.

The default balanced profile limits one scene update to 100 ms.

Game runtime statistics are available with:

```python
stats = game.performance_stats()
```

The result includes:

- target FPS
- processed frame count
- hitch count
- total clamped time
- latest raw delta
- latest normalized delta

## Fixed-Step Simulation

`FixedStepClock` converts variable frame time into bounded fixed simulation
steps.

Example:

```python
from hyperkit import FixedStepClock

clock = FixedStepClock(
    step=1 / 60,
    max_substeps=5,
)

steps = clock.advance(dt)

for _ in range(steps):
    update_physics(clock.step)
```

The clock drops excessive backlog instead of allowing an unbounded
"spiral of death" after a long frame.

## Lifecycle Reliability

The game runtime now has explicit scene hooks:

- `on_pause()`
- `on_background()`
- `on_resume()`
- `on_stop()`

`Game.stop()` is idempotent and is used by the Kivy application stop
callback.

Active touches are cancelled when the game is paused, backgrounded, or
stopped so stale finger state cannot leak across mobile lifecycle changes.

## Runtime Service Lifecycle

All services registered in `SDKContext` may opt into:

- `on_runtime_start()`
- `on_runtime_pause()`
- `on_runtime_background()`
- `on_runtime_resume()`
- `on_runtime_stop()`

The same service registered under more than one name is notified only once
per lifecycle event.

`AudioManager` uses these hooks to pause music when suspended, resume it
when the runtime returns, and stop audio during runtime shutdown.

## Scene Resource Cleanup

`Scene.release_resources()`:

- calls `dispose()`, `close()`, or `release()` on disposable scene
  objects when available
- clears scene objects
- returns the number of released scene objects

Scene changes release the previous scene before starting the next scene.
Released scenes are marked as not started so they can be reused later.

## Runtime Safe-Area Updates

Mobile safe areas may change with device posture, system UI, or runtime
configuration. HyperKit v0.6 supports replacing safe-area insets without
recreating the game:

```python
from hyperkit import SafeAreaInsets

game.update_safe_area(
    SafeAreaInsets(
        left=0,
        right=0,
        top=32,
        bottom=20,
    )
)
```

`MobileDisplayProfile.with_safe_area(...)` returns a new immutable profile
with the updated insets.

## Touch Input Tuning

`TouchTracker` supports `move_min_distance`.

Small pointer movement below that threshold is filtered before
`on_touch_move` reaches the scene.

```python
game = Game(
    touch_move_min_distance=3,
)
```

This can reduce noisy move events on mobile touchscreens without changing
tap or swipe detection.

`TouchTracker.cancel_all()` returns the number of active pointers that
were cancelled.

## Android Guidance

For production-oriented mobile testing:

1. Use `balanced` first.
2. Test `performance` on devices where 60 FPS is important.
3. Use `battery` for slower-paced games where 30 FPS is acceptable.
4. Profile real devices, not only desktop.
5. Test pause → background → resume repeatedly.
6. Test interrupted touches during lifecycle changes.
7. Test long frame hitches and verify movement/physics do not jump.
8. Verify music and runtime services recover correctly after resume.

## v0.6 Completion Rule

The v0.6 development milestone is complete when:

- performance profile tests pass
- frame-hitch clamping tests pass
- fixed-step backlog protection tests pass
- lifecycle stress and idempotency tests pass
- scene resource cleanup tests pass
- touch filtering tests pass
- runtime service lifecycle tests pass
- all v0.5 complete-game and developer-tooling regressions remain green
- Python 3.9–3.12 CI remains green
- package build and `twine check` remain green

The public compatibility contract remains API `0.2`.
The public API freeze remains scheduled for v0.9.
