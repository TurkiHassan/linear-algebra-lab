"""0010 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def det2(a, b, c, d):
    return a * d - b * c


def det_laplace(M):
    """Determinant of an n x n matrix (list of rows) by Laplace expansion along the first row."""
    n = len(M)
    if n == 0 or any(len(row) != n for row in M):
        raise ValueError("square matrix required")
    if n == 1:
        return M[0][0]
    return sum((-1) ** j * M[0][j] * det_laplace([row[:j] + row[j + 1:] for row in M[1:]]) for j in range(n))


def is_invertible_2(a, b, c, d):
    return det2(a, b, c, d) != 0


def _check(name, got, want):
    ok = abs(got - want) < TOL if isinstance(want, float) else got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("det7", det2(2, 1, -3, 2), 7)
    ok &= _check("det0", det2(2, 4, 1, 2), 0)
    ok &= _check("det-3", det2(0, 2, 1.5, 4), -3)
    ok &= _check("laplace lesson matrix", det_laplace([[2, 4, 6], [3, 8, 5], [-1, 1, 2]]), 44)
    ok &= _check("laplace 4x4", det_laplace([[1, 2, 0, 3], [0, 1, 4, 1], [2, 0, 1, 0], [1, 1, 1, 2]]), 10)
    ok &= _check("laplace triangular = diagonal product", det_laplace([[2, 5], [0, 3]]), 6)
    ok &= _check("inv", is_invertible_2(2, 1, -3, 2), True)
    ok &= _check("sing", is_invertible_2(2, 4, 1, 2), False)
    print("ALL OK" if ok else "SOME FAILED")
