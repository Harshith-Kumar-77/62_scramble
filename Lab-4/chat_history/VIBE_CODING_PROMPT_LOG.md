git status
git add .
git commit -m "Fix bugs and improve scramble game"
git push# Lab 4 — Vibe-coding prompt and analysis log

**Important:** This is a prepared record of prompts and code-analysis decisions for the included package. It is not an exported transcript from a separate ChatGPT share page. If the instructor requires a complete ChatGPT history URL/PDF, add that real export before submitting.

## Prompt 1 — inspect before editing
> Analyze the existing Word Scramble project before changing code. Read the README and inspect the game engine, main entry point, and text input component. Identify actual bugs separately from missing features. For each issue, explain reproduction steps, expected vs actual behavior, root cause, minimal fix, and a test. Do not rewrite unrelated parts.

## Analysis result
The baseline `submit_guess()` normalized the input but compared it with `scrambled_word` rather than `secret_word`. The README explicitly describes this bug. The baseline also lacked a hint system, countdown timer, and interactive letter tiles; `update()` was empty and the scrambled string was rendered as a static label.

## Prompt 2 — fix the confirmed bug
> Correct guess validation so the submitted normalized answer is compared to the secret target word, never the scrambled display string. Empty input should not score. Incorrect input should show feedback, clear the entry field, and keep the same round. Preserve keyboard and mouse submission paths.

## Prompt 3 — progressive hints
> Add a progressive hint action that reveals one unrevealed letter at its true position each time it is used. Track the number of hints used and reduce the round's point reward proportionally, never below zero. Add a visible button and keyboard shortcut. Keep normal guessing functional.

## Prompt 4 — countdown
> Add a visible 30-second countdown bar for each active round. When time reaches zero, show the secret word in timeout feedback and advance to a new round after a brief readable delay. Ensure delta time is used rather than assuming every frame takes exactly the same duration.

## Prompt 5 — interactive letter tiles
> Replace the static-only scrambled display with clickable graphical letter tiles. Keep typed guesses and Enter/Submit working as an alternative. Ensure the tile arrangement can be changed by interaction and the game remains playable.

## Prompt 6 — tests and review
> Add unit tests for the pure game rules: correct answer versus scrambled string, whitespace/case normalization, empty guess, scramble preserving letters, repeated/single-letter edge cases, progressive hints, hint reward floor, and letter validation. Clearly distinguish tests actually executed from GUI tests that still require a local Pygame run.

## Review notes
- Added `game/game_logic.py` so critical rules can be tested without opening a GUI.
- Added unit tests under `tests/`.
- Added a manual acceptance checklist for GUI-only behavior.
- Do not claim the GUI was tested in the build environment: Pygame was unavailable there. Install dependencies and run the game locally before recording the final video.


## Follow-up verification prompts and outcomes

### Prompt 7 — test the full game state and event paths
> Re-review the entire project. Add tests for GameEngine state transitions, scoring, wrong/empty answers, timeout behavior, hints, keyboard shortcuts, tile selection, restart, text input boundaries, and render smoke behavior. Do not claim a real GUI test if Pygame is unavailable.

### Findings and fixes
- Fixed the H shortcut/input focus conflict.
- Replaced tile rotation with click-order tile selection and deselection.
- Blocked answer submission and hint usage after timeout.
- Clamped negative frame deltas.
- Aligned TextBox character acceptance with the ASCII game word bank.
- Pinned Pygame to 2.6.1 and documented Python 3.13 as the recommended runtime.

### Actual test outcome
- `python -m unittest discover -s tests -v`: 33 passed, 0 failed.
- `python -m compileall -q main.py game tests`: passed.
- Real Pygame GUI launch: not executed in the authoring environment because Pygame was unavailable. This remains a required local manual check.
