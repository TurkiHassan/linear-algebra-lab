"""0024 · singular value decomposition — full solution."""

TOL = 1e-9


def transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


def gram(A):
    return matmul(transpose(A), A)


def _sym_eigen2(G):
    """Eigenvalues of a symmetric 2x2, descending, with unit eigenvectors."""
    t = G[0][0] + G[1][1]
    d = G[0][0] * G[1][1] - G[0][1] * G[1][0]
    disc = max(0.0, t * t - 4 * d)          # symmetric: never negative, clamp float noise
    s = disc ** 0.5
    lams = [(t + s) / 2, (t - s) / 2]
    vecs = []
    for lam in lams:
        a, b = G[0][0] - lam, G[0][1]
        c, e = G[1][0], G[1][1] - lam
        if abs(a) > TOL or abs(b) > TOL:
            v = [-b, a]
        elif abs(c) > TOL or abs(e) > TOL:
            v = [-e, c]
        else:
            v = [1, 0] if not vecs else [-vecs[0][1], vecs[0][0]]
        n = (v[0] ** 2 + v[1] ** 2) ** 0.5
        vecs.append([v[0] / n, v[1] / n] if n > TOL else [1, 0])
    return lams, vecs


def singular_values2(A):
    lams, _ = _sym_eigen2(gram(A))
    return [max(0.0, l) ** 0.5 for l in lams]


def right_vectors2(A):
    _, vecs = _sym_eigen2(gram(A))
    return vecs


def left_vector(A, v, sigma):
    if sigma < TOL:
        return None
    w = [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]
    return [w[0] / sigma, w[1] / sigma]


def svd2(A):
    s = singular_values2(A)
    V = right_vectors2(A)
    u1 = left_vector(A, V[0], s[0])
    u2 = left_vector(A, V[1], s[1])
    if u1 is None:
        u1 = [1, 0]
    if u2 is None:
        u2 = [-u1[1], u1[0]]            # complete the basis when sigma2 is zero
    U = [[u1[0], u2[0]], [u1[1], u2[1]]]
    S = [[s[0], 0], [0, s[1]]]
    Vt = [[V[0][0], V[0][1]], [V[1][0], V[1][1]]]
    return U, S, Vt


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
    ok &= _check("transpose", transpose(A), [[3, 4], [0, 5]])
    ok &= _check("matmul", matmul([[1, 2], [3, 4]], [[2, 0], [1, 3]]), [[4, 6], [10, 12]])
    ok &= _check("gram", gram(A), [[25, 20], [20, 25]])
    s = singular_values2(A)
    ok &= _check("singular values", s, [45 ** 0.5, 5 ** 0.5])
    ok &= _check("product is |det|", s[0] * s[1], 15)
    V = right_vectors2(A)
    ok &= _check("right vectors are unit", [V[0][0] ** 2 + V[0][1] ** 2, V[1][0] ** 2 + V[1][1] ** 2], [1, 1])
    ok &= _check("right vectors orthogonal", V[0][0] * V[1][0] + V[0][1] * V[1][1], 0)
    u1 = left_vector(A, V[0], s[0])
    ok &= _check("left vector is unit", u1[0] ** 2 + u1[1] ** 2, 1)
    U, S, Vt = svd2(A)
    ok &= _check("sigma on the diagonal", [S[0][0], S[1][1]], s)
    ok &= _check("U S Vt rebuilds A", matmul(matmul(U, S), Vt), A)
    print("ALL OK" if ok else "SOME FAILED")
