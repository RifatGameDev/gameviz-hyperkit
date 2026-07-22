# Beginner Quick Start Tutorial

This tutorial helps a new user create their first HyperKit game project.

HyperKit is currently an early SDK preview. For now, the public validation build is available on TestPyPI.

---

## What You Will Build

You will create a small Tap Counter game.

The game will include:

- a game window
- a player object
- tap/click input
- score tracking
- a generated project structure
- starter asset folders

---

## Requirements

You need:

- Python 3.11 recommended
- pip
- a terminal or command prompt
- basic Python knowledge

Optional but recommended:

- Anaconda or Miniconda
- VS Code

---

## Option 1: Install from TestPyPI

Create a clean environment:

```bash
conda create -n hyperkit-tutorial python=3.11 -y
conda activate hyperkit-tutorial
```

Install HyperKit from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gameviz-hyperkit==0.1.1.dev1
```

Check installation:

```bash
hyperkit doctor
```

---

## Option 2: Install from Local Repository

If you cloned the GitHub repository, go to the project root:

```bash
cd path/to/gameviz-hyperkit
```

Install in editable mode:

```bash
pip install -e .
```

Check installation:

```bash
hyperkit doctor
```

---

## Create Your First Game

Create a new Tap Counter project:

```bash
hyperkit new my-first-game --template tap_counter
```

Go inside the generated project:

```bash
cd my-first-game
```

Run the game:

```bash
python main.py
```

A game window should open.

---

## Generated Project Structure

Your generated project will look like this:

```text
my-first-game/
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

Important files:

- `main.py` contains the game code.
- `README.md` explains the generated template.
- `hyperkit.toml` stores project metadata.
- `assets/` contains folders for images, audio, fonts, and data.

---

## Try Other Templates

You can list available templates:

```bash
hyperkit list-templates
```

Create a Flappy Mini game:

```bash
hyperkit new my-flappy-game --template flappy_mini
```

Create a Swipe Runner game:

```bash
hyperkit new my-runner-game --template swipe_runner
```

Create a Puzzle Game:

```bash
hyperkit new my-puzzle-game --template puzzle_game
```

Create a Quiz Game:

```bash
hyperkit new my-quiz-game --template quiz_game
```

Create a Simple Physics game:

```bash
hyperkit new my-physics-game --template simple_physics
```

---

## Basic HyperKit Concepts

HyperKit projects usually use these core concepts:

### Game

`Game` creates the game window and starts the app.

### Scene

`Scene` organizes game objects and game logic.

### GameObject

`GameObject` represents visual objects such as players, enemies, buttons, coins, and labels.

### Input

HyperKit supports tap/click input and swipe input.

### Helpers

HyperKit includes helpers for score, audio, animation, particles, camera shake, timers, bounds, and progress bars.

---

## Example Minimal Game

```python
from hyperkit import Game, GameObject, Scene


class MyScene(Scene):
    def start(self):
        self.player = self.add(
            GameObject(
                x=300,
                y=500,
                width=100,
                height=100,
                color=(0.2, 0.7, 1.0, 1),
                shape="circle",
            )
        )

    def on_tap(self, x, y):
        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2


Game(title="My First HyperKit Game").set_scene(MyScene()).run()
```

---

## Validate Your Project

Inside a generated project, run:

```bash
hyperkit validate
```

If the project is valid, HyperKit will show:

```text
Status: valid
```

---

## Common Problems

### Command not found: hyperkit

Make sure the correct environment is activated.

```bash
conda activate hyperkit-tutorial
```

Then run:

```bash
hyperkit doctor
```

### Python cannot import hyperkit

Reinstall the package:

```bash
pip install -e .
```

Or install from TestPyPI again:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gameviz-hyperkit==0.1.1.dev1
```

### Game window does not open

Make sure Kivy is installed correctly:

```bash
python -c "import kivy; print(kivy.__version__)"
```

---

## Next Steps

After this tutorial, try:

- changing object colors
- changing player size
- adding score
- trying another template
- adding image assets
- adding audio effects
- reading the template helper guide

Recommended next docs:

- [Templates Guide](TEMPLATES.md)
- [Template Helper Usage Guide](TEMPLATE_HELPERS.md)
- [Project Health Report](PROJECT_HEALTH_REPORT.md)