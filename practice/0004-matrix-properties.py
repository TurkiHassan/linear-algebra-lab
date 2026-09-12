"""0004 · matrix properties — practice (fill the gaps, then run the file).

Run:  python3 practice/0004-matrix-properties.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""


def is_zero_matrix(M):
    """True iff every entry is 0."""
    # TODO
    raise NotImplementedError


def neg_matrix(M):
    """Return -M (additive inverse)."""
    # TODO
    raise NotImplementedError


def mat_add(A, B):
    """Entrywise addition (same shape)."""
    # TODO
    raise NotImplementedError


def scalar_zero_deduce(c, A):
    """Apply the cA = O rule. Return 'c_zero' | 'A_zero' | 'no_trigger'.

    Compute cA first: if it is not zero -> 'no_trigger'.
    If cA is zero and c == 0 -> 'c_zero'; elif cA zero and c != 0 -> 'A_zero'.
    """
    # TODO
    raise NotImplementedError


def _check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    O = [[0, 0], [0, 0]]
    A = [[1, 2], [3, 4]]
    ok = True
    ok &= _check("zero detected", is_zero_matrix(O), True)
    ok &= _check("nonzero rejected", is_zero_matrix(A), False)
    ok &= _check("A + (-A) = O", mat_add(A, neg_matrix(A)), O)
    ok &= _check("c=0 explains", scalar_zero_deduce(0, A), "c_zero")
    ok &= _check("c=5 forces A=0", scalar_zero_deduce(5, O), "A_zero")
    ok &= _check("cA != 0", scalar_zero_deduce(5, A), "no_trigger")
    print("ALL OK" if ok else "SOME FAILED")
