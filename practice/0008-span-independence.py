"""0008 · span & independence — practice (fill the gaps, then run the file).

Run:  python3 practice/0008-span-independence.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""


def det2(a, b, c, d):
    """Determinant of [[a, b], [c, d]]."""
    # TODO
    raise NotImplementedError


def is_independent_2d(u, v):
    """Two 2D vectors are independent iff det != 0."""
    # TODO: columns u, v -> det = u0*v1 - u1*v0
    raise NotImplementedError


def dependence_weights(u, v):
    """Return nonzero (c1, c2) with c1*u + c2*v = 0, or None if independent."""
    # TODO: if independent -> None; else find small integer weights
    raise NotImplementedError


def _check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("(1,1),(2,2) dependent", is_independent_2d([1, 1], [2, 2]), False)
    ok &= _check("(1,0),(0,1) independent", is_independent_2d([1, 0], [0, 1]), True)
    w = dependence_weights([1, 1], [2, 2])
    ok &= _check("weights kill to zero", [w[0] * 1 + w[1] * 2, w[0] * 1 + w[1] * 2], [0, 0])
    ok &= _check("weights nonzero", (w[0] != 0 or w[1] != 0), True)
    ok &= _check("independent -> None", dependence_weights([1, 0], [0, 1]), None)
    print("ALL OK" if ok else "SOME FAILED")
