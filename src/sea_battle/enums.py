from enum import Enum, auto


class HitResult(Enum):
    game_started = auto()
    miss = auto()
    ship_hit = auto()
    ship_destroyed = auto()
    ship_was_destroyed = auto()


class Grid_State(Enum):
    ship_destroyed = auto()
    hit = auto()
    empty = auto()
    maybe_ship = auto()
    cannot_be_ship = auto()
    unknown = auto()
