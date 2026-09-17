"""0015 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def is_linear_map(f, dim=3):
    zero = [0] * dim
    if any(abs(v) > TOL for v in f(zero)):
        return False
    u = [1, 2, -1][:dim]
    v = [3, -1, 2][:dim]
    lam = 3
    add_first = f([a + b for a, b in zip(u, v)])
    add_last = [a + b for a, b in zip(f(u), f(v))]
    scale_first = f([lam * a for a in u])
    scale_last = [lam * a for a in f(u)]
    close = lambda p, q: all(abs(a - b) < TOL for a, b in zip(p, q))
    return close(add_first, add_last) and close(scale_first, scale_last)


def point_on_line(p, d, t):
    return [pi + t * di for pi, di in zip(p, d)]


def affine_dim(n, rank_a):
    return n - rank_a


def shape_name(n, rank_a):
    k = affine_dim(n, rank_a)
    return {0: "point", 1: "line", 2: "plane"}.get(k, "space-" + str(k))


def passes_through_origin(p):
    return all(abs(v) < TOL for v in p)


def _check(name, got, want):
    ok = all(abs(a - b) < TOL for a, b in zip(got, want)) if isinstance(want, list) else got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("linear", is_linear_map(lambda v: [v[0] + v[1], v[1] - v[2], v[0]]), True)
    ok &= _check("affine", is_linear_map(lambda v: [v[0] + v[1] + 1, v[1] - v[2], v[0]]), False)
    ok &= _check("t = 0", point_on_line([1, 2, 3], [2, -1, 1], 0), [1, 2, 3])
    ok &= _check("t = 1", point_on_line([1, 2, 3], [2, -1, 1], 1), [3, 1, 4])
    ok &= _check("t = -1", point_on_line([1, 2, 3], [2, -1, 1], -1), [-1, 3, 2])
    ok &= _check("dim", affine_dim(3, 2), 1)
    ok &= _check("line", shape_name(3, 2), "line")
    ok &= _check("point", shape_name(3, 3), "point")
    ok &= _check("off origin", passes_through_origin([1, 2, 3]), False)
    ok &= _check("on origin", passes_through_origin([0, 0, 0]), True)
    print("ALL OK" if ok else "SOME FAILED")
