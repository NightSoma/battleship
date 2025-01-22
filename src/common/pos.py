from dataclasses import dataclass
from typing import ClassVar

from utils.timer import timer


@dataclass(frozen=True, slots=True)
class Pos:
    row: int
    col: int

    up: ClassVar["Pos"]
    down: ClassVar["Pos"]
    left: ClassVar["Pos"]
    right: ClassVar["Pos"]
    up_right: ClassVar["Pos"]
    up_left: ClassVar["Pos"]
    down_right: ClassVar["Pos"]
    down_left: ClassVar["Pos"]

    adjasent_pos: ClassVar["list[Pos]"]
    diagonals_pos: ClassVar["list[Pos]"]
    all_pos_around: ClassVar["list[Pos]"]

    @timer(print_enabled=False)
    def __add__(self, other: object) -> "Pos":
        if not isinstance(other, Pos):
            return NotImplemented

        return Pos(self.row + other.row, self.col + other.col)

    @timer(print_enabled=False)
    def __mul__(self, other: object) -> "Pos":
        if not (isinstance(other, int)):
            return NotImplemented

        return Pos(self.row * other, self.col * other)

    @property
    @timer(print_enabled=False)
    def as_tuple(self) -> tuple[int, int]:
        return self.row, self.col

    @property
    @timer(print_enabled=False)
    def copy(self) -> "Pos":
        return Pos(self.row, self.col)


Pos.up = Pos(-1, 0)
Pos.down = Pos(1, 0)
Pos.left = Pos(0, -1)
Pos.right = Pos(0, 1)
Pos.up_right = Pos(-1, 1)
Pos.up_left = Pos(-1, -1)
Pos.down_right = Pos(1, 1)
Pos.down_left = Pos(1, -1)

Pos.adjasent_pos = [Pos.up, Pos.right, Pos.down, Pos.left]
Pos.diagonals_pos = [Pos.up_right, Pos.down_right, Pos.down_left, Pos.up_left]
Pos.all_pos_around = [
    Pos.up,
    Pos.up_right,
    Pos.right,
    Pos.down_right,
    Pos.down,
    Pos.down_left,
    Pos.left,
    Pos.up_left,
]
