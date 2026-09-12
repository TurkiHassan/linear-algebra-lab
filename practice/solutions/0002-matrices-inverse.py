"""0002 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def mat_shape(M):
    return (len(M), len(M[0]))


def mat_add(A, B):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]


def mat_mul(A, B):
    if len(A[0]) != len(B):
        raise ValueError("inner dimensions must match")
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


def inv_2x2(a, b, c, d):
    det = a * d - b * c
    if det == 0:
        return None
    return [[d / det, -c / det], [-b / det, a / det]]


def _check(name, got, want):
    if isinstance(want, float):
        ok = abs(got - want) < TOL
    elif isinstance(want, list):
        ok = all(abs(x - y) < TOL for r1, r2 in zip(got, want) for x, y in zip(r1, r2))
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("shape", mat_shape([[1, 2, 3], [4, 5, 6]]), (2, 3))
    ok &= _check("add", mat_add([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[6, 8], [10, 12]])
    ok &= _check("mul", mat_mul([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]]), [[58, 64], [139, 154]])
    ok &= _check("inv", inv_2x2(2, 1, -3, 2), [[2 / 7, 3 / 7], [-1 / 7, 2 / 7]])
    ok &= _check("singular", inv_2x2(2, 4, 1, 2), None)
    print("ALL OK" if ok else "SOME FAILED")
