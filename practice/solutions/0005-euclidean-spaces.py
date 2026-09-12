"""0005 solution — kept separate from the exercise on purpose."""

import math

TOL = 1e-9


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def norm(u):
    return math.sqrt(dot(u, u))


def distance(u, v):
    return norm([x - y for x, y in zip(u, v)])


def is_orthogonal(u, v):
    return abs(dot(u, v)) < TOL


def _check(name, got, want):
    ok = abs(got - want) < TOL if isinstance(want, float) else got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("dot", dot([1, 2], [3, -1]), 1)
    ok &= _check("norm", norm([3, 4]), 5.0)
    ok &= _check("dist", distance([0, 0], [1, 1]), math.sqrt(2))
    ok &= _check("orth", is_orthogonal([3, 1], [-1, 3]), True)
    ok &= _check("not-orth", is_orthogonal([1, 0], [1, 1]), False)
    print("ALL OK" if ok else "SOME FAILED")
