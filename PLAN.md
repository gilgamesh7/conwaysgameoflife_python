# Implementation Plan — Conway's Game of Life (Phase 1)

This plan outlines the ordered, incremental development units for Phase 1. Each unit is small, self-contained, and verified by tests before proceeding to the next.

---

## Unit 0: Environment Setup & Project Configuration
- [x] Create `pyproject.toml` specifying Python 3.14, runtime dependency `result>=0.17.0`, and dev dependency `pytest>=8.0.0`.
- [x] Establish package structure:
  - `src/game_of_life/__init__.py`
  - `tests/__init__.py`
- [x] Sync dependencies with `uv` into `.venv`.
- [x] Run `pytest` to verify tooling and test runner discovery.
- **Acceptance Criteria**:
  - [x] `uv run pytest` runs without errors.
  - [x] `python3 -c "from result import Ok, Err"` executes successfully.

---

## Unit 1: Predefined Patterns Module (`patterns.py`)
- [x] Write tests in `tests/test_patterns.py` for standard patterns:
  - Still life: `Block` (2×2)
  - Oscillator: `Blinker` (period 2)
  - Spaceship: `Glider`
- [x] Implement `src/game_of_life/patterns.py`:
  - Data structures (dataclasses/tuples) for pattern coordinates and bounding sizes.
  - Pattern registry or retrieval function returning `Result[Pattern, str]`.
- [x] Run tests and verify all pattern tests pass.
- **Acceptance Criteria**:
  - [x] Canonical patterns are accurately defined by relative coordinates.
  - [x] Pattern lookups return `Ok(Pattern)` or `Err("Pattern not found")`.
  - [x] 100% test pass rate in `tests/test_patterns.py`.

---

## Unit 2: Core Simulation Engine & B2S23 Rules (`engine.py`)
- [x] Write unit tests in `tests/test_engine.py`:
  - Grid creation (30×30 dimensions, all dead cells).
  - Fixed dead-wall neighbor counting (corners, edges, center cells).
  - B2S23 Conway rules:
    - Live cell with $< 2$ neighbors dies (underpopulation).
    - Live cell with $2$ or $3$ neighbors survives (survival).
    - Live cell with $> 3$ neighbors dies (overpopulation).
    - Dead cell with exactly $3$ neighbors becomes alive (reproduction).
  - Oscillator lifecycle (Blinker period 2 oscillation).
  - Random seeding: live cell count is $\le 100$ and within bounds.
  - Pattern placement onto the grid returning `Result[None, str]`.
- [x] Implement `src/game_of_life/engine.py`:
  - `Grid` class / dataclass with width, height, and cell states.
  - `count_live_neighbors(grid, row, col) -> int` with fixed wall boundary checks.
  - `step(grid) -> Grid` returning a new generation without mutating in place.
  - `seed_random(grid, max_live_cells=100) -> Result[Grid, str]`.
  - `place_pattern(grid, pattern, origin_row, origin_col) -> Result[Grid, str]`.
- [x] Run `pytest` and verify all tests pass.
- **Acceptance Criteria**:
  - [x] All B2S23 rules verified via automated tests.
  - [x] Fixed wall boundaries prevent `IndexError` and do not wrap.
  - [x] Seeding strictly enforces $1 \le \text{live cells} \le 100$.

---

## Unit 3: Terminal View & Decoupled Rendering (`app.py` renderer)
- [x] Design decoupled renderer in `src/game_of_life/app.py`:
  - `render_grid(grid: Grid, live_symbol: str = "♥", dead_symbol: str = " ") -> str`
  - Generation and population statistics banner.
  - Consistent character width and alignment across all 30 rows and 30 columns.
- [x] Add unit test in `tests/test_engine.py` or separate test file verifying:
  - Correct number of lines rendered (30 rows).
  - Correct symbols placed at alive/dead coordinates.
  - Independence: renderer receives a `Grid` data object, with no circular dependency on presentation logic.
- **Acceptance Criteria**:
  - [x] Output string represents the 30×30 grid accurately with heart symbols for live cells and spaces for dead cells.
  - [x] Zero terminal escape codes embedded in the core data engine.

---

## Unit 4: Simulation Loop, Audio Click & Graceful Exit (`app.py` CLI)
- [x] Implement the interactive CLI execution loop in `src/game_of_life/app.py`:
  - Initialization: 30×30 grid seeded with $\le 100$ random cells.
  - Loop:
    - Render current grid and generation count.
    - Trigger terminal bell sound (`\a`).
    - Advance to next generation via `step()`.
    - Pause for 3.0 seconds (`time.sleep(3.0)`).
  - Graceful exit:
    - Wrap loop in `try ... except KeyboardInterrupt:`.
    - On `Ctrl+C`, catch interrupt cleanly, leaving the final rendered generation and a graceful shutdown notice on screen.
- [x] Provide CLI invocation via `python -m game_of_life` or entrypoint in `__main__.py` / `app.py`.
- **Acceptance Criteria**:
  - [x] Application runs continuously advancing every 3 seconds with audible bell.
  - [x] `Ctrl+C` exits cleanly without stack traces and leaves the final grid visible.

---

## Unit 5: Verification, Documentation & Retrospective
- [x] Perform full manual run and verify acceptance criteria AC1–AC7.
- [x] Run all automated tests via `uv run pytest`.
- [x] Check type annotations and docstrings.
- [x] Create `RETRO.md` documenting architecture trade-offs and lessons learned.
- [x] Update `README.md` checkboxes.
- **Acceptance Criteria**:
  - [x] All automated tests pass.
  - [x] AC1–AC7 checked off in `README.md`.
  - [x] `RETRO.md` written.
