# Swipe Runner Template

Swipe Runner is a beginner-friendly HyperKit template for learning lane-based swipe gameplay.

The player swipes left or right to change lanes and avoid moving obstacles.

---

## Features

- three-lane runner gameplay
- swipe left and right input
- moving obstacle
- score and high-score display
- progress bar feedback
- simple game-over and restart flow
- camera shake feedback
- particle feedback
- clean mobile-style layout
- helper-based starter structure

---

## Run

From inside the generated project folder:

`python main.py`

Or with the HyperKit CLI:

`hyperkit run`

---

## Gameplay

Swipe left or right to move between lanes.

The player scores when an obstacle moves off screen.

The game ends if the player touches the obstacle.

After game over:

- tap to restart
- or swipe to restart

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
- handling swipe input
- creating lane-based movement
- creating moving obstacles
- tracking score and high score
- using ScoreManager for score and high-score tracking
- using ProgressBar for goal progress feedback
- using ParticleEmitter for movement feedback
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

Swipe left or right to change lanes.

After game over, tap or swipe to restart.

---

## Main Files

Generated project files:

- `main.py` contains the game logic
- `hyperkit.toml` stores project metadata
- `assets/` contains starter asset folders

---

## Customization Ideas

Try changing:

- runner speed
- lane positions
- player size
- obstacle size
- obstacle speed
- score goal
- colors
- camera shake intensity
- particle count

---

## Useful Variables

Inside `main.py`, you can change:

`self.lanes`

`self.runner_speed`

`self.score_goal`

You can also customize the player:

`self.player.width`

`self.player.height`

`self.player.color`

---

## Next Steps

After learning this template, try:

- Tap Counter
- Flappy Mini
- Puzzle Game
- Quiz Game
- Simple Physics