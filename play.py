from nordle.nordle import (
    Nordle,
    Status,
    GuessResult,
    Options,
    CharacterPatternGenerator,
)
from colorama import Fore, Back, Style
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


def run_game(
    show_hints: bool, show_pattern: bool, max_tries: int, pattern_length: int, char_mode: bool
) -> int:
    options = Options()
    options.number_of_guesses = max_tries
    options.pattern_length = pattern_length
    if char_mode:
        options.pattern_generator = CharacterPatternGenerator()
    game = Nordle(options)
    game.new_game()

    if show_pattern:
        p = game.hidden_pattern_to_guess()
        print("Pattern to guess: " + " ".join(p))

    while game.current_status() == Status.STARTED:
        guesses = game.remaining_guesses()
        print(f"Guesses Left: {guesses}")
        msg = "Please enter your guess separated by space (like 1 2 3 4): "
        user_input = str(input(msg))
        user_input = user_input.strip()

        if not user_input:
            print("Incorrect input. Please try again.")
            continue

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
        return Status.WON
    else:
        print("You Lost!")
        return Status.LOST


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
    parser.add_argument(
        "-c",
        "--character",
        action="store_true",
        dest="character",
        help="Switch to character based mode.",
    )

    args = parser.parse_args()

    print(f"{Back.WHITE}{Fore.BLACK} WELCOME TO NORDLE!! {Style.RESET_ALL}")
    total_played = 0
    total_lost = 0
    total_won = 0

    while True:
        result = run_game(
            args.hints,
            args.debug,
            int(args.max_tries),
            int(args.pattern_length),
            args.character,
        )
        total_played += 1
        if result == Status.WON:
            total_won += 1
        else:
            total_lost += 1

        print(f"Games played: {total_played}, Won: {total_won}, Lost: {total_lost} ")
        if str(input("\nContinue y/n: ")) != "y":
            break


if __name__ == "__main__":
    main()
