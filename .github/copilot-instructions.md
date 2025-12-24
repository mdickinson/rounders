# Copilot Instructions for Rounders Repository

## Repository Overview

**Rounders** is a Python package that extends Python's built-in `round()` function with 13 different rounding modes and the ability to round to significant figures. The package provides drop-in replacements for `round()` that use alternative rounding modes (e.g., TIES_TO_AWAY, TO_PLUS, TO_MINUS), as well as specialized functions for rounding to significant figures.

**Repository Type**: Python library/package  
**Primary Language**: Python (100%)  
**Minimum Python Version**: 3.10  
**Package Manager**: uv (Astral's fast Python package manager)  
**Lines of Code**: ~4,000 (excluding tests and dependencies)  
**Key Dependencies**: typing-extensions (conditional for Python < 3.11)

## Build Tools and Environment

This project uses **uv** (version 0.9.9) for all dependency management, building, and testing. The workflow uses uv's locked dependencies via `uv.lock` for reproducible builds.

### Installing uv

If uv is not available, install it first:
```bash
pip install uv==0.9.9
```

### Environment Setup

**ALWAYS run this command first** before any other commands:
```bash
uv sync --locked
```
- Time: ~30-60 seconds on first run, faster on subsequent runs
- Creates `.venv/` virtual environment
- Installs all dependencies including dev tools (pytest, mypy, coverage)
- The `--locked` flag ensures exact versions from `uv.lock` are used

## Testing

### Running Tests

To run all tests:
```bash
uv run pytest
```
- Time: ~3-8 seconds
- Runs 68 tests across the test suite
- Tests are located in `src/rounders/test/` and `src/rounders/overloads/test/`
- Configuration in `pyproject.toml` under `[tool.pytest.ini_options]`

### Running Tests with Coverage

```bash
uv run coverage run
uv run coverage report
```
- Time: ~8-10 seconds for coverage run
- Current coverage: ~95%
- Coverage configuration in `pyproject.toml` under `[tool.coverage.run]`

### Running Specific Tests

```bash
uv run pytest src/rounders/test/test_round.py
uv run pytest -v  # verbose output
```

## Type Checking

```bash
uv run mypy
```
- Time: ~5-10 seconds
- Checks types for all files in the `rounders` package
- Configuration in `pyproject.toml` under `[tool.mypy]`
- This project uses strict type checking (`strict = true`)
- **ALWAYS passes** in the current state

## Linting and Formatting

### Linting with Ruff

```bash
uvx ruff check
```
- Time: ~2-3 seconds
- Checks code style, imports, docstrings
- Configuration in `pyproject.toml` under `[tool.ruff.lint]`
- Enabled checks: pydocstyle (D), isort (I), pyupgrade (UP), pycodestyle warnings (W)
- Uses NumPy docstring convention

### Formatting with Ruff

```bash
uvx ruff format --check  # Check formatting
uvx ruff format          # Fix formatting
```
- Time: ~1-2 seconds
- Formats 23 Python files

### Important: uvx vs uv run

- Use `uvx` for tools that don't need to be in the project environment (ruff)
- Use `uv run` for tools installed in the dev dependencies (pytest, mypy, coverage)

## Building the Package

```bash
uv build
```
- Time: ~5-10 seconds
- Creates `dist/` directory (automatically gitignored)
- Builds both source distribution (.tar.gz) and wheel (.whl)
- Uses `uv_build` backend (specified in `pyproject.toml`)

## Project Structure and Architecture

```
rounders/
├── .github/
│   └── workflows/
│       ├── on-commit.yml    # CI: runs on PRs and manual dispatch
│       └── on-release.yml   # CD: publishes to PyPI
├── src/rounders/            # Main package source
│   ├── __init__.py          # Package interface, exports all public APIs
│   ├── modes.py             # 13 rounding mode implementations
│   ├── round_to.py          # Top-level rounding functions (round, round_to_int, etc.)
│   ├── mode_specific.py     # Mode-specific rounding functions (13 variants)
│   ├── intermediate_form.py # Internal representation for rounding operations
│   ├── target_format.py     # Target format specification
│   ├── format.py            # Formatting support
│   ├── generics.py          # Generic operations using singledispatch
│   ├── py.typed             # PEP 561 marker for type information
│   ├── overloads/           # Type-specific implementations
│   │   ├── float.py         # Float-specific optimizations (737 lines)
│   │   ├── decimal.py       # Decimal type support
│   │   ├── fraction.py      # Fraction type support
│   │   ├── int.py           # Integer type support
│   │   └── intermediate_form.py  # IntermediateForm support
│   └── test/                # Unit tests
│       ├── test_round.py    # Main rounding tests (1021 lines)
│       ├── test_format.py
│       ├── test_intermediate_form.py
│       └── test_target_format.py
├── changelog.d/             # Changelog entries (managed by scriv)
├── pyproject.toml           # Project configuration (build, test, lint)
├── uv.lock                  # Locked dependencies
└── README.md                # Comprehensive documentation
```

### Key Architectural Elements

1. **Single Dispatch Pattern**: Uses `functools.singledispatch` for type-specific operations in `generics.py`
2. **Rounding Modes**: 13 rounding modes defined in `modes.py`:
   - 6 to-nearest modes: TIES_TO_EVEN, TIES_TO_ODD, TIES_TO_AWAY, TIES_TO_ZERO, TIES_TO_MINUS, TIES_TO_PLUS
   - 6 directed modes: TO_EVEN, TO_ODD, TO_AWAY, TO_ZERO, TO_MINUS, TO_PLUS
   - 1 special mode: TO_ZERO_05_AWAY
3. **Type Support**: Out-of-the-box support for int, float, Decimal, and Fraction
4. **Intermediate Form**: Internal representation that decouples input types from rounding logic

## GitHub Workflows (CI/CD)

### on-commit.yml (Pull Request Checks)
Runs on: Pull requests and manual dispatch

**Matrix Testing**: Tests against Python 3.10, 3.11, 3.12, 3.13, 3.14, 3.14t, pypy3.11

Steps for each Python version:
1. `uv sync --locked` - Set up environment
2. `uv run mypy` - Type checking
3. `uv run pytest` - Run tests

**Style Check** (separate job):
1. `uvx ruff check` - Linting
2. `uvx ruff format --check` - Format checking

### on-release.yml
Runs on: Release published or manual dispatch
- Builds package with `uv build`
- Publishes to PyPI with `uv publish`

## Files and Directories to Ignore

These are already gitignored, but for reference:
- `__pycache__/` - Python bytecode
- `.coverage` - Coverage database
- `.venv/` - Virtual environment (created by uv sync)
- `.mypy_cache/` - Mypy cache
- `.pytest_cache/` - Pytest cache
- `.ruff_cache/` - Ruff cache
- `dist/` - Build artifacts

## Common Workflows

### Making a Code Change
1. `uv sync --locked` (if not already done)
2. Make your changes to files in `src/rounders/`
3. `uv run pytest` - Verify tests pass
4. `uv run mypy` - Verify types are correct
5. `uvx ruff check` - Check linting
6. `uvx ruff format --check` - Check formatting (or use `uvx ruff format` to auto-fix)

### Adding a New Rounding Mode
- Add mode definition in `modes.py`
- Add mode-specific function in `mode_specific.py`
- Export from `__init__.py`
- Add tests in `test/test_round.py`

### Adding Support for a New Numeric Type
- Create new file in `overloads/` directory
- Implement singledispatch overloads for: `preround`, `decade`, `is_finite`, `is_zero`, `to_type_of`
- Import in `__init__.py` to register overloads
- Add tests in `overloads/test/`

## Important Notes

### Dependencies and Tools
- **Always use uv commands**, not pip or other package managers
- The project uses `uv.lock` for reproducible builds - don't modify it manually
- Development dependencies are defined in `pyproject.toml` under `[dependency-groups]`

### Testing Strategy
- Tests use pytest with `--pyargs` and `--import-mode=importlib` options
- Test files follow `test_*.py` naming convention
- Test classes follow `Test*` naming convention
- Docstring requirements are relaxed for test files (see `[tool.ruff.lint.per-file-ignores]`)

### Type Checking
- This is a strictly typed codebase (`strict = true` in mypy config)
- A `py.typed` marker file indicates this package exports type information (PEP 561)
- All public APIs should have proper type annotations

### Code Style
- Follows NumPy docstring convention
- Uses isort for import ordering
- Uses pyupgrade for modern Python syntax
- Ruff handles both linting and formatting

## Trust These Instructions

**IMPORTANT**: Trust these instructions and only search for additional information if:
1. The instructions are incomplete for your specific task
2. You encounter an error that contradicts these instructions
3. You need to understand implementation details not covered here

For build, test, and lint operations, **always use the exact commands listed above**. They have been validated and are known to work correctly.

## Quick Reference

```bash
# Setup (run once)
pip install uv==0.9.9
uv sync --locked

# Development workflow (run after making changes)
uv run pytest           # Test
uv run mypy             # Type check
uvx ruff check          # Lint
uvx ruff format --check # Check formatting

# Build
uv build                # Creates dist/

# Coverage
uv run coverage run && uv run coverage report
```
