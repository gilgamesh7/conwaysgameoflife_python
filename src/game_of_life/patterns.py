"""Predefined Conway's Game of Life patterns and coordinates.

This module provides immutable pattern definitions (still-lifes, oscillators,
and spaceships) along with safe, Result-based pattern lookup.
"""

from dataclasses import dataclass
from typing import Final
from result import Err, Ok, Result


@dataclass(frozen=True, slots=True)
class Pattern:
    """Immutable definition of a Conway pattern.

    Attributes:
        name: Human-readable name of the pattern.
        width: Bounding box width (columns).
        height: Bounding box height (rows).
        live_cells: Frozen set of relative (row, col) coordinates that are alive.
    """

    name: str
    width: int
    height: int
    live_cells: frozenset[tuple[int, int]]


# Canonical patterns defined by relative (row, col) offsets
_PATTERNS: Final[dict[str, Pattern]] = {
    "block": Pattern(
        name="Block",
        width=2,
        height=2,
        live_cells=frozenset({(0, 0), (0, 1), (1, 0), (1, 1)}),
    ),
    "blinker": Pattern(
        name="Blinker",
        width=3,
        height=1,
        live_cells=frozenset({(0, 0), (0, 1), (0, 2)}),
    ),
    "glider": Pattern(
        name="Glider",
        width=3,
        height=3,
        live_cells=frozenset({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)}),
    ),
}


def list_patterns() -> list[str]:
    """Return a sorted list of registered pattern names."""
    return sorted(_PATTERNS.keys())


def get_pattern(name: str) -> Result[Pattern, str]:
    """Retrieve a predefined pattern by name.

    Performs case-insensitive lookup.

    Args:
        name: Name of the pattern (e.g. 'block', 'blinker', 'glider').

    Returns:
        Ok(Pattern) if found, Err(error_message) otherwise.
    """
    normalized = name.strip().lower()
    if normalized in _PATTERNS:
        return Ok(_PATTERNS[normalized])

    available = ", ".join(list_patterns())
    return Err(f"Unknown pattern '{name}'. Available patterns: {available}")
