# Template Helper Usage Guide

This guide explains how HyperKit starter templates use helper systems to make mobile 2D game prototypes easier to build.

HyperKit templates are designed for small mobile-friendly games such as tap games, runners, puzzle games, quiz games, and simple physics games.

---

## Upgraded Templates

The following templates currently demonstrate helper-based implementation:

- `tap_counter`
- `flappy_mini`
- `swipe_runner`
- `puzzle_game`
- `quiz_game`
- `simple_physics`

Create a template project:

```bash
hyperkit new my-game --template tap_counter
cd my-game
python main.py
```

---

## Helper Systems Used in Templates

### AssetManager

`AssetManager` loads files from the generated project's `assets` folder.

Common use:

```python
from pathlib import Path
from hyperkit import AssetManager

assets = AssetManager(project_path=Path(__file__).parent)
player_image = assets.load_image("player.png")
```

Templates use this for image-based GameObjects.

---

### Image-Based GameObjects

GameObjects can use an image instead of a plain color shape.

```python
from hyperkit import GameObject

player = GameObject(
    x=300,
    y=560,
    width=120,
    height=120,
    image_path=player_image,
    name="player",
)
```

If `image_path` is set, HyperKit draws the image. Otherwise, it draws the normal rectangle or circle.

---

### ScoreManager

`ScoreManager` handles current score and high score.

```python
from hyperkit import ScoreManager

score = ScoreManager(high_score_key="my_game_high_score")
score.add(1)
```

Templates use it for score, best score, quiz correct count, puzzle matches, and runner score.

---

### ProgressBar

`ProgressBar` creates a UI bar using HyperKit objects.

```python
from hyperkit import ProgressBar

progress = ProgressBar(
    scene=self,
    x=60,
    y=1015,
    width=600,
    height=32,
    value=0,
    max_value=10,
    text_format="Progress: {value:.0f}/{max_value:.0f}",
)
```

Templates use it for target score, distance, quiz progress, puzzle matches, and energy.

---

### ParticleEmitter

`ParticleEmitter` creates simple visual feedback.

```python
from hyperkit import ParticleEmitter

particles = ParticleEmitter(self)

particles.burst(
    x=300,
    y=500,
    count=20,
)
```

Always update particles in the scene update loop:

```python
def update(self, dt):
    particles.update(dt)
    super().update(dt)
```

Templates use particles for taps, coins, correct answers, collisions, and completion feedback.

---

### CameraShake

`CameraShake` adds impact feedback.

```python
from hyperkit import CameraShake

camera_shake = CameraShake(self)
camera_shake.shake(intensity=18, duration=0.25)
```

Always update camera shake in the scene update loop:

```python
def update(self, dt):
    camera_shake.update(dt)
    super().update(dt)
```

Templates use camera shake for wrong answers, collisions, scoring, and completion feedback.

---

### BoundsManager

`BoundsManager` keeps objects inside the screen or world.

```python
from hyperkit import BoundsManager, ScreenBounds

bounds = BoundsManager(
    screen=ScreenBounds(width=720, height=1280)
)

bounds.keep_on_screen(player)
bounds.bounce_on_screen(ball)
```

Templates use bounds for player movement, ball bounce, and screen safety.

---

### InputActionMap

`InputActionMap` maps taps, area taps, and swipes to named actions.

```python
from hyperkit import InputActionMap

actions = InputActionMap()

actions.map_tap("jump", callback=jump)
actions.map_swipe("move_left", direction="left", callback=move_left)
actions.map_area(
    "attack",
    x=200,
    y=500,
    width=300,
    height=120,
    callback=attack,
)
```

Use it from scene input methods:

```python
def on_tap(self, x, y):
    actions.handle_tap(x, y)

def on_swipe(self, start, end, direction):
    actions.handle_swipe(start, end, direction)
```

Templates use it for tap scoring, answer buttons, puzzle tiles, flapping, and swipe movement.

---

### Cooldown

`Cooldown` limits how often an action can happen.

```python
from hyperkit import Cooldown

launch_cooldown = Cooldown(duration=0.4)

if launch_cooldown.use():
    launch_ball()
```

Always update cooldowns:

```python
def update(self, dt):
    launch_cooldown.update(dt)
    super().update(dt)
```

The Simple Physics template uses this for launch timing.

---

## Recommended Template Structure

Generated projects should use this structure:

```text
my-game/
├── main.py
├── README.md
├── hyperkit.toml
└── assets/
    ├── README.md
    ├── images/
    ├── audio/
    ├── fonts/
    └── data/
```

Templates can auto-generate simple placeholder assets, but real projects should replace those files with proper game art.

---

## Template Upgrade Checklist

When upgrading or creating a HyperKit template, check these items:

- Uses `AssetManager` if visual assets are needed
- Uses image-based `GameObject` when possible
- Uses `ScoreManager` for score/high-score flow
- Uses `ProgressBar` for goals, energy, distance, health, or quiz progress
- Uses `ParticleEmitter` for feedback
- Uses `CameraShake` for impact feedback
- Uses `BoundsManager` for screen/world safety
- Uses `InputActionMap` for clean input handling
- Uses `Cooldown` for repeated actions when needed
- Includes a clean template `README.md`
- Works after `hyperkit new`
- Passes syntax and template tests

---

## Current Template Helper Matrix

| Template | Assets | Score | Progress | Particles | Shake | Bounds | Input Actions | Cooldown |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tap_counter` | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No |
| `flappy_mini` | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No |
| `swipe_runner` | Yes | Yes | Yes | Yes | Yes | No | Yes | No |
| `puzzle_game` | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No |
| `quiz_game` | No | Yes | Yes | Yes | Yes | No | Yes | No |
| `simple_physics` | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes |

---

## Notes

The helper systems are optional. A very small prototype can still use only `Game`, `Scene`, and `GameObject`.

For better production-style templates, prefer helper-based structure because it makes code easier to read, test, and extend.
