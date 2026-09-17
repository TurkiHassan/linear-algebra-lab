"""0012 · rank & solvability — practice (fill the gaps, then run the file).

Run:  python3 practice/0012-rank.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def row_echelon(rows):
    """Reduce a list of rows to row echelon form and return the new rows.

    Allowed moves only: swap rows, scale a row, add a multiple of one row
    to another.
    """
    # TODO: forward elimination, pivot by pivot.
    raise NotImplementedError


def rank(rows):
    """Number of nonzero rows after elimination = number of pivots."""
    # TODO: reduce first, then count rows that are not all (near) zero.
    raise NotImplementedError


def augment(a_rows, b):
    """Glue the constant vector b onto A as one extra column -> [A|b]."""
    # TODO
    raise NotImplementedError


def solution_case(a_rows, b):
    """Return "unique", "none" or "infinite" from the two ranks and n.

    rk(A) < rk(A|b)          -> "none"
    rk(A) == rk(A|b) == n    -> "unique"
    rk(A) == rk(A|b) < n     -> "infinite"
    """
    # TODO
    raise NotImplementedError


def nullity(a_rows):
    """dim of the solution space of Ax = 0 -> n - rank(A)."""
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, (int, float)) and not isinstance(want, bool):
        ok = abs(got - want) < TOL
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    A = [[1, 2, 1], [-2, -3, 1], [3, 5, 0]]          # lecture example, rk = 2
    ok &= _check("rank of lecture matrix", rank(A), 2)
    ok &= _check("rank of identity", rank([[1, 0], [0, 1]]), 2)
    ok &= _check("rank of zero matrix", rank([[0, 0], [0, 0]]), 0)
    ok &= _check("nullity 3 - 2", nullity(A), 1)
    ok &= _check("unique", solution_case([[1, 0], [0, 1]], [2, 3]), "unique")
    ok &= _check("none", solution_case([[1, 1], [2, 2]], [1, 3]), "none")
    ok &= _check("infinite", solution_case([[1, 1], [2, 2]], [1, 2]), "infinite")
    print("ALL OK" if ok else "SOME FAILED")
