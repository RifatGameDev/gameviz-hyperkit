# GameViz HyperKit

**GameViz HyperKit** is a lightweight Python SDK for quickly creating **2D hypercasual and hybrid casual game prototypes**.

It is designed for beginners, students, game jam developers, and small teams who want to test simple game ideas faster using Python.

> HyperKit is not a full game engine like Unity, Unreal, or Godot.
> It is a prototype-focused SDK with reusable systems and ready-made templates.

---

## Features

* 2D game prototype structure
* Scene system
* GameObject system
* Tap/click input
* Swipe input
* Score and high-score system
* Save system
* Collision helpers
* Simple physics helpers
* Text label and basic UI helpers
* Responsive virtual canvas scaling
* Ready-made hypercasual game templates
* CLI project generator
* Project metadata with `hyperkit.toml`
* Starter asset folder structure
* Asset loading helpers
* Image rendering support for `GameObject`
* Audio playback helpers
* Animation helpers
* Sprite animation helper
* Particle helper
* Camera shake helper
* Scene transition helper
* Timer and cooldown helpers

---

## Installation

For local development:

```bash
pip install -e .
```

After installation, check if HyperKit is working:

```bash
hyperkit doctor
```

---

## Create a New Game

Create a new project from a template:

```bash
hyperkit new my-game --template tap_counter
cd my-game
python main.py
```

You can also use dash-style names:

```bash
hyperkit new my-game --template tap-counter
```

Generated projects include a starter asset structure:

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

---

## Available Templates

Check available templates:

```bash
hyperkit list-templates
```

Current templates:

| Template       | Command Name                        | Description                                    |
| -------------- | ----------------------------------- | ---------------------------------------------- |
| Tap Counter    | `tap_counter` / `tap-counter`       | Tap/click scoring prototype                    |
| Flappy Mini    | `flappy_mini` / `flappy-mini`       | Flappy-style tap-to-jump prototype             |
| Swipe Runner   | `swipe_runner` / `swipe-runner`     | 3-lane swipe runner prototype                  |
| Puzzle Game    | `puzzle_game` / `puzzle-game`       | Color matching puzzle prototype                |
| Quiz Game      | `quiz_game` / `quiz-game`           | Educational quiz game prototype                |
| Simple Physics | `simple_physics` / `simple-physics` | Gravity, bounce, and coin collection prototype |

---

## Examples

Official example projects are available in the `examples/` folder.

Examples include:

* `basic_tap_demo`
* `swipe_input_demo`
* `score_highscore_demo`
* `asset_loading_demo`
* `image_rendering_demo`
* `audio_playback_demo`
* `animation_demo`
* `sprite_animation_demo`

Run an example:

```bash
cd examples/basic_tap_demo
python main.py
```

---

## Example Usage

```python
from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel


class MyScene(Scene):
    def start(self):
        self.score = ScoreManager(high_score_key="my_game_high_score")

        self.player = self.add(
            GameObject(
                x=300,
                y=500,
                width=100,
                height=100,
                color=(0.2, 0.75, 1.0, 1),
                shape="circle",
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=30,
                y=1180,
                text="Score: 0",
                font_size=32,
                color=(1, 1, 1, 1),
            )
        )

        self.start_game()

    def on_tap(self, x, y):
        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2
        self.score.add(1)
        self.score_label.set_text(f"Score: {self.score.value}")


Game(title="My HyperKit Game", width=720, height=1280).set_scene(MyScene()).run()
```

---

## Asset Loading

HyperKit projects include an `assets/` folder:

```text
assets/
├── images/
├── audio/
├── fonts/
└── data/
```

Use `AssetManager` to load assets:

```python
from hyperkit import AssetManager

assets = AssetManager()

player_image = assets.load_image("player.png")
jump_sound = assets.load_audio("jump.wav")
game_font = assets.load_font("game_font.ttf")

level_data = assets.load_json("level.json")
items = assets.load_csv("items.csv")
message = assets.load_text("message.txt")
```

Supported asset types:

| Folder          | Supported Types                  |
| --------------- | -------------------------------- |
| `assets/images` | `.png`, `.jpg`, `.jpeg`, `.webp` |
| `assets/audio`  | `.wav`, `.mp3`, `.ogg`           |
| `assets/fonts`  | `.ttf`, `.otf`                   |
| `assets/data`   | `.json`, `.csv`, `.txt`          |

> FBX is not directly supported in HyperKit v0.2.
> Export FBX source assets as PNG frames or sprite sheets before using them in a HyperKit game.

---

## Image Rendering

HyperKit can render images using `GameObject(image_path=...)`.

```python
from hyperkit import AssetManager, GameObject

assets = AssetManager()
player_image = assets.load_image("player.png")

player = GameObject(
    x=300,
    y=500,
    width=120,
    height=120,
    image_path=player_image,
)
```

If `image_path` is provided, HyperKit renders the image.
If `image_path` is empty, HyperKit renders the normal shape and color.

---

## Audio Playback

HyperKit includes a simple `AudioManager` for sound effects and background music.

```python
from hyperkit import AssetManager, AudioManager

assets = AssetManager()
audio = AudioManager()

click_sound = assets.load_audio("click.wav")
audio.play_sound(click_sound)
```

Background music example:

```python
music = assets.load_audio("background.wav")

audio.play_music(music, loop=True)
audio.stop_music()
```

Supported audio types:

| Folder         | Supported Types        |
| -------------- | ---------------------- |
| `assets/audio` | `.wav`, `.mp3`, `.ogg` |

For best compatibility during development, use `.wav` for sound effects.

---

## Animation Helpers

HyperKit includes simple tween animation helpers for object movement, size, and color.

```python
from hyperkit import AnimationManager, GameObject

animations = AnimationManager()

player = GameObject(x=100, y=100, width=100, height=100)

animations.move_to(player, x=400, y=600, duration=0.5)
animations.resize_to(player, width=150, height=150, duration=0.3)
animations.color_to(player, color=(1, 0.5, 0.2, 1), duration=0.5)
```

Update animations inside your scene update method:

```python
def update(self, dt):
    animations.update(dt)
    super().update(dt)
```

Supported easing names:

```text
linear
ease_in_quad
ease_out_quad
ease_in_out_quad
```

---

## Sprite Animation

HyperKit supports simple frame-based sprite animation using `SpriteAnimator`.

```python
from hyperkit import AssetManager, GameObject, SpriteAnimator

assets = AssetManager()

player = GameObject(
    x=300,
    y=500,
    width=120,
    height=120,
)

sprite = SpriteAnimator(player)

sprite.add_animation(
    "run",
    frames=[
        assets.load_image("run_1.png"),
        assets.load_image("run_2.png"),
        assets.load_image("run_3.png"),
    ],
    fps=8,
    loop=True,
)

sprite.play("run")
```

Update the sprite animation inside your scene update method:

```python
def update(self, dt):
    sprite.update(dt)
    super().update(dt)
```

---

## Particle Effects

HyperKit includes a simple `ParticleEmitter` for burst effects.

```python
from hyperkit import ParticleEmitter

particles = ParticleEmitter(self)

particles.burst(
    x=300,
    y=500,
    count=20,
)
```

Update particles inside your scene update method:

```python
def update(self, dt):
    particles.update(dt)
    super().update(dt)
```

---

## Camera Shake

HyperKit includes a simple `CameraShake` helper for impact feedback.

```python
from hyperkit import CameraShake

camera_shake = CameraShake(self)

camera_shake.shake(intensity=18, duration=0.35)
```

Update camera shake inside your scene update method:

```python
def update(self, dt):
    camera_shake.update(dt)
    super().update(dt)
```

---

## Scene Transitions

HyperKit includes a simple `SceneTransition` helper for fade-in and fade-out scene changes.

```python
from hyperkit import SceneTransition

self.transition = SceneTransition(self)
self.transition.fade_in(duration=0.4)
```

To change scenes with a fade-out:

```python
self.transition.fade_to_scene(NextScene(), duration=0.4)
```

Update transitions inside your scene update method:

```python
def update(self, dt):
    self.transition.update(dt)
    super().update(dt)
```

---

## Timers and Cooldowns

HyperKit includes timer helpers for delayed actions, repeating actions, and cooldown-based gameplay.

```python
from hyperkit import Cooldown, Timer

spawn_timer = Timer(
    duration=1.0,
    repeat=True,
    on_complete=spawn_enemy,
)

jump_cooldown = Cooldown(duration=0.5)
```

Update timers inside your scene update method:

```python
def update(self, dt):
    spawn_timer.update(dt)
    jump_cooldown.update(dt)
    super().update(dt)
```

Use cooldowns to limit actions:

```python
if jump_cooldown.use():
    player_jump()
```

---

## CLI Commands

```bash
hyperkit doctor
```

Check the local HyperKit environment, Python version, Kivy installation, and build tool status.

```bash
hyperkit list-templates
```

Show all available HyperKit game templates.

```bash
hyperkit info
```

Show project metadata from `hyperkit.toml`.

```bash
hyperkit validate
```

Validate the current HyperKit project structure.

```bash
hyperkit new my-game --template tap_counter
```

Create a new game project from a template.

You can use underscore-style names:

```bash
hyperkit new my-game --template tap_counter
```

Or dash-style names:

```bash
hyperkit new my-game --template tap-counter
```

Available templates:

```text
tap_counter / tap-counter
flappy_mini / flappy-mini
swipe_runner / swipe-runner
puzzle_game / puzzle-game
quiz_game / quiz-game
simple_physics / simple-physics
```

```bash
hyperkit run
```

Run a HyperKit project from the current folder.

```bash
hyperkit run --path path/to/project
```

Run a HyperKit project from a specific folder.

```bash
hyperkit init-android
```

Create experimental Android build configuration.

```bash
hyperkit init-android --title "My Game"
```

Create Android configuration with a custom game title.

```bash
hyperkit build android
```

Experimental Android build command.

> Android build support is still experimental and will be improved in future versions.

---

## Current Status

HyperKit is currently in active development.

Current version goal:

```text
0.2.x = SDK core + multiple working templates
```

Stable public release target:

```text
1.0.0 = polished SDK, documentation, tests, examples, and mobile build support
```

---

## Current Limitations

* This is not a full game engine.
* Advanced 3D rendering is not supported.
* Android APK build support is still experimental.
* The current focus is 2D hypercasual and hybrid casual prototypes.
* Templates are designed for learning and prototyping, not final commercial game production yet.

---

## Roadmap

Planned improvements:

* Better UI system
* More game templates
* Asset loading improvements
* Audio helper improvements
* Sprite animation improvements
* Particle helper
* Improved mobile touch support
* Android Gradle / Chaquopy build pipeline
* AdMob / analytics helper layer
* Better documentation and examples

---

## Development

Run tests:

```bash
pytest
```

Build package:

```bash
python -m build
```

Check package:

```bash
twine check dist/*
```

---

## License

MIT License.

---

## Author

Developed by **Md. Rifat Hossain Chowdhury** / **GameViz**.
