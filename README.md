# Conways Game of Life using Antigravity
Generate Conway's Game of Life using AI-Assisted Coding

# Links
- [Real Python - Live AI Assisted Coding Repository](https://github.com/realpython/live-ai-assisted-coding)
- [You Tube - Conways Game of Life Explanation](https://youtu.be/484FWxvO-Ro?si=lD4WLgAttiOk1QwG)
- 

# Conway's Game of Life Rules 
1. Alive cells die if they have fewer than two (underpopulation) or more than three living neighbors (overpopulation).
2. Alive cells stay alive if they have two or three living neighbors.
3. Dead cells with exactly three living neighbors become alive (reproduction).

# Strategy
* Agreed on the aims and the definition of done before any code was written
* Asked the AI agent to research the tricky bits and draft a plan, and then had a second model review that plan

# Setup
## Initial
### Antigravity CLI
- curl -fsSL https://antigravity.google/cli/install.sh | bash
- echo 'export PATH="/Users/vrbabu/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
- agy --version
NOTE :  Antigravity CLI updates itself in place whenever a newer release is available. But you can trigger that manually at any time with agy update.
- To authenticate : agy
- To get available models : agy models
- Set model from list : agy --model "Gemini 3.8 Flash (High)"
### Useful commands
- Setting reasoning effort directly: agy --effort high
- Non-interactive / Print mode : agy -p "Explain the Game of Life rules" --model gemini-3.8-flash-high
- The agent might autonomously write its findings to an artifact. Artifacts are files saved alongside your conversations that serve as a structured record of the agent’s plans, execution results, and summaries for your review. You can reveal them in the artifact review panel by pressing Ctrl+R or using the /artifact slash command at any time.
<br> Note: If the agent doesn’t create one automatically, then you can explicitly prompt it to formalize its findings into an artifact for you to review.
- Implement the refactor you proposed and check if the code runs correctly.
- Resume a Past Conversation : agy --conversation=2aac6e9d-f723-4361-8b69-da94c2b6d89e (or -c)
- agy -p "Summarize the staged changes in one line for a commit message."

### Useful / slash commands
- Check your remaining allowance : /usage or /quota
- Prefix a prompt with /grill-me, and the agent interviews you with clarifying questions before it writes a single line, which suits fuzzy, underspecified tasks. Prefix it with /goal, and the agent runs straight through to completion without the intermediate approvals 
- /planning when a task sits between those extremes. The agent works out an approach before it starts, which suits deep research, complex multi-step work, or collaborative sessions where you want to see the shape of the plan before code lands.
- /fork command splits the current conversation so you can explore an alternative approach without losing your original thread. Meanwhile, /rewind rolls the history back to an earlier message when a session drifts off course.
- 

### Useful Prompts
- What does this project do? Give a concise high-level summary.
- Review @transactions.py for correctness and code-quality problems,
  and check it against this project's conventions. Be specific about
  any bugs.
- Use subagents : Add JSON, Markdown, and HTML export formats alongside the
  existing text report. Treat each as an independent job and
  spin up a subagent per format, each in its own formats
  module mirroring the format_report() signature. Then wire
  them into @cli.py behind a --format option and run the CLI
  once per format to verify.

### Setting House Rule for agents
Antigravity CLI reads an AGENTS.md file from your project root, the same way Gemini CLI reads GEMINI.md. The sample project ships one that spells out a few house rules: See AGENTS.md


---

# Phase 1: Product Brief & Specifications

## 1. Product Brief
**Conway's Game of Life (Phase 1 — Terminal Edition)** is a modular, well-tested Python 3.14 command-line application that runs Conway's Game of Life on a 30×30 grid with fixed dead walls. The board initializes with a random seed of up to 100 live cells (represented by heart symbols) and advances every 3 seconds accompanied by a terminal bell click. The simulation displays the generation count and runs until the user issues a graceful exit via `Ctrl+C`, leaving the final generation configuration intact on screen. The architecture strictly isolates the simulation engine and rules from the terminal view so the text renderer can be replaced with a graphical display in Phase 2.

## 2. Requirements

### Functional Requirements (FR)
- **FR1 (Grid & Topology)**: Maintain a 30×30 grid bounded by **fixed dead walls** (any neighbor outside the 0–29 index range is permanently dead).
- **FR2 (Random Seeding)**: Seed the grid at startup with a random count of live cells up to 100 (i.e., $1 \le \text{count} \le 100$).
- **FR3 (B2S23 Game Rules)**:
  - *Underpopulation*: A live cell with $< 2$ live neighbors dies.
  - *Survival*: A live cell with 2 or 3 live neighbors survives.
  - *Overpopulation*: A live cell with $> 3$ live neighbors dies.
  - *Reproduction*: A dead cell with exactly 3 live neighbors becomes alive.
- **FR4 (Decoupled Visual Display)**:
  - Render live cells as hearts (`♥` or `❤️`) and dead cells as spaces (` `).
  - Display the current generation count above or below the board.
  - Keep the rendering logic behind an abstract view interface so it can be swapped for a GUI in Phase 2 without modifying game rules.
- **FR5 (Clock & Pacing)**: Advance by one generation every 3 seconds.
- **FR6 (Audible Click)**: Trigger a terminal bell (`\a`) on each generation advance.
- **FR7 (Graceful Exit)**: Handle `Ctrl+C` cleanly to stop the clock immediately without traceback, leaving the final grid configuration and generation count on screen.

### Non-Functional Requirements (NFR)
- **NFR1 (Modern Python Standards)**: Use Python 3.14 idioms, descriptive names, full type hints, docstrings, and single-responsibility functions.
- **NFR2 (Modularity)**: Multi-module design (`grid.py`, `rules.py`, `views.py`, `engine.py`, `cli.py`).
- **NFR3 (Minimal Dependencies)**: Rely entirely on the Python standard library to keep the codebase simple and accessible for a beginner.
- **NFR4 (Test Coverage)**: Automated unit tests for core rules, grid boundaries, and seed constraints.

## 3. Explicit Acceptance Criteria
- [x] **AC1 (Grid Dimensions & Seeding)**: On startup, a 30×30 grid is created with a random number of live cells $\le 100$.
- [x] **AC2 (Fixed Boundary Behavior)**: Cells on edges and corners calculate neighbors against fixed dead walls without indexing errors or wrapping.
- [x] **AC3 (Visual Rendering)**: Live cells display as hearts; dead cells display as spaces; generation count is visibly updated on each tick.
- [x] **AC4 (B2S23 Rule Accuracy)**: Unit tests pass for all four Conway transition cases (underpopulation, survival, overpopulation, reproduction) using canonical patterns (e.g. Blinker, Block).
- [x] **AC5 (3-Second Clock & Bell)**: Generations advance every 3 seconds with a terminal bell sound emitted on each tick.
- [x] **AC6 (Graceful Exit)**: Pressing `Ctrl+C` halts the loop cleanly, prints no stack traces, and leaves the final generation displayed on screen.
- [x] **AC7 (Architecture Decoupling)**: Simulation logic operates independently of `print()` calls and the terminal environment.

## 4. Out-of-Scope for Phase 1
- Graphical window display (Pygame / Tkinter) — deferred to Phase 2.
- Interactive mouse or keyboard grid drawing.
- Pattern file import/export (RLE, Life 1.05 formats).
- Playback controls (pause, step back, variable speed).
- Infinite / toroidal wrapping grid.

## 5. Definition of Done
A unit or release is considered **Done** only when:
1. All acceptance criteria (AC1–AC7) are met and verified.
2. Automated unit tests run and pass.
3. Code is formatted, type-annotated, and documented.
4. Documentation is updated to reflect the state of the project.
