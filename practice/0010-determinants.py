"""0010 · determinants — practice (fill the gaps, then run the file).

Run:  python3 practice/0010-determinants.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def det2(a, b, c, d):
    """det [[a, b], [c, d]] = ad - bc."""
    # TODO
    raise NotImplementedError


def det_laplace(M):
    """Determinant of an n x n matrix (list of rows) by Laplace expansion along the first row."""
    # TODO: det = sum over j of (-1)**j * M[0][j] * det(minor with row 0 and column j removed)
    raise NotImplementedError


def is_invertible_2(a, b, c, d):
    """True iff det != 0."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    ok = abs(got - want) < TOL if isinstance(want, float) else got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("det [[2,-3],[1,2]]=7", det2(2, 1, -3, 2), 7)
    ok &= _check("det [[2,1],[4,2]]=0", det2(2, 4, 1, 2), 0)
    ok &= _check("det [[0,3/2],[2,4]]=-3", det2(0, 2, 1.5, 4), -3)
    ok &= _check("laplace lesson matrix", det_laplace([[2, 4, 6], [3, 8, 5], [-1, 1, 2]]), 44)
    ok &= _check("laplace 4x4", det_laplace([[1, 2, 0, 3], [0, 1, 4, 1], [2, 0, 1, 0], [1, 1, 1, 2]]), 10)
    ok &= _check("laplace triangular = diagonal product", det_laplace([[2, 5], [0, 3]]), 6)
    ok &= _check("invertible", is_invertible_2(2, 1, -3, 2), True)
    ok &= _check("singular", is_invertible_2(2, 4, 1, 2), False)
    print("ALL OK" if ok else "SOME FAILED")
