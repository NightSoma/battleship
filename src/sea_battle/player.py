import random

from common.grid import Grid
from common.pos import Pos
from sea_battle.enums import Grid_State, HitResult


class SimplePlayer:
    def __init__(
        self, board_rows: int, board_cols: int, seed: int | None = None
    ) -> None:
        self.rng = random.Random()
        self.rng.seed(seed)

        self.board_rows = board_rows
        self.board_cols = board_cols

        self.board_grid_state: Grid[Grid_State] = Grid(
            board_rows, board_cols, Grid_State.unknown
        )
        self.last_guess: Pos | None = None

        self.possible_places: list[Pos] = [
            Pos(row, col)
            for col in range(self.board_cols)
            for row in range(self.board_rows)
        ]
        self.rng.shuffle(self.possible_places)

    def get_guess(self) -> Pos:
        while self.possible_places:
            self.last_guess = self.possible_places.pop()
            if self.board_grid_state[self.last_guess.as_tuple] in [
                Grid_State.maybe_ship,
                Grid_State.unknown,
            ]:
                return self.last_guess

        raise ValueError("No possible places left")

    def give_feedback(self, guess_result: HitResult) -> None:
        if self.last_guess is None:
            return
        pos = self.last_guess
        match guess_result:
            case HitResult.ship_hit:
                self.board_grid_state[pos.as_tuple] = Grid_State.hit
                self.set_diagonal_cells_as_not_possible(pos)
                is_hit_around = self.check_if_another_hits_was_around(pos)
                if not is_hit_around:
                    self.mark_sides_around_as_possible(pos)

            case HitResult.ship_destroyed:
                self.board_grid_state[pos.as_tuple] = Grid_State.hit
                self.mark_ship_destroyed_and_area_around(pos)

            case HitResult.miss:
                self.board_grid_state[pos.as_tuple] = Grid_State.empty

            case HitResult.ship_was_destroyed:
                raise ValueError("Ship was destroyed before!")

            case _:
                raise ValueError(f"Unknown guess result {guess_result}")

        self.last_guess = None

    def mark_ship_destroyed_and_area_around(self, pos: Pos) -> None:
        stack: list[Pos] = [pos]
        while stack:
            pos = stack.pop()

            grid_state = self.board_grid_state[pos.as_tuple]
            if grid_state in [
                Grid_State.unknown,
                Grid_State.maybe_ship,
            ]:
                self.board_grid_state[pos.as_tuple] = Grid_State.cannot_be_ship
                continue

            if grid_state not in [Grid_State.hit]:
                continue

            self.board_grid_state[pos.as_tuple] = Grid_State.ship_destroyed

            for dir_offset in Pos.all_pos_around:
                new_pos = pos + dir_offset

                if self.board_grid_state.is_inside(
                    *new_pos.as_tuple
                ) and self.board_grid_state[new_pos.as_tuple] not in [
                    Grid_State.cannot_be_ship,
                    Grid_State.ship_destroyed,
                ]:
                    stack.append(new_pos)

    def check_if_another_hits_was_around(self, pos: Pos) -> bool:
        dir_offset = None
        opposite_offset = None
        for dir_offset in Pos.adjasent_pos:
            new_pos = pos + dir_offset
            if (
                self.board_grid_state.is_inside(*new_pos.as_tuple)
                and self.board_grid_state[new_pos.as_tuple] == Grid_State.hit
            ):
                opposite_offset = dir_offset * -1
                break
        else:
            return False
        oposite_cell = pos + opposite_offset
        if self.board_grid_state.is_inside(*oposite_cell.as_tuple):
            self.board_grid_state[oposite_cell.as_tuple] = Grid_State.maybe_ship
            self.possible_places.append(oposite_cell)

        if dir_offset in [Pos.up, Pos.down]:
            for dir_offset in [Pos.right, Pos.left]:
                self.board_grid_state.set_or_none(
                    (pos + dir_offset).as_tuple, Grid_State.cannot_be_ship
                )
        else:
            for dir_offset in [Pos.up, Pos.down]:
                self.board_grid_state.set_or_none(
                    (pos + dir_offset).as_tuple, Grid_State.cannot_be_ship
                )

        return True

    def set_diagonal_cells_as_not_possible(self, pos: Pos) -> None:
        for dir_offset in Pos.diagonals_pos:
            self.board_grid_state.set_or_none(
                (pos + dir_offset).as_tuple, Grid_State.cannot_be_ship
            )

    def mark_sides_around_as_possible(self, pos: Pos) -> None:
        for dir_offset in Pos.adjasent_pos:
            new_pos = pos + dir_offset
            if (
                self.board_grid_state.is_inside(*new_pos.as_tuple)
                and self.board_grid_state[new_pos.as_tuple] == Grid_State.unknown
            ):
                self.board_grid_state[new_pos.as_tuple] = Grid_State.maybe_ship
                self.possible_places.append(new_pos)

    @property
    def debug_grid(self) -> Grid[str]:
        grid = Grid(self.board_rows, self.board_cols, " ")
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board_grid_state[row, col] != Grid_State.unknown:
                    grid[row, col] = self.board_grid_state[row, col].name[:1]
        return grid
