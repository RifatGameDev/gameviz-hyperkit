# Template Quality Checklist

This checklist is used to keep HyperKit templates clean, beginner-friendly, and reliable.

---

## Required Files

Each template should include:

- `main.py`
- `README.md`

---

## Required Template Code Standards

Each template `main.py` should:

- be valid Python syntax
- import from `hyperkit`
- define at least one `Scene` class
- include a `start()` method
- call `self.start_game()`
- include a runnable entry point
- create a `Game(...)`
- call `.set_scene(...)`
- call `.run()`

---

## Required README Sections

Each template README should include:

- template title
- `## Features`
- `## Run`
- `## Gameplay`
- `## Helper Systems Used`

---

## Helper-Based Template Expectations

The upgraded templates should demonstrate the following helper systems where useful:

| Template | Expected Helpers |
|---|---|
| `tap_counter` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `BoundsManager`, `InputActionMap`, `ScoreManager` |
| `flappy_mini` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `BoundsManager`, `InputActionMap`, `ScoreManager` |
| `swipe_runner` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `InputActionMap`, `ScoreManager` |
| `puzzle_game` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `BoundsManager`, `InputActionMap`, `ScoreManager` |
| `quiz_game` | `ProgressBar`, `ParticleEmitter`, `CameraShake`, `InputActionMap`, `ScoreManager` |
| `simple_physics` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `BoundsManager`, `InputActionMap`, `Cooldown` |

---

## Template Goals

A good HyperKit template should be:

- easy to run
- easy to understand
- mobile-friendly
- small enough for beginners
- useful as a starting point for real game prototypes
- visually clear
- structured around reusable HyperKit helpers
