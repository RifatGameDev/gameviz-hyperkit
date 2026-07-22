# Puzzle Game Template

Puzzle Game is a beginner-friendly HyperKit template for learning grid-based tap puzzle gameplay.

The player taps the glowing tile, follows the pattern, and tries to complete the puzzle goal.

---

## Features

- simple 3x3 puzzle grid
- tap-based puzzle interaction
- glowing active tile
- score and high-score display
- progress bar feedback
- simple win and restart flow
- wrong-tile feedback
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

Tap the glowing tile.

Each correct tap:

- increases the score
- updates the progress bar
- moves the active tile
- creates particle feedback

The puzzle is complete when the player reaches the goal.

If the player taps the wrong tile, the run ends.

After the run ends, tap again to restart.

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
- creating a grid of interactive tiles
- checking whether a tap is inside a tile
- tracking score and high score
- using ScoreManager for score and high-score tracking
- using ProgressBar for goal progress feedback
- using ParticleEmitter for correct tap feedback
- using CameraShake for wrong tap feedback
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

Tap or click the glowing tile.

After game over or puzzle completion, tap again to restart.

---

## Main Files

Generated project files:

- `main.py` contains the game logic
- `hyperkit.toml` stores project metadata
- `assets/` contains starter asset folders

---

## Customization Ideas

Try changing:

- grid size
- tile size
- tile spacing
- score goal
- active tile pattern
- tile colors
- camera shake intensity
- particle count

---

## Useful Variables

Inside `main.py`, you can change:

`self.grid_size`

`self.tile_size`

`self.tile_gap`

`self.score_goal`

You can also customize the tile colors inside:

`_highlight_active_tile()`

`_handle_wrong_tap()`

`_set_win_state()`

---

## Next Steps

After learning this template, try:

- Tap Counter
- Flappy Mini
- Swipe Runner
- Quiz Game
- Simple Physics