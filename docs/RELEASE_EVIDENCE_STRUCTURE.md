# Release Evidence Structure

This document defines how HyperKit manual QA evidence should be organized before a beta or stable release.

---

## Purpose

Release evidence provides a consistent record that each polished template was:

- generated successfully
- launched successfully
- tested manually
- checked visually
- tested across repeated gameplay rounds
- reviewed for release readiness

---

## Evidence Root

Release evidence is stored under:

`docs/release-evidence/`

Template-specific evidence is stored under:

`docs/release-evidence/templates/`

---

## Template Evidence Folders

The repository includes one evidence folder for each polished template:

- `tap_counter`
- `flappy_mini`
- `swipe_runner`
- `puzzle_game`
- `quiz_game`
- `simple_physics`

---

## Expected Evidence Files

Each template evidence folder should eventually contain:

- `manual-qa-result.md`
- `validation-output.txt`
- `runtime-notes.md`
- `screenshot.png`
- `demo.gif` or a short demo video when available
- `issue-notes.md` when issues are discovered

The folder README explains what evidence is expected.

---

## Required Evidence

Before a template is marked beta-ready, include:

- completed manual QA result
- automated validation output
- at least one runtime screenshot
- notes for any failed or incomplete QA item
- final PASS, PASS WITH NOTES, or FAIL decision

---

## Optional Evidence

Additional evidence may include:

- demo GIF
- short gameplay video
- multiple screen-size screenshots
- console output
- performance notes
- issue reproduction screenshots

---

## File Naming Rules

Use clear lowercase names with hyphens when adding extra evidence.

Examples:

- `startup-screen.png`
- `game-over-state.png`
- `restart-test.png`
- `validation-output.txt`
- `screen-size-notes.md`

Avoid unclear names such as:

- `image1.png`
- `test-final-final.png`
- `newfile.txt`

---

## Evidence Safety Rules

Do not include:

- access tokens
- passwords
- private API keys
- personal user data
- private company information
- machine-specific absolute paths
- unnecessary environment secrets

Review logs and screenshots before committing them.

---

## Recommended QA Flow

For each template:

1. Generate a new project.
2. Run all automated validation commands.
3. Launch the generated game.
4. Complete the manual QA checklist.
5. Copy the manual QA result template.
6. Save the completed result as `manual-qa-result.md`.
7. Add screenshots and useful logs.
8. Record issues and final readiness decision.

---

## Completion Criteria

The release evidence structure is complete when every template folder contains:

- a completed manual QA result
- validation output
- runtime evidence
- issue notes when required
- a final release-readiness decision

Phase 57 creates the evidence structure. Actual runtime evidence will be added during manual QA.