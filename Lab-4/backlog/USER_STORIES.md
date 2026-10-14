# Backlog issue drafts — Word Scramble Repair Lab

Create the Epic first, then create these as separate GitHub Issues and link them as sub-issues / children of the Epic. Story points are suggested estimates; adjust to your instructor's convention. These are drafts only; this package does not create GitHub issues in your account.

## Story 1 — Fix secret-word validation
- **Type:** Bug / User Story
- **Story points:** 2
- **Priority:** High
- **Labels:** `bug`, `user-story`, `priority:high`
- **Story:** As a player, I want my guess checked against the actual secret word so correct answers are accepted and scrambled text is not incorrectly accepted.
- **Acceptance criteria:**
  - A case-insensitive, whitespace-trimmed secret-word guess is accepted.
  - The scrambled display string is not accepted unless it is also the true word.
  - Empty input produces feedback and does not score.
  - An incorrect guess clears the input but does not change the current round.

## Story 2 — Add progressive hints
- **Type:** Feature / User Story
- **Story points:** 3
- **Priority:** Medium
- **Labels:** `enhancement`, `user-story`, `priority:medium`
- **Story:** As a player, I want to reveal one letter at a time so I can get unstuck without immediately giving away the whole answer.
- **Acceptance criteria:**
  - A button and keyboard shortcut request a hint.
  - Each hint reveals a previously hidden letter in its correct position.
  - Each hint reduces the round reward by one point, with a minimum of zero.
  - Repeated requests do not reveal nonexistent letters or crash.

## Story 3 — Add a round countdown
- **Type:** Feature / User Story
- **Story points:** 5
- **Priority:** Medium
- **Labels:** `enhancement`, `user-story`, `priority:medium`
- **Story:** As a player, I want a visible countdown so each round has a clear time limit.
- **Acceptance criteria:**
  - A timer bar and remaining seconds are visible.
  - Timer decreases based on elapsed frame time.
  - Timeout displays the correct word and proceeds to a new round after feedback.
  - A new round starts with a full timer.

## Story 4 — Interactive letter tiles
- **Type:** Feature / User Story
- **Story points:** 5
- **Priority:** Medium
- **Labels:** `enhancement`, `user-story`, `priority:medium`
- **Story:** As a player, I want to interact with letter tiles so I can experiment with word order visually.
- **Acceptance criteria:**
  - Each scrambled letter is rendered as a clickable tile.
  - Clicking a tile changes the tile arrangement.
  - Keyboard guess entry and Enter/Submit remain available.
  - Tiles remain visible and usable across rounds.

## Story 5 — Add automated logic tests
- **Type:** Engineering / User Story
- **Story points:** 3
- **Priority:** High
- **Labels:** `testing`, `user-story`, `priority:high`
- **Story:** As a developer, I want repeatable tests for core game rules so later changes do not reintroduce the validation bug.
- **Acceptance criteria:**
  - Tests cover normalization, correct validation, empty input, scrambling, hints, score penalty, and alphabetic validation.
  - Tests run with `python -m unittest discover -s tests -v`.
  - GUI-only tests are separately documented as manual checks.

## Suggested priority order
1. Validation bug (2 points)
2. Automated logic tests (3 points)
3. Progressive hints (3 points)
4. Countdown timer (5 points)
5. Interactive tiles (5 points)

**Note:** Story point estimates are relative effort, not hours. Epic itself usually has no story points; estimate the child stories.
