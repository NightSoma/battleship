import pytest

from common.grid import Grid
from common.pos import Pos
from sea_battle_event.config import GameConfig
from sea_battle_event.enums import EventName
from sea_battle_event.event_manager import EnentManager
from sea_battle_event.player import Grid_State, SimpleAIPlayer


def test__init__():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)

    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
        Pos(1, 0),
    ]

    assert player.board_grid_state == Grid(3, 3, Grid_State.UNKNOWN)


def test_get_guess():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)
    player.get_guess()
    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
    ]
    assert event_manager.event_queue[0] == (EventName.PLAYER_GUESS, (Pos(1, 0),), {})


def test_get_guess__error_no_possible_places_left():
    config = GameConfig(0, 0, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)
    player.get_guess()
    assert event_manager.event_queue[0] == (EventName.NO_PLACES_LEFT, (), {})


def test_feedback__no_guess_was_taken():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)

    assert player.last_guess is None
    player.ship_destroyed()
    player.ship_hit()
    player.shot_missed()
    assert player.last_guess is None


def test_feedback__ship_hit_first_hit():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)

    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
        Pos(1, 0),
    ]
    player.last_guess = Pos(1, 0)
    assert player.possible_places.pop() == Pos(1, 0)
    event_manager.add_to_event_queue(EventName.SHIP_HIT, Pos(1, 0))
    event_manager.process_events()

    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
        Pos(0, 0),
        Pos(1, 1),
    ]
    assert player.board_grid_state[0, 1] == Grid_State.CANNOT_BE_SHIP
    assert player.board_grid_state[2, 1] == Grid_State.CANNOT_BE_SHIP

    assert player.board_grid_state[1, 0] == Grid_State.HIT

    assert player.board_grid_state[0, 0] == Grid_State.MAYBE_SHIP
    assert player.board_grid_state[1, 1] == Grid_State.MAYBE_SHIP
    assert player.board_grid_state[2, 0] == Grid_State.MAYBE_SHIP


def test_feedback__ship_hit_second_hit_horizontal():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)

    player.last_guess = Pos(1, 0)
    player.possible_places.pop()
    event_manager.add_to_event_queue(EventName.SHIP_HIT, Pos(1, 0))
    event_manager.process_events()
    player.last_guess = Pos(1, 1)
    event_manager.add_to_event_queue(EventName.SHIP_HIT, Pos(1, 1))
    event_manager.process_events()
    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
        Pos(0, 0),
        Pos(1, 1),
    ]


def test_feedback__ship_hit_second_hit_vertical():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)

    player.last_guess = Pos(1, 0)
    player.possible_places.pop()
    event_manager.add_to_event_queue(EventName.SHIP_HIT, Pos(1, 0))
    event_manager.process_events()
    player.last_guess = Pos(2, 0)
    event_manager.add_to_event_queue(EventName.SHIP_HIT, Pos(2, 0))
    event_manager.process_events()
    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
    ]


def test_feedback__ship_destroyed():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)

    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
        Pos(1, 0),
    ]
    player.last_guess = Pos(1, 0)
    assert player.possible_places.pop() == Pos(1, 0)
    event_manager.add_to_event_queue(EventName.SHIP_HIT, Pos(1, 0))
    event_manager.process_events()
    player.last_guess = Pos(1, 1)
    assert player.possible_places.pop() == Pos(1, 1)
    event_manager.add_to_event_queue(EventName.SHIP_DESTROYED, Pos(1, 1))
    event_manager.process_events()

    assert player.possible_places == []

    assert player.board_grid_state[1, 0] == Grid_State.SHIP_DESTROYED
    assert player.board_grid_state[1, 1] == Grid_State.SHIP_DESTROYED

    assert player.board_grid_state[0, 0] == Grid_State.CANNOT_BE_SHIP
    assert player.board_grid_state[0, 1] == Grid_State.CANNOT_BE_SHIP
    assert player.board_grid_state[0, 2] == Grid_State.CANNOT_BE_SHIP
    assert player.board_grid_state[1, 2] == Grid_State.CANNOT_BE_SHIP
    assert player.board_grid_state[2, 0] == Grid_State.CANNOT_BE_SHIP
    assert player.board_grid_state[2, 1] == Grid_State.CANNOT_BE_SHIP
    assert player.board_grid_state[2, 2] == Grid_State.CANNOT_BE_SHIP


def test_feedback__miss():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)

    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
        Pos(1, 0),
    ]
    player.last_guess = Pos(1, 0)
    assert player.possible_places.pop() == Pos(1, 0)
    event_manager.add_to_event_queue(EventName.SHOT_MISSED, Pos(1, 0))
    event_manager.process_events()
    assert player.board_grid_state[1, 0] == Grid_State.EMPTY
    assert player.possible_places == [
        Pos(0, 1),
        Pos(0, 2),
        Pos(1, 2),
        Pos(1, 1),
        Pos(2, 2),
        Pos(2, 0),
        Pos(2, 1),
        Pos(0, 0),
    ]


def test_feedback__ship_was_destroyed():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)
    event_manager.add_to_event_queue(EventName.SHIP_WAS_ALREADY_DESTROYED, Pos(1, 0))
    player.last_guess = Pos(1, 0)
    with pytest.raises(ValueError):
        event_manager.process_events()


def test_debug_grid():
    config = GameConfig(3, 3, 42, [1, 2])
    event_manager = EnentManager()
    player = SimpleAIPlayer(event_manager, config)

    player.get_guess()
    event_manager.add_to_event_queue(EventName.SHIP_HIT, Pos(1, 0))
    event_manager.process_events()
    grid = Grid(width=3, height=3, fill_value=" ")
    grid.grid = [
        ["M", "C", " "],
        ["H", "M", " "],
        ["M", "C", " "],
    ]

    assert player.debug_grid == grid
