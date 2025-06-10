from common.grid import Grid
from common.pos import Pos
from sea_battle_event.board import Board
from sea_battle_event.config import GameConfig
from sea_battle_event.enums import EventName
from sea_battle_event.event_manager import EnentManager


def test_check_hit__big_board():
    event_manager = EnentManager()
    config = GameConfig(10, 10, 42, [1, 1, 1, 1, 2, 2, 2, 3, 3, 4])
    board = Board(event_manager, config)

    assert board.num_ships_alive == 10
    event_manager.add_to_event_queue(EventName.PLAYER_GUESS, Pos(4, 3))
    event_manager.process_events()

    shot_result_pairs = [
        (Pos(4, 3), EventName.SHIP_HIT),
        (Pos(4, 4), EventName.SHOT_MISSED),
        (Pos(5, 3), EventName.SHIP_HIT),
        (Pos(6, 3), EventName.SHIP_HIT),
        (Pos(7, 3), EventName.SHIP_DESTROYED),
        (Pos(7, 3), EventName.SHIP_WAS_ALREADY_DESTROYED),
    ]
    for pos, result in shot_result_pairs:
        board.check_hit(pos)
        assert event_manager.event_queue[-1] == (result, (pos,), {})

    assert board.num_ships_alive == 9


def test_check_hit__all_ships_destroyed():
    event_manager = EnentManager()
    config = GameConfig(3, 3, 42, [1, 2])
    board = Board(event_manager, config)

    assert board.num_ships_alive == 2

    board.check_hit(Pos(0, 1))
    assert event_manager.event_queue[-1] == (EventName.SHIP_DESTROYED, (Pos(0, 1),), {})

    assert board.num_ships_alive == 1

    board.check_hit(Pos(2, 1))
    assert event_manager.event_queue[-1] == (EventName.SHIP_HIT, (Pos(2, 1),), {})
    board.check_hit(Pos(2, 2))
    assert event_manager.event_queue[-1] == (EventName.SHIP_DESTROYED, (Pos(2, 2),), {})

    assert board.num_ships_alive == 0

    board.check_hit(Pos(2, 1))
    assert event_manager.event_queue[-1] == (
        EventName.SHIP_WAS_ALREADY_DESTROYED,
        (Pos(2, 1),),
        {},
    )

    assert board.num_ships_alive == 0


def test__str__():
    event_manager = EnentManager()
    config = GameConfig(3, 3, 42, [1, 2])
    board = Board(event_manager, config)

    assert str(board) == " # \n   \n ##"


def test_debug_grid():
    event_manager = EnentManager()
    config = GameConfig(3, 3, 42, [1, 2])
    board = Board(event_manager, config)

    board.check_hit(Pos(0, 1))
    assert event_manager.event_queue[-1] == (EventName.SHIP_DESTROYED, (Pos(0, 1),), {})

    board.check_hit(Pos(1, 1))

    assert event_manager.event_queue[-1] == (EventName.SHOT_MISSED, (Pos(1, 1),), {})

    grid = Grid(width=3, height=3, fill_value=" ")
    grid.grid = [
        [" ", "#", " "],
        [" ", "x", " "],
        [" ", "2", "2"],
    ]

    assert board.debug_grid == grid
