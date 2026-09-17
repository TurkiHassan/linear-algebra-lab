"""0018 · orthonormal basis, Gram-Schmidt & orthogonal complement — practice.

Run:  python3 practice/0018-gram-schmidt.py
Full solution lives in practice/solutions/ (kept separate on purpose).
Only standard library.
"""

import math

TOL = 1e-9


def dot(x, y):
    """Plain dot product."""
    # TODO
    raise NotImplementedError


def normalize(x):
    """Divide a vector by its length; return None for the zero vector."""
    # TODO
    raise NotImplementedError


def project_onto(v, u):
    """The component of v along u: (<v,u> / <u,u>) * u."""
    # TODO
    raise NotImplementedError


def gram_schmidt(vectors):
    """Return an ORTHOGONAL family; drop any vector that collapses to zero.

    u1 = b1, and every later uk is bk minus its projections on all previous u.
    """
    # TODO
    raise NotImplementedError


def orthonormalize(vectors):
    """Gram-Schmidt followed by normalisation."""
    # TODO
    raise NotImplementedError


def coords_in_orthonormal(x, basis):
    """In an orthonormal basis the coordinates are just inner products."""
    # TODO
    raise NotImplementedError


def normal_vector(u1, u2):
    """A basis of U^perp when U = span{u1, u2} in R^3 — the cross product."""
    # TODO
    raise NotImplementedError


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
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | got=" + str(got)))
    return ok


if __name__ == "__main__":
    ok = True
    b1, b2 = [1, 1, 0], [1, 0, 1]
    gs = gram_schmidt([b1, b2])
    ok &= _check("gram-schmidt", gs, [[1, 1, 0], [0.5, -0.5, 1]])
    ok &= _check("result is orthogonal", abs(dot(gs[0], gs[1])) < TOL, True)
    on = orthonormalize([b1, b2])
    ok &= _check("unit length", math.sqrt(dot(on[0], on[0])), 1.0)
    ok &= _check("dependent input collapses", len(gram_schmidt([[1, 1, 0], [2, 2, 0]])), 1)
    ok &= _check("coords in standard basis", coords_in_orthonormal([3, 4], [[1, 0], [0, 1]]), [3, 4])
    ok &= _check("normal of the plane", normal_vector([1, 1, 0], [0, 1, 1]), [1, -1, 1])
    print("ALL OK" if ok else "SOME FAILED")
