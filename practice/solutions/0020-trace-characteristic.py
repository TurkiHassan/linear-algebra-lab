"""0020 · trace & characteristic polynomial — full solution."""

TOL = 1e-9


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def matmul2(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def trace_cycle_holds(A, B):
    return abs(trace(matmul2(A, B)) - trace(matmul2(B, A))) < TOL


def char_poly2(A):
    return [1, -trace(A), det2(A)]


def eigenvalues2(A):
    t, d = trace(A), det2(A)
    disc = t * t - 4 * d
    if disc < 0:
        return None
    s = disc ** 0.5
    return sorted([(t - s) / 2, (t + s) / 2])


def invariants_match(A):
    r = eigenvalues2(A)
    if r is None:
        return None
    return abs(sum(r) - trace(A)) < TOL and abs(r[0] * r[1] - det2(A)) < TOL


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
    R = [[0, -1], [1, 0]]
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
