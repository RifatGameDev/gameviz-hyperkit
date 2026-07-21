# Template Manual QA Checklist

Use this checklist to manually test all polished HyperKit templates after automated validation passes.

---

## QA Environment

Record the following before testing:

- operating system
- Python version
- HyperKit version
- screen resolution
- virtual environment name
- test date
- tester name

---

## Common Startup Checklist

For every template:

- [ ] Generate a new project successfully
- [ ] Confirm main.py exists
- [ ] Confirm hyperkit.toml exists
- [ ] Confirm asset folders exist
- [ ] Run python main.py
- [ ] Confirm the game window opens
- [ ] Confirm no startup exception appears
- [ ] Confirm the game title is correct
- [ ] Confirm UI text is readable
- [ ] Confirm the game closes normally

---

## Tap Counter QA

Generate:

`hyperkit new qa-tap-counter --template tap-counter`

Check:

- [ ] Tap or click input increases the score
- [ ] The target moves after input
- [ ] The target remains visible
- [ ] High score updates correctly
- [ ] Goal progress updates correctly
- [ ] ProgressBar updates correctly
- [ ] Status messages change correctly
- [ ] Goal-reached feedback appears
- [ ] Particle feedback works
- [ ] Camera shake works without breaking the layout

---

## Flappy Mini QA

Generate:

`hyperkit new qa-flappy-mini --template flappy-mini`

Check:

- [ ] Tap input moves the bird upward
- [ ] Gravity moves the bird downward
- [ ] Pipes move correctly
- [ ] Pipe collision triggers game over
- [ ] Ground collision triggers game over
- [ ] Ceiling collision triggers game over
- [ ] Passing a pipe increases the score
- [ ] ProgressBar updates correctly
- [ ] Tap after game over restarts the game
- [ ] Bird and pipe positions reset correctly

---

## Swipe Runner QA

Generate:

`hyperkit new qa-swipe-runner --template swipe-runner`

Check:

- [ ] Swipe left changes the lane
- [ ] Swipe right changes the lane
- [ ] The player cannot move beyond the outside lanes
- [ ] The obstacle moves downward
- [ ] Avoiding an obstacle increases the score
- [ ] Collision triggers game over
- [ ] ProgressBar updates correctly
- [ ] Tap after game over restarts the game
- [ ] Swipe after game over restarts the game
- [ ] Player and obstacle positions reset correctly

---

## Puzzle Game QA

Generate:

`hyperkit new qa-puzzle-game --template puzzle-game`

Check:

- [ ] The 3x3 puzzle grid appears
- [ ] One active tile is clearly highlighted
- [ ] Tapping the correct tile increases the score
- [ ] The active tile changes after a correct tap
- [ ] Tapping a wrong tile ends the run
- [ ] Correct tap particle feedback works
- [ ] Wrong tap camera shake works
- [ ] Goal progress updates correctly
- [ ] Puzzle completion feedback appears
- [ ] Tap after completion or failure restarts the puzzle

---

## Quiz Game QA

Generate:

`hyperkit new qa-quiz-game --template quiz-game`

Check:

- [ ] The first question appears
- [ ] Three answer choices appear
- [ ] Tapping a correct answer increases the score
- [ ] Tapping a wrong answer does not increase the score
- [ ] The next question appears correctly
- [ ] Question progress updates correctly
- [ ] ProgressBar updates correctly
- [ ] Correct-answer particle feedback works
- [ ] Wrong-answer camera shake works
- [ ] Tap after quiz completion restarts the quiz

---

## Simple Physics QA

Generate:

`hyperkit new qa-simple-physics --template simple-physics`

Check:

- [ ] Gravity moves the ball downward
- [ ] Tap input applies upward force
- [ ] The ball bounces on the floor
- [ ] The ball bounces from the side walls
- [ ] The ball can hit the target
- [ ] Target collision increases the score
- [ ] The target moves after collection
- [ ] ProgressBar updates correctly
- [ ] Particle feedback works
- [ ] Restart behavior works correctly

---

## Screen and Layout QA

Test each template on at least two window sizes.

Check:

- [ ] UI remains readable
- [ ] Main gameplay objects remain visible
- [ ] Status text is not cut off
- [ ] ProgressBar remains visible
- [ ] Input coordinates remain accurate
- [ ] No major element overlap appears
- [ ] Gameplay remains usable

---

## Repeat Run QA

For every template:

- [ ] Close and reopen the generated game
- [ ] Complete at least two gameplay rounds
- [ ] Test rapid repeated input
- [ ] Test restart more than once
- [ ] Confirm no exception appears
- [ ] Confirm high-score persistence does not break the game

---

## Recording QA Results

Use the following document to record the result for each tested template:

- [Manual QA Result Template](MANUAL_QA_RESULT_TEMPLATE.md)

Store completed QA results and supporting files under:

- [Release Evidence Workspace](release-evidence/README.md)

Save one completed `manual-qa-result.md` file inside the matching template evidence folder.

---

## QA Result

Record one result for each template:

- PASS
- PASS WITH NOTES
- FAIL

Any failed item should include:

- template name
- test step
- expected result
- actual result
- error output
- screenshot when useful

---

## Release Rule

A template should not be marked runtime-ready until:

- all automated checks pass
- all critical manual QA checks pass
- no startup or gameplay-blocking errors remain
- restart behavior is stable
- visual layout is usable