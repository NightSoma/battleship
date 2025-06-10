from dataclasses import dataclass


@dataclass(slots=True)
class Ship:
    cells: dict[tuple[int, int], bool]

    @property
    def alive(self) -> bool:
        return self.alive_cells_num > 0

    @property
    def alive_cells_num(self) -> int:
        return sum(1 for alive in self.cells.values() if alive)

    def __len__(self) -> int:
        return len(self.cells)
