"""0023 · diagonalization & the spectral theorem — practice.

Run:  python3 practice/0023-diagonalization.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def eigenvalues2(A):
    """Real roots of L^2 - tr(A)*L + det(A), ascending; None when complex."""
    # TODO
    raise NotImplementedError


def algebraic_multiplicity(A, lam):
    """How many times lam appears as a root — 0, 1 or 2."""
    # TODO
    raise NotImplementedError


def geometric_multiplicity2(A, lam):
    """dim ker(A - lam*I): 2 when A - lam*I is all zeros, 1 when it is singular, else 0."""
    # TODO
    raise NotImplementedError


def is_diagonalizable2(A):
    """True when the geometric multiplicities add up to 2."""
    # TODO
    raise NotImplementedError


def diagonalize2(A):
    """Return (P, D) with A = P D P^-1, or None when A is not diagonalizable."""
    # TODO: columns of P are eigenvectors, diagonal of D the matching eigenvalues.
    raise NotImplementedError


def matrix_power2(A, k):
    """A^k via P D^k P^-1 when possible, else by repeated multiplication."""
    # TODO
    raise NotImplementedError


def is_orthogonally_diagonalizable(A):
    """True exactly when A is symmetric — that is the spectral theorem."""
    # TODO
    raise NotImplementedError


def _flat(x):
    if isinstance(x, list):
        out = []
        for v in x:
            out.extend(_flat(v))
        return out
    return [x]


def _check(name, got, want):
    if isinstance(want, list):
        g, w = (_flat(got) if got is not None else None), _flat(want)
        ok = g is not None and len(g) == len(w) and all(abs(a - b) < 1e-6 for a, b in zip(g, w))
    elif isinstance(want, (int, float)) and not isinstance(want, bool):
        ok = got is not None and abs(got - want) < 1e-6
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    SYM = [[2, 1], [1, 2]]
    SHEAR = [[2, 1], [0, 2]]
    SCALED_I = [[3, 0], [0, 3]]
    ROT = [[0, -1], [1, 0]]
    ok = True
    ok &= _check("eigenvalues", eigenvalues2(SYM), [1, 3])
    ok &= _check("algebraic of shear", algebraic_multiplicity(SHEAR, 2), 2)
    ok &= _check("geometric of shear", geometric_multiplicity2(SHEAR, 2), 1)
    ok &= _check("geometric of 3I", geometric_multiplicity2(SCALED_I, 3), 2)
    ok &= _check("symmetric diagonalizes", is_diagonalizable2(SYM), True)
    ok &= _check("shear does not", is_diagonalizable2(SHEAR), False)
    ok &= _check("rotation does not", is_diagonalizable2(ROT), False)
    P, D = diagonalize2(SYM)
    ok &= _check("D is the spectrum", [D[0][0], D[1][1]], [1, 3])
    ok &= _check("A squared", matrix_power2(SYM, 2), [[5, 4], [4, 5]])
    ok &= _check("A to the 5", matrix_power2(SYM, 5), [[122, 121], [121, 122]])
    ok &= _check("orthogonally diagonalizable", is_orthogonally_diagonalizable(SYM), True)
    ok &= _check("not orthogonally", is_orthogonally_diagonalizable(SHEAR), False)
    print("ALL OK" if ok else "SOME FAILED")
