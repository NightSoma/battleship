from dataclasses import dataclass

from utils.timer import timer


@dataclass(slots=True)
class Ship:
    cells: dict[tuple[int, int], bool]

    @property
    @timer(print_enabled=False)
    def alive(self) -> bool:
        return self.alive_cells_num > 0

    @property
    @timer(print_enabled=False)
    def alive_cells_num(self) -> int:
        return sum(1 for alive in self.cells.values() if alive)

    @timer(print_enabled=False)
    def __len__(self) -> int:
        return len(self.cells)
