# Research & Technical Decisions — Conway's Game of Life (Phase 1)

This document records the technical evaluations, trade-offs, and architectural decisions made for Phase 1 of Conway's Game of Life, following the working principles in [AGENTS.md](AGENTS.md).

---

## 1. Testing Framework: `pytest` via `uv`

### Options Considered
1. **Python Standard Library `unittest`**:
   - *Pros*: Zero dependencies, included with Python 3.14.
   - *Cons*: Verbose syntax (`self.assertEqual`), boilerplate classes, less descriptive failure output.
2. **`pytest` managed with `uv` (Selected)**:
   - *Pros*:
     - Standard in modern Python development.
     - Clean `assert` statements without class boilerplate.
     - Excellent parameterization (`@pytest.mark.parametrize`) for testing B2S23 cellular automaton rules against various neighbor configurations.
     - Fast execution, automatic test discovery in `tests/`, and clear diff displays when assertions fail.
     - Managed cleanly and reproducibly via `uv` in `pyproject.toml`.

### Decision
Use **`pytest`** managed via **`uv`** as a development dependency.

---

## 2. Error Handling Pattern: 3rd-Party `result` Package

### Options Considered
1. **Standard Python Exceptions (`raise ValueError`)**:
   - *Pros*: Native to Python.
   - *Cons*: Exceptions are invisible in type signatures, making error paths implicit and easy to overlook.
2. **Custom Minimal `Result` class**:
   - *Pros*: No external dependency.
   - *Cons*: Requires maintenance and lacks advanced features (pattern matching helpers, unwrap methods).
3. **`result` library (`rustedpy/result`) (Selected)**:
   - *Pros*:
     - Brings Rust-style `Result[T, E]`, `Ok(value)`, and `Err(error)` to Python.
     - Fully type-annotated and compatible with `mypy` and Python 3.10+ / 3.14 pattern matching:
       ```python
       match result:
           case Ok(grid):
               ...
           case Err(err_msg):
               ...
       ```
     - Makes domain validation failures (e.g. invalid grid dimensions, out-of-bounds coordinates, invalid seed counts) explicit and safe.

### Decision
Adopt the **`result`** package as a core runtime dependency.

---

## 3. Project Architecture & Layout

### Directory Layout (`src/` Layout)
```text
conwaysgameoflife_python/
├── AGENTS.md                  # Development principles & agent instructions
├── README.md                  # Project overview, specifications & acceptance criteria
├── RESEARCH.md                # Research findings & technical decisions (this file)
├── PLAN.md                    # Ordered development units & progress tracker
├── RETRO.md                   # Retrospective lessons learned
├── pyproject.toml             # Project metadata, dependencies & tool configuration
├── src/
│   └── game_of_life/
│       ├── __init__.py        # Exposes public package API
│       ├── engine.py          # Grid state, B2S23 transition rules, neighbor counting
│       ├── patterns.py        # Predefined patterns (Block, Blinker, Glider)
│       └── app.py             # Rendering, clock loop, sound, and CLI runner
└── tests/
    ├── __init__.py
    ├── test_engine.py         # Tests for B2S23 rules, boundaries, and grid updates
    └── test_patterns.py       # Tests for pattern definitions and coordinate bounds
```

### Architectural Separation
- **`engine.py`**: Pure business logic. Completely agnostic to terminal or GUI rendering. Holds grid data, calculates live neighbors with fixed dead walls, and evaluates B2S23 generation transitions.
- **`patterns.py`**: Static and functional definitions of Conway patterns as offset coordinates, validated with `Result`.
- **`app.py`**: Presentation and orchestration. In Phase 1, it renders text with heart symbols, handles the 3-second clock, emits terminal bell clicks, and catches `Ctrl+C`. In Phase 2, the display functions can be swapped for a graphical interface without touching `engine.py`.

---

## 4. Grid Representation & Topology

### Grid Model: 2D Array vs. Set of Coordinates
- **Option A (2D Array/List of lists or tuples)**:
  - Fixed 30×30 matrix.
  - Very intuitive for beginners to visualize and render row by row.
  - Fast coordinate lookup `grid[row][col]`.
- **Option B (Sparse Set of (row, col) tuples)**:
  - Memory-efficient for unbounded boards.
  - Slightly more abstract for beginners when rendering fixed 30×30 boards.

### Decision
Use a 2D grid structure (or dataclass encapsulating a 30×30 grid of integers/booleans) with explicit bounds checking:
- **Topology**: Fixed dead walls. Any neighbor coordinate $(r, c)$ where $r < 0 \lor r \ge 30 \lor c < 0 \lor c \ge 30$ is strictly evaluated as dead (value $0$).

---

## 5. Terminal Display, Timing & Audio Mechanics

1. **Cell Representation**:
   - Live cell: Heart symbol (`♥` or `❤️`). Note: `♥` (U+2665 Black Heart Suit) is single-width in most monospace fonts; `❤️` (U+2764) is double-width emoji. We will use a consistent single or padded character (`♥ ` or `❤️ `) paired with spaces (`  `) to prevent row misalignment.
   - Dead cell: Spaces (`  ` or ` `) matching the exact width of the live cell character.
2. **Clock Advance**:
   - Standard 3.0-second delay between generations using `time.sleep(3.0)`.
3. **Audible Click**:
   - Cross-platform terminal bell: `sys.stdout.write('\a')` followed by `sys.stdout.flush()`.
4. **Graceful Exit**:
   - `try ... except KeyboardInterrupt:` wrapped around the main simulation loop.
   - On interrupt, terminal output prints a final message without clearing the terminal, leaving the final generation and generation counter intact on screen.
