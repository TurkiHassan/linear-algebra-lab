"""0017 · angles, orthogonality & orthogonal matrices — practice.

Run:  python3 practice/0017-orthogonality.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

import math

TOL = 1e-9


def dot(x, y):
    """Plain dot product."""
    # TODO
    raise NotImplementedError


def angle_deg(x, y):
    """Angle in degrees from cos(w) = <x,y> / (||x|| ||y||).

    Clamp the cosine into [-1, 1] before acos — floating point drifts.
    """
    # TODO
    raise NotImplementedError


def are_orthogonal(x, y):
    """Orthogonal iff the inner product is zero."""
    # TODO
    raise NotImplementedError


def is_orthonormal_pair(x, y):
    """Orthogonal AND both lengths equal to 1."""
    # TODO
    raise NotImplementedError


def is_orthogonal_matrix2(A):
    """A is orthogonal iff its columns are orthonormal (A^T A = I)."""
    # TODO
    raise NotImplementedError


def rotation_or_reflection(A):
    """Return "rotation" (det = +1), "reflection" (det = -1) or "neither"."""
    # TODO: only meaningful for an orthogonal matrix.
    raise NotImplementedError


def pythagoras_holds(x, y):
    """||x + y||^2 == ||x||^2 + ||y||^2 happens exactly when x and y are orthogonal."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, bool) or isinstance(want, str):
        ok = got == want
    else:
        ok = abs(got - want) < 1e-4
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    r = math.sqrt(2) / 2
    ok &= _check("dot", dot([1, 2, 2], [2, 1, 0]), 4)
    ok &= _check("right angle", angle_deg([1, 0, 1], [0, 1, 0]), 90.0)
    ok &= _check("same direction", angle_deg([1, 1], [2, 2]), 0.0)
    ok &= _check("orthogonal", are_orthogonal([1, 0, 1], [0, 1, 0]), True)
    ok &= _check("not orthonormal (length 2)", is_orthonormal_pair([2, 0], [0, 2]), False)
    ok &= _check("orthonormal", is_orthonormal_pair([1, 0], [0, 1]), True)
    ok &= _check("rotation matrix is orthogonal", is_orthogonal_matrix2([[r, -r], [r, r]]), True)
    ok &= _check("scaled columns are not", is_orthogonal_matrix2([[2, 0], [0, 2]]), False)
    ok &= _check("rotation", rotation_or_reflection([[r, -r], [r, r]]), "rotation")
    ok &= _check("reflection", rotation_or_reflection([[1, 0], [0, -1]]), "reflection")
    ok &= _check("pythagoras", pythagoras_holds([3, 0], [0, 4]), True)
    ok &= _check("no pythagoras", pythagoras_holds([3, 1], [1, 4]), False)
    print("ALL OK" if ok else "SOME FAILED")
