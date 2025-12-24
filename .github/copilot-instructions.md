# Copilot Instructions for Rounders Repository

## Repository Overview

**Rounders** is a Python package extending Python's `round()` with 13 rounding modes and significant figures support.

**Key Info**: Python 3.10+ library, ~4K lines, uses **uv 0.9.9** package manager, strict typing, 68 tests, 95% coverage

## Build Tools and Commands

**Package Manager**: uv 0.9.9 (install: `pip install uv==0.9.9`)

### Essential Commands (ALWAYS run uv sync first)

```bash
# Setup (REQUIRED before all other commands)
uv sync --locked              # ~30-60s first run, installs deps in .venv/

# Testing
uv run pytest                 # ~3-8s, runs 68 tests
uv run coverage run && uv run coverage report  # ~8-10s, shows coverage

# Type Checking
uv run mypy                   # ~5-10s, strict mode, must pass

# Linting/Formatting
uvx ruff check                # ~2-3s, lints (pydocstyle, isort, pyupgrade)
uvx ruff format --check       # ~1-2s, check formatting
uvx ruff format               # Fix formatting

# Building
uv build                      # ~5-10s, creates dist/ (gitignored)
```

**Important**: Use `uvx` for standalone tools (ruff), `uv run` for project deps (pytest, mypy)

## Project Structure

```
src/rounders/
├── __init__.py              # Package interface, all public exports
├── modes.py (166L)          # 13 rounding mode implementations
├── round_to.py (121L)       # Main functions: round, round_to_int, round_to_places, round_to_figures
├── mode_specific.py (105L)  # 13 mode-specific functions (ceil, floor, etc.)
├── intermediate_form.py     # Internal representation for rounding
├── generics.py              # Generic ops using singledispatch pattern
├── format.py (303L)         # Formatting support
├── target_format.py         # Target format specification
├── py.typed                 # PEP 561 type marker
├── overloads/               # Type-specific implementations (singledispatch)
│   ├── float.py (737L)      # Float optimizations with lookup tables
│   ├── decimal.py           # Decimal type support
│   ├── fraction.py          # Fraction type support
│   ├── int.py               # Integer type support
│   └── test/                # Overload-specific tests
└── test/                    # Main test suite
    ├── test_round.py (1021L)  # Primary rounding tests
    ├── test_format.py
    ├── test_intermediate_form.py
    └── test_target_format.py
```

### Architecture
- **Pattern**: functools.singledispatch for type-specific operations
- **Types**: int, float, Decimal, Fraction supported out-of-the-box
- **Modes**: 6 to-nearest (TIES_TO_*), 6 directed (TO_*), 1 special (TO_ZERO_05_AWAY)
- **Config**: All in `pyproject.toml` (build, test, lint, type checking)

## CI/CD Workflows

### `.github/workflows/on-commit.yml` (Pull Request Checks)
**Runs on**: PRs and manual dispatch  
**Matrix**: Python 3.10, 3.11, 3.12, 3.13, 3.14, 3.14t, pypy3.11

Jobs:
1. **test** (per Python version): `uv sync --locked` → `uv run mypy` → `uv run pytest`
2. **style** (once): `uvx ruff check` → `uvx ruff format --check`

### `.github/workflows/on-release.yml`
**Runs on**: Release published  
**Steps**: `uv build` → `uv publish` (to PyPI)

## Development Workflow

### Making Changes
1. `uv sync --locked` (if not done)
2. Make changes in `src/rounders/`
3. `uv run pytest` + `uv run mypy` + `uvx ruff check` + `uvx ruff format --check`

### Adding Rounding Mode
Edit: `modes.py`, `mode_specific.py`, `__init__.py`, add tests to `test/test_round.py`

### Adding Numeric Type Support
Create `overloads/newtype.py`, implement singledispatch overloads, import in `__init__.py`, add tests

## Key Facts

- **ALWAYS** use uv commands (not pip)
- `uv.lock` ensures reproducible builds - don't modify manually
- **Strict typing**: All public APIs need type annotations
- **NumPy docstrings**: Required for non-test files
- **Test conventions**: `test_*.py` files, `Test*` classes
- **Gitignored**: `__pycache__/`, `.coverage`, `.venv/`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `dist/`
- **Changelog**: Managed by scriv in `changelog.d/`

## Trust These Instructions

**IMPORTANT**: Trust these commands - they've been validated. Only search if:
- Instructions incomplete for your task
- You encounter errors contradicting these instructions
- You need implementation details not covered here

Use the exact commands above for build/test/lint - they work correctly.
