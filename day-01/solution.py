import re
from itertools import chain
from pathlib import Path

DIGIT_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGIT_NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def process_lines(lines, look_for_words=False):
    lines_computed = []
    for line in lines:
        match_iters = []
        substrings = DIGIT_NUMBERS
        if look_for_words:
            substrings += DIGIT_WORDS
        for substring in substrings:
            iter = re.finditer(substring, line)
            match_iters.append(iter)
        matches = chain(*match_iters)
        matches = sorted(matches, key=lambda x: x.start())
        match_first, match_last = matches[0][0], matches[-1][0]
        if match_first in DIGIT_WORDS:
            match_first = DIGIT_NUMBERS[DIGIT_WORDS.index(match_first)]
        if match_last in DIGIT_WORDS:
            match_last = DIGIT_NUMBERS[DIGIT_WORDS.index(match_last)]
        comb = int(f"{match_first}{match_last}")
        lines_computed.append(comb)
    return sum(lines_computed)


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    input_small_fp = script_dir / "input_small.txt"
    input_fp = script_dir / "input.txt"

    in_fp = input_fp

    input_txt = in_fp.read_text()
    lines = input_txt.splitlines()

    sol_part_1 = process_lines(lines, look_for_words=False)
    print(sol_part_1)

    sol_part_2 = process_lines(lines, look_for_words=True)
    print(sol_part_2)
