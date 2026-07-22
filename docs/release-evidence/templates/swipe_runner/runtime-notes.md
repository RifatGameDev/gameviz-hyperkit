# Swipe Runner Runtime Notes

## Environment

- Operating system: Windows
- Python version: 3.11.15
- HyperKit version: 0.1.1.dev1
- Environment: hyperkit
- Generated project: qa-swipe-runner
- Test date: 2026-07-22

## Startup

- Game window opened successfully: Yes
- Startup exception: None
- Correct window title displayed: Yes
- Three lanes displayed correctly: Yes
- Player and obstacle displayed correctly: Yes
- UI text displayed correctly: Yes

## Swipe Movement

- Swipe left changed the lane: Yes
- Swipe right changed the lane: Yes
- One swipe moved one lane: Yes
- Player remained inside valid lanes: Yes
- Edge-lane protection worked: Yes
- Player label followed the player: Yes
- Particle feedback worked: Yes
- Camera feedback worked: Yes

## Obstacle and Scoring

- Obstacle moved downward correctly: Yes
- Obstacle reset correctly: Yes
- Obstacle appeared in different lanes: Yes
- Obstacle remained aligned with a lane: Yes
- Avoiding an obstacle increased the score: Yes
- ProgressBar updated correctly: Yes
- High score updated correctly: Yes

## Collision and Restart

- Collision triggered game over: Yes
- Game-over feedback appeared correctly: Yes
- Tap after game over restarted the game: Yes
- Swipe after game over restarted the game: Yes
- Player position reset correctly: Yes
- Obstacle position reset correctly: Yes
- Current score reset correctly: Yes
- High score remained available: Yes
- Multiple restarts worked: Yes

## Repeatability

- Rapid repeated swipes worked: Yes
- Multiple launches worked: Yes
- Saved high score caused startup problems: No
- Runtime exceptions: None

## Window Sizes Tested

- Normal window size
- Smaller resized window

## Issues

- No release-blocking issues found.

## Final Result

Final result: PASS