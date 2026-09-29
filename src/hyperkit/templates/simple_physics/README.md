# Simple Physics Template

Simple Physics is a beginner-friendly HyperKit template for learning HyperKit's reusable 2D physics, bouncing, triggers, and force-style gameplay.

The player taps to push the ball upward and keeps it bouncing while collecting targets.

---

## Features

- PhysicsWorld-driven ball movement
- dynamic and static physics bodies
- reusable PhysicsMaterial bounce behavior
- collision layers and masks
- trigger-based target collection
- tap-to-apply-force input
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
- BodyType
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
- using PhysicsWorld for gravity and integration
- using dynamic and static PhysicsBody instances
- applying force-style input through body velocity
- configuring bounce with PhysicsMaterial
- filtering collisions with layers and masks
- handling collision and trigger callbacks
- tracking score and high score
- using ScoreManager for score and high-score tracking
- using ProgressBar for goal progress feedback
- using ParticleEmitter for tap and target feedback
- using CameraShake for bounce feedback
- preparing BoundsManager for additional world-bound organization
- preparing InputActionMap for extended input organization
- preparing AssetManager for optional image assets
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