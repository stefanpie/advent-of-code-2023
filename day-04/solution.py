from dataclasses import dataclass
from pathlib import Path


@dataclass
class Card:
    id: int
    numbers_winning: set[int]
    numbers_mine: set[int]

    @property
    def num_matches(self) -> int:
        return len(self.numbers_winning.intersection(self.numbers_mine))


def parse_input(input_txt) -> list[Card]:
    lines = input_txt.splitlines()
    cards = []
    for line in lines:
        card_txt, numbers_txt = line.split(":")
        card_txt = card_txt.strip()
        numbers_txt = numbers_txt.strip()
        card_id = int(card_txt.split()[1])
        numbers_winning_txt, numbers_mine_txt = numbers_txt.split("|")
        numbers_winning_txt = numbers_winning_txt.strip()
        numbers_mine_txt = numbers_mine_txt.strip()
        numbers_winning = set(int(n) for n in numbers_winning_txt.split())
        numbers_mine = set(int(n) for n in numbers_mine_txt.split())
        card = Card(card_id, numbers_winning, numbers_mine)
        cards.append(card)
    return cards


def part_one(cards: list[Card]):
    scores = []
    for card in cards:
        num_matches = card.num_matches
        if num_matches == 0:
            scores.append(0)
        else:
            scores.append(2 ** (num_matches - 1))
    return sum(scores)


def part_two(cards: list[Card]):
    card_counts = {card.id: 1 for card in cards}
    for card in cards:
        num_matches = card.num_matches
        current_count = card_counts[card.id]
        for i in range(num_matches):
            card_counts[card.id + i + 1] += current_count
    return sum(card_counts.values())


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    input_small_fp = script_dir / "input_small.txt"
    input_fp = script_dir / "input.txt"

    in_fp = input_fp

    cards = parse_input(in_fp.read_text())

    sol_part_1 = part_one(cards)
    print(sol_part_1)

    sol_part_2 = part_two(cards)
    print(sol_part_2)
