"""0016 solution — kept separate from the exercise on purpose."""

import math

TOL = 1e-9


def norm_l1(x):
    return sum(abs(v) for v in x)


def norm_l2(x):
    return math.sqrt(sum(v * v for v in x))


def norm_linf(x):
    return max(abs(v) for v in x)


def inner_A(x, y, A):
    Ay = [A[0][0] * y[0] + A[0][1] * y[1], A[1][0] * y[0] + A[1][1] * y[1]]
    return x[0] * Ay[0] + x[1] * Ay[1]


def is_positive_definite2(A):
    if abs(A[0][1] - A[1][0]) > TOL:
        return False
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return A[0][0] > TOL and det > TOL


def cauchy_schwarz_holds(x, y):
    ip = sum(a * b for a, b in zip(x, y))
    return abs(ip) <= norm_l2(x) * norm_l2(y) + TOL


def distance(x, y):
    return norm_l2([a - b for a, b in zip(x, y)])


def _check(name, got, want):
    ok = got == want if isinstance(want, bool) else abs(got - want) < TOL
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    x = [3, -4]
    ok &= _check("l1", norm_l1(x), 7)
    ok &= _check("l2", norm_l2(x), 5)
    ok &= _check("linf", norm_linf(x), 4)
    ok &= _check("ordering", norm_linf(x) <= norm_l2(x) <= norm_l1(x), True)
    ok &= _check("dot", inner_A([1, 1], [-1, 1], [[1, 0], [0, 1]]), 0)
    ok &= _check("weighted", inner_A([1, 1], [-1, 1], [[2, 0], [0, 1]]), -1)
    ok &= _check("PD", is_positive_definite2([[9, 6], [6, 5]]), True)
    ok &= _check("not PD", is_positive_definite2([[9, 6], [6, 3]]), False)
    ok &= _check("Cauchy-Schwarz", cauchy_schwarz_holds([1, 2, 2], [2, 1, 0]), True)
    ok &= _check("distance", distance([1, 2, 2], [2, 1, 0]), math.sqrt(6))
    print("ALL OK" if ok else "SOME FAILED")
