"""
Algorithms for determining efficiently whether a fraction terminates.

Given a fraction n / d (written in lowest terms, with d positive), we want to determine
whether n / d has a terminating decimal expansion, and if so, the length of that decimal
expansion. That amounts to determining whether d has any prime factors other than 2 and
5: if it does, then n / d does not terminate. If the only prime factors of d are 2 and
5, then the length of the decimal expansion is the larger of the exponents of 2 and 5 in
the prime factorization of d.

It's easy to find and remove powers of two using bit trickery, so what remains is
identifying powers of five. We want to:

- efficiently determine whether a given positive integer is an exact power of five, with
  minimal work in the case that it isn't, and
- if it is, compute the exponent.

For the remainder of this description, assume n is a positive integer. Since n must be
representable in Python, we can reasonably assume that n < 2**2**64; i.e., that the
bit length of n is at most 2**64.

## Bit-length methods

Suppose b is the bit length of n, so 2**(b - 1) <= n < 2**b. Let L and U be lower
and upper (respectively) bounds on log5(2). Then if n = 5**e for some nonnegative
integer e, we have:

    (b - 1)L <= e < bU

So

    ceil((b - 1)L) <= e < ceil(bU).

If the bounds L and U are sufficiently tight and b is not too large, these bounds
determine e uniquely. In particular, if bU - (b - 1)L <= 1, then ceil(bU) <=
ceil((b - 1)L) + 1, so there's at most one integer e satisfying the inequalities. Given
our assumption that b <= 2**64, it's enough that U - L < (1 - log5(2)) / 2**64, and
since log5(2) < 0.5, it's enough that U - L < 2**-65.

Suitable bounds are:

    L = 12055151410 / 27991194747 < log(2) / log(5) < 579001193 / 1344399137 = U

with a difference U - L = 1/37631338061465733339, which is just a touch smaller than
2**-65 = 1/36893488147419103232.

## Methods based on low order bits

If n = 5**e, then the last two bits of n are 01. Any pattern of low-order bits ending
in 01 can arise from a power of 5. Moreover, the last b + 2 bits of 5**e determine e
modulo 2**b (so for example, the last 10 bits determine e mod 256).

So we can use a lookup table of size 256 (say) to determine the value of the exponent
e modulo 256 from the last 10 bits of n. If n is small enough (less than 5**256), we can
just check directly that n matches the corresponding power of 5.

## Overall strategy

The log5exact function below combines the above methods:

- For d smaller than 5**256, use the ten least significant bits of d to determine the
  exponent e and matching power 5**e, and compare d with 5**e.
- For the general case, use the bit-length method to compute e, and check that:
  - e mod 256 matches the exponent determined by the least significant bits of n, then
  - 5**e matches d modulo 2**60 (a fast limited-precision check), then
  - 5**e = d.
"""

# Numerator and denominator of tight lower and upper bounds for log5(2).
_Ln, _Ld = 12055151410, 27991194747
_Un, _Ud = 579001193, 1344399137


def exponent_from_bit_length(b: int) -> int:
    """
    Given the bit length b of an integer n = 5**e, return e.

    Parameters
    ----------
    b
        The bit length of n. Assumed to satisfy 0 <= b <= 2**64. Results for b
        outside this range are not defined: the function may raise, or may return
        nonsense.

    Returns
    -------
    int
        An integer e such that n = 5**e has bit length b.

    Raises
    ------
    ValueError
        If there is no integer e such that n = 5**e has bit length b.
    """
    if (e := -((b - 1) * _Ln // -_Ld)) == -(b * _Un // -_Ud) - 1:
        return e
    raise ValueError(f"No power of 5 has bit length {b}")


# _5_POW_EXPONENT_FROM_LOW_BITS maps low-order bits of a power of 5 to the matching
# exponent.
_5_POW_EXPONENT_FROM_LOW_BITS = {pow(5, e, 1024): e for e in range(256)}

# Direct mapping from power of 5 to exponent for fast path variant.
_5_POW_LIMIT = 5**64
_5_POW_TO_EXPONENT = {5**e: e for e in range(64)}


def log5exact(n: int) -> int:
    """
    Find the exponent of an exact power of 5 (direct mapping variant).

    Returns e if n = 5**e for some nonnegative integer e. Raises ValueError otherwise.

    This variant uses a direct mapping {5**e: e} for the fast path, avoiding the
    two-step lookup through low bits.
    """
    if n < _5_POW_LIMIT:
        if (e := _5_POW_TO_EXPONENT.get(n)) is not None:
            return e
    else:
        e = exponent_from_bit_length(n.bit_length())
        if (
            e & 0xFF == _5_POW_EXPONENT_FROM_LOW_BITS.get(n & 0x3FF)
            and pow(5, e, 2**60) == n % 2**60
            and pow(5, e) == n
        ):
            return e

    raise ValueError(f"{n} is not a power of 5")


def reciprocal_as_decimal(d: int) -> tuple[int, int]:
    """
    Given a positive integer d, express 1 / d in the form m * 10**e.

    Parameters
    ----------
    d
        A positive integer.

    Returns
    -------
    tuple[int, int]
        A pair (m, e) such that 1 / d = m * 10**e.

    Raises
    ------
    ValueError
        If 1 / d cannot be expressed in the desired form. In other words, raises if d
        has any prime factors other than 2 and 5.
    """
    two_exp = (~(d | -d)).bit_length()
    if (five_exp := log5exact(d >> two_exp)) >= two_exp:
        return 1 << (five_exp - two_exp), -five_exp
    else:
        return 5 ** (two_exp - five_exp), -two_exp
