"""Unit tests for predefined Conway patterns in game_of_life.patterns."""

import pytest
from result import Err, Ok
from game_of_life.patterns import Pattern, get_pattern, list_patterns


def test_list_patterns_contains_canonical_patterns() -> None:
    """Ensure canonical patterns (block, blinker, glider) are listed."""
    patterns = list_patterns()
    assert "block" in patterns
    assert "blinker" in patterns
    assert "glider" in patterns


def test_get_pattern_block() -> None:
    """Test retrieving the 2x2 Block still-life pattern."""
    result = get_pattern("block")
    assert isinstance(result, Ok)
    pattern: Pattern = result.ok()
    assert pattern.name == "Block"
    assert pattern.width == 2
    assert pattern.height == 2
    assert pattern.live_cells == frozenset({(0, 0), (0, 1), (1, 0), (1, 1)})


def test_get_pattern_blinker() -> None:
    """Test retrieving the 3x1 Blinker oscillator pattern."""
    result = get_pattern("blinker")
    assert isinstance(result, Ok)
    pattern: Pattern = result.ok()
    assert pattern.name == "Blinker"
    assert pattern.width == 3
    assert pattern.height == 1
    assert pattern.live_cells == frozenset({(0, 0), (0, 1), (0, 2)})


def test_get_pattern_glider() -> None:
    """Test retrieving the 3x3 Glider spaceship pattern."""
    result = get_pattern("glider")
    assert isinstance(result, Ok)
    pattern: Pattern = result.ok()
    assert pattern.name == "Glider"
    assert pattern.width == 3
    assert pattern.height == 3
    # Canonical glider coordinates (row, col)
    assert pattern.live_cells == frozenset({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)})


def test_get_pattern_case_insensitive() -> None:
    """Pattern retrieval should be case-insensitive and ignore surrounding whitespace."""
    assert get_pattern("BLINKER").is_ok()
    assert get_pattern("  Block  ").is_ok()


def test_get_pattern_not_found() -> None:
    """Unknown pattern lookup returns an Err with a helpful error message."""
    result = get_pattern("nonexistent_shape")
    assert isinstance(result, Err)
    assert "Unknown pattern 'nonexistent_shape'" in result.err()


def test_pattern_immutability() -> None:
    """Pattern instances and their coordinates must be immutable."""
    result = get_pattern("block")
    pattern = result.ok()
    with pytest.raises(AttributeError):
        pattern.name = "Mutated"  # type: ignore[misc]
