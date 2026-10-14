import unittest
from game.game_logic import normalize_guess, is_correct_guess, scramble_word, reveal_next_hint, hinted_reward, valid_letter

class TestGameLogic(unittest.TestCase):
    def test_correct_guess_uses_secret_not_scrambled(self):
        self.assertTrue(is_correct_guess("PYTHON", "PYTHON"))
        self.assertFalse(is_correct_guess("NOPYTH", "PYTHON"))

    def test_guess_is_trimmed_and_case_insensitive(self):
        self.assertEqual(normalize_guess("  python  "), "PYTHON")
        self.assertTrue(is_correct_guess(" python ", "PYTHON"))

    def test_empty_guess_is_not_correct(self):
        self.assertFalse(is_correct_guess("", "PYTHON"))
        self.assertFalse(is_correct_guess("   ", "PYTHON"))

    def test_scramble_preserves_letters_and_changes_order_when_possible(self):
        result = scramble_word("PYTHON")
        self.assertEqual(sorted(result), sorted("PYTHON"))
        self.assertNotEqual(result, "PYTHON")

    def test_single_and_identical_letters_terminate(self):
        self.assertEqual(scramble_word("A"), "A")
        self.assertEqual(scramble_word("AAA"), "AAA")

    def test_hint_reveals_one_correct_position_at_a_time(self):
        positions, pattern = reveal_next_hint("CODE", set())
        self.assertEqual(positions, {0})
        self.assertEqual(pattern, "C _ _ _")
        positions, pattern = reveal_next_hint("CODE", positions)
        self.assertEqual(positions, {0, 1})
        self.assertEqual(pattern, "C O _ _")

    def test_hint_reward_never_goes_below_zero(self):
        self.assertEqual(hinted_reward(1, 0), 1)
        self.assertEqual(hinted_reward(1, 1), 0)
        self.assertEqual(hinted_reward(1, 5), 0)

    def test_letter_validation(self):
        self.assertTrue(valid_letter("A"))
        self.assertTrue(valid_letter("z"))
        self.assertFalse(valid_letter("7"))
        self.assertFalse(valid_letter("AB"))
        self.assertFalse(valid_letter("é"))

    def test_scramble_preserves_each_word_in_the_game_word_bank(self):
        from game.game_logic import WORDS
        for word in WORDS:
            result = scramble_word(word)
            with self.subTest(word=word):
                self.assertEqual(sorted(result), sorted(word))
                if len(set(word)) > 1:
                    self.assertNotEqual(result, word)

    def test_scramble_fallback_terminates_when_shuffle_does_not_change_word(self):
        class NoOpRandom:
            @staticmethod
            def shuffle(items):
                pass
        result = scramble_word("PLANET", NoOpRandom())
        self.assertEqual(sorted(result), sorted("PLANET"))
        self.assertNotEqual(result, "PLANET")

    def test_hint_stops_at_all_positions(self):
        positions = set()
        for _ in "CODE":
            positions, pattern = reveal_next_hint("CODE", positions)
        self.assertEqual(positions, {0, 1, 2, 3})
        self.assertEqual(pattern, "C O D E")
        positions_again, pattern_again = reveal_next_hint("CODE", positions)
        self.assertEqual(positions_again, positions)
        self.assertEqual(pattern_again, "C O D E")

    def test_hint_reward_clamps_negative_values(self):
        self.assertEqual(hinted_reward(-5, 0), 0)
        self.assertEqual(hinted_reward(3, -2), 3)

if __name__ == "__main__":
    unittest.main()
