"""0029 · backpropagation and automatic differentiation — full solution.

The graph is the one from the lecture:
    a = x^2, b = exp(a), c = a + b, d = sqrt(c), e = cos(c), f = d + e

Run:  python3 practice/solutions/0029-backprop.py
Only standard library.
"""
import math

TOL = 1e-9


def forward_pass(x):
    """Values of every node, in topological order: a, b, c, d, e, f."""
    a = x * x
    b = math.exp(a)
    c = a + b
    d = math.sqrt(c)
    e = math.cos(c)
    f = d + e
    return {"x": x, "a": a, "b": b, "c": c, "d": d, "e": e, "f": f}


def local_derivatives(V):
    """Derivative of each elementary operation with respect to its own input."""
    return {
        "da_dx": 2 * V["x"],
        "db_da": math.exp(V["a"]),
        "dc_da": 1.0,
        "dc_db": 1.0,
        "dd_dc": 1 / (2 * math.sqrt(V["c"])),
        "de_dc": -math.sin(V["c"]),
        "df_dd": 1.0,
        "df_de": 1.0,
    }


def backward_pass(V):
    """Adjoints df/dnode, walked from the output back to the input.

    A node feeding two children contributes one term per path, and the terms add.
    """
    L = local_derivatives(V)
    adj = {"f": 1.0}
    adj["d"] = adj["f"] * L["df_dd"]
    adj["e"] = adj["f"] * L["df_de"]
    adj["c"] = adj["d"] * L["dd_dc"] + adj["e"] * L["de_dc"]
    adj["b"] = adj["c"] * L["dc_db"]
    adj["a"] = adj["b"] * L["db_da"] + adj["c"] * L["dc_da"]
    adj["x"] = adj["a"] * L["da_dx"]
    return adj


def numeric_derivative(x, h=1e-6):
    """Independent central difference on the whole function — the referee."""
    f = lambda t: forward_pass(t)["f"]
    return (f(x + h) - f(x - h)) / (2 * h)


def agrees(a, b, tol=1e-5):
    """True when the two routes to the same derivative land on the same number."""
    return abs(a - b) < tol


def chain_product(derivs):
    """Derivative of a chain of layers: multiply every local derivative."""
    out = 1.0
    for d in derivs:
        out *= d
    return out


def vjp(v, J):
    """Vector-Jacobian product: a row (1 x m) times J (m x n) gives a row (1 x n)."""
    n = len(J[0])
    return [sum(v[i] * J[i][j] for i in range(len(J))) for j in range(n)]


def cheaper_mode(n_in, n_out):
    """Which sweep costs fewer passes: 'reverse' when the output is the narrow end."""
    return "reverse" if n_out <= n_in else "forward"


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
    V = forward_pass(1.0)
    ok = True
    ok &= _check("forward a", V["a"], 1.0)
    ok &= _check("forward b", V["b"], 2.7182818285)
    ok &= _check("forward c", V["c"], 3.7182818285)
    ok &= _check("forward d", V["d"], 1.9282846855)
    ok &= _check("forward e", V["e"], -0.8382724736)
    ok &= _check("forward f", V["f"], 1.0900122120)
    L = local_derivatives(V)
    ok &= _check("local dd/dc", L["dd_dc"], 0.2592978121)
    ok &= _check("local de/dc", L["de_dc"], 0.5452515567)
    adj = backward_pass(V)
    ok &= _check("adjoint at c sums two paths", adj["c"], 0.8045493688)
    ok &= _check("adjoint at a sums two paths", adj["a"], 2.9915412980)
    ok &= _check("df/dx by backprop", adj["x"], 5.9830825959)
    ok &= _check("backprop matches the central difference",
                 agrees(adj["x"], numeric_derivative(1.0)), True)
    ok &= _check("chain_product", chain_product([2, 3, 0.5]), 3.0)
    ok &= _check("vjp keeps a row", vjp([1, 2], [[1, 0, 2], [0, 1, 3]]), [1, 2, 8])
    ok &= _check("reverse wins on a scalar loss", cheaper_mode(1000000, 1), "reverse")
    ok &= _check("forward wins on a narrow input", cheaper_mode(1, 500), "forward")
    print("ALL OK" if ok else "SOME FAILED")
