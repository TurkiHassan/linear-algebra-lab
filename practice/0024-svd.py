"""0024 · singular value decomposition — practice.

Run:  python3 practice/0024-svd.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def transpose(A):
    """Swap rows and columns."""
    # TODO
    raise NotImplementedError


def matmul(A, B):
    """Multiply two matrices of compatible shape."""
    # TODO
    raise NotImplementedError


def gram(A):
    """A^T A — symmetric and positive semidefinite for every A."""
    # TODO
    raise NotImplementedError


def singular_values2(A):
    """Singular values of a 2x2 matrix, DESCENDING.

    They are the square roots of the eigenvalues of A^T A, which are never negative.
    """
    # TODO
    raise NotImplementedError


def right_vectors2(A):
    """Unit eigenvectors of A^T A, matching singular_values2 in order."""
    # TODO
    raise NotImplementedError


def left_vector(A, v, sigma):
    """u = A v / sigma; None when sigma is zero."""
    # TODO
    raise NotImplementedError


def svd2(A):
    """Return (U, S, Vt) with A = U S Vt, all 2x2."""
    # TODO
    raise NotImplementedError


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
