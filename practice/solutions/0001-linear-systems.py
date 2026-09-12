"""0001 solution — kept separate from the exercise on purpose."""
TOL = 1e-9


def is_linear_flags(power_ok, has_func_of_var, has_product_xy):
    return bool(power_ok and (not has_func_of_var) and (not has_product_xy))


def det_2x2(a, b, c, d):
    return a * d - b * c


def gauss_pivot_first_row(row):
    p = row[0]
    return [r / p for r in row]


def back_substitute_triangular(R):
    n = len(R)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = R[i][n] - sum(R[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / R[i][i]
    return x


def _check(name, got, want):
    ok = abs(got - want) < TOL if isinstance(want, float) else got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("linear", is_linear_flags(True, False, False), True)
    ok &= _check("nonlinear pow", is_linear_flags(False, False, False), False)
    ok &= _check("nonlinear func", is_linear_flags(True, True, False), False)
    ok &= _check("nonlinear prod", is_linear_flags(True, False, True), False)
    ok &= _check("det7", det_2x2(2, 1, -3, 2), 7)
    ok &= _check("det0", det_2x2(2, 4, 1, 2), 0)
    ok &= _check("pivot", gauss_pivot_first_row([2, 4, 6, 22]), [1, 2, 3, 11])
    ok &= _check("z", back_substitute_triangular([[1, 2, 3, 11], [0, 1, -2, -3], [0, 0, 11, 22]])[2], 2)
    print("ALL OK" if ok else "SOME FAILED")
