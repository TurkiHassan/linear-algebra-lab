"""0027 · partial derivatives and gradients — practice.

Run:  python3 practice/0027-partial-gradients.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""
import math

TOL = 1e-9


def partial(f, x, i, h=1e-6):
    """Partial derivative of f at x along axis i — every other coordinate frozen."""
    # TODO
    raise NotImplementedError


def gradient(f, x, h=1e-6):
    """All partials collected in order — the gradient as a row vector."""
    # TODO
    raise NotImplementedError


def gradient_shape(x):
    """The gradient of f: R^n -> R lives in R^(1 x n), so its shape is (1, n)."""
    # TODO
    raise NotImplementedError


def directional_derivative(f, x, d, h=1e-6):
    """Rate of change along the direction d — the gradient dotted with a unit d."""
    # TODO
    raise NotImplementedError


def steepest_ascent(f, x, h=1e-6):
    """Unit vector in the direction the gradient points — the fastest way up."""
    # TODO
    raise NotImplementedError


def descent_step(f, x, eta, h=1e-6):
    """One gradient descent step: walk against the gradient."""
    # TODO
    raise NotImplementedError


def chain_path(f, path, dpath, t, h=1e-6):
    """df/dt for x = path(t): sum over every route from t to f."""
    # TODO
    raise NotImplementedError


def is_perpendicular(u, v, tol=1e-6):
    """True when the inner product vanishes — the gradient and the level curve tangent."""
    # TODO
    raise NotImplementedError


def _flat(x):
    if isinstance(x, list):
        out = []
        for v in x:
            out.extend(_flat(v))
        return out
    if isinstance(x, tuple):
        return list(x)
    return [x]


def _check(name, got, want, tol=1e-6):
    if isinstance(want, (list, tuple)):
        g, w = (_flat(got) if got is not None else None), _flat(want)
        ok = g is not None and len(g) == len(w) and all(abs(a - b) < tol for a, b in zip(g, w))
    elif isinstance(want, (int, float)) and not isinstance(want, bool):
        ok = got is not None and abs(got - want) < tol
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    slide = lambda v: (v[0] + 2 * v[1] ** 3) ** 2
    poly = lambda v: v[0] ** 2 * v[1] + v[0] * v[1] ** 3
    bowl = lambda v: v[0] ** 2 + v[1] ** 2
    ok = True
    ok &= _check("partial along x", partial(slide, [1, 1], 0), 6, 1e-4)
    ok &= _check("partial along y", partial(slide, [1, 1], 1), 36, 1e-3)
    ok &= _check("gradient of the slide example", gradient(slide, [1, 1]), [6, 36], 1e-3)
    ok &= _check("gradient of the second example", gradient(poly, [1, 1]), [3, 4], 1e-4)
    ok &= _check("gradient shape is a row", gradient_shape([1, 1, 1]), (1, 3))
    ok &= _check("directional derivative along x", directional_derivative(bowl, [1, 2], [1, 0]), 2, 1e-4)
    ok &= _check("steepest ascent is a unit vector",
                 sum(v * v for v in steepest_ascent(bowl, [1, 2])), 1, 1e-6)
    ok &= _check("descent step moves toward the minimum", descent_step(bowl, [1, 2], 0.1), [0.8, 1.6], 1e-5)
    path = lambda t: [math.sin(t), math.cos(t)]
    dpath = lambda t: [math.cos(t), -math.sin(t)]
    f2 = lambda v: v[0] ** 2 + 2 * v[1]
    t0 = math.pi / 2
    ok &= _check("chain rule along the path", chain_path(f2, path, dpath, t0), -2, 1e-4)
    ok &= _check("matches the closed form",
                 chain_path(f2, path, dpath, 1.0), 2 * math.sin(1.0) * (math.cos(1.0) - 1), 1e-4)
    g = gradient(bowl, [1, 2])
    ok &= _check("gradient is perpendicular to the level tangent", is_perpendicular(g, [-g[1], g[0]]), True)
    print("ALL OK" if ok else "SOME FAILED")
