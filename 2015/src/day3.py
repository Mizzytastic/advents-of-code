import functools

direction_map: dict[str, tuple[int, int]] = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0)
}

def multi_walkers(movements: str, walkers: int = 1) -> int():

    class Walker():

        def __init__(self):
            self.current: tuple[int, int] = (0, 0)
            self.visited: set[tuple[int, int]] = {self.current}

    walker_list = [Walker() for _ in range(walkers)]

    for n, ch in enumerate(movements):
        walker = walker_list[n % walkers]
        x, y = walker.current
        dx, dy = direction_map[ch]
        walker.current = (x + dx, y + dy)
        walker.visited.add(walker.current)

    result = len(functools.reduce(lambda visited, walker: visited | walker.visited, walker_list, set()))
    return result

def part1solver(movements: str) -> int:
    return multi_walkers(movements)

def part1() -> None:
    with open("../input/day3test_1.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part1solver(test) == int(expected)

    with open("../input/day3.txt") as file:
        for line in file:
            print(part1solver(line.strip()))

def part2solver(movements: str) -> int:
    return multi_walkers(movements, 2)

def part2():
    with open("../input/day3test_2.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part2solver(test) == int(expected)

    with open("../input/day3.txt") as file:
        for line in file:
            print(part2solver(line.strip()))


if __name__ == "__main__":
    part1()
    part2()