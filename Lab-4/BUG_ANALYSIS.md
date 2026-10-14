# Lab 4 — Bug Analysis and Test Report

**Repository reviewed:** https://github.com/SETAPESU26/62_scramble  
**Date reviewed:** 14 October 2026  
**Scope:** `README.md`, `main.py`, `game/game_engine.py`, `game/text_box.py` from the public repository.

## Baseline findings

1. **Confirmed functional bug — guess compared with the scrambled display.** In the baseline `game/game_engine.py`, `submit_guess()` used `guess == self.scrambled_word` even though the intended answer is `self.secret_word`. Consequently, the intended answer can be rejected and entering the scrambled sequence can be accepted. Fix: normalize and compare against `secret_word`.
2. **Required feature absent — progressive hints.** No hint button, revealed-position state, or score penalty existed in the baseline. Added progressive letter reveal; each hint reduces the one-point round reward by one, to a minimum of zero.
3. **Required feature absent — countdown timer.** Baseline `update()` was a no-op. Added a 30-second countdown bar and timeout feedback, followed by automatic next round.
4. **Required feature absent — interactive letter tiles.** Baseline rendered only a static spaced string. Added selectable letter tiles: clicks append the chosen tile to the answer in click order; clicking a selected tile again removes it. Selected tiles are visually highlighted. Keyboard input and Enter/Submit remain available.
5. **Minor inconsistency — window caption.** Baseline `main.py` titled the window “Anvil Dodge - Pygame Edition” despite the game being Word Scramble. Updated caption.

## Implemented behavior
- Guess normalization trims whitespace and uppercases input.
- Correct answer is compared to the secret target word.
- Empty submission receives feedback and does not score.
- Incorrect guess clears the entry field and keeps the current secret word.
- Hint reveals one additional letter in its true position per click / H key.
- Each hint reduces the round's possible reward by one point (minimum zero).
- Timer counts down from 30 seconds; timeout reveals the answer in feedback and moves on after a short delay.
- Clickable letter tiles are added while typed input remains supported.
- R / Restart resets the score and begins a new round.

## Follow-up review findings and fixes

A deeper review of the prepared implementation found additional edge cases; these have now been fixed:
1. Pressing `H` while the answer field had focus could append `H` before invoking a hint. The shortcut now triggers only when the input field is not focused, so words containing H remain typeable.
2. The previous tile behavior rotated a letter but did not reliably build a guess in click order. Tile clicks now select/deselect individual tile positions and assemble the answer in the order clicked.
3. A correct answer could be submitted during the timeout feedback window. Submissions and hints are now blocked once time is up.
4. Negative frame deltas could increase the timeout feedback duration. `update()` now clamps negative deltas to zero.
5. Text input accepted Unicode alphabetic characters although the game word bank and helper validation are ASCII-only. TextBox now uses the shared ASCII letter validator.
6. Requirements are pinned to Pygame 2.6.1 and the README recommends Python 3.13; Python 3.14 currently has no compatible wheel for that Pygame version in this setup.

## Test execution
Run from the project root:

```bash
python -m unittest discover -s tests -v
```

The current suite has 33 passing tests: pure game-logic tests plus headless GameEngine/TextBox tests using a lightweight Pygame test double. Coverage includes scoring, wrong/empty guesses, timer and timeout state, hint penalties, keyboard shortcuts, tile assembly/deselection, restart and button events, text input boundaries, and render-method smoke testing. `python -m compileall -q main.py game tests` also passed.

**Environment limitation:** Pygame is not installed in the authoring environment, and network access to install it was unavailable. Therefore the GUI could not be launched here. The unit-test suite was executed independently; please run the GUI locally after installing `pygame` and capture real before/after videos. GUI interaction, timing and rendering still require manual validation on the target computer.

## Manual acceptance test checklist
1. Start game; note the displayed scrambled word and secret answer only as known to the test operator.
2. Enter the true secret word. Expected: success feedback and score reward, then a new round.
3. Enter the displayed scrambled word when it differs from the secret. Expected: incorrect feedback; same round remains.
4. Submit empty input. Expected: prompt and no score change.
5. Enter an incorrect guess. Expected: input clears, same round remains.
6. Press H / click HINT twice. Expected: two more correctly positioned letters become visible; possible round reward is reduced.
7. Let timer reach zero. Expected: timeout reveals the answer in feedback and advances after a short delay.
8. Click letter tiles and verify tile sequence changes; submit a typed answer to confirm keyboard path remains functional.
9. Press R / click Restart. Expected: score resets and a fresh round begins.
10. Close the window normally.

## Honest evidence note
The package includes a recording guide but not fabricated gameplay recordings. Record the original baseline before edits, then record the modified project after running it locally. Also export the actual AI conversation/share link if your instructor requires the complete conversation page; the included prompt log is a prepared project record, not a platform export.
