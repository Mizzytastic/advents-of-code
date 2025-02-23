import dataclasses
import enum
import re
import itertools
from typing import Callable

class InstructionType(enum.Enum):
    TURN_ON = enum.auto()
    TURN_OFF = enum.auto()
    TOGGLE = enum.auto()


    @property
    def do_type(self) -> Callable[[bool], bool]:
        def on(_: bool) -> bool:
            return True

        def off(_: bool) -> bool:
            return False

        def toggle(val: bool) -> bool:
            return not val

        match self.name:
            case "TURN_ON":
                return on
            case "TURN_OFF":
                return off
            case "TOGGLE":
                return toggle
            case _:
                raise Exception("Not reachable")


@dataclasses.dataclass(frozen=True, slots=True)
class Instruction:
    type: InstructionType
    minx: int
    miny: int
    maxx: int
    maxy: int


def parse_instructions(instruction_strs: list[str]) -> list[Instruction]:
    instruction_re = re.compile(r"(?P<type>turn on|turn off|toggle) (?P<minx>\d{1,3}),(?P<miny>\d{1,3}) through (?P<maxx>\d{1,3}),(?P<maxy>\d{1,3})")

    instructions: list[Instruction] = []
    for string in instruction_strs:
        # ignore typechecker because advent of code gives nice data we know will match, don't need to worry about None
        matched_instruction: re.Match = instruction_re.fullmatch(string) # type: ignore

        match matched_instruction.group("type"):
            case "turn on":
                ins_type = InstructionType.TURN_ON
            case "turn off":
                ins_type = InstructionType.TURN_OFF
            case "toggle":
                ins_type = InstructionType.TOGGLE

        instructions.append(Instruction(ins_type, 
            int(matched_instruction.group("minx")), int(matched_instruction.group("miny")),
            int(matched_instruction.group("maxx")) + 1, int(matched_instruction.group("maxy")) + 1))

    return instructions


@dataclasses.dataclass(frozen=True, slots=True)
class SwitchCell:
    status: bool
    minx: int
    miny: int
    maxx: int
    maxy: int


type Grid = list[list[SwitchCell]]


class SwitchGrid:
    """A sparse array of booleans that handles instructions"""

    
    def __init__(self, stating_state: bool = False, minx: int = 0, miny: int = 0, maxx: int = 1000, maxy: int = 1000):
        self.grid: Grid = [[SwitchCell(stating_state, minx, miny, maxx, maxy)]]


    def grid_from_instructions(self, instructions: list[Instruction], starting_state: bool = False, minx: int = 0, miny: int = 0, maxx: int = 1000, maxy: int = 1000) -> None:
        rowbreaks: set[int] = {miny, maxy}
        colbreaks: set[int] = {minx, maxx}
        for instruction in instructions:
            rowbreaks.add(instruction.miny)
            rowbreaks.add(instruction.maxy)
            colbreaks.add(instruction.minx)
            colbreaks.add(instruction.maxx)

        ordered_rowbreaks = sorted(list(rowbreaks))
        ordered_colbreaks = sorted(list(colbreaks))
        grid = [[SwitchCell(starting_state, xpair[0], ypair[0], xpair[1], ypair[1]) 
            for xpair in itertools.pairwise(ordered_colbreaks)] 
            for ypair in itertools.pairwise(ordered_rowbreaks)]

        self.rowbreaks = {rowbreak:n for n, rowbreak in enumerate(ordered_rowbreaks)}
        self.colbreaks = {colbreak:n for n, colbreak in enumerate(ordered_colbreaks)}
        self.grid = grid

    def do_instructions(self, instructions: list[Instruction]):
        self.grid_from_instructions(instructions)
        for instruction in instructions:
            for y in range(self.rowbreaks[instruction.miny], self.rowbreaks[instruction.maxy]):
                for x in range(self.colbreaks[instruction.minx], self.colbreaks[instruction.maxx]):
                    self.grid[y][x] = dataclasses.replace(self.grid[y][x], status = instruction.type.do_type(self.grid[y][x].status))

    def get_total_on(self) -> int:
        total = 0

        for row in self.grid:
            for cell in row:
                if cell.status:
                    total += (cell.maxx - cell.minx) * (cell.maxy - cell.miny)

        return total

def part1solver(instruction_strs: list[str]) -> int:
    instructions = parse_instructions(instruction_strs)

    grid = SwitchGrid()
    grid.do_instructions(instructions)
    return grid.get_total_on()


def part1() -> None:
    with open("../input/day6test_1.txt") as file:
        tests = []
        current_test: list[str] = []
        for line in file:
            if line.startswith("expected:"):
                tests.append( (current_test, int(line.strip().removeprefix("expected:"))) )
                current_test = []
            else:
                current_test.append(line.strip())
        
        for test, expected in tests:
            assert part1solver(test) == expected

    with open("../input/day6.txt") as file:
        print(part1solver([line.strip() for line in file]))
 

if __name__ == "__main__":
    part1()