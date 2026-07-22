# Tap Counter Template

Tap Counter is a beginner-friendly HyperKit template for learning basic tap/click gameplay.

The player taps anywhere on the screen to move the target and increase the score.

---

## Features

- beginner-friendly tap/click gameplay
- score and high-score display
- tap goal progress
- progress bar feedback
- simple status messages
- target color feedback
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

Tap or click anywhere on the game window.

Each tap:

- moves the target
- increases the score
- updates the progress bar
- updates the status message
- adds camera shake feedback
- adds particle feedback

The starter goal is:

`30 taps`

After reaching the goal, the template continues running so the player can keep increasing the high score.

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
- tracking score and high score
- using ScoreManager for score and high-score tracking
- using ProgressBar for goal progress feedback
- using ParticleEmitter for tap feedback
- using CameraShake for impact feedback
- using ScreenBounds to keep the target visible
- preparing InputActionMap for input organization
- preparing AssetManager for future image assets
- creating a clean mobile-style layout
- preparing BoundsManager for future bounds organization

---

## How to Run

From inside the generated project folder:

`python main.py`

Or with the HyperKit CLI:

`hyperkit run`

---

## Controls

Tap or click anywhere on the game window.

---

## Main Files

Generated project files:

- `main.py` contains the game logic
- `hyperkit.toml` stores project metadata
- `assets/` contains starter asset folders

---

## Customization Ideas

Try changing:

- the tap goal
- the target size
- target colors
- label text
- progress bar position
- score behavior
- background color
- particle count
- camera shake intensity

---

## Useful Variables

Inside `main.py`, you can change:

`self.tap_goal = 30`

You can also customize the target:

`self.target.width`

`self.target.height`

`self.target.color`

---

## Next Steps

After learning this template, try:

- Flappy Mini
- Swipe Runner
- Puzzle Game
- Quiz Game
- Simple Physics