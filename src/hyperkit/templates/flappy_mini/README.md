# Flappy Mini Template

Flappy Mini is a beginner-friendly HyperKit template for learning tap-to-jump gameplay.

The player taps to keep the bird in the air and pass moving pipes.

---

## Features

- tap-to-jump gameplay
- gravity-based movement
- moving obstacle pipes
- score and high-score display
- progress bar feedback
- simple game-over and restart flow
- camera shake feedback
- particle feedback
- clean mobile-style layout
- helper-based starter structure
- randomized vertical pipe-gap positions

---

## Run

From inside the generated project folder:

`python main.py`

Or with the HyperKit CLI:

`hyperkit run`

---

## Gameplay

Tap or click anywhere on the game window.

Each tap:

- pushes the bird upward
- creates small particle feedback
- gives light camera feedback

The player scores when the pipe moves off screen.
The pipe gap changes vertical position after each completed pipe cycle.

The game ends if the bird:

- hits the ground
- hits the ceiling
- touches a pipe

After game over, tap again to restart.

---

## Helper Systems Used

This template demonstrates these HyperKit helper systems:

- AssetManager
- BoundsManager
- GameObject
- TextLabel
- ScoreManager
- ProgressBar
- ParticleEmitter
- CameraShake
- ScreenBounds
- InputActionMap

---

## What This Template Demonstrates

- creating a HyperKit game scene
- adding GameObjects
- using TextLabel UI
- handling tap/click input
- using gravity-style movement
- creating simple moving obstacles
- tracking score and high score
- using ScoreManager for score and high-score tracking
- using ProgressBar for goal progress feedback
- using ParticleEmitter for tap feedback
- using CameraShake for impact feedback
- preparing BoundsManager for future bounds organization
- preparing InputActionMap for input organization
- preparing AssetManager for future image assets
- creating a clean mobile-style layout

---

## How to Run

From inside the generated project folder:

`python main.py`

Or with the HyperKit CLI:

`hyperkit run`

---

## Controls

Tap or click anywhere to flap upward.

After game over, tap again to restart.

---

## Main Files

Generated project files:

- `main.py` contains the game logic
- `hyperkit.toml` stores project metadata
- `assets/` contains starter asset folders

---

## Customization Ideas

Try changing:

- gravity
- jump force
- pipe speed
- pipe gap
- bird size
- colors
- score goal
- camera shake intensity
- particle count
- pipe gap size
- minimum and maximum gap positions

---

## Useful Variables

Inside `main.py`, you can change:

`self.gravity`

`self.jump_force`

`self.pipe_speed`

`self.score_goal`

`self.pipe_gap`

`self.pipe_min_gap_center`

`self.pipe_max_gap_center`

You can also customize the bird:

`self.bird.width`

`self.bird.height`

`self.bird.color`

---

## Next Steps

After learning this template, try:

- Tap Counter
- Swipe Runner
- Puzzle Game
- Quiz Game
- Simple Physics