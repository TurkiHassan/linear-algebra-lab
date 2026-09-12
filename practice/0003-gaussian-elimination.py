"""0003 · gaussian elimination — practice (fill the gaps, then run the file).

Run:  python3 practice/0003-gaussian-elimination.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

TOL = 1e-9


def row_scale(row, c):
    """Multiply a row by nonzero constant c."""
    # TODO: return [c * x for x in row]
    raise NotImplementedError


def row_add(target, source, c):
    """Return target + c * source (new list)."""
    # TODO: entrywise
    raise NotImplementedError


def back_substitute(R):
    """Solve upper-triangular augmented 3x4 system R (rows of 4)."""
    # TODO: bottom-up, like lesson 0001
    raise NotImplementedError


def _check(name, got, want):
    if isinstance(want, list):
        ok = all(abs(x - y) < TOL for x, y in zip(got, want))
    else:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("R1/2", row_scale([2, 4, 6, 22], 0.5), [1, 2, 3, 11])
    ok &= _check("-3R1+R2", row_add([3, 8, 5, 27], [1, 2, 3, 11], -3), [0, 2, -4, -6])
    ok &= _check("solve lesson system", back_substitute([[1, 2, 3, 11], [0, 1, -2, -3], [0, 0, 1, 2]]), [3, 1, 2])
    print("ALL OK" if ok else "SOME FAILED")
