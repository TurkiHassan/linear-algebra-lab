"""0025 · low-rank approximation — full solution."""

TOL = 1e-9


def outer(u, v):
    return [[u[i] * v[j] for j in range(len(v))] for i in range(len(u))]


def rank_of(A):
    if all(abs(v) < TOL for row in A for v in row):
        return 0
    if abs(A[0][0] * A[1][1] - A[0][1] * A[1][0]) > 1e-9:
        return 2
    return 1


def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _singular_values(A):
    """Both singular values of a 2x2, descending."""
    a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
    g = [[a * a + c * c, a * b + c * d], [a * b + c * d, b * b + d * d]]     # A^T A
    t = g[0][0] + g[1][1]
    det = g[0][0] * g[1][1] - g[0][1] * g[1][0]
    disc = max(0.0, t * t - 4 * det)
    s = disc ** 0.5
    return [max(0.0, (t + s) / 2) ** 0.5, max(0.0, (t - s) / 2) ** 0.5]


def _svd_parts(A):
    """(sigma_i, u_i, v_i) for i = 1, 2."""
    a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
    g = [[a * a + c * c, a * b + c * d], [a * b + c * d, b * b + d * d]]
    sig = _singular_values(A)
    lams = [sig[0] ** 2, sig[1] ** 2]
    out = []
    prev = None
    for lam, s in zip(lams, sig):
        p, q = g[0][0] - lam, g[0][1]
        if abs(p) > TOL or abs(q) > TOL:
            v = [-q, p]
        else:
            r, w = g[1][0], g[1][1] - lam
            v = [-w, r] if (abs(r) > TOL or abs(w) > TOL) else ([1, 0] if prev is None else [-prev[1], prev[0]])
        n = (v[0] ** 2 + v[1] ** 2) ** 0.5
        v = [v[0] / n, v[1] / n] if n > TOL else [1, 0]
        prev = v
        if s > TOL:
            w = [a * v[0] + b * v[1], c * v[0] + d * v[1]]
            u = [w[0] / s, w[1] / s]
        else:
            u = [0, 0]
        out.append((s, u, v))
    return out


def spectral_norm2(A):
    return _singular_values(A)[0]


def truncate2(A, k):
    out = [[0.0, 0.0], [0.0, 0.0]]
    for s, u, v in _svd_parts(A)[:k]:
        for i in range(2):
            for j in range(2):
                out[i][j] += s * u[i] * v[j]
    return out


def approx_error(A, k):
    return spectral_norm2(mat_sub(A, truncate2(A, k)))


def eckart_young_holds(A, k):
    sig = _singular_values(A)
    expected = sig[k] if k < len(sig) else 0.0
    return abs(approx_error(A, k) - expected) < 1e-6


def _flat(x):
    if isinstance(x, list):
        out = []
        for v in x:
            out.extend(_flat(v))
        return out
    return [x]


def _check(name, got, want, tol=1e-6):
    if isinstance(want, list):
        g, w = (_flat(got) if got is not None else None), _flat(want)
        ok = g is not None and len(g) == len(w) and all(abs(a - b) < tol for a, b in zip(g, w))
    elif isinstance(want, (int, float)) and not isinstance(want, bool):
        ok = got is not None and abs(got - want) < tol
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    A = [[3, 0], [4, 5]]
    ok = True
    ok &= _check("outer", outer([1, 3], [1, 1]), [[1, 1], [3, 3]])
    ok &= _check("outer has rank 1", rank_of(outer([1, 3], [1, 1])), 1)
    ok &= _check("A has rank 2", rank_of(A), 2)
    ok &= _check("zero has rank 0", rank_of([[0, 0], [0, 0]]), 0)
    ok &= _check("subtract", mat_sub(A, [[1, 1], [1, 1]]), [[2, -1], [3, 4]])
    ok &= _check("spectral norm", spectral_norm2(A), 45 ** 0.5)
    ok &= _check("rank-1 approximation", truncate2(A, 1), [[1.5, 1.5], [4.5, 4.5]])
    ok &= _check("its rank really is 1", rank_of(truncate2(A, 1)), 1)
    ok &= _check("full rank gives A back", truncate2(A, 2), A)
    ok &= _check("error equals sigma2", approx_error(A, 1), 5 ** 0.5)
    ok &= _check("eckart-young at k=1", eckart_young_holds(A, 1), True)
    ok &= _check("eckart-young at k=0", eckart_young_holds(A, 0), True)
    print("ALL OK" if ok else "SOME FAILED")
