# Quiz Game Template

Quiz Game is a beginner-friendly HyperKit template for learning tap-based question and answer gameplay.

The player reads a question, taps an answer, and completes the quiz.

---

## Features

- tap-based answer selection
- multiple questions
- answer button UI
- score and high-score display
- progress bar feedback
- correct and wrong answer feedback
- simple quiz-complete and restart flow
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

Read the question and tap one answer.

Each answer:

- updates the score if correct
- moves to the next question
- updates the progress bar
- shows visual feedback

The quiz ends after all questions are answered.

After quiz completion, tap again to restart.

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
- creating answer buttons
- checking tapped answers
- tracking score and high score
- using ScoreManager for score and high-score tracking
- using ProgressBar for quiz progress feedback
- using ParticleEmitter for correct answer feedback
- using CameraShake for wrong answer feedback
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

Tap or click one answer box.

After quiz completion, tap again to restart.

---

## Main Files

Generated project files:

- `main.py` contains the game logic
- `hyperkit.toml` stores project metadata
- `assets/` contains starter asset folders

---

## Customization Ideas

Try changing:

- questions
- answer text
- correct answer indexes
- button positions
- score goal
- colors
- camera shake intensity
- particle count

---

## Useful Variables

Inside `main.py`, you can change:

`self.questions`

`self.score_goal`

You can also customize answer buttons inside:

`_create_answer_buttons()`

---

## Next Steps

After learning this template, try:

- Tap Counter
- Flappy Mini
- Swipe Runner
- Puzzle Game
- Simple Physics