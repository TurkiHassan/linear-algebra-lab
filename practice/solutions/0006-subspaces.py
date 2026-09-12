"""0006 solution — kept separate from the exercise on purpose."""


def on_line_through_origin(p):
    return p[1] == p[0]


def on_offset_line(p):
    return p[1] == p[0] + 1


def closed_under_add(pred, pts):
    return all(pred([a[0] + b[0], a[1] + b[1]]) for a in pts for b in pts)


def closed_under_scale(pred, pts, scalars):
    return all(pred([k * p[0], k * p[1]]) for p in pts for k in scalars)


def is_subspace(pred, pts, scalars):
    return bool(pred([0, 0]) and closed_under_add(pred, pts) and closed_under_scale(pred, pts, scalars))


def _check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    pts = [[0, 0], [1, 1], [2, 2], [-1, -1]]
    sc = [-1, 0, 2]
    ok = True
    ok &= _check("line0", is_subspace(on_line_through_origin, pts, sc), True)
    ok &= _check("offset", is_subspace(on_offset_line, [[0, 1], [1, 2]], sc), False)
    ok &= _check("zero-missing", on_offset_line([0, 0]), False)
    print("ALL OK" if ok else "SOME FAILED")
