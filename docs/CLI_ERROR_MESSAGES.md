# CLI Error Messages

This document explains common HyperKit CLI errors and how to fix them.

---

## Unknown Template

Example:

`hyperkit new my-game --template tapcounter`

Possible output:

`Unknown template 'tapcounter'. Available templates: tap-counter, flappy-mini, swipe-runner, puzzle-game, quiz-game, simple-physics. Did you mean 'tap-counter'?`

Fix:

`hyperkit new my-game --template tap_counter`

Or:

`hyperkit new my-game --template tap-counter`

You can check all templates:

`hyperkit list-templates`

---

## Missing Template Name

If the template name is empty, HyperKit will show a clear error that a template name is required.

Fix:

`hyperkit new my-game --template tap_counter`

---

## Missing main.py

If you run:

`hyperkit run`

outside a generated HyperKit project, HyperKit may not find `main.py`.

Fix:

Go inside the project folder:

`cd my-game`

Then run:

`hyperkit run`

Or run with a path:

`hyperkit run --path path/to/project`

---

## Project Path Does Not Exist

If the path passed to `--path` does not exist, HyperKit will show a clear project path error.

Fix:

Check the folder path and run again:

`hyperkit run --path path/to/project`

---

## Recommended Debug Commands

Use these commands when something does not work:

`hyperkit doctor`

`hyperkit list-templates`

`hyperkit validate`

`hyperkit health`