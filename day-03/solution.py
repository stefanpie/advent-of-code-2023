import math
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Numbers:
    row_col_start: tuple[int, int]
    row_col_end: tuple[int, int]
    number: int

    @property
    def coordinates(self):
        row, col_start = self.row_col_start
        _, col_end = self.row_col_end
        return [(row, col) for col in range(col_start, col_end)]


@dataclass
class Symbol:
    row_col: tuple[int, int]
    symbol: str

    @property
    def adjcent_coordinates(self):
        row, col = self.row_col
        return [
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
        ]


@dataclass
class SchematicGrid:
    numbers: list[Numbers]
    symbols: list[Symbol]


def parse_input(input_txt):
    part_numbers = []
    symbols = []

    for row_idx, line in enumerate(input_txt.splitlines()):
        matches_numbers = re.finditer(r"\d+", line)
        for match_number in matches_numbers:
            number = int(match_number[0])
            row_col_start = (row_idx, match_number.start())
            row_col_end = (row_idx, match_number.end())
            part_numbers.append(Numbers(row_col_start, row_col_end, number))
        matches_symbols = re.finditer(r"[^\d.]", line)
        for match_symbol in matches_symbols:
            symbol = match_symbol[0]
            row_col = (row_idx, match_symbol.start())
            symbols.append(Symbol(row_col, symbol))

    return SchematicGrid(part_numbers, symbols)


# The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)
def part_one(schematic):
    check_coordinates = set()
    for symbol in schematic.symbols:
        for adjcent_coordinate in symbol.adjcent_coordinates:
            check_coordinates.add(adjcent_coordinate)

    part_numbers = []
    for number in schematic.numbers:
        for coordinate in number.coordinates:
            if coordinate in check_coordinates:
                part_numbers.append(number.number)
                break
    return sum(part_numbers)


# The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.
# This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.
def part_two(schematic):
    gears = []
    stars = [symbol for symbol in schematic.symbols if symbol.symbol == "*"]
    for star in stars:
        adjcent_numbers = set()
        for adjcent_coordinate in star.adjcent_coordinates:
            for number in schematic.numbers:
                if adjcent_coordinate in number.coordinates:
                    adjcent_numbers.add(number.number)
        if len(adjcent_numbers) == 2:
            gears.append(math.prod(adjcent_numbers))
    return sum(gears)


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    input_small_fp = script_dir / "input_small.txt"
    input_fp = script_dir / "input.txt"

    in_fp = input_fp

    schematic = parse_input(in_fp.read_text())

    sol_part_1 = part_one(schematic)
    print(sol_part_1)

    sol_part_2 = part_two(schematic)
    print(sol_part_2)
