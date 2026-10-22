"""Core simulation engine for Conway's Game of Life.

Provides the Grid data model, neighbor counting with fixed dead walls,
pure generation transitions (B2S23), pattern placement, and random seeding.
"""

from dataclasses import dataclass
import random
from typing import Final
from result import Err, Ok, Result
from game_of_life.patterns import Pattern

# 8 adjacent neighbor relative offsets: (dr, dc)
_NEIGHBOR_OFFSETS: Final[tuple[tuple[int, int], ...]] = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)

ALIVE: Final[int] = 1
DEAD: Final[int] = 0


@dataclass(frozen=True, slots=True)
class Grid:
    """Immutable representation of the 2D Game of Life grid.

    Attributes:
        width: Number of columns in the grid.
        height: Number of rows in the grid.
        cells: 2D tuple of cell states (1 for alive, 0 for dead).
    """

    width: int
    height: int
    cells: tuple[tuple[int, ...], ...]

    @property
    def live_cell_count(self) -> int:
        """Return the total number of live cells on the grid."""
        return sum(cell for row in self.cells for cell in row)

    def is_in_bounds(self, row: int, col: int) -> bool:
        """Check if coordinates fall within the grid boundaries."""
        return 0 <= row < self.height and 0 <= col < self.width

    def get_cell(self, row: int, col: int) -> int:
        """Get the state of the cell at (row, col).

        Returns 0 (DEAD) if out of bounds (fixed dead wall behavior).
        """
        if not self.is_in_bounds(row, col):
            return DEAD
        return self.cells[row][col]

    def with_cell(self, row: int, col: int, value: int) -> "Grid":
        """Return a new Grid with the cell at (row, col) set to value."""
        if not self.is_in_bounds(row, col):
            return self
        new_cells = [list(r) for r in self.cells]
        new_cells[row][col] = ALIVE if value else DEAD
        return Grid(
            width=self.width,
            height=self.height,
            cells=tuple(tuple(r) for r in new_cells),
        )


def create_empty_grid(width: int = 30, height: int = 30) -> Result[Grid, str]:
    """Create an empty Grid with all dead cells.

    Args:
        width: Number of columns (must be >= 1).
        height: Number of rows (must be >= 1).

    Returns:
        Ok(Grid) if dimensions are valid, Err(message) otherwise.
    """
    if width <= 0 or height <= 0:
        return Err(f"Invalid dimensions {width}x{height}. Both width and height must be >= 1.")

    cells = tuple(tuple(DEAD for _ in range(width)) for _ in range(height))
    return Ok(Grid(width=width, height=height, cells=cells))


def count_live_neighbors(grid: Grid, row: int, col: int) -> int:
    """Count the number of live neighbors for the cell at (row, col).

    Adheres strictly to fixed dead walls: any neighbor outside the grid boundary
    is evaluated as permanently dead (0).
    """
    if not grid.is_in_bounds(row, col):
        return 0

    count = 0
    for dr, dc in _NEIGHBOR_OFFSETS:
        nr, nc = row + dr, col + dc
        if grid.is_in_bounds(nr, nc) and grid.cells[nr][nc] == ALIVE:
            count += 1
    return count


def step(grid: Grid) -> Grid:
    """Advance the grid by one generation according to B2S23 Conway rules.

    Rules:
        1. Underpopulation: Live cell with < 2 live neighbors dies.
        2. Survival: Live cell with 2 or 3 live neighbors lives on.
        3. Overpopulation: Live cell with > 3 live neighbors dies.
        4. Reproduction: Dead cell with exactly 3 live neighbors becomes alive.

    Returns:
        A new Grid instance representing the next generation.
    """
    next_cells: list[tuple[int, ...]] = []

    for r in range(grid.height):
        row_cells: list[int] = []
        for c in range(grid.width):
            live_neighbors = count_live_neighbors(grid, r, c)
            current_state = grid.cells[r][c]

            if current_state == ALIVE:
                # Survival: 2 or 3 neighbors; otherwise Under/Overpopulation
                new_state = ALIVE if live_neighbors in (2, 3) else DEAD
            else:
                # Reproduction: exactly 3 neighbors
                new_state = ALIVE if live_neighbors == 3 else DEAD

            row_cells.append(new_state)
        next_cells.append(tuple(row_cells))

    return Grid(width=grid.width, height=grid.height, cells=tuple(next_cells))


def place_pattern(
    grid: Grid,
    pattern: Pattern,
    origin_row: int,
    origin_col: int,
) -> Result[Grid, str]:
    """Stamp a predefined pattern onto the grid at the given origin.

    Args:
        grid: Target Grid.
        pattern: Pattern instance to place.
        origin_row: Starting row for the top-left of the pattern.
        origin_col: Starting column for the top-left of the pattern.

    Returns:
        Ok(new_grid) if placement fits within boundaries, Err(message) otherwise.
    """
    if origin_row < 0 or origin_col < 0:
        return Err(f"Origin coordinates ({origin_row}, {origin_col}) cannot be negative.")

    if (origin_row + pattern.height > grid.height) or (origin_col + pattern.width > grid.width):
        return Err(
            f"Pattern '{pattern.name}' ({pattern.width}x{pattern.height}) at "
            f"({origin_row}, {origin_col}) exceeds grid dimensions ({grid.width}x{grid.height})."
        )

    new_cells = [list(r) for r in grid.cells]
    for dr, dc in pattern.live_cells:
        target_r = origin_row + dr
        target_c = origin_col + dc
        new_cells[target_r][target_c] = ALIVE

    return Ok(Grid(width=grid.width, height=grid.height, cells=tuple(tuple(r) for r in new_cells)))


def seed_random(
    grid: Grid,
    max_live_cells: int = 100,
    rng: random.Random | None = None,
) -> Result[Grid, str]:
    """Seed the grid with a random count of live cells up to max_live_cells.

    Args:
        grid: Base empty or existing grid.
        max_live_cells: Maximum number of live cells to seed (1 <= count <= max).
        rng: Optional random generator instance for deterministic testing.

    Returns:
        Ok(new_grid) on success, Err(message) if arguments are invalid.
    """
    total_cells = grid.width * grid.height
    if max_live_cells <= 0 or max_live_cells > total_cells:
        return Err(
            f"Invalid max_live_cells {max_live_cells}. Must be between 1 and {total_cells}."
        )

    generator = rng if rng is not None else random.Random()
    count_to_seed = generator.randint(1, min(max_live_cells, total_cells))

    # Pick unique random coordinate positions across the grid
    all_positions = [(r, c) for r in range(grid.height) for c in range(grid.width)]
    chosen_positions = generator.sample(all_positions, k=count_to_seed)

    new_cells = [list(r) for r in grid.cells]
    for r, c in chosen_positions:
        new_cells[r][c] = ALIVE

    return Ok(Grid(width=grid.width, height=grid.height, cells=tuple(tuple(r) for r in new_cells)))
