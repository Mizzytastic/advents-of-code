import hashlib
from typing import Generator

import _hashlib
type hash = _hashlib.HASH

def prefix_plus_number_md5(prefix: str) -> Generator[tuple[int, hash]]:
    prefix_md5 = hashlib.md5(bytes(prefix, "UTF-8"))

    suffix_int = 0
    while True:
        full_md5 = prefix_md5.copy()
        full_md5.update(bytes(str(suffix_int), "UTF-8"))
        yield (suffix_int, full_md5)
        suffix_int += 1

def find_md5_prefix_and_num(prefix: str, hash_prefix: str) -> int:
    for n, md5 in prefix_plus_number_md5(prefix):
        hashed = md5.digest()

        if hashed.hex().startswith(hash_prefix):
            return n

    raise Exception("Unreachable code")

def part1solver(prefix: str) -> int:
    return find_md5_prefix_and_num(prefix, "00000")

def part1() -> None:
    with open("../input/day4test_1.txt") as file:
        for test, expected in (line.strip().split(":") for line in file):
            assert part1solver(test) == int(expected)

    with open("../input/day4.txt") as file:
        for line in file:
            print(part1solver(line))

def part2solver(prefix: str) -> int:
    return find_md5_prefix_and_num(prefix, "000000")

def part2() -> None:
    with open("../input/day4.txt") as file:
        for line in file:
            print(part2solver(line))

if __name__ == "__main__":
    part1()
    part2()