"""Find the exponent of an exact power of 5."""

# _5_POW_FROM_LOW_BITS maps bits 9 through 2 of a power of 5 to the matching power.
# _5_POW_EXPONENT_FROM_LOW_BITS maps bits 9 through 2 of a power of 5 to the matching
# exponent.
_5_POW_FROM_LOW_BITS = [0] * 256
_5_POW_EXPONENT_FROM_LOW_BITS = [0] * 256
for _e in range(256):
    key = ((_five_e := 5**_e) >> 2) & 0xFF
    _5_POW_FROM_LOW_BITS[key] = _five_e
    _5_POW_EXPONENT_FROM_LOW_BITS[key] = _e
_5_POW_256 = 5**256


def log5exact(d: int) -> int:
    """
    Find the exponent of an exact power of 5.

    Returns e if d = 5**e for some nonnegative integer e. Otherwise,
    raises ValueError.
    """
    # d must be positive, and its last two bits must be 01.
    if d <= 0 or d & 3 != 1:
        raise ValueError(f"{d} is not a power of 5")

    # If d is a power of 5, it's divisible by 5**e where e is determined
    # by the eight least significant bits of d >> 2.
    low_bits = d >> 2 & 0xFF
    q = d
    q, rem = divmod(q, _5_POW_FROM_LOW_BITS[low_bits])
    if rem:
        raise ValueError(f"{d} is not a power of 5")
    exponent = _5_POW_EXPONENT_FROM_LOW_BITS[low_bits]

    while True:
        q, r = divmod(q, _5_POW_256)
        if r:
            break
        exponent += 256

    if r != 1:
        raise ValueError(f"{d} is not a power of 5")

    return exponent
