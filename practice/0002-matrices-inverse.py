"""0002 · matrices & inverse — practice (fill the gaps, then run the file).

Run:  python3 practice/0002-matrices-inverse.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def mat_shape(M):
    """Return (rows, cols) of matrix M (list of lists)."""
    # TODO: rows = len(M), cols = len(M[0])
    raise NotImplementedError


def mat_add(A, B):
    """Add two same-shape matrices."""
    # TODO: entrywise addition; assume shapes match
    raise NotImplementedError


def mat_mul(A, B):
    """Multiply (m×n) by (n×p). Raise ValueError if inner dims differ."""
    # TODO: triple loop; check len(A[0]) == len(B)
    raise NotImplementedError


def inv_2x2(a, b, c, d):
    """Inverse of [[a, b], [c, d]]. Return None if singular (det == 0)."""
    # TODO: det = a*d - b*c; if 0 -> None; else [[d,-c],[-b,a]] / det
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, float):
        ok = abs(got - want) < TOL
    elif isinstance(want, list):
        ok = all(abs(x - y) < TOL for r1, r2 in zip(got, want) for x, y in zip(r1, r2))
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("shape 2x3", mat_shape([[1, 2, 3], [4, 5, 6]]), (2, 3))
    ok &= _check("add", mat_add([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[6, 8], [10, 12]])
    ok &= _check("mul 2x3*3x2", mat_mul([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]]), [[58, 64], [139, 154]])
    ok &= _check("inv [[2,-3],[1,2]]", inv_2x2(2, 1, -3, 2), [[2 / 7, 3 / 7], [-1 / 7, 2 / 7]])
    ok &= _check("singular -> None", inv_2x2(2, 4, 1, 2), None)
    try:
        mat_mul([[1, 2]], [[1, 2]])
        print("FAIL inner-dim check"); ok = False
    except ValueError:
        print("PASS inner-dim check")
    print("ALL OK" if ok else "SOME FAILED")
