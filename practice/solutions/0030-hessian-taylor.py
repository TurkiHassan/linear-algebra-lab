"""0030 · Hessian, linearization and the multivariate Taylor series — full solution.

Run:  python3 practice/solutions/0030-hessian-taylor.py
Only standard library.
"""
import math

TOL = 1e-9
H = 1e-4


def gradient(f, x, h=H):
    """All first partials, in order — the gradient as a row."""
    out = []
    for i in range(len(x)):
        up, down = list(x), list(x)
        up[i] += h
        down[i] -= h
        out.append((f(up) - f(down)) / (2 * h))
    return out


def hessian(f, x, h=H):
    """Every second partial, by central differences — the curvature matrix."""
    n = len(x)
    Hm = [[0.0] * n for _ in range(n)]
    f0 = f(x)
    for i in range(n):
        for j in range(n):
            if i == j:
                up, down = list(x), list(x)
                up[i] += h
                down[i] -= h
                Hm[i][j] = (f(up) - 2 * f0 + f(down)) / (h * h)
            else:
                pp, pm, mp, mm = list(x), list(x), list(x), list(x)
                pp[i] += h; pp[j] += h
                pm[i] += h; pm[j] -= h
                mp[i] -= h; mp[j] += h
                mm[i] -= h; mm[j] -= h
                Hm[i][j] = (f(pp) - f(pm) - f(mp) + f(mm)) / (4 * h * h)
    return Hm


def is_symmetric(M, tol=1e-3):
    """True when the order of differentiation does not matter — it never should."""
    n = len(M)
    return all(abs(M[i][j] - M[j][i]) < tol for i in range(n) for j in range(n))


def eigenvalues2(M):
    """Both eigenvalues of a symmetric 2x2, descending — the curvature along each axis."""
    t = M[0][0] + M[1][1]
    d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    disc = t * t - 4 * d
    if disc < 0:
        return None
    s = math.sqrt(disc)
    return [(t + s) / 2, (t - s) / 2]


def classify(M, tol=1e-6):
    """'minimum', 'maximum', 'saddle' or 'flat' from the signs of the eigenvalues."""
    ev = eigenvalues2(M)
    if ev is None:
        return "unknown"
    if all(v > tol for v in ev):
        return "minimum"
    if all(v < -tol for v in ev):
        return "maximum"
    if any(abs(v) <= tol for v in ev):
        return "flat"
    return "saddle"


def linearize(f, x0, x):
    """First-order Taylor: f(x0) + grad f(x0) . (x - x0)."""
    g = gradient(f, x0)
    delta = [a - b for a, b in zip(x, x0)]
    return f(x0) + sum(a * b for a, b in zip(g, delta))


def taylor2(f, x0, delta):
    """Second-order Taylor: add 0.5 * delta^T H delta to the linearization."""
    g = gradient(f, x0)
    Hm = hessian(f, x0)
    x = [a + b for a, b in zip(x0, delta)]
    quad = 0.0
    for i in range(len(delta)):
        for j in range(len(delta)):
            quad += delta[i] * Hm[i][j] * delta[j]
    return linearize(f, x0, x) + 0.5 * quad


def newton_step(f, x0):
    """delta* = - H^-1 (grad f)^T for a two-variable f — the jump to the model's centre."""
    g = gradient(f, x0)
    Hm = hessian(f, x0)
    det = Hm[0][0] * Hm[1][1] - Hm[0][1] * Hm[1][0]
    if abs(det) < TOL:
        return None
    inv = [[Hm[1][1] / det, -Hm[0][1] / det], [-Hm[1][0] / det, Hm[0][0] / det]]
    return [-(inv[0][0] * g[0] + inv[0][1] * g[1]), -(inv[1][0] * g[0] + inv[1][1] * g[1])]


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
