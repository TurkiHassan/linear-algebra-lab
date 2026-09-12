"""0011 · drills bank — practice (fill the gaps, then run the file).

Run:  python3 practice/0011-drills.py
Full solution lives in practice/solutions/ (kept separate on purpose).
One function per past lesson — the whole path in one file.
"""

import math

TOL = 1e-9


def det2(a, b, c, d):
    """0002/0010: det [[a, b], [c, d]]."""
    # TODO
    raise NotImplementedError


def dot(u, v):
    """0005: inner product."""
    # TODO
    raise NotImplementedError


def independent_2d(u, v):
    """0008: True iff det != 0."""
    # TODO
    raise NotImplementedError


def coords_tilted(x, y):
    """0009: coords of (x, y) in basis (1,1),(1,-1)."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, float):
        ok = abs(got - want) < TOL
    elif isinstance(want, list):
        ok = all(abs(a - b) < TOL for a, b in zip(got, want))
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("D10 det", det2(2, 1, -3, 2), 7)
    ok &= _check("D5 dot", dot([1, 2], [3, -1]), 1)
    ok &= _check("D8 independent", independent_2d([1, 0], [0, 1]), True)
    ok &= _check("D8 dependent", independent_2d([1, 1], [2, 2]), False)
    ok &= _check("D9 coords", coords_tilted(4, 2), [3, 1])
    ok &= _check("D5 dist via norm", math.hypot(1, 1), math.sqrt(2))
    print("ALL OK" if ok else "SOME FAILED")
