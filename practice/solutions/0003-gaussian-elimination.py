"""0003 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def row_scale(row, c):
    return [c * x for x in row]


def row_add(target, source, c):
    return [t + c * s for t, s in zip(target, source)]


def back_substitute(R):
    n = len(R)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (R[i][n] - sum(R[i][j] * x[j] for j in range(i + 1, n))) / R[i][i]
    return x


def _check(name, got, want):
    ok = all(abs(x - y) < TOL for x, y in zip(got, want))
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("scale", row_scale([2, 4, 6, 22], 0.5), [1, 2, 3, 11])
    ok &= _check("add", row_add([3, 8, 5, 27], [1, 2, 3, 11], -3), [0, 2, -4, -6])
    ok &= _check("solve", back_substitute([[1, 2, 3, 11], [0, 1, -2, -3], [0, 0, 1, 2]]), [3, 1, 2])
    print("ALL OK" if ok else "SOME FAILED")
