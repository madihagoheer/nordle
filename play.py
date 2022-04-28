from nordle.nordle import Nordle, Status, GuessResult, Options
from colorama import Fore, Style
from typing import List, Optional, Set
import argparse


def format_hints(list: List[str], result: GuessResult) -> str:
    formatted_string = "Hint: "
    indeces = result.get_indeces_matched()
    items = result.get_items_matched()
    for index in range(len(list)):
        if index in indeces:
            formatted_string += f"{Fore.GREEN}{list[index]}{Style.RESET_ALL} "
        elif list[index] in items:
            formatted_string += f"{Fore.YELLOW}{list[index]}{Style.RESET_ALL} "
        else:
            formatted_string += f"{Fore.RED}{list[index]}{Style.RESET_ALL} "

    return formatted_string


def run_game(show_hints: bool, debug: bool, max_tries: int, pattern_length: int):
    options = Options()
    options.number_of_guesses = max_tries
    options.number_groups = pattern_length
    game = Nordle(options)
    game.new_game()
    while game.current_status() == Status.STARTED:
        guesses = game.remaining_guesses()
        print(f"Guesses Left: {guesses}")
        msg = "Please enter your guess separated by space (like 1 2 3 4): "
        user_input = str(input(msg)).strip()
        if not user_input:
            print("Incorrect input. Please try again.")
        else:
            print("\n")
            list = user_input.split(" ")
            result = game.make_guess(list)
            if game.remaining_guesses() > 0:
                if result.result == GuessResult.CONTENT_MATCH:
                    print("The player had guessed a number!")
                    if show_hints:
                        print(format_hints(list, result))
                elif result.result == GuessResult.POSITION_MATCH:
                    print(
                        "The player had guessed a correct number and its correct location"
                    )
                    if show_hints:
                        print(format_hints(list, result))
                elif result.result == GuessResult.NO_MATCH:
                    print("The player's guess was incorrect")
                    if show_hints:
                        print(format_hints(list, result))

    if game.current_status() == Status.WON:
        print("Congratulatinos You WON!")
    else:
        print("You Lost!")


def main():
    parser = argparse.ArgumentParser(description="Nordle Options.")
    parser.add_argument(
        "-n",
        "--no_hints",
        action="store_false",
        dest="hints",
        help="Do not show Hints.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug",
        help="Show pattern to guess.",
    )
    parser.add_argument(
        "-m",
        "--max_tries",
        dest="max_tries",
        help="Maximum number of retries.",
        default=10,
    )
    parser.add_argument(
        "-p",
        "--pattern_length",
        dest="pattern_length",
        help="Maximum number of retries.",
        default=4,
    )

    args = parser.parse_args()
    run_game(args.hints, args.debug, int(args.max_tries), int(args.pattern_length))


if __name__ == "__main__":
    main()
