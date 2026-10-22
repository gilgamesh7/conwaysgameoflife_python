
# Conway's Game of Life — Agent Instructions

## Project Goal

Build Conway's Game of Life as a small, well-tested Python application.
The purpose is both to deliver a working application and to learn
AI-assisted software development.

# Phase 1 Requirements 
1. When I add section "Phase 2 Requirements " , ignore this section
1. Use a 30 X 30 grid
1. Use a text display . Code it so this one be replaced by a graphical display later.
1. Seed the display at random with live cells, covering up to 100 cells .
1. Each live cell is to be denoted by a heart shape
1. Start the clock.
1. The generation clock has to advance every 3 seconds.
1. Make an audible click at each tick (advance) of the generation clock
1. Stop when escape is pressed, and leave final configuration on screen


## Working Principles

- Work incrementally, one approved development unit at a time.
- Read the relevant project documentation before changing code.
- Explain the proposed approach before implementing a substantial change.
- Do not implement the entire application in one step.
- Do not silently expand the agreed scope.
- Ask before making significant architectural or dependency changes.
- Keep changes small enough for a beginner to review and understand.
- Explain important technical decisions and trade-offs.

## Product and Engineering Standards

- Follow the B2S23 rules of Conway's Game of Life exactly
- Prefer readable, explicit Python over clever abstractions.
- Use type hints and descriptive names.
- Keep business logic separate from the user interface.
- Write automated tests for core logic and bug fixes.
- Avoid unnecessary dependencies.
- Do not introduce a framework without explaining why it is needed.
- Never claim a test passed unless it was actually run and passed.
- Use Python 3.14 with its idioms
- Modularity should be multi-module, with clear separation of concerns
- Generate Docstrings for documentation
- Use Type Hints
- Add Input Validation 
- Use results package for Rust-style error handling
- Enhance readability with named constants and small focused functions
- Functions should have single responsibility
- Maintain Code style consistency - Consistent quoting, type hints, structured comments

## Development Workflow

1. Review the current repository and existing files.
2. Clarify requirements and define the acceptance criteria.
3. Research technical options and record decisions in RESEARCH.md.
4. Create or update PLAN.md with small, ordered development units.
5. Present the plan for review before implementation.
6. Implement only the next approved unit.
7. Run relevant tests and checks after implementation.
8. Explain changed files, test results, and any limitations.
9. Update PLAN.md to reflect completed work.
10. Record useful lessons in RETRO.md.

## Git and Safety

- Inspect git status before making changes.
- Do not overwrite unrelated user changes.
- Do not commit, push, or delete files without explicit approval.
- Never store credentials, tokens, or secrets in the repository.
- Do not run destructive commands without explaining their impact
  and obtaining approval.

## Definition of Done

A development unit is complete only when:
- Its agreed acceptance criteria are met.
- Relevant automated tests pass.
- The code is readable and maintainable.
- Documentation is updated where necessary.
- The agent reports what changed and what remains incomplete.