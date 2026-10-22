"""Unit tests for the presentation and rendering logic in game_of_life.app."""

from game_of_life.app import render_grid, render_view
from game_of_life.engine import create_empty_grid
from game_of_life.patterns import get_pattern


def test_render_grid_empty_dimensions() -> None:
    """An empty 30x30 grid should render 30 rows of spaces."""
    grid = create_empty_grid(30, 30).ok()
    rendered = render_grid(grid, live_symbol="♥ ", dead_symbol="  ")
    lines = rendered.split("\n")

    assert len(lines) == 30
    # Every row should contain 30 columns of double-space (60 characters)
    for line in lines:
        assert line == "  " * 30


def test_render_grid_with_live_cells() -> None:
    """Live cells should render with the specified live symbol."""
    grid = create_empty_grid(5, 5).ok()
    # Place a cell at (2, 2)
    grid = grid.with_cell(2, 2, 1)

    rendered = render_grid(grid, live_symbol="♥ ", dead_symbol="  ")
    lines = rendered.split("\n")

    assert len(lines) == 5
    # Row 2 should contain live symbol at position index 2 (col 2)
    row_2 = lines[2]
    expected_row_2 = "  " * 2 + "♥ " + "  " * 2
    assert row_2 == expected_row_2


def test_render_view_includes_generation_and_population() -> None:
    """render_view should include generation header, population count, and the grid."""
    grid = create_empty_grid(10, 10).ok()
    grid = grid.with_cell(1, 1, 1).with_cell(2, 2, 1)

    output = render_view(grid, generation=5, live_symbol="♥ ", dead_symbol="  ")

    assert "Generation: 5" in output
    assert "Live Cells: 2" in output
    assert "♥ " in output


def test_render_pattern_block() -> None:
    """Block pattern should render as a 2x2 cluster of hearts."""
    grid = create_empty_grid(4, 4).ok()
    block = get_pattern("block").ok()
    # Place block at (1, 1)
    grid = grid.with_cell(1, 1, 1).with_cell(1, 2, 1).with_cell(2, 1, 1).with_cell(2, 2, 1)

    rendered = render_grid(grid, live_symbol="♥ ", dead_symbol="  ")
    lines = rendered.split("\n")

    assert lines[0] == "  " * 4
    assert lines[1] == "  " + "♥ " * 2 + "  "
    assert lines[2] == "  " + "♥ " * 2 + "  "
    assert lines[3] == "  " * 4


def test_emit_bell(capsys: pytest.CaptureFixture[str]) -> None:
    """emit_bell should print the ASCII bell character \\a."""
    from game_of_life.app import emit_bell

    emit_bell()
    captured = capsys.readouterr()
    assert "\a" in captured.out


def test_run_simulation_bounded_generations() -> None:
    """run_simulation should execute bounded generations and return the final grid."""
    import random
    from game_of_life.app import run_simulation

    rng = random.Random(42)
    final_grid = run_simulation(
        max_generations=3,
        interval=0.001,
        enable_bell=False,
        rng=rng,
    )
    assert final_grid.width == 30
    assert final_grid.height == 30


def test_run_simulation_keyboard_interrupt_graceful_exit(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """When KeyboardInterrupt (Ctrl+C) occurs, simulation halts gracefully leaving state on screen."""
    import time
    from game_of_life.app import run_simulation

    # Simulate Ctrl+C on the first sleep
    def mock_sleep(_: float) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(time, "sleep", mock_sleep)

    final_grid = run_simulation(interval=3.0, enable_bell=False)
    captured = capsys.readouterr()

    assert final_grid is not None
    assert "Simulation halted by user (Ctrl+C)" in captured.out
    assert "Final configuration preserved on screen." in captured.out

