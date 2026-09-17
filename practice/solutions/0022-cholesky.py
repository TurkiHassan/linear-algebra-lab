"""0022 · LU & Cholesky decomposition — full solution."""

TOL = 1e-9


def is_symmetric(A):
    return all(abs(A[i][j] - A[j][i]) < TOL for i in range(len(A)) for j in range(len(A)))


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def is_positive_definite2(A):
    return is_symmetric(A) and A[0][0] > TOL and det2(A) > TOL


def lu2(A):
    if abs(A[0][0]) < TOL:
        return None
    m = A[1][0] / A[0][0]
    L = [[1, 0], [m, 1]]
    U = [[A[0][0], A[0][1]], [0, A[1][1] - m * A[0][1]]]
    return L, U


def cholesky2(A):
    if not is_positive_definite2(A):
        return None
    l11 = A[0][0] ** 0.5
    l21 = A[1][0] / l11
    rest = A[1][1] - l21 * l21
    if rest <= TOL:
        return None
    return [[l11, 0], [l21, rest ** 0.5]]


def reconstruct(L, R):
    return [[L[0][0] * R[0][0] + L[0][1] * R[1][0], L[0][0] * R[0][1] + L[0][1] * R[1][1]],
            [L[1][0] * R[0][0] + L[1][1] * R[1][0], L[1][0] * R[0][1] + L[1][1] * R[1][1]]]


def det_from_cholesky(L):
    return (L[0][0] * L[1][1]) ** 2


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
