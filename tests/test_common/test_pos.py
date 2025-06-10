import pytest

from common.pos import Pos


def test__init__():
    pos = Pos(1, 2)
    assert pos.row == 1
    assert pos.col == 2


def test__add__positive_numbers():
    p1 = Pos(10, 12)
    p2 = Pos(11, 0)
    p3 = p2 + p1
    assert p3 == Pos(21, 12)


def test__add__negative_numbers():
    p1 = Pos(10, 12)
    p2 = Pos(-2, -5)
    p3 = p2 + p1
    assert p3 == Pos(8, 7)


def test__add__with_non_pos():
    pos1 = Pos(1, 2)
    other = 5
    with pytest.raises(TypeError):
        pos1 + other  # type: ignore


def test__mul__():
    p1 = Pos(10, 12)
    p3 = p1 * 2
    assert p3 == Pos(20, 24)


def test__mul__with_non_pos():
    pos1 = Pos(1, 2)
    other = "5"
    with pytest.raises(TypeError):
        pos1 * other  # type: ignore


def test_as_tuple():
    assert Pos(1, 2).as_tuple == (1, 2)


def test_copy():
    pos1 = Pos(1, 2)
    pos2 = pos1.copy
    assert pos2 == pos1


def test_up():
    assert Pos.up == Pos(-1, 0)


def test_right():
    assert Pos.right == Pos(0, 1)


def test_down():
    assert Pos.down == Pos(1, 0)


def test_left():
    assert Pos.left == Pos(0, -1)


def test_up_right():
    assert Pos.up_right == Pos(-1, 1)


def test_up_left():
    assert Pos.up_left == Pos(-1, -1)


def test_down_right():
    assert Pos.down_right == Pos(1, 1)


def test_down_left():
    assert Pos.down_left == Pos(1, -1)
