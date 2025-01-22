import pytest

from common.grid import Grid
from common.pos import Pos
from sea_battle.enums import HitResult
from sea_battle.player import Grid_State, SimplePlayer


def test__init__():
    player = SimplePlayer(3, 3, 42)

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

    assert player.board_grid_state == Grid(3, 3, Grid_State.unknown)


def test_get_guess():
    player = SimplePlayer(3, 3, 42)
    guess = player.get_guess()
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
    assert guess == Pos(1, 0)


def test_get_guess__error_no_possible_places_left():
    player = SimplePlayer(0, 0, 42)
    with pytest.raises(ValueError):
        player.get_guess()


def test_feedback__no_guess_was_taken():
    player = SimplePlayer(3, 3, 42)
    assert player.last_guess is None
    player.give_feedback(HitResult.ship_was_destroyed)
    assert player.last_guess is None


def test_feedback__ship_hit_first_hit():
    player = SimplePlayer(3, 3, 42)
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
    player.give_feedback(HitResult.ship_hit)

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
        Pos(2, 0),
    ]
    assert player.board_grid_state[0, 1] == Grid_State.cannot_be_ship
    assert player.board_grid_state[2, 1] == Grid_State.cannot_be_ship

    assert player.board_grid_state[1, 0] == Grid_State.hit

    assert player.board_grid_state[0, 0] == Grid_State.maybe_ship
    assert player.board_grid_state[1, 1] == Grid_State.maybe_ship
    assert player.board_grid_state[2, 0] == Grid_State.maybe_ship


def test_feedback__ship_hit_second_hit():
    player = SimplePlayer(3, 3, 42)
    player.last_guess = Pos(1, 0)
    player.possible_places.pop()
    player.give_feedback(HitResult.ship_hit)
    player.last_guess = Pos(1, 1)
    player.give_feedback(HitResult.ship_hit)
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
        Pos(2, 0),
        Pos(1, 2),
    ]


def test_feedback__ship_destroyed():
    player = SimplePlayer(3, 3, 42)
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
    player.give_feedback(HitResult.ship_hit)
    player.last_guess = Pos(1, 1)
    assert player.possible_places.pop() == Pos(2, 0)
    player.give_feedback(HitResult.ship_destroyed)

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

    assert player.board_grid_state[1, 0] == Grid_State.ship_destroyed
    assert player.board_grid_state[1, 1] == Grid_State.ship_destroyed

    assert player.board_grid_state[0, 0] == Grid_State.cannot_be_ship
    assert player.board_grid_state[0, 1] == Grid_State.cannot_be_ship
    assert player.board_grid_state[0, 2] == Grid_State.cannot_be_ship
    assert player.board_grid_state[1, 2] == Grid_State.cannot_be_ship
    assert player.board_grid_state[2, 0] == Grid_State.cannot_be_ship
    assert player.board_grid_state[2, 1] == Grid_State.cannot_be_ship
    assert player.board_grid_state[2, 2] == Grid_State.cannot_be_ship


def test_feedback__miss():
    player = SimplePlayer(3, 3, 42)
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
    player.give_feedback(HitResult.miss)
    assert player.board_grid_state[1, 0] == Grid_State.empty
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
    player = SimplePlayer(3, 3, 42)
    player.last_guess = Pos(0, 0)
    with pytest.raises(ValueError):
        player.give_feedback(HitResult.ship_was_destroyed)


def test_feedback__unknown_hitresult():
    player = SimplePlayer(3, 3, 42)
    player.last_guess = Pos(0, 0)
    with pytest.raises(ValueError):
        player.give_feedback(HitResult.game_started)


def test_debug_grid():
    player = SimplePlayer(3, 3, seed=42)
    player.get_guess()
    player.give_feedback(HitResult.ship_hit)
    grid = Grid(width=3, height=3, fill_value=" ")
    grid.grid = [
        ["m", "c", " "],
        ["h", "m", " "],
        ["m", "c", " "],
    ]

    assert player.debug_grid == grid
