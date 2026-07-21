# Template Stabilization Checklist

This checklist defines what should be completed before HyperKit templates are considered beta-ready or stable-ready.

---

## Purpose

Template stabilization means checking that polished templates are not only clean, but also reliable, consistent, and ready for public use.

---

## Template List

This checklist applies to:

- tap_counter
- flappy_mini
- swipe_runner
- puzzle_game
- quiz_game
- simple_physics

---

## Code Stability Checklist

Each template should:

- run without errors
- use valid Python syntax
- avoid temporary debug code
- avoid local machine paths
- keep code beginner-friendly
- use clear class and variable names
- use HyperKit helper systems consistently
- avoid unused complexity
- keep the game entry point clear

---

## Gameplay Stability Checklist

Each template should provide:

- clear starting state
- clear player controls
- visible score or progress
- meaningful feedback after input
- restart behavior where useful
- stable behavior after repeated runs
- no broken object positions
- no confusing UI overlap

---

## Generated Project Checklist

Each template should be tested after project generation.

Recommended flow:

`hyperkit new test-project --template tap-counter`

`cd test-project`

`python main.py`

The generated project should include:

- `main.py`
- `hyperkit.toml`
- asset folders
- working template logic
- clear starter code

All polished templates should pass:

`hyperkit validate-generated-projects`

---

## Documentation Checklist

Each template README should include:

- template purpose
- features
- run instructions
- gameplay explanation
- controls
- helper systems used
- customization ideas
- useful variables
- next steps

---

## Media Checklist

Each template should eventually include:

- screenshot.png
- demo.gif
- thumbnail.png

Media should be stored under:

`docs/media/templates/`

---

## Test Checklist

Before beta or stable release, run:

`pytest`

`hyperkit validate-templates`

`hyperkit health`

`hyperkit release-check`

`hyperkit pre-release-audit`

`hyperkit validate-generated-projects`

---

## Beta-Ready Criteria

A template can be considered beta-ready when:

- it runs from a generated project
- it has a polished README
- it passes template validation
- it passes generated project smoke tests
- it has no local paths or temporary files
- it has clear gameplay feedback

---

## Stable-Ready Criteria

A template can be considered stable-ready when:

- it meets all beta-ready criteria
- it has screenshot or demo media
- it has consistent documentation quality
- it has been tested on multiple screen sizes
- it has been reviewed for beginner clarity
- it is useful as a real prototype starting point

---

## Current Status

The templates have completed their first polish pass.

The next work is stabilization, media preparation, and beta-readiness review.