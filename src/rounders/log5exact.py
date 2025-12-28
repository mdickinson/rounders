"""Find the exponent of an exact power of 5.

We want to:

- efficiently determine whether a given integer is an exact power of 5 (with minimal
  work in the case that it isn't), and
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

The code below uses both of the above tricks:

- First check that n is positive and congruent to 1 modulo 4.
- Use the last 10 bits of n to determine e mod 256. If n < 5**256, then
  e < 256, so we can check directly that n matches 5**e (using a table of
  powers of 5, keyed on the last 8 bits of n >> 2).
- Use the bit-length method to compute e. Check that e mod 256 matches what we
  already know.
- Before checking that n = 5**e, do a fast limited precision check modulo 2**60.
"""

# Numerator and denominator of tight lower and upper bounds for log2(5).
_Ln, _Ld = 12055151410, 27991194747
_Un, _Ud = 579001193, 1344399137

# Bound below which we do a direct lookup based on low-order bits.
_5_POW_256 = 5**256

# _5_POW_EXPONENT_FROM_LOW_BITS maps bits 9 through 2 of a power of 5 to the matching
# exponent. _5_POW_FROM_LOW_BITS maps the same bits to the corresponding power.
_5_POW_EXPONENT_FROM_LOW_BITS = [
    e for _, e in sorted((pow(5, e, 1024) >> 2, e) for e in range(256))
]
_5_POW_FROM_LOW_BITS = [5**e for e in _5_POW_EXPONENT_FROM_LOW_BITS]


def exponent_from_bit_length(b: int) -> int:
    """
    Given the bit length b of an integer n = 5**e, return e.

    Raise ValueError if b cannot possibly be the bit length of a power of 5.
    """
    if (e := -((b - 1) * _Ln // -_Ld)) == -(b * _Un // -_Ud) - 1:
        return e
    raise ValueError(f"bit length {b} does not correspond to a power of 5")


def log5exact(d: int) -> int:
    """
    Find the exponent of an exact power of 5.

    Returns e if d = 5**e for some nonnegative integer e. Otherwise,
    raises ValueError.
    """
    # Any power of 5 must be positive and congruent to 1 modulo 4.
    if d <= 0 or d & 0x3 != 1:
        raise ValueError(f"{d} is not a power of 5")

    # Find the smallest power of 5 matching the last 10 bits of d.
    # For small d, it's enough to compare directly that power.
    low_bits = (d & 0x3FF) >> 2
    if d < _5_POW_256:
        if d == _5_POW_FROM_LOW_BITS[low_bits]:
            return _5_POW_EXPONENT_FROM_LOW_BITS[low_bits]
        else:
            raise ValueError(f"{d} is not a power of 5")

    # For larger d, compute the exponent based on the bit length, and check that
    # its last 8 bits match what we already know.
    e = exponent_from_bit_length(d.bit_length())
    if e & 0xFF != _5_POW_EXPONENT_FROM_LOW_BITS[low_bits]:
        raise ValueError(f"{d} is not a power of 5")

    # At this point we know that d has the same bit length as 5**e, and matches 5**e
    # modulo 2**10. Before checking the full value, do a fast check modulo 2**60.
    if pow(5, e, 2**60) == d & 2**60 - 1 and pow(5, e) == d:
        return e

    raise ValueError(f"{d} is not a power of 5")
