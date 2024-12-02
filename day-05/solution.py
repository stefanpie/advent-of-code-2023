from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pp

DIR_CURRENT = Path(__file__).parent


@dataclass
class SeedRange:
    start: int
    length: int


@dataclass
class Mapping:
    dest_start: int
    src_start: int
    length: int

    def map_num(self, num: int) -> int:
        if not self.is_num_in_mapping(num):
            raise ValueError(f"Number {num} is not in range of mapping {self}")
        return self.dest_start + (num - self.src_start)

    def is_num_in_mapping(self, num: int) -> bool:
        return self.src_start <= num < self.src_start + self.length

    def is_range_in_mapping(self, seed_range: SeedRange) -> bool:
        return not (
            seed_range.start >= self.src_start + self.length
            or seed_range.start + seed_range.length <= self.src_start
        )

    def map_range(self, seed_range: SeedRange) -> list[SeedRange]:
        mapped_ranges = []
        start = seed_range.start
        end = seed_range.start + seed_range.length

        mapping_start = self.src_start
        mapping_end = self.src_start + self.length

        if end <= mapping_start or start >= mapping_end:
            # No overlap, range remains unmapped
            return [seed_range]

        # Overlapping region
        overlap_start = max(start, mapping_start)
        overlap_end = min(end, mapping_end)

        # Before mapping
        if start < overlap_start:
            unmapped_length = overlap_start - start
            mapped_ranges.append(SeedRange(start, unmapped_length))

        # Mapped region
        mapped_length = overlap_end - overlap_start
        mapped_start = self.dest_start + (overlap_start - self.src_start)
        mapped_ranges.append(SeedRange(mapped_start, mapped_length))

        # After mapping
        if overlap_end < end:
            unmapped_start = overlap_end
            unmapped_length = end - overlap_end
            mapped_ranges.append(SeedRange(unmapped_start, unmapped_length))

        return mapped_ranges


@dataclass
class MappingGroup:
    all_mappings: list[Mapping] = field(default_factory=list)

    def map_num(self, num: int) -> int:
        can_be_mapped_all = [
            mapping for mapping in self.all_mappings if mapping.is_num_in_mapping(num)
        ]
        assert len(can_be_mapped_all) == 1 or len(can_be_mapped_all) == 0
        if len(can_be_mapped_all) == 1:
            return can_be_mapped_all[0].map_num(num)
        else:
            return num

    def map_range(self, seed_range: SeedRange) -> list[SeedRange]:
        mapped_ranges = []
        remaining_ranges = [seed_range]

        for mapping in self.all_mappings:
            new_remaining_ranges = []
            for r in remaining_ranges:
                if mapping.is_range_in_mapping(r):
                    mapped = mapping.map_range(r)
                    mapped_ranges.extend(mapped)
                else:
                    new_remaining_ranges.append(r)
            remaining_ranges = new_remaining_ranges

        # Add any remaining ranges that were not mapped
        mapped_ranges.extend(remaining_ranges)
        return mapped_ranges


@dataclass
class ParsedData:
    seeds: list[int] = field(default_factory=list)
    maps: dict[tuple[str, str], MappingGroup] = field(default_factory=dict)


@dataclass
class ParsedDataPart2:
    seed_ranges: list[SeedRange] = field(default_factory=list)
    maps: dict[tuple[str, str], MappingGroup] = field(default_factory=dict)

    @classmethod
    def from_parsed_data(cls, parsed_data: ParsedData) -> "ParsedDataPart2":
        seed_ranges = []
        for seed_start, seed_length in zip(
            parsed_data.seeds[::2], parsed_data.seeds[1::2]
        ):
            seed_range = SeedRange(seed_start, seed_length)
            seed_ranges.append(seed_range)
        return cls(seed_ranges, parsed_data.maps)


SECTIONS_MAPPINGS = [
    ("seed", "soil"),
    ("soil", "fertilizer"),
    ("fertilizer", "water"),
    ("water", "light"),
    ("light", "temperature"),
    ("temperature", "humidity"),
    ("humidity", "location"),
]


def parse_input(input_txt: str) -> ParsedData:
    sections = input_txt.split("\n\n")
    seeds = list(map(int, sections[0].strip().removeprefix("seeds: ").split(" ")))

    map_sections = sections[1:]
    assert len(map_sections) == len(SECTIONS_MAPPINGS)

    maps = {}
    for section_txt, (src, dest) in zip(map_sections, SECTIONS_MAPPINGS):
        section_lines = section_txt.strip().splitlines()[1:]
        mappings = []
        for single_map_line in section_lines:
            dest_start, src_start, length = map(int, single_map_line.split())
            mapping = Mapping(dest_start, src_start, length)
            mappings.append(mapping)
        mapping_group = MappingGroup(mappings)
        maps[(src, dest)] = mapping_group

    parsed_data = ParsedData(seeds, maps)

    return parsed_data


def part_1(input_data: ParsedData) -> int:
    results = {}
    for src, dest in SECTIONS_MAPPINGS:
        mapping_group = input_data.maps[(src, dest)]
        if src == "seed":
            results[dest] = [mapping_group.map_num(seed) for seed in input_data.seeds]
        else:
            assert src in results
            results[dest] = [mapping_group.map_num(result) for result in results[src]]

    min_location = min(results["location"])
    return min_location


def flatten_nested_list(nested_list: list) -> list:
    return [item for sublist in nested_list for item in sublist]


def part_2(input_data: ParsedDataPart2) -> int:
    results: dict[str, list[SeedRange]] = defaultdict(list)
    for src, dest in SECTIONS_MAPPINGS:
        mapping_group = input_data.maps[(src, dest)]

        if src == "seed":
            results[dest] = flatten_nested_list(
                [
                    mapping_group.map_range(seed_range)
                    for seed_range in input_data.seed_ranges
                ]
            )
        else:
            assert src in results
            results[dest] = flatten_nested_list(
                [mapping_group.map_range(result) for result in results[src]]
            )

    min_location_range = min(
        results["location"], key=lambda seed_range: seed_range.start
    )
    min_location = min_location_range.start

    return min_location


if __name__ == "__main__":
    input_fp = DIR_CURRENT / "input.txt"
    input_txt = input_fp.read_text().strip()

    input_data = parse_input(input_txt)

    part_1_output = part_1(input_data)
    print(f"Part 1: {part_1_output}")

    input_data_part2 = ParsedDataPart2.from_parsed_data(input_data)

    part_2_output = part_2(input_data_part2)
    print(f"Part 2: {part_2_output}")
