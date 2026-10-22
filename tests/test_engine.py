"""Comprehensive unit tests for the core simulation engine in game_of_life.engine."""

import random
import pytest
from result import Err, Ok
from game_of_life.engine import (
    Grid,
    count_live_neighbors,
    create_empty_grid,
    place_pattern,
    seed_random,
    step,
)
from game_of_life.patterns import get_pattern


# --- Grid Creation & Validation Tests ---

def test_create_empty_grid_default_dimensions() -> None:
    """Default grid should be 30x30 with 0 live cells."""
    result = create_empty_grid()
    assert isinstance(result, Ok)
    grid = result.ok()
    assert grid.width == 30
    assert grid.height == 30
    assert grid.live_cell_count == 0


def test_create_empty_grid_invalid_dimensions() -> None:
    """Invalid dimensions should return an Err."""
    assert isinstance(create_empty_grid(0, 30), Err)
    assert isinstance(create_empty_grid(30, -5), Err)


# --- Fixed Dead Wall Neighbor Counting Tests ---

def test_neighbor_counting_center_cell() -> None:
    """A center cell with 3 neighbors should count exactly 3."""
    # Place 3 live cells around (5, 5): (4, 4), (4, 5), (6, 6)
    grid = create_empty_grid(10, 10).ok()
    grid = grid.with_cell(4, 4, 1).with_cell(4, 5, 1).with_cell(6, 6, 1)

    assert count_live_neighbors(grid, 5, 5) == 3
    assert count_live_neighbors(grid, 0, 0) == 0


def test_neighbor_counting_fixed_dead_wall_corners() -> None:
    """Corner cells must respect fixed dead walls without wrapping."""
    grid = create_empty_grid(10, 10).ok()
    # Top-left corner (0, 0) has only 3 valid adjacent neighbors: (0, 1), (1, 0), (1, 1)
    grid = grid.with_cell(0, 1, 1).with_cell(1, 0, 1)
    assert count_live_neighbors(grid, 0, 0) == 2

    # Bottom-right corner (9, 9) has only 3 valid neighbors: (8, 8), (8, 9), (9, 8)
    grid = grid.with_cell(8, 9, 1).with_cell(9, 8, 1)
    assert count_live_neighbors(grid, 9, 9) == 2


def test_neighbor_counting_out_of_bounds_target() -> None:
    """Counting neighbors for an out-of-bounds coordinate returns 0."""
    grid = create_empty_grid(10, 10).ok()
    assert count_live_neighbors(grid, -1, 0) == 0
    assert count_live_neighbors(grid, 10, 10) == 0


# --- Conway B2S23 Rules Tests ---

def test_rule_underpopulation() -> None:
    """Live cell with < 2 live neighbors dies."""
    # 0 neighbors: dies
    grid = create_empty_grid(5, 5).ok().with_cell(2, 2, 1)
    next_grid = step(grid)
    assert next_grid.get_cell(2, 2) == 0

    # 1 neighbor: dies
    grid = grid.with_cell(2, 3, 1)
    next_grid = step(grid)
    assert next_grid.get_cell(2, 2) == 0
    assert next_grid.get_cell(2, 3) == 0


def test_rule_survival_two_or_three_neighbors() -> None:
    """Live cell with 2 or 3 live neighbors survives."""
    # 2 neighbors: survives
    grid = (
        create_empty_grid(5, 5)
        .ok()
        .with_cell(2, 2, 1)
        .with_cell(2, 1, 1)
        .with_cell(2, 3, 1)
    )
    next_grid = step(grid)
    assert next_grid.get_cell(2, 2) == 1

    # 3 neighbors: survives
    grid = grid.with_cell(1, 2, 1)
    next_grid = step(grid)
    assert next_grid.get_cell(2, 2) == 1


def test_rule_overpopulation() -> None:
    """Live cell with > 3 live neighbors dies."""
    # 4 neighbors: dies
    grid = (
        create_empty_grid(5, 5)
        .ok()
        .with_cell(2, 2, 1)
        .with_cell(2, 1, 1)
        .with_cell(2, 3, 1)
        .with_cell(1, 2, 1)
        .with_cell(3, 2, 1)
    )
    next_grid = step(grid)
    assert next_grid.get_cell(2, 2) == 0


def test_rule_reproduction() -> None:
    """Dead cell with exactly 3 live neighbors becomes alive."""
    # (2, 2) is dead with 3 neighbors: (2, 1), (2, 3), (1, 2)
    grid = (
        create_empty_grid(5, 5)
        .ok()
        .with_cell(2, 1, 1)
        .with_cell(2, 3, 1)
        .with_cell(1, 2, 1)
    )
    assert grid.get_cell(2, 2) == 0
    next_grid = step(grid)
    assert next_grid.get_cell(2, 2) == 1


# --- Canonical Patterns Multi-generation Tests ---

def test_pattern_block_is_still_life() -> None:
    """Block pattern does not change across generations."""
    grid = create_empty_grid(10, 10).ok()
    block = get_pattern("block").ok()
    grid = place_pattern(grid, block, origin_row=4, origin_col=4).ok()

    gen1 = step(grid)
    assert gen1.cells == grid.cells
    gen2 = step(gen1)
    assert gen2.cells == grid.cells


def test_pattern_blinker_oscillates_period_two() -> None:
    """Horizontal blinker flips to vertical, then back to horizontal."""
    grid = create_empty_grid(10, 10).ok()
    blinker = get_pattern("blinker").ok()  # Horizontal: (0,0), (0,1), (0,2)
    grid = place_pattern(grid, blinker, origin_row=4, origin_col=4).ok()

    # Step 1: Vertical blinker around (4, 5)
    gen1 = step(grid)
    assert gen1.get_cell(3, 5) == 1
    assert gen1.get_cell(4, 5) == 1
    assert gen1.get_cell(5, 5) == 1
    assert gen1.get_cell(4, 4) == 0
    assert gen1.get_cell(4, 6) == 0

    # Step 2: Returns to original horizontal state
    gen2 = step(gen1)
    assert gen2.cells == grid.cells


# --- Pattern Placement Tests ---

def test_place_pattern_out_of_bounds() -> None:
    """Placing pattern outside the grid boundaries returns an Err."""
    grid = create_empty_grid(10, 10).ok()
    block = get_pattern("block").ok()

    # Right edge overflow
    assert isinstance(place_pattern(grid, block, origin_row=5, origin_col=9), Err)
    # Bottom edge overflow
    assert isinstance(place_pattern(grid, block, origin_row=9, origin_col=5), Err)
    # Negative origin
    assert isinstance(place_pattern(grid, block, origin_row=-1, origin_col=0), Err)


# --- Random Seeding Tests ---

def test_seed_random_respects_max_cells() -> None:
    """Random seeding should place between 1 and max_live_cells."""
    grid = create_empty_grid(30, 30).ok()
    rng = random.Random(42)  # Deterministic test seed

    result = seed_random(grid, max_live_cells=100, rng=rng)
    assert isinstance(result, Ok)
    seeded_grid = result.ok()
    assert 1 <= seeded_grid.live_cell_count <= 100
    assert seeded_grid.width == 30
    assert seeded_grid.height == 30


def test_seed_random_invalid_max_cells() -> None:
    """Seeding with <= 0 or > total grid capacity returns an Err."""
    grid = create_empty_grid(10, 10).ok()
    assert isinstance(seed_random(grid, max_live_cells=0), Err)
    assert isinstance(seed_random(grid, max_live_cells=101), Err)
