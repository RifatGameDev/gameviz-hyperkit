# GameViz HyperKit

**GameViz HyperKit** is a lightweight Python SDK for creating **2D hypercasual and hybrid casual game prototypes** quickly.

It is designed for beginners, students, game jam developers, indie developers, and small teams who want to test simple mobile-style game ideas using Python.

> HyperKit is not a full game engine like Unity, Unreal, or Godot.  
> It is a prototype-focused SDK with reusable systems, helper modules, and ready-made templates.

---

## Current Release Status

HyperKit is currently in active development.

Current package validation status:

- TestPyPI validation build: `0.1.1.dev1`
- Real PyPI release: not published yet
- Stable public release target: future `1.0.0`

For now, HyperKit should be considered an early SDK preview.

---

## Package Identity

- Package name: `gameviz-hyperkit`
- Import name: `hyperkit`
- CLI command: `hyperkit`

---

## Who Is HyperKit For?

HyperKit is useful for:

- learning 2D game development with Python
- building quick hypercasual game prototypes
- creating tap, swipe, runner, puzzle, quiz, and physics-style demos
- testing simple game ideas before moving to a larger engine
- students and indie developers who want a small code-first game toolkit

---

## Main Features

- 2D game project structure
- Scene system
- GameObject system
- Tap/click input
- Swipe input
- Score and high-score system
- Save system
- Collision helpers
- Simple physics helpers
- Text label and basic UI helpers
- Responsive virtual canvas scaling
- Asset loading helpers
- Image rendering support
- Audio playback helpers
- Animation helpers
- Sprite animation helper
- Particle helper
- Camera shake helper
- Scene transition helper
- Timer and cooldown helpers
- Input action mapping helper
- Level data loading helper
- Camera follow helper
- Screen bounds and world bounds helpers
- UI progress bar helper
- CLI project generator
- Ready-made starter templates
- Project health and release validation commands

---

## Installation

For local development from the repository:

```bash
pip install -e .
```

Check that HyperKit is working:

```bash
hyperkit doctor
```

Install the current TestPyPI validation build:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gameviz-hyperkit==0.1.1.dev1
```

---

## Quick Start

Create a new game project:

```bash
hyperkit new my-game --template tap_counter
cd my-game
python main.py
```

You can also use dash-style template names:

```bash
hyperkit new my-game --template tap-counter
```

Generated projects include:

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

Check all templates:

```bash
hyperkit list-templates
```

Current templates:

| Template | Command Name | Description |
| --- | --- | --- |
| Tap Counter | `tap_counter` / `tap-counter` | Tap/click scoring prototype |
| Flappy Mini | `flappy_mini` / `flappy-mini` | Flappy-style tap-to-jump prototype |
| Swipe Runner | `swipe_runner` / `swipe-runner` | 3-lane swipe runner prototype |
| Puzzle Game | `puzzle_game` / `puzzle-game` | Color matching puzzle prototype |
| Quiz Game | `quiz_game` / `quiz-game` | Educational quiz game prototype |
| Simple Physics | `simple_physics` / `simple-physics` | Gravity, bounce, and coin collection prototype |

---

## Basic Example

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

## Asset Folders

HyperKit projects use a simple asset structure:

```text
assets/
├── images/
├── audio/
├── fonts/
└── data/
```

Supported asset types:

| Folder | Supported Types |
| --- | --- |
| `assets/images` | `.png`, `.jpg`, `.jpeg`, `.webp` |
| `assets/audio` | `.wav`, `.mp3`, `.ogg` |
| `assets/fonts` | `.ttf`, `.otf` |
| `assets/data` | `.json`, `.csv`, `.txt` |

> FBX is not directly supported in HyperKit.  
> For 2D games, export FBX source assets as PNG images, animation frames, or sprite sheets.

---

## CLI Commands

Check environment:

```bash
hyperkit doctor
```

Show templates:

```bash
hyperkit list-templates
```

Create a new project:

```bash
hyperkit new my-game --template tap_counter
```

Run a project:

```bash
hyperkit run
```

Show project metadata:

```bash
hyperkit info
```

Validate a generated project:

```bash
hyperkit validate
```

Show package health report:

```bash
hyperkit health
```

Show release readiness report:

```bash
hyperkit release-check
```

Show final pre-release audit report:

```bash
hyperkit pre-release-audit
```

Create experimental Android build configuration:

```bash
hyperkit init-android
```

Run experimental Android build:

```bash
hyperkit build android
```

---

## Development Commands

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

Upload to TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

---

## Documentation

- [Version History](docs/VERSION_HISTORY.md)
- [Changelog](CHANGELOG.md)
- [Template Helper Usage Guide](docs/TEMPLATE_HELPERS.md)
- [Templates Guide](docs/TEMPLATES.md)
- [Template Quality Checklist](docs/TEMPLATE_QUALITY_CHECKLIST.md)
- [Release Readiness Checklist](docs/RELEASE_READINESS_CHECKLIST.md)
- [Generated Project Smoke Tests](docs/GENERATED_PROJECT_SMOKE_TESTS.md)
- [Project Health Report](docs/PROJECT_HEALTH_REPORT.md)
- [Release Build Automation](docs/RELEASE_BUILD_AUTOMATION.md)
- [Final Pre-release Audit](docs/FINAL_PRE_RELEASE_AUDIT.md)
- [Beginner Quick Start Tutorial](docs/QUICK_START_TUTORIAL.md)

---

## Current Limitations

- HyperKit is not a full game engine.
- Advanced 3D rendering is not supported.
- Android APK build support is still experimental.
- AdMob and analytics helpers are not implemented yet.
- The current focus is 2D hypercasual and hybrid casual prototypes.
- Templates are designed for learning and prototyping, not final commercial production yet.

---

## Roadmap

Planned improvements:

- better beginner documentation
- more polished starter templates
- template screenshots and GIFs
- improved CLI error messages
- stronger asset and audio workflow
- mobile-friendly project structure
- Android build workflow improvements
- AdMob and analytics helper layer
- more complete example games
- future stable `1.0.0` release

---

## License

MIT License.

---

## Author

Developed by **Md. Rifat Hossain Chowdhury** / **GameViz**.