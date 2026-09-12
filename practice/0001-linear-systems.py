"""0001 · linear systems — practice (fill the gaps, then run the file).

Run:  python3 practice/0001-linear-systems.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only numpy + standard library.
"""

TOL = 1e-9


def is_linear_flags(power_ok, has_func_of_var, has_product_xy):
    """Return True iff the equation is linear.

    power_ok: every variable has power 1
    has_func_of_var: e.g. sin(x), sqrt(x), e**x attached to a variable
    has_product_xy: a term like x*z or x*y exists
    """
    # TODO: combine the three flags into the golden rule.
    raise NotImplementedError


def det_2x2(a, b, c, d):
    """Determinant of [[a, b], [c, d]] -> a*d - b*c."""
    # TODO: one line.
    raise NotImplementedError


def gauss_pivot_first_row(row):
    """Divide the first row [2, 4, 6, 22] by its pivot so the leader is 1."""
    # TODO: return [r / row[0] for r in row]
    raise NotImplementedError


def back_substitute_triangular(R):
    """Solve upper-triangular augmented 3x4 system R (rows of 4).

    Example solved in the lesson ends with z = 2.
    """
    # TODO: standard back substitution, bottom-up.
    raise NotImplementedError


def _check(name, got, want):
    ok = abs(got - want) < TOL if isinstance(want, float) else got == want
    print(("PASS " if ok else "FAIL ") + name + (" | got=" + str(got) if not ok else ""))
    return ok


if __name__ == "__main__":
    all_ok = True
    all_ok &= _check("linear: 3x+2y=7", is_linear_flags(True, False, False), True)
    all_ok &= _check("nonlinear: x+y^2=5", is_linear_flags(False, False, False), False)
    all_ok &= _check("nonlinear: 2y-sinx=6", is_linear_flags(True, True, False), False)
    all_ok &= _check("linear: sin(pi) is const", is_linear_flags(True, False, False), True)
    all_ok &= _check("det [[2,-3],[1,2]]=7", det_2x2(2, 1, -3, 2), 7)
    all_ok &= _check("det [[2,1],[4,2]]=0", det_2x2(2, 4, 1, 2), 0)
    all_ok &= _check("pivot row", gauss_pivot_first_row([2, 4, 6, 22]), [1, 2, 3, 11])
    sol = back_substitute_triangular([[1, 2, 3, 11], [0, 1, -2, -3], [0, 0, 11, 22]])
    all_ok &= _check("z = 2", sol[2], 2)
    print("ALL OK" if all_ok else "SOME FAILED")
