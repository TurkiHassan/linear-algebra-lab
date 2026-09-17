"""0015 · affine spaces — practice.

Run:  python3 practice/0015-affine-spaces.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def is_linear_map(f, dim=3):
    """A map is linear only if f(0) == 0 AND it respects + and scaling."""
    # TODO: start with the cheapest test — the zero vector.
    raise NotImplementedError


def point_on_line(p, d, t):
    """Parametric point of the affine line L = p + t*d."""
    # TODO
    raise NotImplementedError


def affine_dim(n, rank_a):
    """Dimension of the solution set of Ax = b -> n - rank(A)."""
    # TODO
    raise NotImplementedError


def shape_name(n, rank_a):
    """Name the geometry: "point", "line", "plane" or "space-k"."""
    # TODO: 0 -> point, 1 -> line, 2 -> plane, else "space-" + str(k)
    raise NotImplementedError


def passes_through_origin(p):
    """An affine subspace is a vector subspace only when it contains 0."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, list):
        ok = all(abs(a - b) < TOL for a, b in zip(got, want))
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    linear = lambda v: [v[0] + v[1], v[1] - v[2], v[0]]
    affine = lambda v: [v[0] + v[1] + 1, v[1] - v[2], v[0]]
    ok &= _check("Ax is linear", is_linear_map(linear), True)
    ok &= _check("Ax + b is affine", is_linear_map(affine), False)
    ok &= _check("t = 0 gives support point", point_on_line([1, 2, 3], [2, -1, 1], 0), [1, 2, 3])
    ok &= _check("t = 1", point_on_line([1, 2, 3], [2, -1, 1], 1), [3, 1, 4])
    ok &= _check("t = -1", point_on_line([1, 2, 3], [2, -1, 1], -1), [-1, 3, 2])
    ok &= _check("dim of solution set", affine_dim(3, 2), 1)
    ok &= _check("shape is a line", shape_name(3, 2), "line")
    ok &= _check("shape is a point", shape_name(3, 3), "point")
    ok &= _check("origin not on L", passes_through_origin([1, 2, 3]), False)
    ok &= _check("origin on L", passes_through_origin([0, 0, 0]), True)
    print("ALL OK" if ok else "SOME FAILED")
