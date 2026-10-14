"""Headless tests for GameEngine state and input handling.

A tiny pygame test double lets these state tests run without a graphical desktop.
It does not replace a real manual GUI test with pygame installed.
"""
import sys
import types
import unittest
from types import SimpleNamespace


class FakeRect:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.width, self.height = x, y, w, h
        self.w, self.h = w, h
        self.centerx, self.centery = x + w // 2, y + h // 2

    def collidepoint(self, point):
        x, y = point
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


class FakeSurface:
    def __init__(self, text=""):
        self.text = text

    def get_width(self):
        return len(self.text) * 8

    def get_height(self):
        return 20

    def fill(self, *_args, **_kwargs):
        pass

    def blit(self, *_args, **_kwargs):
        pass


class FakeFont:
    def render(self, text, *_args, **_kwargs):
        return FakeSurface(str(text))


fake_pygame = types.ModuleType("pygame")
fake_pygame.Rect = FakeRect
fake_pygame.font = SimpleNamespace(SysFont=lambda *_args, **_kwargs: FakeFont())
fake_pygame.draw = SimpleNamespace(rect=lambda *_args, **_kwargs: None)
fake_pygame.KEYDOWN = 1
fake_pygame.MOUSEBUTTONDOWN = 2
fake_pygame.K_RETURN = 13
fake_pygame.K_KP_ENTER = 271
fake_pygame.K_BACKSPACE = 8
fake_pygame.K_h = ord("h")
fake_pygame.K_r = ord("r")
fake_pygame.Surface = FakeSurface
sys.modules["pygame"] = fake_pygame

from game.game_engine import GameEngine


class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.game = GameEngine(760, 500)
        self.game.secret_word = "PYTHON"
        self.game.scrambled_word = "NOPYTH"
        self.game.tile_order = list("NOPYTH")
        self.game.selected_tile_indices = []
        self.game._layout_tiles()
        self.game.input_box.clear()
        self.game.score = 0
        self.game.remaining_time = self.game.ROUND_SECONDS
        self.game.timeout_pending = 0.0
        self.game.revealed_positions = set()
        self.game.hints_used = 0

    def key(self, key, unicode=""):
        return SimpleNamespace(type=fake_pygame.KEYDOWN, key=key, unicode=unicode)

    def click(self, point):
        return SimpleNamespace(type=fake_pygame.MOUSEBUTTONDOWN, button=1, pos=point)

    def test_correct_guess_scores_and_starts_new_round(self):
        old_word = self.game.secret_word
        self.assertTrue(self.game.submit_guess(old_word.lower()))
        self.assertEqual(self.game.score, 1)
        self.assertIn("CORRECT!", self.game.feedback_msg)
        self.assertEqual(self.game.remaining_time, self.game.ROUND_SECONDS)
        self.assertEqual(self.game.hints_used, 0)

    def test_wrong_guess_does_not_score_or_change_secret(self):
        old_word = self.game.secret_word
        self.game.input_box.text = "WRONG"
        self.assertFalse(self.game.submit_guess())
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.secret_word, old_word)
        self.assertEqual(self.game.input_box.text, "")

    def test_empty_guess_is_rejected_without_penalty(self):
        self.assertFalse(self.game.submit_guess("   "))
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.secret_word, "PYTHON")

    def test_hint_reduces_reward_and_reveals_next_letter(self):
        self.game.request_hint()
        self.assertEqual(self.game.revealed_positions, {0})
        self.assertEqual(self.game.hints_used, 1)
        self.assertTrue(self.game.submit_guess("PYTHON"))
        self.assertEqual(self.game.score, 0)

    def test_timer_counts_down_and_never_goes_negative(self):
        self.game.update(2.5)
        self.assertAlmostEqual(self.game.remaining_time, 27.5)
        self.game.update(100)
        self.assertEqual(self.game.remaining_time, 0)
        self.assertGreater(self.game.timeout_pending, 0)

    def test_timeout_blocks_scoring_and_hinting(self):
        self.game.update(self.game.ROUND_SECONDS)
        old_word = self.game.secret_word
        self.assertFalse(self.game.submit_guess(old_word))
        self.game.request_hint()
        self.assertEqual(self.game.hints_used, 0)
        self.assertEqual(self.game.secret_word, old_word)
        self.assertEqual(self.game.score, 0)

    def test_timeout_advances_to_next_round_after_feedback(self):
        self.game.update(self.game.ROUND_SECONDS)
        self.game.update(self.game.TIMEOUT_FEEDBACK_SECONDS + 0.1)
        self.assertEqual(self.game.timeout_pending, 0)
        self.assertEqual(self.game.remaining_time, self.game.ROUND_SECONDS)
        self.assertIn("New round", self.game.feedback_msg)

    def test_restart_resets_score_and_round_state(self):
        self.game.score = 12
        self.game.hints_used = 2
        self.game.remaining_time = 3
        self.game.handle_event(self.key(fake_pygame.K_r, "r"))
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.remaining_time, self.game.ROUND_SECONDS)
        self.assertEqual(self.game.hints_used, 0)
        self.assertEqual(self.game.input_box.text, "")

    def test_h_key_requests_hint_when_input_is_empty(self):
        self.game.input_box.active = True
        self.game.handle_event(self.key(fake_pygame.K_h, "h"))
        self.assertEqual(self.game.input_box.text, "")
        self.assertEqual(self.game.hints_used, 1)

    def test_h_key_can_be_typed_inside_an_existing_guess(self):
        self.game.input_box.active = True
        self.game.input_box.text = "PYT"
        self.game.handle_event(self.key(fake_pygame.K_h, "h"))
        self.assertEqual(self.game.input_box.text, "PYTH")
        self.assertEqual(self.game.hints_used, 0)

    def test_h_key_requests_hint_when_input_not_focused(self):
        self.game.input_box.active = False
        self.game.handle_event(self.key(fake_pygame.K_h, "h"))
        self.assertEqual(self.game.hints_used, 1)

    def test_clicking_tiles_builds_and_deselects_guess(self):
        first_rect = self.game.tile_rects[0]
        self.game.handle_event(self.click((first_rect.x + 1, first_rect.y + 1)))
        self.assertEqual(self.game.input_box.text, self.game.tile_order[0])
        self.assertEqual(self.game.selected_tile_indices, [0])
        self.game.handle_event(self.click((first_rect.x + 1, first_rect.y + 1)))
        self.assertEqual(self.game.input_box.text, "")
        self.assertEqual(self.game.selected_tile_indices, [])

    def test_submit_button_submits_current_guess(self):
        self.game.input_box.text = "PYTHON"
        self.game.handle_event(self.click((self.game.submit_btn.centerx, self.game.submit_btn.centery)))
        self.assertEqual(self.game.score, 1)

    def test_render_does_not_raise_with_headless_surface(self):
        self.game.render(FakeSurface())

    def test_negative_frame_delta_does_not_increase_timer(self):
        self.game.remaining_time = 10
        self.game.update(-5)
        self.assertEqual(self.game.remaining_time, 10)

    def test_enter_key_submits_guess(self):
        self.game.input_box.text = "PYTHON"
        self.game.handle_event(self.key(fake_pygame.K_RETURN, "\r"))
        self.assertEqual(self.game.score, 1)

    def test_text_box_accepts_ascii_and_rejects_unicode_letters(self):
        self.game.input_box.active = True
        self.game.input_box.handle_event(self.key(ord("a"), "a"))
        self.game.input_box.handle_event(self.key(ord("é"), "é"))
        self.assertEqual(self.game.input_box.text, "A")

    def test_text_box_backspace_and_length_limit(self):
        self.game.input_box.active = True
        self.game.input_box.text = "ABC"
        self.game.input_box.handle_event(self.key(fake_pygame.K_BACKSPACE, ""))
        self.assertEqual(self.game.input_box.text, "AB")
        self.game.input_box.text = "A" * 20
        self.game.input_box.handle_event(self.key(ord("B"), "B"))
        self.assertEqual(len(self.game.input_box.text), 20)

    def test_hint_button_increments_hint_count(self):
        self.game.handle_event(self.click((self.game.hint_btn.centerx, self.game.hint_btn.centery)))
        self.assertEqual(self.game.hints_used, 1)

    def test_restart_button_resets_score(self):
        self.game.score = 5
        self.game.handle_event(self.click((self.game.restart_btn.centerx, self.game.restart_btn.centery)))
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.input_box.text, "")

    def test_tiles_can_form_secret_word_in_selection_order(self):
        # Arrange the displayed tiles in a known order, then click their positions
        # in the order required to spell the secret. This also covers repeated letters.
        self.game.tile_order = list("PYTHON")
        self.game._layout_tiles()
        self.game.selected_tile_indices = []
        for index in range(len(self.game.tile_order)):
            rect = self.game.tile_rects[index]
            self.game.handle_event(self.click((rect.x + 1, rect.y + 1)))
        self.assertEqual(self.game.input_box.text, "PYTHON")
        self.assertTrue(self.game.submit_guess())
        self.assertEqual(self.game.score, 1)


if __name__ == "__main__":
    unittest.main()
