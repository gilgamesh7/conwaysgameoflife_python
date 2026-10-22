# Retrospective — Conway's Game of Life (Phase 1)

## 1. Project Summary

Phase 1 of **Conway's Game of Life** was implemented as a modular, test-driven Python 3.14 command-line application adhering strictly to the B2S23 Conway rules. The application runs on a 30×30 grid with fixed dead walls, seeds up to 100 random live cells depicted as heart symbols (`♥ `), ticks on a 3-second clock with an audible terminal bell (`\a`), and shuts down cleanly on `Ctrl+C`, preserving the final board configuration on screen.

---

## 2. What Went Well

1. **Test-Driven Development (TDD)**:
   - Writing tests before implementation for every unit ensured 100% of the B2S23 rules (underpopulation, survival, overpopulation, reproduction) and edge cases (corners, borders) were verified upfront.
   - Resulted in 31 passing tests executing in 0.05 seconds with zero regressions across units.

2. **Clean Separation of Concerns (Domain vs. Presentation)**:
   - `src/game_of_life/engine.py` is completely isolated from terminal output and I/O.
   - The presentation layer in `src/game_of_life/app.py` purely consumes `Grid` objects and formats strings.
   - This architectural decoupling guarantees that replacing the text renderer with a graphical display (GUI) in Phase 2 will require zero changes to the core engine.

3. **Rust-Style Error Handling with `result`**:
   - Employing `Result[T, E]` (`Ok`, `Err`) made domain constraints explicit in signatures (e.g., negative grid dimensions, out-of-bounds pattern stamps, invalid seed ranges) and avoided hidden runtime exceptions.

4. **Monospace Terminal Alignment**:
   - Addressing character width differences between heart symbols (`♥ `) and dead cell spaces (`  `) prevented horizontal column drift across terminal sizes.

5. **Testability of Time Loops**:
   - Designing `run_simulation()` with injectable parameters (`max_generations`, `interval`, `enable_bell`, `rng`) enabled automated testing of loop execution and `KeyboardInterrupt` handling without slow sleeps or manual intervention.

---

## 3. Challenges & Lessons Learned

1. **Terminal Bell Variability**:
   - The terminal bell (`\a`) standard behavior depends on the host terminal emulator and OS accessibility settings (e.g., visual bell vs audible bell). Flushing `sys.stdout` immediately after `\a` ensures delivery to the terminal.
2. **Double-width vs. Single-width Unicode**:
   - Heart emojis like `❤️` (U+2764 with variation selector) are treated as double-width (2 columns) in most terminals, whereas `♥` (U+2665 Black Heart Suit) is single-width. Pairing `♥` with a trailing space (`♥ `) consistently creates a 2-column cell matching a double-space (`  `).

---

## 4. Readiness for Phase 2

- **Public API**: The package cleanly exports `Grid`, `step`, `create_empty_grid`, `place_pattern`, `seed_random`, and `get_pattern` from `game_of_life`.
- **GUI Integration**: When Phase 2 begins, a GUI framework (such as Pygame or Tkinter) can import `Grid` and `step()` directly, rendering cells onto a graphical canvas without modifying any existing business logic.
