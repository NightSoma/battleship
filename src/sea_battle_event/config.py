from dataclasses import dataclass


@dataclass(slots=True)
class GameConfig:
    rows: int
    cols: int
    seed: int
    ships: list[int]
