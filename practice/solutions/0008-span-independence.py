"""0008 solution — kept separate from the exercise on purpose."""


def det2(a, b, c, d):
    return a * d - b * c


def is_independent_2d(u, v):
    return det2(u[0], u[1], v[0], v[1]) != 0


def dependence_weights(u, v):
    if is_independent_2d(u, v):
        return None
    if u == [0, 0]:
        return (1, 0)
    if v == [0, 0]:
        return (0, 1)
    # parallel nonzero: v = k*u for k = v_i / u_i on a nonzero component
    i = 0 if u[0] != 0 else 1
    # u[i]*c1 + v[i]*c2 = 0 -> (c1, c2) = (v[i], -u[i])
    return (v[i], -u[i])


def _check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("dependent", is_independent_2d([1, 1], [2, 2]), False)
    ok &= _check("independent", is_independent_2d([1, 0], [0, 1]), True)
    w = dependence_weights([1, 1], [2, 2])
    ok &= _check("zero", [w[0] * 1 + w[1] * 2, w[0] * 1 + w[1] * 2], [0, 0])
    ok &= _check("nonzero", (w[0] != 0 or w[1] != 0), True)
    ok &= _check("none", dependence_weights([1, 0], [0, 1]), None)
    print("ALL OK" if ok else "SOME FAILED")
