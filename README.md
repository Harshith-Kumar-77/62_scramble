# Word Scramble Repair Lab — Lab 4 deliverable package

This package is based on the public `SETAPESU26/62_scramble` README and source files reviewed on 14 Oct 2026. The original README requires fixing guess validation and implementing progressive hints, an active countdown, and interactive letter tiles.

## Requirements
- Python 3.10–3.13 (Python 3.13 is recommended for this pinned Pygame version)
- Pygame 2.6.1 (`python -m pip install -r requirements.txt`)

**Python 3.14 note:** Pygame 2.6.1 does not publish a compatible CPython 3.14 Windows wheel, so pip may attempt a source build and fail. Use Python 3.13 in a project virtual environment.

## Run
```bash
python -m pip install -r requirements.txt
python main.py
```

## Run tests
```bash
python -m unittest discover -s tests -v
```
The tests cover pure game logic and GameEngine state/input behavior. Engine tests use a lightweight Pygame test double, so they do not require a display or installed Pygame. They do not replace a real GUI run on Windows.

## Implemented features
1. Correctly compares normalized guesses against the secret word, not the scrambled display.
2. Empty guesses are rejected without penalty; wrong guesses clear the input and do not advance the round.
3. Progressive hints reveal unrevealed secret letters in position and reduce the round reward.
4. A visible round countdown; timeout reveals the answer and advances after a brief feedback period.
5. Clickable letter tiles can be selected in answer order to form a guess; keyboard entry and Enter/Submit remain available.
6. Round/score feedback and a reset/restart key (`R`).

## Verification status

The current automated suite contains 33 tests. All 33 passed in the authoring environment, and `compileall` passed. GameEngine tests use a test double for Pygame and therefore validate state and event handling, not real SDL rendering, mouse latency, or Windows GUI behavior. A local GUI launch and manual acceptance test are still required.

## Lab evidence still required from your computer
The `Lab-4/videos` folder contains recording instructions, not fabricated recordings. Capture actual 10-second desktop/gameplay videos locally before and after running this code. The original class repo is the baseline; do not present a simulated clip as a genuine recording. See `Lab-4/videos/RECORDING_GUIDE.md`.

The `Lab-4/chat_history` folder contains a prepared prompt-and-analysis log for this package. It is not an export of a separate ChatGPT page. If your instructor specifically requires a share link/export, save the actual conversation from your ChatGPT account and replace/add it here.

## GitHub backlog
Issue drafts, acceptance criteria, and suggested story points are in `Lab-4/backlog/`. Create the Epic and stories in your own fork or project repo; this package cannot create issues in your GitHub account.

## Baseline source
Assigned repository: https://github.com/SETAPESU26/62_scramble
Reviewed README describes Word Scramble with one deliberate validation bug and three feature tasks. The published `main.py` caption has a stale “Anvil Dodge” window title; this package corrects it to “Word Scramble Arena”.
