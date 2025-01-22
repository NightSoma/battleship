from enum import Enum, auto


class EventName(Enum):
    GAME_INIT = auto()

    SET_PLAYER = auto()
    SET_BOARD = auto()
    FILL_BOARD_WITH_SHIPS = auto()
    SHIP_PLACED = auto()

    GAME_STARTED = auto()
    NEW_TURN = auto()

    PLAYER_GUESS = auto()
    PLAYER_GET_ANOTHER_GUESS = auto()
    NO_PLACES_LEFT = auto()

    SHOT_MISSED = auto()
    SHIP_HIT = auto()
    SHIP_DESTROYED = auto()
    SHIP_WAS_ALREADY_DESTROYED = auto()

    GAME_OVER = auto()


class Grid_State(Enum):
    SHIP_DESTROYED = auto()
    HIT = auto()
    EMPTY = auto()
    MAYBE_SHIP = auto()
    CANNOT_BE_SHIP = auto()
    UNKNOWN = auto()
