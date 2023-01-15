# Rounder

The "rounder" package extends the functionality provided by Python's
built-in [`round`](https://docs.python.org/3/library/functions.html#round)
function. It aims to provide a more complete and consistent collection of
decimal rounding functionality than is provided by the Python core and standard
library. Specifically, it provides:

* Drop-in replacements for `round` that use rounding modes other than
  round-ties-to-even (for example, the commonly needed round-ties-to-away).
* Functionality for rounding to a given number of significant figures,
  rather than to a set number of places after (or before) the decimal point.

## General-purpose rounding functions

There are four general-purpose rounding functions.

* The `round` function has the same signature as the built-in `round`, but also allows a
  rounding mode to be specified. Like `round`, it supports rounding to the nearest
  integer in the direction of the given rounding mode, and rounding to a given number of
  places while preserving the type of the input.

  ```python
  >>> from rounder import round, TIES_TO_AWAY, TO_MINUS
  >>> round(2.5)  # The default rounding mode is TIES_TO_EVEN
  2
  >>> round(2.5, mode=TIES_TO_AWAY)  # round halfway cases away from zero
  3
  >>> round(2.97, 1, mode=TO_MINUS)  # round towards negative infinity (like floor)
  2.9
  >>> round(Decimal(-1628), -2, mode=TO_MINUS)  # Decimal and Fraction types supported
  Decimal('-1.7E+3')
  ```

* The `round_to_figures` function rounds to a given number of significant figures,
  rather than to a given number of places before or after the decimal point.

  ```python
  >>> from rounder import round_to_figures, TO_AWAY
  >>> round_to_figures(1.234567, 3)
  1.23
  >>> round_to_figures(1234567., 3)
  1230000.0
  >>> round_to_figures(0.0001234567, 3)
  0.000123
  >>> round_to_figures(0.0001234567, 3, mode=TO_AWAY)  # round away from zero
  0.000123
  ```

* The `round_to_int` and `round_to_places` functions provide the two pieces of
  functionality that `round` combines: `round_to_int` rounds to a
  nearby integer using the given rounding mode, while `round_to_places` always
  expects an `ndigits` argument and rounds to the given number of places. The `round`
  function is currently a simple wrapper around `round_to_int` and `round_to_places`.

  ```python
  >>> from rounder import round_to_int, round_to_places, TO_PLUS
  >>> round_to_int(3.1415, mode=TO_PLUS)
  4
  >>> round_to_places(3.1415, 2, mode=TO_PLUS)
  3.15
  ```

There are currently thirteen different rounding modes provided, listed
[below](#rounding-modes).

## Functions providing alternative rounding modes

There are thirteen functions that act as drop-in replacements for `round`, but that
use a different rounding mode. For example, if you always want to round ties away
from zero instead of to the nearest even number, you can do this:

```python
>>> from rounder import round_ties_to_away as round
>>> round(4.5)
5
>>> round(1.25, 1)
1.3
```

Or if you want a version of `math.ceil` that accepts a number of places after the point,
you can do:

```python
>>> from rounder import round_to_plus as ceil
>>> ceil(1.78)
2
>>> ceil(1.782, 2)
1.79
>>> ceil(-1.782, 2)
-1.78
```

The complete list of functions is [below](#rounding-modes)

## Rounding modes

These are the currently supported rounding modes, along with their corresponding
mode-specific rounding functions.

### To-nearest rounding modes

There are six to-nearest rounding modes: these all round to the closest output value,
and differ only in their handling of ties. `TIES_TO_EVEN` is the default rounding mode
for the general-purpose rounding functions, and matches Python's default. `TIES_TO_AWAY`
is the rounding method often taught in schools. `TIES_TO_PLUS` matches JavaScript's
default.

| Rounding mode | Function              | Description                            |
|---------------|-----------------------|----------------------------------------|
| TIES_TO_EVEN  | `round_ties_to_even`  | Ties rounded to the nearest even value |
| TIES_TO_ODD   | `round_ties_to_odd`   | Ties rounded to the nearest odd value  |
| TIES_TO_AWAY  | `round_ties_to_away`  | Ties rounded away from zero            |
| TIES_TO_ZERO  | `round_ties_to_zero`  | Ties rounded towards zero              |
| TIES_TO_MINUS | `round_ties_to_minus` | Ties rounded towards negative infinity |
| TIES_TO_PLUS  | `round_ties_to_plus`  | Ties rounded towards positive infinity |

There are six matching directed rounding modes: for these, all values between any two
representable output values will be rounded in the same direction.

| Rounding mode | Function              | Description                               |
|---------------|-----------------------|-------------------------------------------|
| TO_EVEN       | `round_to_even`       | Round to the nearest even value           |
| TO_ODD        | `round_to_odd`        | Round to the nearest odd value            |
| TO_AWAY       | `round_to_away`       | Round away from zero                      |
| TO_ZERO       | `round_to_zero`       | Round towards zero ("trunc")              |
| TO_MINUS      | `round_to_minus`      | Round towards negative infinity ("floor") |
| TO_PLUS       | `round_to_plus`       | Round towards positive infinity ("ceil")  |

There's one miscellaneous rounding mode `TO_ZERO_05_AWAY`, with corresponding function
`round_to_zero_05_away`.

| Rounding mode   | Function                | Description       |
|-----------------|-------------------------|-------------------|
| TO_ZERO_05_AWAY | `round_to_zero_05_away` | See below         |

This rounding mode matches the `decimal` module's `ROUND_05UP` rounding mode. It
rounds towards zero, _except_ in the case where there's at least one nonzero digit being
rounded away, and rounding towards zero would produce a final significant digit of `0`
or `5` in the rounded result. In that case, it rounds away from zero instead.

```python
from rounder import round_to_zero_05_away
>>> round_to_zero_05_away(1.234, 1)
1.2
>>> round_to_zero_05_away(1.294, 1)
1.2
>>> round_to_zero_05_away(1.534, 1)  # round_to_zero would give 1.5, so round away
1.6
```

## Supported numeric types

Out of the box, `rounder` supports Python's built-in numeric types: `int`, `float`,
`decimal.Decimal` and `fractions.Fraction`. Under the hood, it uses
[`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch)
for all type-specific operations. This should allow easy extension to new numeric
types in the future.
