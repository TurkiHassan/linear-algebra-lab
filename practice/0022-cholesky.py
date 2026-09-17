"""0022 · LU & Cholesky decomposition — practice.

Run:  python3 practice/0022-cholesky.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def is_symmetric(A):
    """True when A equals its own transpose."""
    # TODO
    raise NotImplementedError


def det2(A):
    """Determinant of a 2x2 matrix."""
    # TODO
    raise NotImplementedError


def is_positive_definite2(A):
    """True when A is symmetric and both leading minors are positive."""
    # TODO: minor 1 is A[0][0]; minor 2 is det2(A).
    raise NotImplementedError


def lu2(A):
    """Return (L, U) with A = L U, ones on the diagonal of L.

    Return None when the pivot A[0][0] is zero (a row swap would be needed).
    """
    # TODO
    raise NotImplementedError


def cholesky2(A):
    """Return L with A = L L^T, or None when A is not positive definite."""
    # TODO: l11 = sqrt(a11); l21 = a21 / l11; l22 = sqrt(a22 - l21^2).
    raise NotImplementedError


def reconstruct(L, R):
    """Multiply two 2x2 matrices — used to check a factorisation."""
    # TODO
    raise NotImplementedError


def det_from_cholesky(L):
    """det(A) read off the diagonal of its Cholesky factor."""
    # TODO
    raise NotImplementedError


def _flat(x):
    if isinstance(x, list):
        out = []
        for v in x:
            out.extend(_flat(v))
        return out
    return [x]


def _check(name, got, want):
    if isinstance(want, list):
        g, w = (_flat(got) if got is not None else None), _flat(want)
        ok = g is not None and len(g) == len(w) and all(abs(a - b) < 1e-6 for a, b in zip(g, w))
    elif isinstance(want, (int, float)) and not isinstance(want, bool):
        ok = got is not None and abs(got - want) < 1e-6
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    A = [[2, 1], [6, 5]]
    S = [[4, 2], [2, 5]]
    BAD = [[1, 3], [3, 1]]
    ok = True
    ok &= _check("symmetric", is_symmetric(S), True)
    ok &= _check("not symmetric", is_symmetric(A), False)
    ok &= _check("det", det2(S), 16)
    ok &= _check("positive definite", is_positive_definite2(S), True)
    ok &= _check("positive diagonal is not enough", is_positive_definite2(BAD), False)
    L, U = lu2(A)
    ok &= _check("L of LU", L, [[1, 0], [3, 1]])
    ok &= _check("U of LU", U, [[2, 1], [0, 2]])
    ok &= _check("LU rebuilds A", reconstruct(L, U), A)
    C = cholesky2(S)
    ok &= _check("cholesky factor", C, [[2, 0], [1, 2]])
    ok &= _check("LL^T rebuilds S", reconstruct(C, [[C[0][0], C[1][0]], [C[0][1], C[1][1]]]), S)
    ok &= _check("no factor for BAD", cholesky2(BAD), None)
    ok &= _check("det from diagonal", det_from_cholesky(C), 16)
    print("ALL OK" if ok else "SOME FAILED")
