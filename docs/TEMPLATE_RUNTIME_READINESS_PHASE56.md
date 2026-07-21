# Template Runtime Readiness - Phase 56

This document defines the runtime-readiness requirements for all polished HyperKit templates.

Automated validation confirms project structure, syntax, metadata, and portability. Runtime readiness additionally requires launching and manually testing each generated game.

---

## Purpose

A runtime-ready template should:

- launch without startup errors
- open the graphical game window
- respond correctly to player input
- display its UI clearly
- update gameplay state correctly
- restart correctly where supported
- run consistently after project generation

---

## Templates Covered

Runtime-readiness testing applies to:

- tap_counter
- flappy_mini
- swipe_runner
- puzzle_game
- quiz_game
- simple_physics

---

## Automated Checks

Before manual runtime testing, run:

`pytest`

`hyperkit validate-templates`

`hyperkit validate-generated-projects`

`hyperkit health`

`hyperkit release-check`

`hyperkit pre-release-audit`

All automated checks should pass before beginning manual QA.

---

## Generated Project Setup

Create a separate generated project for each template.

Example:

`hyperkit new runtime-test-tap --template tap-counter`

Enter the project:

`cd runtime-test-tap`

Run the game:

`python main.py`

Repeat the same process for all built-in templates.

---

## Runtime Startup Requirements

Each generated project should:

- start without Python exceptions
- import HyperKit successfully
- create the game window
- display the correct template title
- display the main gameplay objects
- display readable UI text
- accept its expected input
- close normally

---

## Runtime Interaction Requirements

The tester should confirm:

- tap input works where expected
- swipe input works where expected
- score values update correctly
- progress bars update correctly
- game-over or completion states appear correctly
- restart behavior works correctly
- camera shake does not break object positions
- particle effects do not cause runtime errors

---

## Visual Readiness Requirements

Each template should be checked for:

- readable text
- visible player objects
- visible obstacles or targets
- clear score information
- clear status messages
- consistent spacing
- no major UI overlap
- no objects unintentionally leaving the visible area

---

## Repeatability Requirements

Each template should be launched and tested more than once.

The tester should confirm:

- a second launch works
- saved high-score data does not break startup
- restart behavior remains stable
- repeated input does not cause an exception
- the template remains playable after multiple rounds

---

## Current Status

All six templates have automated generated-project validation.

Phase 56 adds the manual runtime-readiness process needed before beta or stable release.