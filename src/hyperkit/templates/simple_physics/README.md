# Simple Physics Template

Simple Physics is a beginner-friendly HyperKit template for learning gravity, bouncing, and force-style gameplay.

The player taps to push the ball upward and keeps it bouncing while collecting targets.

---

## Features

- gravity-style ball movement
- tap-to-apply-force input
- floor bounce behavior
- wall bounce behavior
- target collection
- score and high-score display
- progress bar feedback
- simple restart flow
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

Tap or click anywhere on the game window.

Each tap:

- applies upward force to the ball
- creates particle feedback
- gives light camera feedback

The ball:

- falls due to gravity
- bounces on the floor
- bounces from side walls
- scores when it hits the target

After game over, tap again to restart.

---

## Helper Systems Used

This template demonstrates these HyperKit helper systems:

- AssetManager
- BoundsManager
- Cooldown
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
- applying gravity-style movement
- applying force-style input
- creating simple bounce behavior
- checking target collision
- tracking score and high score
- using ScoreManager for score and high-score tracking
- using ProgressBar for goal progress feedback
- using ParticleEmitter for tap and target feedback
- using CameraShake for bounce feedback
- preparing BoundsManager for future bounds organization
- preparing InputActionMap for input organization
- preparing AssetManager for future image assets
- creating a clean mobile-style layout
- preparing Cooldown for controlled force timing

---

## How to Run

From inside the generated project folder:

`python main.py`

Or with the HyperKit CLI:

`hyperkit run`

---

## Controls

Tap or click anywhere to apply upward force to the ball.

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
- bounce strength
- floor position
- ball speed
- ball size
- target position
- score goal
- camera shake intensity
- particle count

---

## Useful Variables

Inside `main.py`, you can change:

`self.gravity`

`self.jump_force`

`self.bounce_strength`

`self.ball_velocity_x`

`self.score_goal`

You can also customize the ball:

`self.ball.width`

`self.ball.height`

`self.ball.color`

---

## Next Steps

After learning this template, try:

- Tap Counter
- Flappy Mini
- Swipe Runner
- Puzzle Game
- Quiz Game