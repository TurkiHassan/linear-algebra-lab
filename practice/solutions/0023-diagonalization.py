"""0023 · diagonalization & the spectral theorem — full solution."""

TOL = 1e-9


def eigenvalues2(A):
    t = A[0][0] + A[1][1]
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    disc = t * t - 4 * d
    if disc < 0:
        return None
    s = disc ** 0.5
    return sorted([(t - s) / 2, (t + s) / 2])


def algebraic_multiplicity(A, lam):
    r = eigenvalues2(A)
    if r is None:
        return 0
    return sum(1 for v in r if abs(v - lam) < 1e-9)


def geometric_multiplicity2(A, lam):
    B = [[A[0][0] - lam, A[0][1]], [A[1][0], A[1][1] - lam]]
    if all(abs(v) < TOL for row in B for v in row):
        return 2
    if abs(B[0][0] * B[1][1] - B[0][1] * B[1][0]) < 1e-9:
        return 1
    return 0


def is_diagonalizable2(A):
    r = eigenvalues2(A)
    if r is None:
        return False
    seen, total = [], 0
    for lam in r:
        if any(abs(lam - s) < 1e-9 for s in seen):
            continue
        seen.append(lam)
        total += geometric_multiplicity2(A, lam)
    return total == 2


def _eigenvector(A, lam):
    a, b = A[0][0] - lam, A[0][1]
    c, d = A[1][0], A[1][1] - lam
    if abs(a) > TOL or abs(b) > TOL:
        v = [-b, a]
        if abs(v[0]) > TOL or abs(v[1]) > TOL:
            return v
    if abs(c) > TOL or abs(d) > TOL:
        return [-d, c]
    return None


def diagonalize2(A):
    if not is_diagonalizable2(A):
        return None
    r = eigenvalues2(A)
    if abs(r[0] - r[1]) < 1e-9:                 # A is lam * I
        return [[1, 0], [0, 1]], [[r[0], 0], [0, r[1]]]
    v1, v2 = _eigenvector(A, r[0]), _eigenvector(A, r[1])
    P = [[v1[0], v2[0]], [v1[1], v2[1]]]
    D = [[r[0], 0], [0, r[1]]]
    return P, D


def _mul(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def _inv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


def matrix_power2(A, k):
    pair = diagonalize2(A)
    if pair is None:
        out = [[1, 0], [0, 1]]
        for _ in range(k):
            out = _mul(out, A)
        return out
    P, D = pair
    Dk = [[D[0][0] ** k, 0], [0, D[1][1] ** k]]
    return _mul(_mul(P, Dk), _inv(P))


def is_orthogonally_diagonalizable(A):
    return all(abs(A[i][j] - A[j][i]) < TOL for i in range(len(A)) for j in range(len(A)))


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
    SYM = [[2, 1], [1, 2]]
    SHEAR = [[2, 1], [0, 2]]
    SCALED_I = [[3, 0], [0, 3]]
    ROT = [[0, -1], [1, 0]]
    ok = True
    ok &= _check("eigenvalues", eigenvalues2(SYM), [1, 3])
    ok &= _check("algebraic of shear", algebraic_multiplicity(SHEAR, 2), 2)
    ok &= _check("geometric of shear", geometric_multiplicity2(SHEAR, 2), 1)
    ok &= _check("geometric of 3I", geometric_multiplicity2(SCALED_I, 3), 2)
    ok &= _check("symmetric diagonalizes", is_diagonalizable2(SYM), True)
    ok &= _check("shear does not", is_diagonalizable2(SHEAR), False)
    ok &= _check("rotation does not", is_diagonalizable2(ROT), False)
    P, D = diagonalize2(SYM)
    ok &= _check("D is the spectrum", [D[0][0], D[1][1]], [1, 3])
    ok &= _check("A squared", matrix_power2(SYM, 2), [[5, 4], [4, 5]])
    ok &= _check("A to the 5", matrix_power2(SYM, 5), [[122, 121], [121, 122]])
    ok &= _check("orthogonally diagonalizable", is_orthogonally_diagonalizable(SYM), True)
    ok &= _check("not orthogonally", is_orthogonally_diagonalizable(SHEAR), False)
    print("ALL OK" if ok else "SOME FAILED")
