from typing import List, Optional, Set
from abc import abstractmethod
import requests


class Options:
    def __init__(self):
        self.number_of_guesses = 10
        self.number_groups = 4
        self.max_value_of_group = 7


class Status:
    NOT_STARTED = 0
    STARTED = 1
    LOST = 2
    WON = 3


class GuessResult:
    NO_MATCH = 0
    CONTENT_MATCH = 1
    POSITION_MATCH = 2
    FULL_MATCH = 3

    def __init__(self):
        self.result: int = 0
        self.indeces_matched: Set[int] = set()
        self.items_matched: Set[str] = set()

    def get_indeces_matched(self) -> Set[int]:
        return self.indeces_matched

    def get_items_matched(self) -> Set[str]:
        return self.items_matched


class GuessingGameRandomNumberGeneratorBase:
    def generate(self, count: int, min: int, max: int) -> List[str]:
        raise NotImplemented("This function should be implemented in derived class.")


class GuessingGameRandomOrg(GuessingGameRandomNumberGeneratorBase):
    def generate(self, count: int, min: int = 0, max: int = 7) -> List[str]:
        r = requests.get(
            f"https://www.random.org/integers/?num={count}&min={min}&max={max}&col=1&base=10&format=plain&rnd=new"
        )
        return r.text.splitlines()


class NordleGame:
    def __init__(self, options: Optional[Options] = None):
        self.options = options if options else Options()
        self.generator = GuessingGameRandomOrg()
        self.status = Status.NOT_STARTED
        self.pattern_to_guess: List[str] = []
        self.num_current_tries: int = 0

    def current_status(self) -> int:
        """returns a response string"""
        return self.status

    def remaining_guesses(self) -> int:
        return self.options.number_of_guesses - self.num_current_tries

    def hidden_pattern_to_guess(self) -> List[str]:
        return self.pattern_to_guess

    def new_game(self):
        if self.status != Status.NOT_STARTED:
            raise Exception("Game already running")
        self.status = Status.STARTED
        self.pattern_to_guess = self.generator.generate(self.options.number_groups)

    def save_game(self):
        pass

    def load_game(self):
        pass

    def make_guess(self, inp: List[str]) -> GuessResult:
        """returns a number guessed by the user"""

        # Do some sanity checking here
        if self.status != Status.STARTED:
            raise Exception("Game already ended")

        if len(inp) != len(self.pattern_to_guess):
            raise Exception(f"Input length should be: {len(self.pattern_to_guess)}")

        # First bump up the try count
        self.num_current_tries += 1

        result = GuessResult()
        result.result = GuessResult.NO_MATCH

        # If user guessed the exact pattern then end the game
        if inp == self.pattern_to_guess:
            self.status = Status.WON
            result.result = GuessResult.FULL_MATCH
            return result

        # If we have exhausted our tries then exit.
        if self.num_current_tries >= self.options.number_of_guesses:
            self.status = Status.LOST

        # See if any of the items in the guess align with the input
        for i in range(len(self.pattern_to_guess)):
            if inp[i] == self.pattern_to_guess[i]:
                result.indeces_matched.add(i)

        # If there is not index based match then try to see if content
        # matches at any other location
        characters = set(self.pattern_to_guess)
        for num in inp:
            if num in characters:
                result.items_matched.add(num)

        if len(result.indeces_matched) > 0:
            result.result = GuessResult.POSITION_MATCH
        elif len(result.items_matched) > 0:
            result.result = GuessResult.CONTENT_MATCH

        return result
