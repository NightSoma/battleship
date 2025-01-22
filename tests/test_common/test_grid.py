import pytest

from common.grid import Grid


def test__init__():
    assert Grid(width=3, height=3, fill_value=0).grid == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]


def test_is_inside():
    grid = Grid(width=3, height=3, fill_value=0)

    assert grid.is_inside(-1, 0) is False


def test_unsafe_get():
    grid = Grid(width=3, height=3, fill_value=0)
    grid.grid[0][0] = 1
    assert grid.unsafe_get((0, 0)) == 1


def test_unsafe_set():
    grid = Grid(width=3, height=3, fill_value=0)

    assert grid.unsafe_set((0, 0), 1) is None
    assert grid.grid[0][0] == 1


def test_get_or_none():
    grid = Grid(width=3, height=3, fill_value=0)
    grid.grid[0][0] = 1
    assert grid.get_or_none((0, 0)) == 1
    assert grid.get_or_none((-1, -1)) is None


def test_set_or_none():
    grid = Grid(width=3, height=3, fill_value=0)

    grid.set_or_none((-1, -1), 1)
    grid.set_or_none((2, 2), 10)
    assert grid.grid[2][2] == 10


def test__getitem__():
    grid = Grid(width=3, height=3, fill_value=0)

    with pytest.raises(IndexError):
        grid[-1, -1] = 5

    assert grid[2, 2] == 0


def test__setitem__():
    grid = Grid(width=3, height=3, fill_value=0)

    with pytest.raises(IndexError):
        grid[3, 3]

    grid[2, 2] = 10
    assert grid.grid[2][2] == 10
