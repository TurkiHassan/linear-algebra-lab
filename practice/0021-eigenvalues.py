"""0021 · eigenvalues & eigenvectors — practice.

Run:  python3 practice/0021-eigenvalues.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def eigenvalues2(A):
    """Real roots of L^2 - tr(A)*L + det(A), ascending; None when complex."""
    # TODO
    raise NotImplementedError


def apply2(A, v):
    """A @ v for a 2x2 matrix and a 2-vector."""
    # TODO
    raise NotImplementedError


def is_eigenpair(A, lam, v):
    """True when A v == lam * v and v is not the zero vector."""
    # TODO
    raise NotImplementedError


def eigenvector_for(A, lam):
    """A nonzero vector in ker(A - lam*I); None if the kernel is trivial.

    For [[a-lam, b], [c, d-lam]] the row (a-lam, b) gives (-b, a-lam);
    fall back to the second row when the first is all zeros.
    """
    # TODO
    raise NotImplementedError


def normalize(v):
    """Same direction, length 1; None for the zero vector."""
    # TODO
    raise NotImplementedError


def eigen_basis2(A):
    """Two independent eigenvectors when they exist, else None."""
    # TODO
    raise NotImplementedError


def classify_map(A):
    """One of "rotation", "collapse", "stretch", "shear"."""
    # TODO: complex roots -> rotation. A zero root -> collapse.
    #       Two distinct real roots -> stretch. A repeated root -> shear.
    raise NotImplementedError


def _collinear(u, w):
    """Eigenvectors are unique only up to scale, so compare directions, not entries."""
    if u is None or w is None:
        return False
    return abs(u[0] * w[1] - u[1] * w[0]) < 1e-6 and (abs(u[0]) > 1e-9 or abs(u[1]) > 1e-9)


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
    A = [[4, 2], [1, 3]]
    ROT = [[0, -1], [1, 0]]
    COL = [[1, -1], [-1, 1]]
    SHEAR = [[1, 0.5], [0, 1]]
    ok = True
    ok &= _check("eigenvalues", eigenvalues2(A), [2, 5])
    ok &= _check("apply", apply2(A, [2, 1]), [10, 5])
    ok &= _check("eigenpair 5", is_eigenpair(A, 5, [2, 1]), True)
    ok &= _check("eigenpair 2", is_eigenpair(A, 2, [1, -1]), True)
    ok &= _check("not a pair", is_eigenpair(A, 5, [1, 0]), False)
    ok &= _check("zero is never one", is_eigenpair(A, 5, [0, 0]), False)
    ok &= _check("normalize", normalize([3, 4]), [0.6, 0.8])
    v5 = eigenvector_for(A, 5)
    ok &= _check("eigenvector works", is_eigenpair(A, 5, v5), True)
    ok &= _check("eigenvector direction", _collinear(v5, [2, 1]), True)
    ok &= _check("basis exists", len(eigen_basis2(A)), 2)
    ok &= _check("rotation", classify_map(ROT), "rotation")
    ok &= _check("collapse", classify_map(COL), "collapse")
    ok &= _check("stretch", classify_map(A), "stretch")
    ok &= _check("shear", classify_map(SHEAR), "shear")
    print("ALL OK" if ok else "SOME FAILED")
