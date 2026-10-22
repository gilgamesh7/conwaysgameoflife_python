"""Presentation, rendering, and application runner for Conway's Game of Life.

This module provides decoupled text rendering for Phase 1 (with heart symbols for
live cells and spaces for dead cells), with a clean interface that can be replaced
by a graphical display in Phase 2.
"""

import random
import sys
import time
from typing import Final
from game_of_life.engine import ALIVE, Grid, create_empty_grid, seed_random, step

# Default heart symbol and matching 2-character space for monospace terminal alignment
DEFAULT_LIVE_SYMBOL: Final[str] = "♥ "
DEFAULT_DEAD_SYMBOL: Final[str] = "  "


def render_grid(
    grid: Grid,
    live_symbol: str = DEFAULT_LIVE_SYMBOL,
    dead_symbol: str = DEFAULT_DEAD_SYMBOL,
) -> str:
    """Render the 2D grid into a multiline string using symbols for live and dead cells.

    Args:
        grid: The Grid data object to render.
        live_symbol: Character sequence representing an alive cell.
        dead_symbol: Character sequence representing a dead cell.

    Returns:
        A multiline string containing the formatted rows separated by newlines.
    """
    rows: list[str] = []
    for r in range(grid.height):
        row_str = "".join(
            live_symbol if grid.cells[r][c] == ALIVE else dead_symbol
            for c in range(grid.width)
        )
        rows.append(row_str)
    return "\n".join(rows)


def render_view(
    grid: Grid,
    generation: int,
    live_symbol: str = DEFAULT_LIVE_SYMBOL,
    dead_symbol: str = DEFAULT_DEAD_SYMBOL,
) -> str:
    """Render the full frame including header statistics and the grid.

    Args:
        grid: The Grid to display.
        generation: The current generation number.
        live_symbol: Symbol used for alive cells.
        dead_symbol: Symbol used for dead cells.

    Returns:
        Formatted multi-line frame ready for display.
    """
    header = (
        f"Conway's Game of Life (30x30) | Generation: {generation} | "
        f"Live Cells: {grid.live_cell_count} (Ctrl+C to exit)"
    )
    divider = "-" * len(header)
    grid_str = render_grid(grid, live_symbol=live_symbol, dead_symbol=dead_symbol)

    return f"{header}\n{divider}\n{grid_str}"


def emit_bell() -> None:
    """Emit an audible terminal bell character and flush output."""
    sys.stdout.write("\a")
    sys.stdout.flush()


def clear_screen() -> None:
    """Move cursor to home position and clear terminal screen."""
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


def run_simulation(
    max_generations: int | None = None,
    interval: float = 3.0,
    enable_bell: bool = True,
    rng: random.Random | None = None,
) -> Grid:
    """Run the Conway's Game of Life simulation loop.

    Advances the grid on a fixed timer, plays an audible bell on each tick,
    and terminates cleanly on Ctrl+C, leaving the final configuration visible.

    Args:
        max_generations: Optional generation cutoff for testing.
        interval: Delay in seconds between generation advances (default 3.0s).
        enable_bell: Whether to play an audible terminal bell on each tick.
        rng: Optional random generator instance for repeatable seeding.

    Returns:
        The final Grid state after halting.
    """
    grid = create_empty_grid(30, 30).ok()
    grid = seed_random(grid, max_live_cells=100, rng=rng).ok()
    generation = 0

    try:
        while True:
            clear_screen()
            sys.stdout.write(render_view(grid, generation=generation) + "\n")
            sys.stdout.flush()

            if enable_bell:
                emit_bell()

            if max_generations is not None and generation >= max_generations:
                break

            time.sleep(interval)
            grid = step(grid)
            generation += 1

    except KeyboardInterrupt:
        sys.stdout.write(
            "\nSimulation halted by user (Ctrl+C). Final configuration preserved on screen.\n"
        )
        sys.stdout.flush()

    return grid


def main() -> int:
    """CLI entrypoint for running the Game of Life application."""
    run_simulation()
    return 0


if __name__ == "__main__":
    sys.exit(main())

