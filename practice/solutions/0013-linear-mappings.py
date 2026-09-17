"""0013 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def apply2(A, x):
    return [A[0][0] * x[0] + A[0][1] * x[1], A[1][0] * x[0] + A[1][1] * x[1]]


def is_linear(f):
    u, v, lam = [1, 2], [3, -1], 3
    add_first = f([u[0] + v[0], u[1] + v[1]])
    add_last = [a + b for a, b in zip(f(u), f(v))]
    scale_first = f([lam * u[0], lam * u[1]])
    scale_last = [lam * a for a in f(u)]
    close = lambda p, q: all(abs(a - b) < TOL for a, b in zip(p, q))
    return close(add_first, add_last) and close(scale_first, scale_last)


def _rank2(A):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if abs(det) > TOL:
        return 2
    return 0 if all(abs(v) < TOL for row in A for v in row) else 1


def kernel_dim2(A):
    return 2 - _rank2(A)


def image_dim2(A):
    return _rank2(A)


def rank_nullity_holds(A):
    return kernel_dim2(A) + image_dim2(A) == 2


def _check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("linear", is_linear(lambda v: [2 * v[0] + v[1], v[0] - v[1]]), True)
    ok &= _check("affine", is_linear(lambda v: [2 * v[0] + v[1] + 1, v[0] - v[1]]), False)
    ok &= _check("square", is_linear(lambda v: [v[0] ** 2, v[1]]), False)
    ok &= _check("apply2", apply2([[2, 1], [1, -1]], [1, 3]), [5, -2])
    ok &= _check("ker regular", kernel_dim2([[1, 0], [0, 1]]), 0)
    ok &= _check("ker singular", kernel_dim2([[1, 2], [2, 4]]), 1)
    ok &= _check("im singular", image_dim2([[1, 2], [2, 4]]), 1)
    ok &= _check("im zero", image_dim2([[0, 0], [0, 0]]), 0)
    ok &= _check("rank-nullity", rank_nullity_holds([[1, 2], [2, 4]]), True)
    print("ALL OK" if ok else "SOME FAILED")
