# Rounders

The `rounders` package extends the functionality provided by Python's
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
  >>> from rounders import round, TIES_TO_AWAY, TO_MINUS
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
  >>> from rounders import round_to_figures, TO_AWAY
  >>> round_to_figures(1.234567, 3)
  1.23
  >>> round_to_figures(1234567., 3)
  1230000.0
  >>> round_to_figures(0.0001234567, 3)
  0.000123
  >>> round_to_figures(0.0001234567, 3, mode=TO_AWAY)  # round away from zero
  0.000124
  ```

* The `round_to_int` and `round_to_places` functions provide the two pieces of
  functionality that `round` combines: `round_to_int` rounds to a
  nearby integer using the given rounding mode, while `round_to_places` always
  expects an `ndigits` argument and rounds to the given number of places. The `round`
  function is currently a simple wrapper around `round_to_int` and `round_to_places`.

  ```python
  >>> from rounders import round_to_int, round_to_places, TO_PLUS
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
>>> from rounders import round_ties_to_away as round
>>> round(4.5)
5
>>> round(1.25, 1)
1.3
```

Or if you want a version of `math.ceil` that accepts a number of places after the point,
you can do:

```python
>>> from rounders import ceil
>>> ceil(1.78)
2
>>> ceil(1.782, 2)
1.79
>>> ceil(-1.782, 2)
-1.78
```

The complete list of functions is [below](#rounding-modes)

## Rounding modes and mode-specific rounding functions

These are the currently supported rounding modes, along with their corresponding
mode-specific rounding functions. The functions `trunc`, `floor` and `ceil` are
aliases for `round_to_zero`, `round_to_minus` and `round_to_plus`, respectively.

### To-nearest rounding modes

There are six to-nearest rounding modes: these all round to the closest target value
(e.g., to the closest integer in the case of `round_to_int`), and differ only in their
handling of ties.

| Rounding mode   | Function              | Description                            |
|-----------------|-----------------------|----------------------------------------|
| `TIES_TO_EVEN`  | `round_ties_to_even`  | Ties rounded to the nearest even value |
| `TIES_TO_ODD`   | `round_ties_to_odd`   | Ties rounded to the nearest odd value  |
| `TIES_TO_AWAY`  | `round_ties_to_away`  | Ties rounded away from zero            |
| `TIES_TO_ZERO`  | `round_ties_to_zero`  | Ties rounded towards zero              |
| `TIES_TO_MINUS` | `round_ties_to_minus` | Ties rounded towards negative infinity |
| `TIES_TO_PLUS`  | `round_ties_to_plus`  | Ties rounded towards positive infinity |

### Directed rounding modes

There are six matching directed rounding modes: for these, all values between any two
representable output values will be rounded in the same direction.

| Rounding mode | Function              | Description                     |
|---------------|-----------------------|---------------------------------|
| `TO_EVEN`     | `round_to_even`       | Round to the nearest even value |
| `TO_ODD`      | `round_to_odd`        | Round to the nearest odd value  |
| `TO_AWAY`     | `round_to_away`       | Round away from zero            |
| `TO_ZERO`     | `round_to_zero`       | Round towards zero              |
| `TO_MINUS`    | `round_to_minus`      | Round towards negative infinity |
| `TO_PLUS`     | `round_to_plus`       | Round towards positive infinity |

### Miscellaneous rounding modes

There's one miscellaneous rounding mode `TO_ZERO_05_AWAY`, with corresponding function
`round_to_zero_05_away`.

| Rounding mode     | Function                | Description       |
|-------------------|-------------------------|-------------------|
| `TO_ZERO_05_AWAY` | `round_to_zero_05_away` | See below         |

This rounding mode matches the behaviour of `TO_ZERO`, _except_ in the case where
rounding towards zero would produce a final significant digit of `0` or `5`. In that
case, it matches the behaviour of `TO_AWAY` instead. Note that in the case where the
value is already rounded to the required number of digits, neither `TO_ZERO` nor
`TO_AWAY` would change its value, and similarly `TO_ZERO_05_AWAY` does not change
the value in this case.

```python
>>> from rounders import round_to_zero_05_away
>>> round_to_zero_05_away(1.234, 1)  # behaves like `TO_ZERO`
1.2
>>> round_to_zero_05_away(-1.294, 1)  # also behaves like `TO_ZERO`
-1.2
>>> round_to_zero_05_away(1.534, 1)  # `TO_ZERO` would give 1.5, so round away
1.6
>>> round_to_zero_05_away(-2.088, 1)  # `TO_ZERO` would give -2.0, so round away
-2.1
>>> round_to_zero_05_away(3.5, 1)  # `TO_ZERO` wouldn't change the value; leave as-is
3.5
```

## Notes on rounding modes

Some notes on particular rounding modes:

* `TIES_TO_EVEN` goes by a [variety of
  names](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even), including
  "Banker's rounding", "statisticians' rounding", and "Dutch rounding". It matches
  Python's default rounding mode and the IEEE 754 default rounding mode,
  `roundTiesToEven`. Many other languages also use this rounding mode by default.
* `TIES_TO_AWAY` appears to be the rounding mode most commonly taught in schools, and
  the mode that users often mistakenly expect `round` to use. Python 2's `round`
  function used this rounding mode.
* `TIES_TO_PLUS` matches the rounding mode used by JavaScript's `Math.round`, and also
  appears to be commonly taught. (See [ECMA-262, 13th
  edn.](https://262.ecma-international.org/13.0/), §21.3.2.28.)
* `TIES_TO_ZERO` is used in IEEE 754's "Augmented arithmetic operations".
* `TO_ZERO` matches the behaviour of `math.trunc`
* `TO_PLUS` matches the behaviour of `math.ceil`
* `TO_MINUS` matches the behaviour of `math.floor`
* `TO_ODD` is interesting as a form of "round for reround", providing a way to avoid the
  phenomenon of [double
  rounding](https://en.wikipedia.org/wiki/Rounding#Double_rounding). Suppose we're
  given a real number `x` and a number of places `p`. Let `y` be the result of rounding
  `x` to `p + 2` places using the `TO_ODD` rounding mode. Then `y` can act as a proxy
  for `x` when rounding to `p` places, in the sense that `y` and `x` will round the
  same way under any of the rounding modes defined in this module. (The binary analog
  of `TO_ODD` is a little more useful here - it works in the same way, but requires
  only two extra bits for the intermediate value instead of two extra digits.)
* `TO_ZERO_05_AWAY` also provides a form of "round for reround", but is more efficient
  in that it only requires one extra decimal digit instead of two. Given a value `x`
  and a number of places `p`, if `y = round(x, p + 1, mode=TO_ZERO_05_AWAY)`, then
  `round(x, p, mode=mode) == round(y, p, mode=mode)` for any of the thirteen rounding
  modes defined in this package.

  ```python
  >>> from rounders import *
  >>> import random
  >>> x = random.uniform(-1.0, 1.0)
  >>> y = round(x, 5, mode=TO_ZERO_05_AWAY)
  >>> round(x, 4, mode=TO_ZERO) == round(y, 4, mode=TO_ZERO)
  True
  >>> round(x, 4, mode=TIES_TO_ODD) == round(y, 4, mode=TIES_TO_ODD)
  True
  >>> round(x, 4, mode=TO_ZERO_05_AWAY) == round(y, 4, mode=TO_ZERO_05_AWAY)
  True
  ```
On relationships between the rounding modes in this package and rounding modes
elsewhere:

* IEEE 754 defines five "rounding-direction" attributes: `roundTiesToEven`,
  `roundTiesToAway`, `roundTowardPositive`, `roundTowardNegative` and `roundTowardZero`.
  These match `TIES_TO_EVEN`, `TIES_TO_AWAY`, `TO_PLUS`, `TO_MINUS` and `TO_ZERO`,
  respectively. The "Augmented arithmetic operations" section of IEEE 754-2019 also
  defines an attribute `roundTiesToZero`, corresponding to `TIES_TO_ZERO` in this
  module.

  | IEEE 754 rounding direction | `rounders` rounding mode |
  |-----------------------------|--------------------------|
  | `roundTiesToEven`           | `TIES_TO_EVEN`           |
  | `roundTiesToAway`           | `TIES_TO_AWAY`           |
  | `roundTiesToZero`           | `TIES_TO_ZERO`           |
  | `roundTowardPositive`       | `TO_PLUS`                |
  | `roundTowardNegative`       | `TO_MINUS`               |
  | `roundTowardZero`           | `TO_ZERO`                |

* As of Python 3.11, Python's
  [`decimal`](https://docs.python.org/3/library/decimal.html) module defines eight
  rounding options, corresponding to the rounding modes in this module as follows:

  | `decimal` rounding option | `rounders` rounding mode |
  |---------------------------|--------------------------|
  | `ROUND_CEILING`           | `TO_PLUS`                |
  | `ROUND_DOWN`              | `TO_ZERO`                |
  | `ROUND_FLOOR`             | `TO_MINUS`               |
  | `ROUND_HALF_DOWN`         | `TIES_TO_ZERO`           |
  | `ROUND_HALF_EVEN`         | `TIES_TO_EVEN`           |
  | `ROUND_HALF_UP`           | `TIES_TO_AWAY`           |
  | `ROUND_UP`                | `TO_AWAY`                |
  | `ROUND_05UP`              | `TO_ZERO_05_AWAY`        |


## Supported numeric types

Out of the box, `rounders` supports Python's built-in numeric types: `int`, `float`,
`decimal.Decimal` and `fractions.Fraction`. Under the hood, it uses
[`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch)
for all type-specific operations. This should allow easy extension to new numeric
types in the future. The extension mechanism has not yet stabilised.


## Future directions

Major goals for future releases:

- Add formatting support, including the ability to specify rounding direction in a
  format specification.
- Finalise and document mechanisms for adding support for custom types.
- Improve performance of `round`, especially for the `float` type, with the aid of
  a C extension if necessary.
- Better document the pitfalls of `round` applied to binary floats (especially for
  directed rounding modes, where `round` is not idempotent).
