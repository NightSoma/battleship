from common.grid import Grid
from common.pos import Pos
from sea_battle.board import Board
from sea_battle.enums import HitResult


def test_check_hit__big_board():
    board = Board(10, 10, seed=42)
    board.fill_with_ships([1, 1, 1, 1, 2, 2, 2, 3, 3, 4])

    assert board.num_ships_alive == 10
    assert board.check_hit(Pos(4, 3)) == HitResult.ship_hit
    assert board.check_hit(Pos(4, 4)) == HitResult.miss
    assert board.check_hit(Pos(5, 3)) == HitResult.ship_hit
    assert board.check_hit(Pos(6, 3)) == HitResult.ship_hit
    assert board.check_hit(Pos(7, 3)) == HitResult.ship_destroyed
    assert board.num_ships_alive == 9
    assert board.check_hit(Pos(7, 3)) == HitResult.ship_was_destroyed
    assert board.num_ships_alive == 9


def test_check_hit__all_ships_destroyed():
    board = Board(3, 3, seed=42)
    board.fill_with_ships([1, 2])

    assert board.num_ships_alive == 2
    assert board.check_hit(Pos(0, 1)) == HitResult.ship_destroyed
    assert board.num_ships_alive == 1
    assert board.check_hit(Pos(2, 1)) == HitResult.ship_hit
    assert board.check_hit(Pos(2, 2)) == HitResult.ship_destroyed
    assert board.num_ships_alive == 0
    assert board.check_hit(Pos(0, 1)) == HitResult.ship_was_destroyed
    assert board.num_ships_alive == 0


def test__str__():
    board = Board(3, 3, seed=42)
    board.fill_with_ships([1, 2])

    assert str(board) == " # \n   \n ##"


def test_debug_grid():
    board = Board(3, 3, seed=42)
    board.fill_with_ships([1, 2])
    assert board.check_hit(Pos(0, 1)) == HitResult.ship_destroyed
    assert board.check_hit(Pos(1, 1)) == HitResult.miss
    grid = Grid(width=3, height=3, fill_value=" ")
    grid.grid = [
        [" ", "#", " "],
        [" ", "x", " "],
        [" ", "2", "2"],
    ]

    assert board.debug_grid == grid
