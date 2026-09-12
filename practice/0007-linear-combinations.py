"""0007 · linear combinations — practice (fill the gaps, then run the file).

Run:  python3 practice/0007-linear-combinations.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def lincomb(weights, vecs):
    """c1*v1 + c2*v2 + ... (same length)."""
    # TODO
    raise NotImplementedError


def weights_2d(v1, v2, w):
    """Solve w = c1*v1 + c2*v2 for 2D vectors. Return (c1, c2) or None if singular."""
    # TODO: Cramer on columns v1, v2; det = v1[0]*v2[1] - v1[1]*v2[0]
    raise NotImplementedError


def _check(name, got, want):
    if want is None or got is None:
        ok = got == want
    else:
        ok = all(abs(x - y) < TOL for x, y in zip(got, want))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("2(1,0)+3(0,1)", lincomb([2, 3], [[1, 0], [0, 1]]), [2, 3])
    ok &= _check("weights of (5,3)", weights_2d([2, 0], [1, 1], [5, 3]), [1, 3])
    ok &= _check("parallel -> None", weights_2d([1, 1], [2, 2], [5, 3]), None)
    print("ALL OK" if ok else "SOME FAILED")
