# Runtime QA Tracker - Phase 58

This document tracks the runtime QA progress of all polished HyperKit templates.

The machine-readable tracker is stored at:

`docs/release-evidence/qa-tracker.json`

---

## Tracker Command

Run:

`hyperkit validate-release-evidence`

This validates:

- QA tracker structure
- template tracker entries
- allowed QA statuses
- evidence directories
- evidence folder README files
- required evidence for completed templates

For strict release validation, run:

`hyperkit validate-release-evidence --require-complete`

Strict validation fails until every template has completed runtime QA evidence.

---

## Current Template Status

| Template | Status | Evidence |
|---|---|---|
| Tap Counter | PENDING | Not started |
| Flappy Mini | PENDING | Not started |
| Swipe Runner | PENDING | Not started |
| Puzzle Game | PENDING | Not started |
| Quiz Game | PENDING | Not started |
| Simple Physics | PENDING | Not started |

---

## Allowed Status Values

The tracker supports:

- `pending`
- `in_progress`
- `pass`
- `pass_with_notes`
- `fail`

---

## Status Meaning

### pending

Manual runtime QA has not started.

### in_progress

Runtime QA has started, but the result is not final.

### pass

All critical manual QA checks passed.

### pass_with_notes

Critical checks passed, but non-blocking issues or observations remain.

### fail

A startup, gameplay, restart, visual, or other release-blocking issue was found.

---

## Evidence Required for PASS

A template marked `pass` or `pass_with_notes` should include:

- `manual-qa-result.md`
- `validation-output.txt`
- `runtime-notes.md`
- `screenshot.png`

---

## Evidence Required for FAIL

A template marked `fail` should include:

- `manual-qa-result.md`
- `validation-output.txt`
- `runtime-notes.md`
- `issue-notes.md`

---

## Updating a Template

After testing a template:

1. Complete its manual QA result.
2. Store evidence in its template evidence folder.
3. Update its status in `qa-tracker.json`.
4. Add its result file path.
5. Add useful notes.
6. Run the evidence validator.

Example tracker entry:

```json
{
  "display_name": "Tap Counter",
  "status": "pass",
  "result_file": "templates/tap_counter/manual-qa-result.md",
  "notes": "Runtime QA passed on Windows with Python 3.11."
}
```