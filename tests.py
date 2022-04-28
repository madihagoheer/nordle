from unittest import TestCase
from nordle.nordle import (
    Nordle,
    Status,
    GuessResult,
    Options,
    CharacterPatternGenerator,
    PatternGeneratorBase,
)
import os
import re
import io
from typing import List, Optional, Set


class MockGenerator(PatternGeneratorBase):
    def __init__(self, pattern: List[str]):
        self.pattern: List[str] = pattern

    def generate(self, count: int, min: int, max: int) -> List[str]:
        return self.pattern


class NordleTests(TestCase):
    def test_basic_game(self):
        options = Options()
        options.pattern_generator = MockGenerator(["6", "5", "0", "5"])
        game = Nordle(options)
        game.new_game()

        result = game.make_guess(["1", "2", "3", "4"])
        self.assertEqual(result.result, GuessResult.NO_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())

        result = game.make_guess(["1", "2", "3", "0"])
        self.assertEqual(result.result, GuessResult.CONTENT_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set("0"))

        # Check corner case Pattern 6505 > 6555. 2nd last 5 should not be in there.
        result = game.make_guess(["6", "5", "5", "5"])
        self.assertEqual(result.result, GuessResult.POSITION_MATCH)
        self.assertEqual(result.indeces_matched, {0, 1, 3})
        self.assertEqual(result.items_matched, set())

        # Check no items should be matched
        result = game.make_guess(["6", "5", "7", "5"])
        self.assertEqual(result.result, GuessResult.POSITION_MATCH)
        self.assertEqual(result.indeces_matched, {0, 1, 3})
        self.assertEqual(result.items_matched, set())

        # Check correct items should be matched
        result = game.make_guess(["6", "7", "5", "5"])
        self.assertEqual(result.result, GuessResult.POSITION_MATCH)
        self.assertEqual(result.indeces_matched, {0, 3})
        self.assertEqual(result.items_matched, {"5"})

        # Check winning case
        result = game.make_guess(["6", "5", "0", "5"])
        self.assertEqual(result.result, GuessResult.FULL_MATCH)
        self.assertEqual(game.current_status(), Status.WON)

        # Start new game
        game.new_game()
        result = game.make_guess(["6", "7", "5", "5"])
        self.assertEqual(result.result, GuessResult.POSITION_MATCH)
        self.assertEqual(result.indeces_matched, {0, 3})
        self.assertEqual(result.items_matched, {"5"})

    def test_max_tries(self):
        options = Options()
        options.number_of_guesses = 4
        options.pattern_generator = MockGenerator(["6", "5", "0", "5"])
        game = Nordle(options)
        game.new_game()

        result = game.make_guess(["1", "2", "3", "4"])
        self.assertEqual(result.result, GuessResult.NO_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())
        self.assertEqual(game.current_status(), Status.STARTED)

        result = game.make_guess(["1", "2", "3", "4"])
        self.assertEqual(result.result, GuessResult.NO_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())
        self.assertEqual(game.current_status(), Status.STARTED)

        result = game.make_guess(["1", "2", "3", "4"])
        self.assertEqual(result.result, GuessResult.NO_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())
        self.assertEqual(game.current_status(), Status.STARTED)

        result = game.make_guess(["1", "2", "3", "4"])
        self.assertEqual(result.result, GuessResult.NO_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())
        self.assertEqual(game.current_status(), Status.LOST)

    def test_max_tries2(self):
        options = Options()
        options.number_of_guesses = 4
        options.pattern_generator = MockGenerator(["6", "5", "0", "5"])
        game = Nordle(options)
        game.new_game()

        result = game.make_guess(["1", "2", "3", "4"])
        self.assertEqual(result.result, GuessResult.NO_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())
        self.assertEqual(game.current_status(), Status.STARTED)

        result = game.make_guess(["1", "2", "3", "4"])
        self.assertEqual(result.result, GuessResult.NO_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())
        self.assertEqual(game.current_status(), Status.STARTED)

        result = game.make_guess(["1", "2", "3", "4"])
        self.assertEqual(result.result, GuessResult.NO_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())
        self.assertEqual(game.current_status(), Status.STARTED)

        result = game.make_guess(["6", "5", "0", "5"])
        self.assertEqual(result.result, GuessResult.FULL_MATCH)
        self.assertEqual(result.indeces_matched, set())
        self.assertEqual(result.items_matched, set())
        self.assertEqual(game.current_status(), Status.WON)


if __name__ == "__main__":
    import unittest

    unittest.main(verbosity=2)
