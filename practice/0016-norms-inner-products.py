"""0016 · norms & inner products — practice.

Run:  python3 practice/0016-norms-inner-products.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

import math

TOL = 1e-9


def norm_l1(x):
    """Manhattan norm: sum of absolute values."""
    # TODO
    raise NotImplementedError


def norm_l2(x):
    """Euclidean norm: square root of the sum of squares."""
    # TODO
    raise NotImplementedError


def norm_linf(x):
    """Maximum norm: the largest absolute component."""
    # TODO
    raise NotImplementedError


def inner_A(x, y, A):
    """General inner product <x, y> = x^T A y for a 2x2 matrix A."""
    # TODO
    raise NotImplementedError


def is_positive_definite2(A):
    """Symmetric 2x2 is positive definite iff a11 > 0 and det > 0."""
    # TODO: check symmetry first.
    raise NotImplementedError


def cauchy_schwarz_holds(x, y):
    """Check |<x, y>| <= ||x|| * ||y|| for the dot product."""
    # TODO
    raise NotImplementedError


def distance(x, y):
    """d(x, y) = ||x - y|| with the Euclidean norm."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, bool):
        ok = got == want
    elif isinstance(want, (int, float)):
        ok = abs(got - want) < TOL
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    x = [3, -4]
    ok &= _check("l1 of (3,-4)", norm_l1(x), 7)
    ok &= _check("l2 of (3,-4)", norm_l2(x), 5)
    ok &= _check("linf of (3,-4)", norm_linf(x), 4)
    ok &= _check("ordering linf <= l2 <= l1", norm_linf(x) <= norm_l2(x) <= norm_l1(x), True)
    ok &= _check("dot as A = I", inner_A([1, 1], [-1, 1], [[1, 0], [0, 1]]), 0)
    ok &= _check("weighted is not zero", inner_A([1, 1], [-1, 1], [[2, 0], [0, 1]]), -1)
    ok &= _check("PD matrix", is_positive_definite2([[9, 6], [6, 5]]), True)
    ok &= _check("not PD", is_positive_definite2([[9, 6], [6, 3]]), False)
    ok &= _check("Cauchy-Schwarz", cauchy_schwarz_holds([1, 2, 2], [2, 1, 0]), True)
    ok &= _check("distance", distance([1, 2, 2], [2, 1, 0]), math.sqrt(6))
    print("ALL OK" if ok else "SOME FAILED")
