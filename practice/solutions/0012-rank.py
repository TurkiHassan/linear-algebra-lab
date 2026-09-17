"""0012 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def row_echelon(rows):
    m = [list(map(float, r)) for r in rows]
    nrows, ncols = len(m), len(m[0])
    r = 0
    for c in range(ncols):
        if r >= nrows:
            break
        best = max(range(r, nrows), key=lambda i: abs(m[i][c]))
        if abs(m[best][c]) < TOL:
            continue
        m[r], m[best] = m[best], m[r]
        pivot = m[r][c]
        m[r] = [v / pivot for v in m[r]]
        for i in range(nrows):
            if i != r and abs(m[i][c]) > TOL:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m


def rank(rows):
    return sum(1 for r in row_echelon(rows) if any(abs(v) > TOL for v in r))


def augment(a_rows, b):
    return [list(row) + [bi] for row, bi in zip(a_rows, b)]


def solution_case(a_rows, b):
    ra, rab, n = rank(a_rows), rank(augment(a_rows, b)), len(a_rows[0])
    if ra < rab:
        return "none"
    return "unique" if ra == n else "infinite"


def nullity(a_rows):
    return len(a_rows[0]) - rank(a_rows)


def _check(name, got, want):
    ok = got == want if not isinstance(want, float) else abs(got - want) < TOL
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    A = [[1, 2, 1], [-2, -3, 1], [3, 5, 0]]
    ok &= _check("rank", rank(A), 2)
    ok &= _check("identity", rank([[1, 0], [0, 1]]), 2)
    ok &= _check("zero", rank([[0, 0], [0, 0]]), 0)
    ok &= _check("nullity", nullity(A), 1)
    ok &= _check("unique", solution_case([[1, 0], [0, 1]], [2, 3]), "unique")
    ok &= _check("none", solution_case([[1, 1], [2, 2]], [1, 3]), "none")
    ok &= _check("infinite", solution_case([[1, 1], [2, 2]], [1, 2]), "infinite")
    print("ALL OK" if ok else "SOME FAILED")
