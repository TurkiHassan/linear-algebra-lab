"""0019 · orthogonal projections & rotations — practice.

Run:  python3 practice/0019-projections-rotations.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

import math

TOL = 1e-9


def dot(x, y):
    """Plain dot product."""
    # TODO
    raise NotImplementedError


def projection_scalar(x, b):
    """lambda = (b^T x) / ||b||^2 — how far along b the shadow reaches."""
    # TODO
    raise NotImplementedError


def project_on_line(x, b):
    """pi(x) = lambda * b."""
    # TODO
    raise NotImplementedError


def projection_matrix_line(b):
    """P = b b^T / ||b||^2 as a list of rows."""
    # TODO
    raise NotImplementedError


def residual(x, b):
    """x - pi(x); it must be orthogonal to b."""
    # TODO
    raise NotImplementedError


def project_on_plane(x, b1, b2):
    """pi_U(x) = B (B^T B)^-1 B^T x for a 2-column B, done by hand.

    Solve the 2x2 system (B^T B) lam = B^T x, then combine lam[0]*b1 + lam[1]*b2.
    """
    # TODO
    raise NotImplementedError


def rotate(x, theta_deg):
    """Apply R(theta) = [[cos, -sin], [sin, cos]] to a vector in R^2."""
    # TODO
    raise NotImplementedError


def _close(p, q):
    return all(abs(a - b) < 1e-6 for a, b in zip(p, q))


def _check(name, got, want):
    if isinstance(want, bool):
        ok = got == want
    elif isinstance(want, list) and want and isinstance(want[0], list):
        ok = all(_close(a, b) for a, b in zip(got, want))
    elif isinstance(want, list):
        ok = _close(got, want)
    else:
        ok = abs(got - want) < 1e-6
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("lambda for (3,1) on (1,2)", projection_scalar([3, 1], [1, 2]), 1.0)
    ok &= _check("projection is (1,2)", project_on_line([3, 1], [1, 2]), [1, 2])
    ok &= _check("residual is orthogonal", abs(dot(residual([3, 1], [1, 2]), [1, 2])) < TOL, True)
    ok &= _check("lecture example", project_on_line([1, 1, 1], [1, 2, 2]), [5 / 9, 10 / 9, 10 / 9])
    ok &= _check("P rows", projection_matrix_line([1, 2]), [[0.2, 0.4], [0.4, 0.8]])
    ok &= _check("plane example", project_on_plane([6, 0, 0], [1, 1, 1], [0, 1, 2]), [5, 2, -1])
    ok &= _check("rotate 45 of (1,0)", rotate([1, 0], 45), [math.sqrt(2) / 2, math.sqrt(2) / 2])
    ok &= _check("rotate 90 of (1,0)", rotate([1, 0], 90), [0, 1])
    print("ALL OK" if ok else "SOME FAILED")
