"""0014 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def matrix_of(f):
    c1, c2 = f([1, 0]), f([0, 1])
    return [[c1[0], c2[0]], [c1[1], c2[1]]]


def matmul2(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def inverse2(A):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if abs(det) < TOL:
        return None
    return [[A[1][1] / det, -A[0][1] / det], [-A[1][0] / det, A[0][0] / det]]


def similar(A, S):
    Si = inverse2(S)
    if Si is None:
        return None
    return matmul2(Si, matmul2(A, S))


def trace2(A):
    return A[0][0] + A[1][1]


def _check(name, got, want):
    if isinstance(want, list):
        ok = all(abs(a - b) < TOL for ra, rb in zip(got, want) for a, b in zip(ra, rb))
    elif isinstance(want, (int, float)):
        ok = abs(got - want) < TOL
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("matrix of phi", matrix_of(lambda v: [2 * v[0] + v[1], v[0] - v[1]]), [[2, 1], [1, -1]])
    ok &= _check("matrix of swap", matrix_of(lambda v: [v[1], v[0]]), [[0, 1], [1, 0]])
    ok &= _check("matmul", matmul2([[1, 2], [3, 4]], [[2, 0], [1, 3]]), [[4, 6], [10, 12]])
    ok &= _check("inverse", inverse2([[1, 2], [3, 4]]), [[-2, 1], [1.5, -0.5]])
    ok &= _check("singular", inverse2([[1, 2], [2, 4]]), None)
    ok &= _check("trace invariant", trace2(similar([[2, 1], [1, -1]], [[1, 0], [1, 1]])), 1)
    print("ALL OK" if ok else "SOME FAILED")
