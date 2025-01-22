from sea_battle_event.ship import Ship


def test_alive():
    ship = Ship({(0, 0): True})

    assert ship.alive is True


def test_alive_cells_num():
    ship = Ship({(0, 0): True, (0, 1): True})

    assert ship.alive_cells_num == 2


def test__len__():
    ship = Ship({(0, 0): True})

    assert len(ship) == 1
