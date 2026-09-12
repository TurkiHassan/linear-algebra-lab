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


def det3_sarrus(M):
    """3x3 determinant via Sarrus (M = 3 rows of 3)."""
    # TODO: down-diagonals minus up-diagonals
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
    ok &= _check("sarrus lesson matrix", det3_sarrus([[2, 4, 6], [3, 8, 5], [-1, 1, 2]]), 44)
    ok &= _check("invertible", is_invertible_2(2, 1, -3, 2), True)
    ok &= _check("singular", is_invertible_2(2, 4, 1, 2), False)
    print("ALL OK" if ok else "SOME FAILED")
