"""Find the exponent of an exact power of 5.

We want to:

- efficiently determine whether a given positive integer is an exact power of 5, with
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

The code below combines the above methods:

- For d smaller than 5**256, use the ten least significant bits of d to determine the
  exponent e and matching power 5**e, and compare d with 5**e.
- For the general case, use the bit-length method to compute e, and check that:
  - e mod 256 matches the exponent determined by the least significant bits of n, then
  - 5**e matches d modulo 2**60 (a fast limited-precision check), then
  - 5**e = d.
"""

# Numerator and denominator of tight lower and upper bounds for log2(5).
_Ln, _Ld = 12055151410, 27991194747
_Un, _Ud = 579001193, 1344399137


def exponent_from_bit_length(b: int) -> int | None:
    """
    Given the bit length b of an integer n = 5**e, return e.

    Assumes that the input b satisfies 0 <= b <= 2**64; results for b outside this range
    are not defined. Returns None if b is not the bit length of a power of 5.
    """
    if (e := -((b - 1) * _Ln // -_Ld)) == -(b * _Un // -_Ud) - 1:
        return e
    return None


# Bound below which we do a direct lookup based on low-order bits.
_5_POW_256 = 5**256

# _5_POW_EXPONENT_FROM_LOW_BITS maps the low order bits of a power of 5 to the matching
# exponent. _5_POW_FROM_LOW_BITS maps the same bits to the corresponding power.
_5_POW_EXPONENT_FROM_LOW_BITS = {pow(5, e, 1024): e for e in range(256)}
_5_POW_FROM_LOW_BITS = {bits: 5**e for bits, e in _5_POW_EXPONENT_FROM_LOW_BITS.items()}


def log5exact(d: int) -> int:
    """
    Find the exponent of an exact power of 5.

    Returns e if d = 5**e for some nonnegative integer e. Raises ValueError otherwise.
    """
    if d < _5_POW_256:
        if d == _5_POW_FROM_LOW_BITS.get(low_bits := d & 0x3FF):
            return _5_POW_EXPONENT_FROM_LOW_BITS[low_bits]
    else:
        e = exponent_from_bit_length(d.bit_length())
        if (
            e is not None
            and e & 0xFF == _5_POW_EXPONENT_FROM_LOW_BITS.get(d & 0x3FF)
            and pow(5, e, 2**60) == d & 2**60 - 1
            and pow(5, e) == d
        ):
            return e

    raise ValueError(f"{d} is not a power of 5")
