# Manual QA Result Template

Use this template to record the manual runtime QA result for one generated HyperKit template.

Create a separate completed result file for every template and testing environment.

---

## Test Information

- Template name:
- Generated project name:
- HyperKit version:
- Python version:
- Operating system:
- Screen resolution:
- Virtual environment:
- Test date:
- Tester name:

---

## Test Result

Choose one final result:

- [ ] PASS
- [ ] PASS WITH NOTES
- [ ] FAIL

---

## Automated Validation Results

Confirm the following commands passed before manual QA:

- [ ] `pytest`
- [ ] `hyperkit validate-templates`
- [ ] `hyperkit validate-generated-projects`
- [ ] `hyperkit health`
- [ ] `hyperkit release-check`
- [ ] `hyperkit pre-release-audit`

Validation notes:

- Test count:
- Failed checks:
- Additional notes:

---

## Project Generation Result

- Command used:
- Generated project path:
- [ ] Project generation succeeded
- [ ] `main.py` exists
- [ ] `hyperkit.toml` exists
- [ ] Asset folders exist
- [ ] Generated project contains no temporary files
- [ ] Generated project contains no local development paths

Notes:

---

## Runtime Startup Result

- [ ] `python main.py` starts successfully
- [ ] No startup exception appears
- [ ] The game window opens
- [ ] The correct game title appears
- [ ] Main gameplay objects appear
- [ ] UI text is readable
- [ ] The game closes normally

Notes:

---

## Gameplay Result

- [ ] Expected input works
- [ ] Score behavior works
- [ ] Progress behavior works
- [ ] Player feedback works
- [ ] Game-over or completion state works
- [ ] Restart behavior works
- [ ] Repeated input does not cause errors
- [ ] Multiple gameplay rounds work

Notes:

---

## Visual and Layout Result

- [ ] Main gameplay objects remain visible
- [ ] Text is not cut off
- [ ] ProgressBar remains visible
- [ ] Status messages remain readable
- [ ] No major UI overlap appears
- [ ] Input coordinates match visible objects
- [ ] Layout remains usable on tested screen sizes

Tested window sizes:

- 
- 

Notes:

---

## Repeatability Result

- [ ] The game launches successfully a second time
- [ ] Restart works more than once
- [ ] Rapid repeated input does not cause an exception
- [ ] Saved high-score data does not break startup
- [ ] The template remains playable after multiple rounds

Notes:

---

## Issues Found

For every issue, record:

- Issue title:
- Severity:
- Test step:
- Expected result:
- Actual result:
- Error output:
- Reproduction steps:
- Proposed action:

Add more issue entries as needed.

---

## Evidence Files

Record the evidence included with this result:

- [ ] Screenshot
- [ ] Demo GIF or video
- [ ] Validation output
- [ ] Runtime error log
- [ ] Issue notes
- [ ] Additional test notes

Evidence file names:

- 
- 
- 

---

## Final Decision

Final result:

- PASS
- PASS WITH NOTES
- FAIL

Release-blocking issues:

- 

Follow-up work:

- 

---

## Sign-Off

- Tester:
- Review date:
- Reviewer:
- Approved for beta readiness: Yes / No
- Approved for stable readiness: Yes / No