from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Grid(Generic[T]):
    width: int
    height: int
    fill_value: T
    grid: list[list[T]] = field(init=False)

    def __post_init__(self):
        self.grid = [
            [self.fill_value for _ in range(self.width)] for _ in range(self.height)
        ]

    def is_inside(self, row: int, col: int) -> bool:
        """Checks if the given row and column are within the grid's bounds."""
        return 0 <= row < self.height and 0 <= col < self.width

    def unsafe_set(self, key: tuple[int, int], value: T) -> None:
        """Sets the value at the given key without bounds checking.

        Args:
            key: A tuple (row, col) representing the index.
            value: The value to set.

        Raises:
            IndexError: If the index is out of bounds (unchecked).
        """
        row, col = key
        self.grid[row][col] = value

    def unsafe_get(self, key: tuple[int, int]) -> T:
        """Gets the value at the given key without bounds checking.

        Args:
            key: A tuple (row, col) representing the index.

        Returns:
            The value at the given index.

        Raises:
            IndexError: If the index is out of bounds (unchecked).
        """
        row, col = key
        return self.grid[row][col]

    def get_or_none(self, key: tuple[int, int]) -> T | None:
        """Gets the value at the given key or None if out of bounds.

        Args:
            key: A tuple (row, col) representing the index.

        Returns:
            The value at the given index or None if the index is out of bounds.
        """
        row, col = key
        if self.is_inside(row, col):
            return self.grid[row][col]
        return None

    def set_or_none(self, key: tuple[int, int], value: T) -> None:
        """Sets the value at the given key if within bounds, otherwise does nothing.

        Args:
            key: A tuple (row, col) representing the index.
            value: The value to set.
        """
        row, col = key
        if self.is_inside(row, col):
            self.grid[row][col] = value

    def __getitem__(self, key: tuple[int, int]) -> T:
        """Gets the value at the given key, raising IndexError if out of bounds.

        Args:
            key: A tuple (row, col) representing the index.

        Returns:
            The value at the given index.

        Raises:
            IndexError: If the index is out of bounds.
        """
        row, col = key
        if self.is_inside(row, col):
            return self.grid[row][col]
        raise IndexError(f"Index out of range {row}, {col}")

    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        """Sets the value at the given key, raising IndexError if out of bounds.

        Args:
            key: A tuple (row, col) representing the index.
            value: The value to set.

        Raises:
            IndexError: If the index is out of bounds.
        """
        row, col = key
        if self.is_inside(row, col):
            self.grid[row][col] = value
        else:
            raise IndexError(f"Index out of range {row}, {col}")
