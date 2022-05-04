from typing import List, Optional, Set, Dict, Any
from abc import abstractmethod
import requests
import random
import string


class PatternGeneratorBase:
    """
    This class defines the interface for Pattern Generator.
    """

    def generate(self, count: int, min: int, max: int) -> List[str]:
        raise NotImplemented("This function should be implemented in derived class.")


class RandomOrgPatternGenerator(PatternGeneratorBase):
    """
    This RandomOrgPatternGenerator will generate number patterns by getting random numbers from
    https://random.org.
    """

    def generate(self, count: int, min: int = 0, max: int = 7) -> List[str]:
        if count < 1 or min >= max:
            raise Exception("Invalid parameters provided to generate()")

        # In your Terminal you can test this url by using CURL.
        # curl --get "https://www.random.org/integers/?num=4&min=1&max=7&col=1&base=10&format=plain&rnd=new"
        r: requests.models.Response = requests.get(
            f"https://www.random.org/integers/?num={count}&min={min}&max={max}&col=1&base=10&format=plain&rnd=new"
        )
        return r.text.splitlines()


class CharacterPatternGenerator(PatternGeneratorBase):
    """
    This CharacterPatternGenerator will generate character patterns by calling random.choice.
    """

    def generate(self, count: int, min: int = 0, max: int = 26) -> List[str]:
        if count < 1 or min >= max or max > 26:
            raise Exception("Invalid parameters provided to generate()")

        result: List[str] = []
        for _ in range(count):
            result.append(random.choice(string.ascii_uppercase[min:max]))
        return result
        # return [random.choice(string.ascii_uppercase[min:max]) for _ in range(count)]


class Options:
    """
    This class specifies the options that can be specified for Nordle.
    """

    def __init__(self):
        self.number_of_guesses = 10
        self.pattern_length = 4
        self.pattern_max_value = 7
        self.pattern_generator: PatternGeneratorBase = RandomOrgPatternGenerator()


class Status:
    """
    This class specifies the Status codes that represent current status of Nordle game.
    """

    NOT_STARTED = 0
    STARTED = 1
    LOST = 2
    WON = 3


class GuessResult:
    """
    This class is provides information about a guess that was made. It also contains metadata like
    which positions matched and which items matched.
    """

    NO_MATCH = 0
    CONTENT_MATCH = 1
    POSITION_MATCH = 2
    FULL_MATCH = 3

    def __init__(self):
        self.result: int = GuessResult.NO_MATCH
        # This contains all the indices where user has correctly guessed the item.
        self.indeces_matched: Set[int] = set()
        # This contains all the items that are in the pattern but user guessed them at wrong index.
        self.items_matched: Set[str] = set()

    def get_result(self):
        return self.result

    def get_indeces_matched(self) -> Set[int]:
        return self.indeces_matched

    def get_items_matched(self) -> Set[str]:
        return self.items_matched


class Nordle:
    """
    This class represents the Nordle game. Instantiate this class and call new_game() to start
    a new game.
    """

    def __init__(self, options: Optional[Options] = None):
        self.options = options if options else Options()
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
        self.status = Status.STARTED
        # Call the generate function on the pattern generator to get the pattern
        # that user will guess.
        generator = self.options.pattern_generator

        self.pattern_to_guess = generator.generate(
            # Pattern length
            self.options.pattern_length,
            # Min value of pattern
            0,
            # Max value of pattern
            self.options.pattern_max_value
        )

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

        # If user guessed the exact pattern then end the game
        if inp == self.pattern_to_guess:
            self.status = Status.WON
            result.result = GuessResult.FULL_MATCH
            return result

        # If we have exhausted our tries then exit.
        if self.num_current_tries >= self.options.number_of_guesses:
            self.status = Status.LOST

        characters = set(self.pattern_to_guess)
        items_remaining: Dict[str, int] = {}
        for item in self.pattern_to_guess:
            items_remaining[item] = items_remaining.get(item, 0) + 1

        # See if any of the items in the guess align with the input
        for i in range(len(self.pattern_to_guess)):
            item = inp[i]

            if item == self.pattern_to_guess[i]:
                result.indeces_matched.add(i)
                items_remaining[item] -= 1

        # If there is no index based match then try to see if content
        # matches at any other location
        for i in range(len(self.pattern_to_guess)):
            item = inp[i]

            if item != self.pattern_to_guess[i] and item in characters:
                if items_remaining[item] > 0:
                    result.items_matched.add(item)

                items_remaining[item] -= 1

        if len(result.indeces_matched) > 0:
            result.result = GuessResult.POSITION_MATCH
        elif len(result.items_matched) > 0:
            result.result = GuessResult.CONTENT_MATCH

        return result
