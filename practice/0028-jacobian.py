"""0028 · Jacobians and vector-valued gradients — practice.

Run:  python3 practice/0028-jacobian.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def matvec(A, x):
    """Multiply a matrix by a vector — one inner product per row."""
    # TODO
    raise NotImplementedError


def jacobian(f, x, m, h=1e-6):
    """Numeric Jacobian of f: R^n -> R^m at x — one column per input variable."""
    # TODO
    raise NotImplementedError


def jacobian_shape(J):
    """(rows, cols) = (m, n) — outputs by inputs."""
    # TODO
    raise NotImplementedError


def linear_jacobian(A):
    """For f(x) = A x the Jacobian is A itself, at every x."""
    # TODO
    raise NotImplementedError


def residual(Phi, y, theta):
    """e = y - Phi theta."""
    # TODO
    raise NotImplementedError


def least_squares_loss(Phi, y, theta):
    """L = ||e||^2 = e^T e."""
    # TODO
    raise NotImplementedError


def loss_gradient(Phi, y, theta):
    """dL/dtheta = 2 e^T (-Phi) = -2 e^T Phi — a row vector in R^(1 x D)."""
    # TODO
    raise NotImplementedError


def descent_step(Phi, y, theta, eta):
    """One gradient descent update on the parameters."""
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
    A = [[2, 1], [0, 3]]
    Phi = [[1], [2], [3]]
    y = [2, 4, 7]
    ok = True
    ok &= _check("matvec", matvec(A, [1, 2]), [4, 6])
    J = jacobian(lambda v: matvec(A, v), [0.7, -0.4], 2)
    ok &= _check("numeric Jacobian equals A", J, A, 1e-4)
    ok &= _check("same J at a different point", jacobian(lambda v: matvec(A, v), [5, 9], 2), A, 1e-4)
    ok &= _check("jacobian_shape", jacobian_shape(J), (2, 2))
    ok &= _check("linear_jacobian", linear_jacobian(A), A)
    Jc = jacobian(lambda v: [v[0] * v[0] * v[1], v[0] + v[1] ** 3], [1, 2], 2)
    ok &= _check("nonlinear Jacobian at (1,2)", Jc, [[4, 1], [1, 12]], 1e-4)
    ok &= _check("residual at theta = 1", residual(Phi, y, [1]), [1, 2, 4])
    ok &= _check("loss at theta = 1", least_squares_loss(Phi, y, [1]), 21)
    ok &= _check("gradient at theta = 1", loss_gradient(Phi, y, [1]), [-34])
    ok &= _check("one descent step", descent_step(Phi, y, [1], 0.01), [1.34])
    ok &= _check("the step lowered the loss",
                 least_squares_loss(Phi, y, descent_step(Phi, y, [1], 0.01)) < 21, True)
    opt = [31 / 14]
    ok &= _check("gradient vanishes at the optimum", loss_gradient(Phi, y, opt), [0], 1e-9)
    print("ALL OK" if ok else "SOME FAILED")
