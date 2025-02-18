import itertools

def part1solver(line: str) -> int:
    return sum(map(lambda ch: 1 if ch == "(" else -1, line))

def part1() -> None:
    with open("../input/day1test_1.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part1solver(test) == int(expected)

    with open("../input/day1.txt") as file:
        for line in file:
            print(part1solver(line.strip()))

def part2solver(line: str) -> int | None:
    return list(itertools.accumulate(map(lambda ch: 1 if ch == "(" else -1, line), initial = 0)).index(-1)

def part2() -> None:
    with open("../input/day1test_2.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part2solver(test) == int(expected)

    with open("../input/day1.txt") as file:
        for line in file:
            print(part2solver(line.strip()))

if __name__ == "__main__":
    part1()
    part2()