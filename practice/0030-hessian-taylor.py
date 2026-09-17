"""0030 · Hessian, linearization and the multivariate Taylor series — practice.

Run:  python3 practice/0030-hessian-taylor.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""
import math

TOL = 1e-9
H = 1e-4


def gradient(f, x, h=H):
    """All first partials, in order — the gradient as a row."""
    # TODO
    raise NotImplementedError


def hessian(f, x, h=H):
    """Every second partial, by central differences — the curvature matrix."""
    # TODO
    raise NotImplementedError


def is_symmetric(M, tol=1e-3):
    """True when the order of differentiation does not matter — it never should."""
    # TODO
    raise NotImplementedError


def eigenvalues2(M):
    """Both eigenvalues of a symmetric 2x2, descending — the curvature along each axis."""
    # TODO
    raise NotImplementedError


def classify(M, tol=1e-6):
    """'minimum', 'maximum', 'saddle' or 'flat' from the signs of the eigenvalues."""
    # TODO
    raise NotImplementedError


def linearize(f, x0, x):
    """First-order Taylor: f(x0) + grad f(x0) . (x - x0)."""
    # TODO
    raise NotImplementedError


def taylor2(f, x0, delta):
    """Second-order Taylor: add 0.5 * delta^T H delta to the linearization."""
    # TODO
    raise NotImplementedError


def newton_step(f, x0):
    """delta* = - H^-1 (grad f)^T for a two-variable f — the jump to the model's centre."""
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
    slide = lambda v: v[0] ** 2 * v[1] + v[0] * v[1] ** 3
    bowl = lambda v: v[0] ** 2 + v[1] ** 2
    dome = lambda v: -v[0] ** 2 - v[1] ** 2
    saddle = lambda v: v[0] ** 2 - v[1] ** 2
    x0 = [1.0, 1.0]
    ok = True
    ok &= _check("gradient at (1,1)", gradient(slide, x0), [3, 4], 1e-4)
    Hm = hessian(slide, x0)
    ok &= _check("Hessian at (1,1)", Hm, [[2, 5], [5, 6]], 1e-3)
    ok &= _check("Hessian is symmetric", is_symmetric(Hm), True)
    ok &= _check("eigenvalues of the bowl", eigenvalues2(hessian(bowl, x0)), [2, 2], 1e-3)
    ok &= _check("bowl is a minimum", classify(hessian(bowl, x0)), "minimum")
    ok &= _check("dome is a maximum", classify(hessian(dome, x0)), "maximum")
    ok &= _check("x^2 - y^2 is a saddle", classify(hessian(saddle, x0)), "saddle")
    ok &= _check("the slide point is a saddle too", classify(Hm), "saddle")
    ok &= _check("first order at delta = (0.1, 0.1)", linearize(slide, x0, [1.1, 1.1]), 2.7, 1e-3)
    ok &= _check("second order at delta = (0.1, 0.1)", taylor2(slide, x0, [0.1, 0.1]), 2.79, 1e-3)
    truth = slide([1.1, 1.1])
    ok &= _check("true value", truth, 2.7951)
    e1 = abs(truth - linearize(slide, x0, [1.1, 1.1]))
    e2 = abs(truth - taylor2(slide, x0, [0.1, 0.1]))
    ok &= _check("second order is far closer", e2 < e1 / 10, True)
    ok &= _check("Newton step", newton_step(slide, x0), [-2 / 13, -7 / 13], 1e-3)
    print("ALL OK" if ok else "SOME FAILED")
