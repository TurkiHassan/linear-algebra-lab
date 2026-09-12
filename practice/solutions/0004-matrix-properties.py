"""0004 solution — kept separate from the exercise on purpose."""


def is_zero_matrix(M):
    return all(x == 0 for row in M for x in row)


def neg_matrix(M):
    return [[-x for x in row] for row in M]


def mat_add(A, B):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]


def scalar_zero_deduce(c, A):
    cA = [[c * x for x in row] for row in A]
    if not is_zero_matrix(cA):
        return "no_trigger"
    return "c_zero" if c == 0 else "A_zero"


def _check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    O = [[0, 0], [0, 0]]
    A = [[1, 2], [3, 4]]
    ok = True
    ok &= _check("zero", is_zero_matrix(O), True)
    ok &= _check("nonzero", is_zero_matrix(A), False)
    ok &= _check("add-inv", mat_add(A, neg_matrix(A)), O)
    ok &= _check("c_zero", scalar_zero_deduce(0, A), "c_zero")
    ok &= _check("A_zero", scalar_zero_deduce(5, O), "A_zero")
    ok &= _check("no_trigger", scalar_zero_deduce(5, A), "no_trigger")
    print("ALL OK" if ok else "SOME FAILED")
