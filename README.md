# GameViz HyperKit

**GameViz HyperKit** is a lightweight Python SDK for building 2D hypercasual and hybrid-casual mobile game prototypes.

It is not a Unity/Godot replacement. It is a beginner-friendly SDK for fast prototypes, educational games, templates, and simple mobile-ready 2D game ideas.

## What it targets

- 2D hypercasual games
- Tap games
- Swipe games
- Endless runner prototypes
- Puzzle games
- Simple physics games
- Educational mobile games
- Internal game templates

## Install locally during development

```bash
pip install -e .
```

## Create a new game

```bash
hyperkit new tap-game
cd tap-game
python main.py
```

## Build Android APK

Android APK builds use Kivy + Buildozer.

On Linux/macOS or Windows WSL:

```bash
pip install buildozer
hyperkit init-android
hyperkit build android
```

The APK will be created by Buildozer under the `bin/` folder.

## Minimal example

```python
from hyperkit import Game, Scene, GameObject

class MainScene(Scene):
    def start(self):
        self.player = GameObject(x=320, y=240, width=80, height=80)
        self.add(self.player)

    def on_tap(self, x, y):
        self.player.x = x - self.player.width / 2
        self.player.y = y - self.player.height / 2

Game(title="Tap Game").set_scene(MainScene()).run()
```

## CLI commands

```bash
hyperkit new my-game
hyperkit new my-game --template flappy-mini
hyperkit run
hyperkit init-android
hyperkit build android
hyperkit doctor
```

## Current status

Version `0.1.0` is an alpha MVP.
