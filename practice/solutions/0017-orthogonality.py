"""0017 solution — kept separate from the exercise on purpose."""

import math

TOL = 1e-9


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def _norm(x):
    return math.sqrt(dot(x, x))


def angle_deg(x, y):
    c = dot(x, y) / (_norm(x) * _norm(y))
    c = max(-1.0, min(1.0, c))
    return math.degrees(math.acos(c))


def are_orthogonal(x, y):
    return abs(dot(x, y)) < TOL


def is_orthonormal_pair(x, y):
    return are_orthogonal(x, y) and abs(_norm(x) - 1) < TOL and abs(_norm(y) - 1) < TOL


def is_orthogonal_matrix2(A):
    c1 = [A[0][0], A[1][0]]
    c2 = [A[0][1], A[1][1]]
    return is_orthonormal_pair(c1, c2)


def rotation_or_reflection(A):
    if not is_orthogonal_matrix2(A):
        return "neither"
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return "rotation" if det > 0 else "reflection"


def pythagoras_holds(x, y):
    s = [a + b for a, b in zip(x, y)]
    return abs(dot(s, s) - dot(x, x) - dot(y, y)) < TOL


def _check(name, got, want):
    ok = got == want if isinstance(want, (bool, str)) else abs(got - want) < 1e-4
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    r = math.sqrt(2) / 2
    ok &= _check("dot", dot([1, 2, 2], [2, 1, 0]), 4)
    ok &= _check("90", angle_deg([1, 0, 1], [0, 1, 0]), 90.0)
    ok &= _check("0", angle_deg([1, 1], [2, 2]), 0.0)
    ok &= _check("orthogonal", are_orthogonal([1, 0, 1], [0, 1, 0]), True)
    ok &= _check("length 2", is_orthonormal_pair([2, 0], [0, 2]), False)
    ok &= _check("orthonormal", is_orthonormal_pair([1, 0], [0, 1]), True)
    ok &= _check("orthogonal matrix", is_orthogonal_matrix2([[r, -r], [r, r]]), True)
    ok &= _check("scaled", is_orthogonal_matrix2([[2, 0], [0, 2]]), False)
    ok &= _check("rotation", rotation_or_reflection([[r, -r], [r, r]]), "rotation")
    ok &= _check("reflection", rotation_or_reflection([[1, 0], [0, -1]]), "reflection")
    ok &= _check("pythagoras", pythagoras_holds([3, 0], [0, 4]), True)
    ok &= _check("not pythagoras", pythagoras_holds([3, 1], [1, 4]), False)
    print("ALL OK" if ok else "SOME FAILED")
