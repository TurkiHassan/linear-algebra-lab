"""0011 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def det2(a, b, c, d):
    return a * d - b * c


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def independent_2d(u, v):
    return det2(u[0], u[1], v[0], v[1]) != 0


def coords_tilted(x, y):
    return [(x + y) / 2, (x - y) / 2]


def _check(name, got, want):
    if isinstance(want, float):
        ok = abs(got - want) < TOL
    elif isinstance(want, list):
        ok = all(abs(a - b) < TOL for a, b in zip(got, want))
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("det", det2(2, 1, -3, 2), 7)
    ok &= _check("dot", dot([1, 2], [3, -1]), 1)
    ok &= _check("indep", independent_2d([1, 0], [0, 1]), True)
    ok &= _check("dep", independent_2d([1, 1], [2, 2]), False)
    ok &= _check("coords", coords_tilted(4, 2), [3, 1])
    print("ALL OK" if ok else "SOME FAILED")
