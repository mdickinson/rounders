#: Signatures for to-nearest rounding modes
TIES_TO_ZERO = [[1, 1], [1, 1]]
TIES_TO_AWAY = [[2, 2], [2, 2]]
TIES_TO_PLUS = [[2, 2], [1, 1]]
TIES_TO_MINUS = [[1, 1], [2, 2]]
TIES_TO_EVEN = [[1, 2], [1, 2]]
TIES_TO_ODD = [[2, 1], [2, 1]]

#: Signatures for directed rounding modes
TO_ZERO = [[0, 0], [0, 0]]
TO_AWAY = [[3, 3], [3, 3]]
TO_MINUS = [[0, 0], [3, 3]]
TO_PLUS = [[3, 3], [0, 0]]
TO_EVEN = [[0, 3], [0, 3]]
TO_ODD = [[3, 0], [3, 0]]
