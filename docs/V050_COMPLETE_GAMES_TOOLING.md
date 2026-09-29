# HyperKit v0.5 — Complete Games + Developer Tooling

HyperKit v0.5 turns the existing SDK systems into a more complete
game-development workflow.

## Scope

The v0.5 development milestone focuses on two areas:

1. complete built-in small-game loops
2. developer tooling for validating and diagnosing projects

## Complete Built-in Games

The built-in game set is:

- Tap Counter
- Flappy Mini
- Swipe Runner
- Puzzle Game
- Quiz Game
- Simple Physics

Each built-in game is expected to provide:

- runnable `Game(...).set_scene(...).run()` entry
- player input
- score and high-score flow
- visible progress feedback
- game-over/completion state
- restart flow

Run the complete-game validator:

`hyperkit validate-complete-games`

The validator performs static release checks across all six built-in games.

## Runtime Developer Diagnostics

HyperKit v0.5 adds:

- `RuntimeDiagnostics`
- `RuntimeSnapshot`
- `DebugOverlay`

Example:

```python
from hyperkit import DebugOverlay, Scene


class MyScene(Scene):
    def start(self):
        self.debug = DebugOverlay(
            self,
            target_fps=60,
        )
        self.start_game()

    def update(self, dt):
        self.debug.update(dt)
        super().update(dt)
```

The runtime diagnostics helper tracks:

- estimated FPS
- average frame time
- frame count
- elapsed runtime
- slow/dropped-frame count

## Project Diagnostics CLI

Run:

`hyperkit diagnostics`

Or inspect another project:

`hyperkit diagnostics --path path/to/project`

The command reports:

- current HyperKit package version
- Python version
- detected template
- main file
- assets folder
- project validation state
- validation issues when present

## Continuous Integration

The repository includes a general SDK CI workflow for Python:

- 3.9
- 3.10
- 3.11
- 3.12

CI runs:

- full pytest suite
- built-in template validation
- complete-game validation
- generated-project validation
- release-readiness validation

## v0.5 Completion Rule

The v0.5 development milestone is complete when:

- all six complete-game checks pass
- all developer tooling tests pass
- generated projects still validate
- supported Python CI matrix is defined
- existing v0.4 Ads, Analytics, Android, and Game Systems regressions stay green
- full automated regression suite passes

The public compatibility contract remains API `0.2` during v0.5
development. API freeze is reserved for the later v0.9 public-beta stage.
