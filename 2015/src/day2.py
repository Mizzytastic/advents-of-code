import itertools
from typing import Iterable

def part1solver(packages: list[str]) -> int:
    packages = map(lambda line: map(int, line.split("x")), packages)
    sides = map(lambda dims: itertools.combinations(dims, 2), packages)
    paper = [[x * y for x, y in dims] for dims in sides]
    paper = sum(map(lambda sides: min(sides) + sum(map(lambda side: 2 * side, sides)), paper))
    return paper

def part1() -> None:
    with open("../input/day2test.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part1solver([test]) == int(expected)

    with open("../input/day2.txt") as file:
        print(part1solver(list(file)))

def part2solver(packages: list[str]) -> int:
    packages = map(lambda line: map(int, line.split("x")), packages)
    sides = [sorted([side for side in package]) for package in packages]

    accum = 0
    for s in sides:
        bow = list(itertools.accumulate(s, lambda x, y: x * y))[-1]
        smallest_perimiter = sum(map(lambda n: 2 * n, s[:2]))
        accum += bow + smallest_perimiter

    return accum
    

def part2() -> None:
    with open("../input/day2test_2.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part2solver([test]) == int(expected)

    with open("../input/day2.txt") as file:
        print(part2solver(list(file)))

if __name__ == "__main__":
    part1()
    part2()