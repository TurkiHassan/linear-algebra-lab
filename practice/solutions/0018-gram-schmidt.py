"""0018 solution — kept separate from the exercise on purpose."""

import math

TOL = 1e-9


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def normalize(x):
    n = math.sqrt(dot(x, x))
    if n < TOL:
        return None
    return [v / n for v in x]


def project_onto(v, u):
    f = dot(v, u) / dot(u, u)
    return [f * ui for ui in u]


def gram_schmidt(vectors):
    out = []
    for b in vectors:
        u = list(b)
        for prev in out:
            p = project_onto(b, prev)
            u = [a - c for a, c in zip(u, p)]
        if math.sqrt(dot(u, u)) > TOL:
            out.append(u)
    return out


def orthonormalize(vectors):
    return [normalize(u) for u in gram_schmidt(vectors)]


def coords_in_orthonormal(x, basis):
    return [dot(x, b) for b in basis]


def normal_vector(u1, u2):
    return [u1[1] * u2[2] - u1[2] * u2[1],
            u1[2] * u2[0] - u1[0] * u2[2],
            u1[0] * u2[1] - u1[1] * u2[0]]


def _close(p, q):
    return all(abs(a - b) < 1e-6 for a, b in zip(p, q))


def _check(name, got, want):
    if isinstance(want, bool):
        ok = got == want
    elif isinstance(want, list) and want and isinstance(want[0], list):
        ok = len(got) == len(want) and all(_close(a, b) for a, b in zip(got, want))
    elif isinstance(want, list):
        ok = _close(got, want)
    else:
        ok = abs(got - want) < 1e-6
    print(("PASS " if ok else "FAIL ") + name)
    return ok


if __name__ == "__main__":
    ok = True
    gs = gram_schmidt([[1, 1, 0], [1, 0, 1]])
    ok &= _check("gram-schmidt", gs, [[1, 1, 0], [0.5, -0.5, 1]])
    ok &= _check("orthogonal", abs(dot(gs[0], gs[1])) < TOL, True)
    ok &= _check("unit", math.sqrt(dot(orthonormalize([[1, 1, 0], [1, 0, 1]])[0],
                                       orthonormalize([[1, 1, 0], [1, 0, 1]])[0])), 1.0)
    ok &= _check("dependent", len(gram_schmidt([[1, 1, 0], [2, 2, 0]])), 1)
    ok &= _check("coords", coords_in_orthonormal([3, 4], [[1, 0], [0, 1]]), [3, 4])
    ok &= _check("normal", normal_vector([1, 1, 0], [0, 1, 1]), [1, -1, 1])
    print("ALL OK" if ok else "SOME FAILED")
