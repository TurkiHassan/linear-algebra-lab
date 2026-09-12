"""0005 · euclidean vector spaces — practice (fill the gaps, then run the file).

Run:  python3 practice/0005-euclidean-spaces.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library (math).
"""

import math

TOL = 1e-9


def dot(u, v):
    """Inner product: sum of entrywise products."""
    # TODO
    raise NotImplementedError


def norm(u):
    """Euclidean length: sqrt(sum of squares)."""
    # TODO
    raise NotImplementedError


def distance(u, v):
    """d(u, v) = ||u - v||."""
    # TODO: use dot() or norm()
    raise NotImplementedError


def is_orthogonal(u, v):
    """True iff dot product is 0 (within tolerance)."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    ok = abs(got - want) < TOL if isinstance(want, float) else got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("dot (1,2).(3,-1)", dot([1, 2], [3, -1]), 1)
    ok &= _check("norm (3,4)", norm([3, 4]), 5.0)
    ok &= _check("dist (0,0)-(1,1)", distance([0, 0], [1, 1]), math.sqrt(2))
    ok &= _check("orthogonal (3,1),(-1,3)", is_orthogonal([3, 1], [-1, 3]), True)
    ok &= _check("not orthogonal", is_orthogonal([1, 0], [1, 1]), False)
    print("ALL OK" if ok else "SOME FAILED")
