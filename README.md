# GameViz HyperKit

[![PyPI Version](https://img.shields.io/pypi/v/gameviz-hyperkit)](https://pypi.org/project/gameviz-hyperkit/)
[![Python Versions](https://img.shields.io/pypi/pyversions/gameviz-hyperkit)](https://pypi.org/project/gameviz-hyperkit/)
[![License](https://img.shields.io/pypi/l/gameviz-hyperkit)](LICENSE)

**GameViz HyperKit** is a lightweight Python SDK for creating **2D hypercasual and hybrid-casual game prototypes** quickly.

It is designed for beginners, students, game-jam developers, indie developers, and small teams who want to test simple mobile-style game ideas using Python.

> HyperKit is not a full game engine like Unity, Unreal Engine, or Godot.  
> It is a prototype-focused SDK with reusable systems, helper modules, and ready-made templates.

---

## Current Release Status

HyperKit is publicly available on PyPI and remains in active alpha development.

Current package status:

- Current package version: `0.1.2`
- Installation command: `pip install gameviz-hyperkit`
- Package maturity: Alpha / early SDK preview
- API stability target: future `1.0.0`
- Supported Python versions: Python 3.9–3.12

HyperKit is suitable for learning, prototyping, game jams, and early 2D mobile game experiments. It is not yet intended to replace a full production game engine.

---

## Package Identity

- Package name: `gameviz-hyperkit`
- Import name: `hyperkit`
- CLI command: `hyperkit`
- License: MIT

---

## Project Links

- [PyPI Package](https://pypi.org/project/gameviz-hyperkit/)
- [GitHub Repository](https://github.com/RifatGameDev/gameviz-hyperkit)
- [Issue Tracker](https://github.com/RifatGameDev/gameviz-hyperkit/issues)
- [Changelog](CHANGELOG.md)
- [Version History](docs/VERSION_HISTORY.md)

---

## Who Is HyperKit For?

HyperKit is useful for:

- Learning 2D game development with Python
- Building quick hypercasual game prototypes
- Creating tap, swipe, runner, puzzle, quiz, and physics-style demos
- Testing simple game concepts before moving to a larger engine
- Building game-jam and educational projects
- Students and indie developers who want a small code-first game toolkit

---

## Main Features

- 2D game project structure
- Scene system
- GameObject system
- Tap and click input
- Swipe input
- Input action mapping
- Score and high-score system
- Save and persistence system
- Collision helpers
- Simple physics helpers
- Text labels and basic UI helpers
- Responsive virtual canvas scaling
- Asset loading helpers
- Image rendering support
- Audio playback helpers
- Tween and animation helpers
- Sprite animation helper
- Particle helper
- Camera shake helper
- Scene transition helper
- Timer and cooldown helpers
- Level data loading helper
- Camera follow helper
- Screen and world-bound helpers
- UI progress bar helper
- CLI project generator
- Ready-made starter templates
- Generated-project validation
- Project health and release validation commands
- Experimental Android build configuration

---

## Installation

### Install from PyPI

```bash
pip install gameviz-hyperkit
```

Verify the installation:

```bash
hyperkit doctor
hyperkit list-templates
```

### Install for Local Development

Clone the repository:

```bash
git clone https://github.com/RifatGameDev/gameviz-hyperkit.git
cd gameviz-hyperkit
```

Install HyperKit in editable development mode:

```bash
pip install -e ".[dev]"
```

Run the tests:

```bash
pytest
```

---

## Quick Start

Create a Tap Counter project:

```bash
hyperkit new my-game --template tap-counter
cd my-game
hyperkit run
```

You may also launch the generated project directly:

```bash
python main.py
```

The name `my-game` is only an example. You can choose another project name:

```bash
hyperkit new flappy-project --template flappy-mini
cd flappy-project
hyperkit run
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

List all templates:

```bash
hyperkit list-templates
```

| Template | Command Name | Description |
| --- | --- | --- |
| Tap Counter | `tap-counter` | Tap or click scoring prototype |
| Flappy Mini | `flappy-mini` | Flappy-style tap-to-jump prototype |
| Swipe Runner | `swipe-runner` | Three-lane swipe runner prototype |
| Puzzle Game | `puzzle-game` | Color-matching puzzle prototype |
| Quiz Game | `quiz-game` | Educational quiz prototype |
| Simple Physics | `simple-physics` | Gravity, bounce, and coin-collection prototype |

Underscore-style aliases are also accepted:

```text
tap_counter
flappy_mini
swipe_runner
puzzle_game
quiz_game
simple_physics
```

---

## Basic Example

```python
from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel


class MyScene(Scene):
    def start(self):
        self.score = ScoreManager(
            high_score_key="my_game_high_score"
        )

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
        self.score_label.set_text(
            f"Score: {self.score.value}"
        )


game = Game(
    title="My HyperKit Game",
    width=720,
    height=1280,
)

game.set_scene(MyScene())
game.run()
```

---

## Asset Folders

Generated HyperKit projects use this asset structure:

```text
assets/
├── images/
├── audio/
├── fonts/
└── data/
```

| Folder | Supported Types |
| --- | --- |
| `assets/images` | `.png`, `.jpg`, `.jpeg`, `.webp` |
| `assets/audio` | `.wav`, `.mp3`, `.ogg` |
| `assets/fonts` | `.ttf`, `.otf` |
| `assets/data` | `.json`, `.csv`, `.txt` |

> FBX files are not directly supported.  
> For 2D projects, export source assets as PNG images, animation frames, or sprite sheets.

---

## CLI Commands

### Check the environment

```bash
hyperkit doctor
```

### List templates

```bash
hyperkit list-templates
```

### Create a project

```bash
hyperkit new my-game --template tap-counter
```

### Enter the generated project

```bash
cd my-game
```

### Run the project

```bash
hyperkit run
```

### Show project metadata

```bash
hyperkit info
```

### Validate the current project

```bash
hyperkit validate
```

### Show the package health report

```bash
hyperkit health
```

### Show release readiness

```bash
hyperkit release-check
```

### Run the final pre-release audit

```bash
hyperkit pre-release-audit
```

### Validate built-in templates

```bash
hyperkit validate-templates
```

### Validate generated projects

```bash
hyperkit validate-generated-projects
```

### Validate manual QA evidence

```bash
hyperkit validate-release-evidence
```

### Require complete QA evidence

```bash
hyperkit validate-release-evidence --require-complete
```

### Create experimental Android configuration

```bash
hyperkit init-android
```

### Run the experimental Android build workflow

```bash
hyperkit build android
```

---

## Development Commands

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run the complete test suite:

```bash
pytest
```

Build the wheel and source distribution:

```bash
python -m build
```

Validate the distribution files:

```bash
python -m twine check dist/*
```

Package publication is handled through the project's controlled release workflow.

---

## Documentation

- [Version History](docs/VERSION_HISTORY.md)
- [Changelog](CHANGELOG.md)
- [Templates Guide](docs/TEMPLATES.md)
- [Template Helper Usage Guide](docs/TEMPLATE_HELPERS.md)
- [Template Quality Checklist](docs/TEMPLATE_QUALITY_CHECKLIST.md)
- [Release Readiness Checklist](docs/RELEASE_READINESS_CHECKLIST.md)
- [Generated Project Smoke Tests](docs/GENERATED_PROJECT_SMOKE_TESTS.md)
- [Project Health Report](docs/PROJECT_HEALTH_REPORT.md)
- [Release Build Automation](docs/RELEASE_BUILD_AUTOMATION.md)
- [Final Pre-release Audit](docs/FINAL_PRE_RELEASE_AUDIT.md)
- [Beginner Quick Start Tutorial](docs/QUICK_START_TUTORIAL.md)
- [Template Media Guide](docs/TEMPLATE_MEDIA_GUIDE.md)
- [Template Screenshots and Demo Media](docs/TEMPLATE_SCREENSHOTS.md)
- [CLI Error Messages](docs/CLI_ERROR_MESSAGES.md)
- [Template Validation](docs/TEMPLATE_VALIDATION.md)
- [Production Template Polish Checklist](docs/PRODUCTION_TEMPLATE_POLISH_CHECKLIST.md)
- [Template Stabilization Checklist](docs/TEMPLATE_STABILIZATION_CHECKLIST.md)
- [Template Manual QA Checklist](docs/TEMPLATE_MANUAL_QA_CHECKLIST.md)
- [Manual QA Result Template](docs/MANUAL_QA_RESULT_TEMPLATE.md)
- [Release Evidence Structure](docs/RELEASE_EVIDENCE_STRUCTURE.md)
- [Release Evidence Workspace](docs/release-evidence/README.md)

### Template Polish and Runtime Documentation

- [Tap Counter Polish - Phase 48](docs/TAP_COUNTER_POLISH_PHASE48.md)
- [Flappy Mini Polish - Phase 49](docs/FLAPPY_MINI_POLISH_PHASE49.md)
- [Swipe Runner Polish - Phase 50](docs/SWIPE_RUNNER_POLISH_PHASE50.md)
- [Puzzle Game Polish - Phase 51](docs/PUZZLE_GAME_POLISH_PHASE51.md)
- [Quiz Game Polish - Phase 52](docs/QUIZ_GAME_POLISH_PHASE52.md)
- [Simple Physics Polish - Phase 53](docs/SIMPLE_PHYSICS_POLISH_PHASE53.md)
- [Template Polish Summary - Phase 54](docs/TEMPLATE_POLISH_SUMMARY_PHASE54.md)
- [Generated Project Validation - Phase 55](docs/GENERATED_PROJECT_VALIDATION_PHASE55.md)
- [Template Runtime Readiness - Phase 56](docs/TEMPLATE_RUNTIME_READINESS_PHASE56.md)
- [Runtime QA Tracker - Phase 58](docs/RUNTIME_QA_TRACKER_PHASE58.md)

---
---

## Current Limitations

- HyperKit is not a complete general-purpose game engine.
- Advanced 3D rendering is not supported.
- Android APK build support remains experimental.
- AdMob and analytics helper systems are not implemented yet.
- The current focus is 2D hypercasual and hybrid-casual prototypes.
- Templates are intended for learning and prototyping rather than finished commercial production.
- The public API may change before version `1.0.0`.

---

## Roadmap

Planned improvements include:

- Better beginner documentation
- More polished starter templates
- Template screenshots and animated demonstrations
- Stronger asset and audio workflows
- Improved mobile project structure
- Android build workflow improvements
- AdMob integration helpers
- Analytics integration helpers
- Additional complete example games
- More automated package compatibility testing
- Stable API milestone for version `1.0.0`

---

## Contributing

Contributions, issue reports, and improvement suggestions are welcome.

Before submitting changes:

```bash
pip install -e ".[dev]"
pytest
```

Use the issue tracker to report bugs or request features.

---

## License

GameViz HyperKit is distributed under the MIT License.

See [LICENSE](LICENSE) for details.

---

## Author

Developed by **Md. Rifat Hossain Chowdhury** / **GameViz**.

- GitHub: [RifatGameDev](https://github.com/RifatGameDev)
- PyPI package: [gameviz-hyperkit](https://pypi.org/project/gameviz-hyperkit/)