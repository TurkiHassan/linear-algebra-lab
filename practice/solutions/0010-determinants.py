"""0010 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def det2(a, b, c, d):
    return a * d - b * c


def det3_sarrus(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, k = M[2]
    return (a * e * k + b * f * g + c * d * h) - (c * e * g + a * f * h + b * d * k)


def is_invertible_2(a, b, c, d):
    return det2(a, b, c, d) != 0


def _check(name, got, want):
    ok = abs(got - want) < TOL if isinstance(want, float) else got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("det7", det2(2, 1, -3, 2), 7)
    ok &= _check("det0", det2(2, 4, 1, 2), 0)
    ok &= _check("det-3", det2(0, 2, 1.5, 4), -3)
    ok &= _check("sarrus", det3_sarrus([[2, 4, 6], [3, 8, 5], [-1, 1, 2]]), 44)
    ok &= _check("inv", is_invertible_2(2, 1, -3, 2), True)
    ok &= _check("sing", is_invertible_2(2, 4, 1, 2), False)
    print("ALL OK" if ok else "SOME FAILED")
