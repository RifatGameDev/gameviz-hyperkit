# HyperKit Templates

HyperKit includes ready-to-use starter templates for common mobile 2D game styles.

---

## Available Templates

### Tap Counter

A simple tap scoring game.

```bash
hyperkit new my-tap-game --template tap_counter
```

Best for:

- tap games
- clicker games
- score-based prototypes
- simple feedback testing

---

### Flappy Mini

A Flappy-style obstacle avoidance game.

```bash
hyperkit new my-flappy-game --template flappy_mini
```

Best for:

- tap-to-flap games
- obstacle avoidance
- arcade prototypes

---

### Swipe Runner

A lane-based runner game.

```bash
hyperkit new my-runner-game --template swipe_runner
```

Best for:

- endless runner prototypes
- swipe movement
- lane-based mobile games

---

### Puzzle Game

A simple tile matching puzzle.

```bash
hyperkit new my-puzzle-game --template puzzle_game
```

Best for:

- matching puzzles
- simple memory games
- grid-based prototypes

---

### Quiz Game

A multiple-choice educational quiz game.

```bash
hyperkit new my-quiz-game --template quiz_game
```

Best for:

- educational games
- quiz apps
- learning prototypes

---

### Simple Physics

A simple physics-based ball demo.

```bash
hyperkit new my-physics-game --template simple_physics
```

Best for:

- bounce mechanics
- simple gravity tests
- physics prototypes

---

## Helper-Based Templates

Most templates now demonstrate modern HyperKit helper systems:

- `AssetManager`
- `ScoreManager`
- `ProgressBar`
- `ParticleEmitter`
- `CameraShake`
- `BoundsManager`
- `InputActionMap`
- `Cooldown`

Read the full guide:

```text
docs/TEMPLATE_HELPERS.md
```

---

## Recommended Workflow

Create a project:

```bash
hyperkit new my-game --template tap_counter
```

Go to the project:

```bash
cd my-game
```

Run it:

```bash
python main.py
```

Validate it:

```bash
hyperkit validate
```

---

## Template Development Notes

When adding or upgrading a template:

1. Keep the template beginner friendly.
2. Use HyperKit helpers only when they make the template clearer.
3. Keep generated assets small and replaceable.
4. Add or update the template README.
5. Add tests to confirm the template exists and uses expected helpers.
