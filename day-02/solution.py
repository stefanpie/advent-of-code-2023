import math
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

ItemsCount = dict[str, int]  # color: count


@dataclass
class Pull:
    items: ItemsCount


@dataclass
class Game:
    gid: int
    pulls: list[Pull]


Games = list[Game]


def parse_input(input_txt) -> Games:
    games = []
    for line in input_txt.splitlines():
        print(line)
        gid, pulls = line.split(":")
        gid = gid.strip()
        pulls = pulls.strip()

        gid = int(gid.split(" ")[1])

        pulls_split = pulls.split(";")
        pulls_split = [pull.strip() for pull in pulls_split]
        pulls = []
        for pull in pulls_split:
            item_counts = pull.split(",")
            item_counts = [item_count.strip() for item_count in item_counts]
            items_collection = {}
            for item_count in item_counts:
                count, item = item_count.split(" ")
                count = int(count)
                items_collection[item] = count
            pulls.append(Pull(items_collection))
        games.append(Game(gid, pulls))
    return games


# The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
# In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.
def part_one(games: Games, guess_bag_count: ItemsCount) -> int:
    valid_game_ids: list[int] = []
    for game in games:
        game_pulls = game.pulls
        game_all_items: list[tuple[str, int]] = []
        for pull in game_pulls:
            game_all_items += pull.items.items()

        is_valid_items: list[bool] = []
        for item, count in game_all_items:
            if item in guess_bag_count:
                is_valid_items.append(count <= guess_bag_count[item])
            else:
                is_valid_items.append(False)
        if all(is_valid_items):
            valid_game_ids.append(game.gid)

    return sum(valid_game_ids)


# As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?
# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
# For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
def part_two(games: Games) -> int:
    min_bags: list[ItemsCount] = []
    for game in games:
        min_bag: ItemsCount = {}
        for pull in game.pulls:
            for item, count in pull.items.items():
                if item in min_bag:
                    min_bag[item] = max(min_bag[item], count)
                else:
                    min_bag[item] = count
        min_bags.append(min_bag)

    powers = [math.prod(bag.values()) for bag in min_bags]
    return sum(powers)


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    input_small_fp = script_dir / "input_small.txt"
    input_fp = script_dir / "input.txt"

    in_fp = input_fp

    games = parse_input(in_fp.read_text())
    pprint(games)

    guess_bag_count = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    sol_part_1 = part_one(games, guess_bag_count)
    print(sol_part_1)

    sol_part_2 = part_two(games)
    print(sol_part_2)
