import re
from typing import Callable

type Wire = str | int

def gate_parser(gates: list[str]) -> dict[str, tuple[str, tuple[str, ...]]]:
    value_re = r"(?P<value>(\d+|[A-Za-z]+) -> ([A-Za-z]+))"
    not_re = r"(?P<not>NOT (\d+|[A-Za-z]+) -> ([A-Za-z]+))"
    and_re = r"(?P<and>(\d+|[A-Za-z]+) AND (\d+|[A-Za-z]+) -> ([A-Za-z]+))"
    or_re = r"(?P<or>(\d+|[A-Za-z]+) OR (\d+|[A-Za-z]+) -> ([A-Za-z]+))"
    lshift_re = r"(?P<lshift>(\d+|[A-Za-z]+) LSHIFT (\d+) -> ([A-Za-z]+))"
    rshift_re = r"(?P<rshift>(\d+|[A-Za-z]+) RSHIFT (\d+) -> ([A-Za-z]+))"
    gate_re = r"|".join( (value_re, not_re, and_re, or_re, lshift_re, rshift_re) )

    gate_matches = (re.fullmatch(gate_re, gate) for gate in gates)
    parsed_gates = ((parsed.lastgroup, tuple(filter(lambda option: option != None, parsed.groups()))[1:]) 
        for parsed in gate_matches if parsed != None)

    wires_to_gates = {parts[-1]:(gate, parts[:-1]) for gate, parts in parsed_gates}
    return wires_to_gates


def part1solver(gates: list[str]) -> dict[str, int]:
    # First parse the gates into functional objects, and build a table corresponding output wire names to those gates.
    # For each wire in the table, backtrack through the circuit to find its value, building a new table of wire names to values as we go
    wires_to_gates = gate_parser(gates)

    results: dict[str, int] = {}
    def do_gate(wire: str) -> int:
        if wire in results:
            return results[wire]
        else:
            gate, inputs = wires_to_gates[wire]
            input_nums = tuple(map(lambda i: int(i) if i.isdigit() else do_gate(i), inputs))
            match gate:
                case "value":
                    results[wire] = input_nums[0]
                    return input_nums[0]
                case "not":
                    results[wire] = (~input_nums[0]) % 65536
                    return (~input_nums[0]) % 65536
                case "and":
                    results[wire] = input_nums[0] & input_nums[1]
                    return input_nums[0] & input_nums[1]
                case "or":
                    results[wire] = input_nums[0] | input_nums[1]
                    return input_nums[0] | input_nums[1]
                case "lshift":
                    results[wire] = (input_nums[0] << input_nums[1]) % 65536
                    return (input_nums[0] << input_nums[1]) % 65535
                case "rshift":
                    results[wire] = input_nums[0] >> input_nums[1]
                    return input_nums[0] >> input_nums[1]
                case _:
                    raise Exception("Should be unreachable due to advent of code having nice data")

    for wire in wires_to_gates.keys():  
        do_gate(wire)

    return results


def part1() -> int:
    with open("../input/day7test_1.txt") as file:
        gates = []
        results = {}

        read_expected = False
        for line in file:
            if read_expected:
                wire, result = line.strip().split(": ")
                results[wire] = int(result)
            elif line.strip() == "expected":
                read_expected = True
            else:
                gates.append(line.strip())

        assert part1solver(gates) == results

    with open("../input/day7.txt") as file:
        ans = part1solver([line.strip() for line in file])["a"]
        print(ans)
        return(ans)


def part2solver(part1ans: int, gates: list[str]) -> int:
    newgates = [f"{part1ans} -> b" if gate[-2:] == " b" else gate for gate in gates]
    return part1solver(newgates)["a"]


def part2(part1ans: int) -> None:
    with open("../input/day7.txt") as file:
        print(part2solver(part1ans, [line.strip() for line in file]))


if __name__ == "__main__":
    part1ans = part1()
    part2(part1ans)