"""0019 solution — kept separate from the exercise on purpose."""

import math

TOL = 1e-9


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def projection_scalar(x, b):
    return dot(b, x) / dot(b, b)


def project_on_line(x, b):
    lam = projection_scalar(x, b)
    return [lam * bi for bi in b]


def projection_matrix_line(b):
    bb = dot(b, b)
    return [[bi * bj / bb for bj in b] for bi in b]


def residual(x, b):
    p = project_on_line(x, b)
    return [a - c for a, c in zip(x, p)]


def project_on_plane(x, b1, b2):
    g11, g12, g22 = dot(b1, b1), dot(b1, b2), dot(b2, b2)
    r1, r2 = dot(b1, x), dot(b2, x)
    det = g11 * g22 - g12 * g12
    lam1 = (g22 * r1 - g12 * r2) / det
    lam2 = (-g12 * r1 + g11 * r2) / det
    return [lam1 * a + lam2 * b for a, b in zip(b1, b2)]


def rotate(x, theta_deg):
    t = math.radians(theta_deg)
    c, s = math.cos(t), math.sin(t)
    return [c * x[0] - s * x[1], s * x[0] + c * x[1]]


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
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("lambda", projection_scalar([3, 1], [1, 2]), 1.0)
    ok &= _check("projection", project_on_line([3, 1], [1, 2]), [1, 2])
    ok &= _check("residual", abs(dot(residual([3, 1], [1, 2]), [1, 2])) < TOL, True)
    ok &= _check("lecture", project_on_line([1, 1, 1], [1, 2, 2]), [5 / 9, 10 / 9, 10 / 9])
    ok &= _check("P", projection_matrix_line([1, 2]), [[0.2, 0.4], [0.4, 0.8]])
    ok &= _check("plane", project_on_plane([6, 0, 0], [1, 1, 1], [0, 1, 2]), [5, 2, -1])
    ok &= _check("rotate 45", rotate([1, 0], 45), [math.sqrt(2) / 2, math.sqrt(2) / 2])
    ok &= _check("rotate 90", rotate([1, 0], 90), [0, 1])
    print("ALL OK" if ok else "SOME FAILED")
