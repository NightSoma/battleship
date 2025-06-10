import random

from common.grid import Grid
from common.pos import Pos
from common.ship import Ship
from sea_battle_event.config import GameConfig
from sea_battle_event.enums import EventName
from sea_battle_event.event_manager import EnentManager


class Board:
    def __init__(self, event_manager: EnentManager, config: GameConfig):
        self.event_manager = event_manager
        self.subscriptions()

        self.rng = random.Random()
        self.rng.seed(config.seed)

        self.max_ship_lenght: int = max(config.ships)
        self.rows: int = config.rows
        self.cols: int = config.cols

        self.ships: list[Ship] = []
        self.num_ships_alive: int = 0
        self.ships_grid: Grid[Ship | None] = Grid(self.rows, self.cols, None)
        self.hit_grid: Grid[bool] = Grid(self.rows, self.cols, False)

        self.free_cells: dict[int, list[tuple[Pos, Pos]]] = (
            Board.generate_all_valid_ship_placements(
                self.rows, self.cols, self.max_ship_lenght, self.rng
            )
        )

        self.fill_with_ships(config.ships)

    def subscriptions(self) -> None:
        self.event_manager.subscribe(EventName.PLAYER_GUESS, self.check_hit)

    @staticmethod
    def generate_all_valid_ship_placements(
        rows: int,
        cols: int,
        max_ship_lenght: int,
        random_generator: random.Random,
    ) -> dict[int, list[tuple[Pos, Pos]]]:
        free_cells: dict[int, list[tuple[Pos, Pos]]] = {
            i: [] for i in range(1, max_ship_lenght + 1)
        }
        for length in range(max_ship_lenght):
            if length == 0:
                for row in range(rows):
                    for col in range(cols):
                        free_cells[1].append((Pos(row, col), Pos(0, 0)))
                continue

            for direction in Pos.adjasent_pos:
                start_rows, start_cols, end_rows, end_cols = Board.offset_borders(
                    rows, cols, length, direction
                )

                for row in range(start_rows, end_rows):
                    for col in range(start_cols, end_cols):
                        free_cells[length + 1].append((Pos(row, col), direction))

        for values in free_cells.values():
            random_generator.shuffle(values)

        return free_cells

    @staticmethod
    def offset_borders(rows: int, cols: int, length: int, direction: Pos):
        start_rows = 0
        start_cols = 0
        end_rows = rows
        end_cols = cols

        match direction:
            case Pos.up:
                start_rows += length
            case Pos.right:
                end_cols -= length
            case Pos.down:
                end_rows -= length
            case _:
                start_cols += length
        return start_rows, start_cols, end_rows, end_cols

    def fill_with_ships(self, ship_lengths: list[int]) -> None:
        self.event_manager.add_to_event_queue(
            EventName.FILL_BOARD_WITH_SHIPS, ship_lengths
        )
        for length in ship_lengths:
            self.place_random_ship(length)

    def place_random_ship(self, ship_length: int) -> None:
        while self.free_cells[ship_length]:
            pos, direction = self.free_cells[ship_length].pop()

            if self.place_ship(pos, direction, ship_length):
                return

    def place_ship(self, pos: Pos, direction: Pos, ship_length: int) -> bool:
        curr_pos = pos.copy
        for _ in range(0, ship_length):
            if self.is_ships_around(curr_pos):
                return False

            curr_pos = curr_pos + direction

        curr_pos = pos.copy
        ship = Ship({})
        for _ in range(0, ship_length):
            ship.cells[curr_pos.as_tuple] = True
            self.ships_grid[curr_pos.as_tuple] = ship
            curr_pos = curr_pos + direction

        self.event_manager.add_to_event_queue(
            EventName.SHIP_PLACED, ship, pos, direction, ship_length
        )
        self.num_ships_alive += 1
        self.ships.append(ship)
        return True

    def is_ships_around(self, pos: Pos) -> bool:
        for dir_pos in Pos.all_pos_around:
            pos_shifted = pos + dir_pos

            if not self.ships_grid.is_inside(*pos_shifted.as_tuple):
                continue
            if self.ships_grid[pos_shifted.as_tuple] is not None:
                return True
        return False

    def check_hit(self, pos: Pos) -> None:
        ship = self.ships_grid[pos.as_tuple]
        self.hit_grid[pos.as_tuple] = True
        if ship is None:
            self.event_manager.add_to_event_queue(EventName.SHOT_MISSED, pos)
        elif not ship.alive:
            self.event_manager.add_to_event_queue(
                EventName.SHIP_WAS_ALREADY_DESTROYED, pos
            )
        else:
            ship.cells[pos.as_tuple] = False
            if ship.alive:
                self.event_manager.add_to_event_queue(EventName.SHIP_HIT, pos)
            else:
                self.num_ships_alive -= 1
                if self.num_ships_alive <= 0:
                    self.event_manager.add_to_event_queue(EventName.GAME_OVER)
                self.event_manager.add_to_event_queue(EventName.SHIP_DESTROYED, pos)

    @property
    def debug_grid(self) -> Grid[str]:
        grid = Grid(self.rows, self.cols, " ")
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.ships_grid[row, col]
                if self.hit_grid[row, col] is True and cell is not None:
                    grid[row, col] = "#"
                elif cell is not None:
                    grid[row, col] = str(len(cell))
                elif self.hit_grid[row, col] is True:
                    grid[row, col] = "x"

        return grid

    def __str__(self) -> str:
        final_str: list[str] = []

        for row in range(self.rows):
            row_str: list[str] = []
            for col in range(self.cols):
                if self.ships_grid[row, col] is None:
                    row_str.append(" ")
                    continue
                row_str.append("#")
            final_str.append("".join(row_str))

        return "\n".join(final_str)
