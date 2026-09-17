"""0020 · trace & characteristic polynomial — practice.

Run:  python3 practice/0020-trace-characteristic.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def trace(A):
    """Sum of the diagonal entries of a square matrix."""
    # TODO: add A[i][i] for every i.
    raise NotImplementedError


def det2(A):
    """Determinant of a 2x2 matrix."""
    # TODO
    raise NotImplementedError


def matmul2(A, B):
    """Multiply two 2x2 matrices."""
    # TODO
    raise NotImplementedError


def trace_cycle_holds(A, B):
    """True when tr(AB) == tr(BA) — it always is, but prove it numerically."""
    # TODO
    raise NotImplementedError


def char_poly2(A):
    """Coefficients of p(L) = L^2 - tr(A)*L + det(A), as [1, -tr, det]."""
    # TODO
    raise NotImplementedError


def eigenvalues2(A):
    """Real roots of the characteristic polynomial, ascending; None when complex."""
    # TODO: discriminant = tr^2 - 4*det. Negative -> no real root.
    raise NotImplementedError


def invariants_match(A):
    """True when sum(roots) == tr(A) and prod(roots) == det(A). None when complex."""
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
        g, w = _flat(got) if got is not None else None, _flat(want)
        ok = g is not None and len(g) == len(w) and all(abs(a - b) < TOL for a, b in zip(g, w))
    elif isinstance(want, (int, float)) and not isinstance(want, bool):
        ok = got is not None and abs(got - want) < TOL
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    A = [[4, 2], [1, 3]]
    B = [[0, -1], [2, 5]]
    R = [[0, -1], [1, 0]]          # rotation by 90 degrees: no real eigenvalue
    ok = True
    ok &= _check("trace 2x2", trace(A), 7)
    ok &= _check("trace 3x3", trace([[1, 2, 3], [0, -1, 4], [5, 0, 2]]), 2)
    ok &= _check("det", det2(A), 10)
    ok &= _check("matmul", matmul2(A, B), [[4, 6], [6, 14]])
    ok &= _check("tr(AB) = tr(BA)", trace_cycle_holds(A, B), True)
    ok &= _check("char poly", char_poly2(A), [1, -7, 10])
    ok &= _check("eigenvalues", eigenvalues2(A), [2, 5])
    ok &= _check("rotation has none", eigenvalues2(R), None)
    ok &= _check("invariants", invariants_match(A), True)
    print("ALL OK" if ok else "SOME FAILED")
