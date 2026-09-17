"""0021 · eigenvalues & eigenvectors — full solution."""

TOL = 1e-9


def eigenvalues2(A):
    t = A[0][0] + A[1][1]
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    disc = t * t - 4 * d
    if disc < 0:
        return None
    s = disc ** 0.5
    return sorted([(t - s) / 2, (t + s) / 2])


def apply2(A, v):
    return [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]


def is_eigenpair(A, lam, v):
    if abs(v[0]) < TOL and abs(v[1]) < TOL:
        return False
    w = apply2(A, v)
    return abs(w[0] - lam * v[0]) < 1e-9 and abs(w[1] - lam * v[1]) < 1e-9


def eigenvector_for(A, lam):
    a, b = A[0][0] - lam, A[0][1]
    c, d = A[1][0], A[1][1] - lam
    if abs(a) > TOL or abs(b) > TOL:
        v = [-b, a]
        if abs(v[0]) > TOL or abs(v[1]) > TOL:
            return v
    if abs(c) > TOL or abs(d) > TOL:
        return [-d, c]
    return [1, 0]           # A = lam*I: every direction is an eigenvector


def normalize(v):
    n = (v[0] ** 2 + v[1] ** 2) ** 0.5
    if n < TOL:
        return None
    return [v[0] / n, v[1] / n]


def eigen_basis2(A):
    r = eigenvalues2(A)
    if r is None:
        return None
    if abs(r[0] - r[1]) < TOL:
        return None                     # repeated root: usually only one direction
    v1, v2 = eigenvector_for(A, r[0]), eigenvector_for(A, r[1])
    if v1 is None or v2 is None:
        return None
    if abs(v1[0] * v2[1] - v1[1] * v2[0]) < TOL:
        return None
    return [v1, v2]


def classify_map(A):
    r = eigenvalues2(A)
    if r is None:
        return "rotation"
    if abs(r[0]) < TOL or abs(r[1]) < TOL:
        return "collapse"
    if abs(r[0] - r[1]) < TOL:
        return "shear"
    return "stretch"


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
