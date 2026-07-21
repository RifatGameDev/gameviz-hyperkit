# HyperKit Release Evidence

This directory stores manual QA results and release-readiness evidence for polished HyperKit templates.

---

## Template Evidence

Evidence is organized under:

`templates/`

Each template has its own folder:

- tap_counter
- flappy_mini
- swipe_runner
- puzzle_game
- quiz_game
- simple_physics

---

## Required Template Evidence

Each template folder should eventually include:

- completed manual QA result
- automated validation output
- runtime screenshot
- runtime notes
- issue notes when needed
- final release-readiness decision

Use:

- [Manual QA Result Template](../MANUAL_QA_RESULT_TEMPLATE.md)
- [Release Evidence Structure](../RELEASE_EVIDENCE_STRUCTURE.md)
- [Template Manual QA Checklist](../TEMPLATE_MANUAL_QA_CHECKLIST.md)

---
## Runtime QA Tracker

The machine-readable tracker is:

`qa-tracker.json`

The human-readable tracker guide is:

- [Runtime QA Tracker](../RUNTIME_QA_TRACKER_PHASE58.md)

Validate the tracker and evidence structure with:

`hyperkit validate-release-evidence`

Before a beta or stable release, run strict validation:

`hyperkit validate-release-evidence --require-complete`

Do not commit private credentials, tokens, personal data, or sensitive environment information.