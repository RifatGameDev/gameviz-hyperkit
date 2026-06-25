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

- `basic_tap_demo`
- `swipe_input_demo`
- `score_highscore_demo`

Run an example:

```bash
cd examples/basic_tap_demo
python main.py

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

    def on_tap(self, x, y):
        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2
        self.score.add(1)
        self.score_label.set_text(f"Score: {self.score.value}")


Game(title="My HyperKit Game", width=720, height=1280).set_scene(MyScene()).run()
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

Example output includes:

```text
Name
Template
Template folder
Created by
HyperKit version
Main file
```

```bash
hyperkit validate
```

Validate the current HyperKit project structure.

It checks whether the project has:

```text
main.py
hyperkit.toml
valid template metadata
```

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
* Asset loading
* Audio helper
* Animation helper
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
