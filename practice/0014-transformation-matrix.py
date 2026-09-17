"""0014 · transformation matrix & basis change — practice.

Run:  python3 practice/0014-transformation-matrix.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def matrix_of(f):
    """Build the 2x2 transformation matrix of a linear map on R^2.

    Columns are the images of e1 and e2, written in the standard basis.
    """
    # TODO: call f([1, 0]) and f([0, 1]) and place them as COLUMNS.
    raise NotImplementedError


def matmul2(A, B):
    """Multiply two 2x2 matrices."""
    # TODO
    raise NotImplementedError


def inverse2(A):
    """Inverse of a 2x2 matrix; return None when det == 0."""
    # TODO
    raise NotImplementedError


def similar(A, S):
    """Same map, new basis: S^-1 A S."""
    # TODO
    raise NotImplementedError


def trace2(A):
    """a11 + a22 — invariant under a basis change."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, list) and want and isinstance(want[0], list):
        ok = all(abs(a - b) < TOL for ra, rb in zip(got, want) for a, b in zip(ra, rb))
    elif isinstance(want, (int, float)) and not isinstance(want, bool):
        ok = abs(got - want) < TOL
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    phi = lambda v: [2 * v[0] + v[1], v[0] - v[1]]
    swap = lambda v: [v[1], v[0]]
    ok &= _check("matrix of phi", matrix_of(phi), [[2, 1], [1, -1]])
    ok &= _check("matrix of swap", matrix_of(swap), [[0, 1], [1, 0]])
    ok &= _check("matmul", matmul2([[1, 2], [3, 4]], [[2, 0], [1, 3]]), [[4, 6], [10, 12]])
    ok &= _check("inverse", inverse2([[1, 2], [3, 4]]), [[-2, 1], [1.5, -0.5]])
    ok &= _check("singular has no inverse", inverse2([[1, 2], [2, 4]]), None)
    S = [[1, 0], [1, 1]]                       # new basis (1,1) and (0,1)
    A = [[2, 1], [1, -1]]
    ok &= _check("trace is invariant", trace2(similar(A, S)), trace2(A))
    print("ALL OK" if ok else "SOME FAILED")
