<!--
A new scriv changelog fragment.

Uncomment the section that is right (remove the HTML comment wrapper).
For top level release notes, leave all the headers commented out.
-->

<!--
### Removed

- A bullet item for the Removed category.

-->
<!--
### Added

- A bullet item for the Added category.

-->

### Changed

- **Breaking change**: The first parameter of all rounding functions has been
  renamed to `number` for consistency with Python's built-in `round()` function.
  Previously, different functions used `x` or `value`. This affects users who pass
  the first argument by keyword name. Code using positional arguments is unaffected.


<!--
### Deprecated

- A bullet item for the Deprecated category.

-->
<!--
### Fixed

- A bullet item for the Fixed category.

-->
<!--
### Security

- A bullet item for the Security category.

-->
