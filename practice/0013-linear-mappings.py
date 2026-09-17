"""0013 · linear mappings, kernel & image — practice.

Run:  python3 practice/0013-linear-mappings.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def apply2(A, x):
    """Apply a 2x2 matrix A = [[a, b], [c, d]] to x = [x1, x2]."""
    # TODO
    raise NotImplementedError


def is_linear(f):
    """Test Phi(x + y) == Phi(x) + Phi(y) and Phi(3x) == 3*Phi(x).

    Use two fixed probes, e.g. u = [1, 2] and v = [3, -1].
    """
    # TODO
    raise NotImplementedError


def kernel_dim2(A):
    """dim ker(A) for a 2x2 matrix: 0 if det != 0, else 2 - rank."""
    # TODO
    raise NotImplementedError


def image_dim2(A):
    """dim Im(A) = rank of the 2x2 matrix."""
    # TODO
    raise NotImplementedError


def rank_nullity_holds(A):
    """Check dim ker + dim Im == 2 for a 2x2 matrix."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    lin = lambda v: [2 * v[0] + v[1], v[0] - v[1]]
    aff = lambda v: [2 * v[0] + v[1] + 1, v[0] - v[1]]
    sq = lambda v: [v[0] ** 2, v[1]]
    ok &= _check("Ax is linear", is_linear(lin), True)
    ok &= _check("Ax + b is not", is_linear(aff), False)
    ok &= _check("x^2 is not", is_linear(sq), False)
    ok &= _check("apply2", apply2([[2, 1], [1, -1]], [1, 3]), [5, -2])
    ok &= _check("regular: ker = 0", kernel_dim2([[1, 0], [0, 1]]), 0)
    ok &= _check("singular: ker = 1", kernel_dim2([[1, 2], [2, 4]]), 1)
    ok &= _check("singular: im = 1", image_dim2([[1, 2], [2, 4]]), 1)
    ok &= _check("zero matrix: im = 0", image_dim2([[0, 0], [0, 0]]), 0)
    ok &= _check("rank-nullity", rank_nullity_holds([[1, 2], [2, 4]]), True)
    print("ALL OK" if ok else "SOME FAILED")
