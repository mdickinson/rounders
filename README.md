The goal of the "rounder" package is to provide a more unified, consistent
and complete approach to decimal rounding in Python.

Particular goals include:

* Allow a rounding mode to be used when rounding; in particular, allow "round"
  to do standard "high school" rounding (using the round-ties-to-away mode)
  rather than the default "Banker's rounding" (round-ties-to-even).
* Provide a comprehensive selection of rounding modes (currently 13 different
  rounding modes are provided).
* Provide variants of `math.floor` and `math.ceil` that support operating to a given
  number of places.
* Make it easy to round to a given number of significant figures as well as to
  a given number of decimal places.
* Support all built-in numeric types, and provide an extension mechanism to allow
  third-party types to be easily supported.
* Provide a basis for more flexible string formatting for numeric types, including
  the `fractions.Fraction` type (which doesn't currently support float formatting).
