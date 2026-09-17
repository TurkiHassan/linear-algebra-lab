"""0025 · low-rank approximation — practice.

Run:  python3 practice/0025-low-rank.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def outer(u, v):
    """u v^T — a matrix of rank 1 whenever u and v are nonzero."""
    # TODO
    raise NotImplementedError


def rank_of(A):
    """Rank of a 2x2 matrix: 0, 1 or 2."""
    # TODO: all zeros -> 0. det != 0 -> 2. Otherwise 1.
    raise NotImplementedError


def mat_sub(A, B):
    """A - B, entry by entry."""
    # TODO
    raise NotImplementedError


def spectral_norm2(A):
    """Largest singular value of a 2x2 matrix.

    It is sqrt of the largest eigenvalue of A^T A.
    """
    # TODO
    raise NotImplementedError


def truncate2(A, k):
    """The rank-k approximation: keep the first k layers sigma_i u_i v_i^T.

    k = 0 gives the zero matrix; k >= 2 gives A back.
    """
    # TODO
    raise NotImplementedError


def approx_error(A, k):
    """The spectral norm of what truncation threw away."""
    # TODO
    raise NotImplementedError


def eckart_young_holds(A, k):
    """True when approx_error(A, k) equals sigma_(k+1)."""
    # TODO
    raise NotImplementedError


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
    A = [[3, 0], [4, 5]]
    ok = True
    ok &= _check("outer", outer([1, 3], [1, 1]), [[1, 1], [3, 3]])
    ok &= _check("outer has rank 1", rank_of(outer([1, 3], [1, 1])), 1)
    ok &= _check("A has rank 2", rank_of(A), 2)
    ok &= _check("zero has rank 0", rank_of([[0, 0], [0, 0]]), 0)
    ok &= _check("subtract", mat_sub(A, [[1, 1], [1, 1]]), [[2, -1], [3, 4]])
    ok &= _check("spectral norm", spectral_norm2(A), 45 ** 0.5)
    ok &= _check("rank-1 approximation", truncate2(A, 1), [[1.5, 1.5], [4.5, 4.5]])
    ok &= _check("its rank really is 1", rank_of(truncate2(A, 1)), 1)
    ok &= _check("full rank gives A back", truncate2(A, 2), A)
    ok &= _check("error equals sigma2", approx_error(A, 1), 5 ** 0.5)
    ok &= _check("eckart-young at k=1", eckart_young_holds(A, 1), True)
    ok &= _check("eckart-young at k=0", eckart_young_holds(A, 0), True)
    print("ALL OK" if ok else "SOME FAILED")
