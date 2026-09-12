"""0006 · subspaces — practice (fill the gaps, then run the file).

Run:  python3 practice/0006-subspaces.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""


def on_line_through_origin(p):
    """Line y = x: True iff p[1] == p[0]."""
    # TODO
    raise NotImplementedError


def on_offset_line(p):
    """Line y = x + 1: True iff p[1] == p[0] + 1."""
    # TODO
    raise NotImplementedError


def closed_under_add(pred, pts):
    """True iff pred(a+b) holds for every pair in pts."""
    # TODO
    raise NotImplementedError


def closed_under_scale(pred, pts, scalars):
    """True iff pred(k*p) holds for every p in pts and k in scalars."""
    # TODO
    raise NotImplementedError


def is_subspace(pred, pts, scalars):
    """Three-condition test: zero in set, closed under add and scale."""
    # TODO: pred([0, 0]) and closed_under_add(...) and closed_under_scale(...)
    raise NotImplementedError


def _check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    pts = [[0, 0], [1, 1], [2, 2], [-1, -1]]
    sc = [-1, 0, 2]
    ok = True
    ok &= _check("line0 is subspace", is_subspace(on_line_through_origin, pts, sc), True)
    ok &= _check("offset not subspace", is_subspace(on_offset_line, [[0, 1], [1, 2]], sc), False)
    ok &= _check("zero missing -> False", on_offset_line([0, 0]), False)
    print("ALL OK" if ok else "SOME FAILED")
