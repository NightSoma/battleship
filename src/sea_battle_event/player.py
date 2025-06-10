import random
from typing import Any

from common.grid import Grid
from common.pos import Pos
from sea_battle_event.config import GameConfig
from sea_battle_event.enums import EventName, Grid_State
from sea_battle_event.event_manager import EnentManager


class SimpleAIPlayer:
    def __init__(self, event_manager: EnentManager, config: GameConfig) -> None:
        self.event_manager = event_manager
        self.rng = random.Random()
        self.rng.seed(config.seed)

        self.board_rows = config.rows
        self.board_cols = config.cols

        self.board_grid_state: Grid[Grid_State] = Grid(
            self.board_rows, self.board_cols, Grid_State.UNKNOWN
        )
        self.last_guess: Pos | None = None

        self.possible_places: list[Pos] = [
            Pos(row, col)
            for col in range(self.board_cols)
            for row in range(self.board_rows)
        ]
        self.rng.shuffle(self.possible_places)

        self.subscriptions()

    def subscriptions(self):
        self.event_manager.subscribe(EventName.NEW_TURN, self.get_guess)

        self.event_manager.subscribe(EventName.SHIP_DESTROYED, self.ship_destroyed)
        self.event_manager.subscribe(EventName.SHIP_HIT, self.ship_hit)
        self.event_manager.subscribe(
            EventName.SHIP_WAS_ALREADY_DESTROYED, self.ship_was_already_destroyed
        )
        self.event_manager.subscribe(EventName.SHOT_MISSED, self.shot_missed)

        self.event_manager.subscribe(EventName.PLAYER_GET_ANOTHER_GUESS, self.get_guess)

    def get_guess(self, *_: Any) -> None:
        while self.possible_places:
            self.last_guess = self.possible_places.pop()
            if self.board_grid_state[self.last_guess.as_tuple] in [
                Grid_State.MAYBE_SHIP,
                Grid_State.UNKNOWN,
            ]:
                self.event_manager.add_to_event_queue(
                    EventName.PLAYER_GUESS, self.last_guess
                )
                return

        self.event_manager.add_to_event_queue(EventName.NO_PLACES_LEFT)

    def ship_destroyed(self, *_: Any) -> None:
        if self.last_guess is None:
            return
        self.board_grid_state[self.last_guess.as_tuple] = Grid_State.HIT
        self.mark_ship_destroyed_and_area_around(self.last_guess)
        self.last_guess = None

        self.event_manager.add_to_event_queue(EventName.PLAYER_GET_ANOTHER_GUESS)

    def ship_hit(self, *_: Any) -> None:
        if self.last_guess is None:
            return
        self.board_grid_state[self.last_guess.as_tuple] = Grid_State.HIT
        self.set_diagonal_cells_as_not_possible(self.last_guess)
        is_hit_around = self.check_if_another_hits_was_around(self.last_guess)
        if not is_hit_around:
            self.mark_sides_around_as_possible(self.last_guess)
        self.last_guess = None

        self.event_manager.add_to_event_queue(EventName.PLAYER_GET_ANOTHER_GUESS)

    def shot_missed(self, *_: Any) -> None:
        if self.last_guess is None:
            return
        self.board_grid_state[self.last_guess.as_tuple] = Grid_State.EMPTY
        self.last_guess = None

    def ship_was_already_destroyed(self, *_: Any) -> None:
        raise ValueError("Ship was destroyed before!")

    def mark_ship_destroyed_and_area_around(self, pos: Pos) -> None:
        stack: list[Pos] = [pos]
        while stack:
            pos = stack.pop()

            grid_state = self.board_grid_state[pos.as_tuple]
            if grid_state in [Grid_State.UNKNOWN, Grid_State.MAYBE_SHIP]:
                self.board_grid_state[pos.as_tuple] = Grid_State.CANNOT_BE_SHIP
                continue

            if grid_state not in [Grid_State.HIT]:
                continue

            self.board_grid_state[pos.as_tuple] = Grid_State.SHIP_DESTROYED

            for dir_offset in Pos.all_pos_around:
                new_pos = pos + dir_offset

                if self.board_grid_state.is_inside(
                    *new_pos.as_tuple
                ) and self.board_grid_state[new_pos.as_tuple] not in [
                    Grid_State.CANNOT_BE_SHIP,
                    Grid_State.SHIP_DESTROYED,
                ]:
                    stack.append(new_pos)

    def check_if_another_hits_was_around(self, pos: Pos) -> bool:
        dir_offset = None
        opposite_offset = None
        for dir_offset in Pos.adjasent_pos:
            new_pos = pos + dir_offset
            if (
                self.board_grid_state.is_inside(*new_pos.as_tuple)
                and self.board_grid_state[new_pos.as_tuple] == Grid_State.HIT
            ):
                opposite_offset = dir_offset * -1
                break
        else:
            return False
        oposite_cell = pos + opposite_offset
        if self.board_grid_state.is_inside(*oposite_cell.as_tuple):
            self.board_grid_state[oposite_cell.as_tuple] = Grid_State.MAYBE_SHIP
            self.possible_places.append(oposite_cell)

        if dir_offset in [Pos.up, Pos.down]:
            for dir_offset in [Pos.right, Pos.left]:
                self.board_grid_state.set_or_none(
                    (pos + dir_offset).as_tuple, Grid_State.CANNOT_BE_SHIP
                )
        else:
            for dir_offset in [Pos.up, Pos.down]:
                self.board_grid_state.set_or_none(
                    (pos + dir_offset).as_tuple, Grid_State.CANNOT_BE_SHIP
                )

        return True

    def set_diagonal_cells_as_not_possible(self, pos: Pos) -> None:
        for dir_offset in Pos.diagonals_pos:
            self.board_grid_state.set_or_none(
                (pos + dir_offset).as_tuple, Grid_State.CANNOT_BE_SHIP
            )

    def mark_sides_around_as_possible(self, pos: Pos) -> None:
        for dir_offset in Pos.adjasent_pos:
            new_pos = pos + dir_offset
            if (
                self.board_grid_state.is_inside(*new_pos.as_tuple)
                and self.board_grid_state[new_pos.as_tuple] == Grid_State.UNKNOWN
            ):
                self.board_grid_state[new_pos.as_tuple] = Grid_State.MAYBE_SHIP
                self.possible_places.append(new_pos)

    @property
    def debug_grid(self) -> Grid[str]:
        grid = Grid(self.board_rows, self.board_cols, " ")
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board_grid_state[row, col] != Grid_State.UNKNOWN:
                    grid[row, col] = self.board_grid_state[row, col].name[:1]
        return grid
