
<a id='changelog-0.2.0'></a>
# 0.2.0 — 2024-06-08

This minor release focuses on clean-up of the original code, and mostly consists
of changes to the internal logic to better support the planned formatting
functionality.

## Added

- Added the `RoundingMode` type to the top-level exports, since it's potentially
  useful for type hints in client code.

- Added a `py.typed` marker.

## Changed

- Rounding modes now have a more user-friendly representation.

- The library internals have been significantly reworked, to help support the
  coming formatting functionality.

- The minimum Python version is now Python 3.8.

- We now use `setuptools_scm` for versioning.

- The source now uses `ruff` for formatting and linting.

- A dependabot config has been added, to help keep GitHub Actions workflows up to date.

- The README documentation has been expanded and updated.

## Fixed

- Missing docstrings have been added.

<a id='changelog-0.2.0'></a>
# 0.1.0 — 2023-01-31

This is the initial release of the rounders package.

The rounders package extends the functionality provided by Python's
built-in `round` function. It aims to provide a more complete and
consistent collection of decimal rounding functionality than is
provided by the Python core and standard library.
