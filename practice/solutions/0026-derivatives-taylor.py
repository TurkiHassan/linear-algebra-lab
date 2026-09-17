"""0026 · derivatives and Taylor series — full solution.

Run:  python3 practice/solutions/0026-derivatives-taylor.py
Only standard library.
"""
import math

TOL = 1e-9


def difference_quotient(f, x, h):
    """Average slope of f between x and x + h."""
    return (f(x + h) - f(x)) / h


def derivative(f, x, h=1e-6):
    """Numeric derivative by the central difference — far more accurate than one-sided."""
    return (f(x + h) - f(x - h)) / (2 * h)


def poly_eval(c, x):
    """Evaluate a polynomial given as [a0, a1, a2, ...] at x."""
    total = 0.0
    for k, a in enumerate(c):
        total += a * x ** k
    return total


def poly_derivative(c):
    """Coefficients of the derivative: a_k x^k  ->  k a_k x^(k-1)."""
    return [k * a for k, a in enumerate(c)][1:]


def factorial(n):
    """n! — the denominator of every Taylor coefficient."""
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def taylor_coeffs(derivs, x0):
    """Taylor coefficients from [f(x0), f'(x0), f''(x0), ...] — the x0 only labels the centre."""
    return [d / factorial(k) for k, d in enumerate(derivs)]


def taylor_eval(derivs, x0, x):
    """Value of the Taylor polynomial built from derivs, centred at x0, evaluated at x."""
    total = 0.0
    for k, a in enumerate(taylor_coeffs(derivs, x0)):
        total += a * (x - x0) ** k
    return total


def product_rule(fx, dfx, gx, dgx):
    """(f g)' = f' g + f g'."""
    return dfx * gx + fx * dgx


def quotient_rule(fx, dfx, gx, dgx):
    """(f / g)' = (f' g - f g') / g^2."""
    return (dfx * gx - fx * dgx) / (gx * gx)


def chain_rule(dg_at_fx, df_at_x):
    """(g(f(x)))' = g'(f(x)) f'(x)."""
    return dg_at_fx * df_at_x


def _flat(x):
    if isinstance(x, list):
        out = []
        for v in x:
            out.extend(_flat(v))
        return out
    return [x]


def _check(name, got, want, tol=1e-6):
    if isinstance(want, list):
        g, w = (_flat(got) if got is not None else None), _flat(want)
        ok = g is not None and len(g) == len(w) and all(abs(a - b) < tol for a, b in zip(g, w))
    elif isinstance(want, (int, float)) and not isinstance(want, bool):
        ok = got is not None and abs(got - want) < tol
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    sq = lambda t: t * t
    ok = True
    ok &= _check("difference quotient is 4 + h", difference_quotient(sq, 2, 0.1), 4.1)
    ok &= _check("smaller h, closer to 4", difference_quotient(sq, 2, 0.001), 4.001)
    ok &= _check("derivative of x^2 at 2", derivative(sq, 2), 4, 1e-5)
    ok &= _check("poly_eval", poly_eval([1, 0, 2], 3), 19)
    ok &= _check("poly_derivative", poly_derivative([1, 0, 2]), [0, 4])
    ok &= _check("factorial", [factorial(0), factorial(3), factorial(5)], [1, 6, 120])
    ok &= _check("taylor_coeffs of exp", taylor_coeffs([1, 1, 1, 1], 0), [1, 1, 0.5, 1 / 6])
    ok &= _check("T3 of exp at 0.5", taylor_eval([1, 1, 1, 1], 0, 0.5), 1.6458333333)
    ok &= _check("error is one term wide", abs(math.exp(0.5) - taylor_eval([1, 1, 1, 1], 0, 0.5)), 0.0028879, 1e-5)
    ok &= _check("product rule", product_rule(4, 4, math.exp(2), math.exp(2)), 8 * math.exp(2))
    ok &= _check("quotient rule", quotient_rule(4, 4, 2, 1), (4 * 2 - 4 * 1) / 4)
    ok &= _check("chain rule on sqrt(x^2+1)", chain_rule(1 / (2 * math.sqrt(5)), 4), 2 / math.sqrt(5))
    ok &= _check("chain rule matches numeric", chain_rule(1 / (2 * math.sqrt(5)), 4),
                 derivative(lambda t: math.sqrt(t * t + 1), 2), 1e-5)
    print("ALL OK" if ok else "SOME FAILED")
