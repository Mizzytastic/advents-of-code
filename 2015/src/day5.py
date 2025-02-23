def is_nice_part_1(string: str) -> bool:
    pairs = [string[ix: ix+2] for ix in range(len(string) - 1)]
    vowel_count = len(list(filter(lambda ch: ch in "aeiou", string)))
    matched_pair = any(map(lambda pair: pair[0] == pair[1], pairs))
    naughty_pair = any(map(lambda pair: pair in ("ab", "cd", "pq", "xy"), pairs))
    return vowel_count >= 3 and matched_pair and not naughty_pair

def is_nice_part_2(string: str) -> bool:
    pairs = [string[ix:ix+2] for ix in range(len(string) - 1)]
    triples = [string[ix:ix+3] for ix in range(len(string) - 2)]

    triple_edges_match = any(map(lambda triple: triple[0] == triple[2], triples))
    matching_pairs = False
    for n, pair in enumerate(pairs):
        if pair in pairs[n+2:]:
            matching_pairs = True
            break
    
    return triple_edges_match and matching_pairs

def part1solver(strings: list[str]) -> int:
    return len(list(filter(is_nice_part_1, strings)))

def part1() -> None:
    with open("../input/day5test_1.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part1solver([test]) == bool(int(expected))

    with open("../input/day5.txt") as file:
        print(part1solver([line.strip() for line in file]))

def part2solver(strings: list[str]) -> int:
    return len(list(filter(is_nice_part_2, strings)))

def part2() -> None:
    with open("../input/day5test_2.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part2solver([test]) == bool(int(expected))

    with open("../input/day5.txt") as file:
        print(part2solver([line.strip() for line in file]))

if __name__ == "__main__":
    part1()
    part2()