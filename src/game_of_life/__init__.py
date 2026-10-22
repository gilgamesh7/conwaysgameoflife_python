"""Conway's Game of Life package.

A modular, test-driven implementation of Conway's Game of Life in Python 3.14.
"""

from game_of_life.app import (
    DEFAULT_DEAD_SYMBOL,
    DEFAULT_LIVE_SYMBOL,
    emit_bell,
    main,
    render_grid,
    render_view,
    run_simulation,
)
from game_of_life.engine import (
    ALIVE,
    DEAD,
    Grid,
    count_live_neighbors,
    create_empty_grid,
    place_pattern,
    seed_random,
    step,
)
from game_of_life.patterns import Pattern, get_pattern, list_patterns

__all__ = [
    "ALIVE",
    "DEAD",
    "DEFAULT_DEAD_SYMBOL",
    "DEFAULT_LIVE_SYMBOL",
    "Grid",
    "Pattern",
    "count_live_neighbors",
    "create_empty_grid",
    "emit_bell",
    "get_pattern",
    "list_patterns",
    "main",
    "place_pattern",
    "render_grid",
    "render_view",
    "run_simulation",
    "seed_random",
    "step",
]
__version__ = "0.1.0"
