"""0009 · basis & dimension — practice (fill the gaps, then run the file).

Run:  python3 practice/0009-basis-dimension.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def det2(a, b, c, d):
    """Determinant of [[a, b], [c, d]]."""
    # TODO
    raise NotImplementedError


def is_basis_2d(u, v):
    """Basis of R^2 iff independent (det != 0)."""
    # TODO
    raise NotImplementedError


def coords_tilted(x, y):
    """Coordinates of (x, y) in basis (1,1),(1,-1): ((x+y)/2, (x-y)/2)."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, (int, float)):
        ok = abs(got - want) < TOL
    elif isinstance(want, list):
        ok = all(abs(a - b) < TOL for a, b in zip(got, want))
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("standard is basis", is_basis_2d([1, 0], [0, 1]), True)
    ok &= _check("tilted is basis", is_basis_2d([1, 1], [1, -1]), True)
    ok &= _check("parallel not basis", is_basis_2d([1, 1], [2, 2]), False)
    ok &= _check("coords of (4,2)", coords_tilted(4, 2), [3, 1])
    ok &= _check("dim R2 = 2", 1 + 1, 2)
    print("ALL OK" if ok else "SOME FAILED")
