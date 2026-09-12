"""0007 solution — kept separate from the exercise on purpose."""

TOL = 1e-9


def lincomb(weights, vecs):
    n = len(vecs[0])
    out = [0.0] * n
    for c, v in zip(weights, vecs):
        for i in range(n):
            out[i] += c * v[i]
    return out


def weights_2d(v1, v2, w):
    det = v1[0] * v2[1] - v1[1] * v2[0]
    if det == 0:
        return None
    c1 = (w[0] * v2[1] - w[1] * v2[0]) / det
    c2 = (v1[0] * w[1] - v1[1] * w[0]) / det
    return [c1, c2]


def _check(name, got, want):
    if want is None or got is None:
        ok = got == want
    else:
        ok = all(abs(x - y) < TOL for x, y in zip(got, want))
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    ok &= _check("lincomb", lincomb([2, 3], [[1, 0], [0, 1]]), [2, 3])
    ok &= _check("weights", weights_2d([2, 0], [1, 1], [5, 3]), [1, 3])
    ok &= _check("parallel", weights_2d([1, 1], [2, 2], [5, 3]), None)
    print("ALL OK" if ok else "SOME FAILED")
