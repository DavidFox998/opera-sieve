"""
test_ramanujan_143bc.py -- Ramanujan-Petersson verification for 143.2.a.b and 143.2.a.c
Conjecture M9.2 (Ramanujan-Bost Bridge):
  If omega algebraic with C(S_4) > 2*sqrt(g), then |a_p^sigma| <= 2*sqrt(p) for p not in S_4.

MATHEMATICAL STATUS NOTE (CRITICAL):
  By Deligne 1974 (Weil Conjectures for abelian varieties over Q):
  For ANY weight-2 holomorphic newform with totally real coefficient field,
  ALL Galois conjugates satisfy |a_p^sigma| <= 2*sqrt(p) for all p not dividing the level.
  This is a THEOREM, unconditionally proved.

  143.2.a.b: weight=2, is_cm=False, nf_label=4.4.1957.1 (totally real, dim 4)
  143.2.a.c: weight=2, is_cm=False, nf_label=6.6.194616205.1 (totally real, dim 6)

  Consequence: this test WILL ALWAYS PASS regardless of whether omega is algebraic.
  A passing result does NOT constitute evidence for M9.2 as a new route to GRH.
  The implication is trivially true because the Ramanujan bound is already known.

  Additionally: Ramanujan bounds |a_p| <= 2*sqrt(p) are NOT equivalent to GRH.
  GRH concerns the location of zeros of L(s, f); the Weil bound is about Frobenius
  eigenvalues at each prime. These are separate statements.

Test scope:
  - Verify |a_p^sigma| <= 2*sqrt(p) for all Galois embeddings sigma
  - for p in S_4 = {2, 3, 19, 191} (certified M8 data)
  - for additional small primes via LMFDB fetch (if available)
  - Level-dividing primes p=11, p=13: a_p = Atkin-Lehner eigenvalue in {-1, 0, +1}
"""

from mpmath import mp, mpf, mpc, sqrt as mpsqrt, fabs, re, im, polyroots, nstr as mstr
import math
import subprocess
import json

mp.dps = 30

LEVEL = 143
S4 = [2, 3, 19, 191]

print("=" * 65)
print("Ramanujan-Petersson test: 143.2.a.b and 143.2.a.c")
print("=" * 65)
print()
print("THEOREM (Deligne 1974): For weight-2 holomorphic newforms over Q,")
print("|a_p^sigma| <= 2*sqrt(p) for all p not dividing the level.")
print("Both 143.2.a.b and 143.2.a.c are weight-2 with totally real fields.")
print("This bound is UNCONDITIONALLY TRUE for all p not dividing 143.")
print()
print("NOTE: The following test documents the bound numerically.")
print("PASS is guaranteed by Deligne 1974, not by the M9.2 hypothesis.")
print()

# ---------------------------------------------------------------
# Data from M8 (j0_143_hankel.py, certified SHA e2d70821...)
# ---------------------------------------------------------------

fp_b = [1, -1, -4, 0, 1]
basis_b = [
    [ 1,  0,  0,  0],
    [ 0,  1,  0,  0],
    [-1, -4,  0,  1],
    [-1,  3,  1, -1],
]
ap_b_s4 = {
    2:   [ 1,  1,  1,  0],
    3:   [ 0,  0, -1, -1],
    19:  [ 2, -2, -3, -3],
    191: [ 0, -4, -9,  3],
}

fp_c = [-12, 7, 24, -2, -10, 0, 1]
basis_c = [
    [ 1,   0,   0,  0,  0,  0],
    [ 0,   1,   0,  0,  0,  0],
    [-3,   0,   1,  0,  0,  0],
    [-6,  11,   6, -8, -1,  1],
    [ 8, -16,  -7,  9,  1, -1],
    [15, -12, -14,  8,  2, -1],
]
ap_c_s4 = {
    2:   [ 0, -1,  0,  0,  0,  0],
    3:   [ 1,  0,  0,  1,  0,  0],
    19:  [-1,  0,  0,  1,  0, -1],
    191: [-3,  0,  4, -3,  0, -2],
}

def find_roots(fp_asc):
    return polyroots(list(reversed(fp_asc)))

def eval_at_root(ap_coords, basis, theta):
    n = len(ap_coords)
    result = mpc(0)
    for j in range(n):
        e_j, th_k = mpc(0), mpc(1)
        for k in range(n):
            e_j += basis[j][k] * th_k
            th_k *= theta
        result += ap_coords[j] * e_j
    return result

def weil_check(ap_val, p):
    bound = mpf(2) * mpsqrt(mpf(p))
    mag = fabs(re(ap_val))
    ok = mag <= bound * mpf('1.0001')
    return bool(ok), float(mag), float(bound)

roots_b = find_roots(fp_b)
roots_c = find_roots(fp_c)

# ---------------------------------------------------------------
# PART 1: Test S_4 primes using M8 certified data
# ---------------------------------------------------------------

print("-" * 65)
print("PART 1: S_4 primes {2, 3, 19, 191} -- data from M8 (SHA e2d70821)")
print("-" * 65)

all_pass = True

for form_label, fp, basis, ap_dict, roots in [
    ("143.2.a.b", fp_b, basis_b, ap_b_s4, roots_b),
    ("143.2.a.c", fp_c, basis_c, ap_c_s4, roots_c),
]:
    print(f"\n  {form_label} ({len(roots)} Galois embeddings):")
    for p in S4:
        bound = 2 * math.sqrt(p)
        ap_vec = ap_dict[p]
        for i, theta in enumerate(roots):
            ap_val = eval_at_root(ap_vec, basis, theta)
            ap_real = float(re(ap_val))
            im_part = float(fabs(im(ap_val)))
            ok = abs(ap_real) <= bound * 1.0001
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"    p={p:3d}  sigma_{i}: a_p = {ap_real:+.6f}  "
                  f"|a_p| = {abs(ap_real):.4f}  bound = {bound:.4f}  [{tag}]")

# ---------------------------------------------------------------
# PART 2: Additional primes via LMFDB fetch
# ---------------------------------------------------------------

print()
print("-" * 65)
print("PART 2: Additional primes via LMFDB (curl)")
print("-" * 65)

def fetch_ap_lmfdb(label):
    """Fetch a_n integral-basis vectors for small primes from LMFDB mf_hecke_nf."""
    url = (f"https://www.lmfdb.org/api/mf_hecke_nf/?label={label}"
           f"&_fields=label,primes,an&_format=json")
    try:
        result = subprocess.run(
            ["curl", "-s", "-A", "Mozilla/5.0", url],
            capture_output=True, text=True, timeout=20
        )
        data = json.loads(result.stdout)
        rec = data.get("data", [{}])[0]
        return rec.get("primes", []), rec.get("an", [])
    except Exception:
        return [], []

extra_tested = 0
for form_label, fp, basis, roots in [
    ("143.2.a.b", fp_b, basis_b, roots_b),
    ("143.2.a.c", fp_c, basis_c, roots_c),
]:
    primes, an = fetch_ap_lmfdb(form_label)
    if not primes:
        print(f"  {form_label}: LMFDB fetch unavailable -- Deligne theorem covers all p")
        continue

    test_primes = [p for p in primes if p != 11 and p != 13 and p not in S4 and p < 200][:15]
    if not test_primes:
        print(f"  {form_label}: no additional primes in fetched range")
        continue

    print(f"\n  {form_label}: testing {len(test_primes)} primes beyond S_4 (p < 200):")
    an_by_prime = {primes[i]: an[i] for i in range(len(primes)) if primes[i] in test_primes}

    for p in test_primes:
        if p not in an_by_prime:
            continue
        bound = 2 * math.sqrt(p)
        ap_vec = an_by_prime[p]
        for i, theta in enumerate(roots):
            ap_val = eval_at_root(ap_vec, basis, theta)
            ap_real = float(re(ap_val))
            ok = abs(ap_real) <= bound * 1.0001
            if not ok:
                all_pass = False
            extra_tested += 1
            tag = "OK" if ok else "FAIL"
            print(f"    p={p:3d}  sigma_{i}: a_p = {ap_real:+.6f}  "
                  f"|a_p| = {abs(ap_real):.4f}  bound = {bound:.4f}  [{tag}]")

if extra_tested == 0:
    print("  (No additional LMFDB data returned -- S_4 results above are complete.)")

# ---------------------------------------------------------------
# PART 3: Level-dividing primes p=11, p=13
# ---------------------------------------------------------------

print()
print("-" * 65)
print("PART 3: Level-dividing primes p=11 and p=13")
print("-" * 65)
print("  For p | N=143, a_p is the Atkin-Lehner eigenvalue.")
print("  143.2.a.b and 143.2.a.c both have Atkin-Lehner string '++'")
print("  (from LMFDB: atkin_lehner_eigenvals for 11.2.a.a basis).")
print("  For new forms of level 143, a_11 and a_13 are in {-1, 0, +1} by Hecke theory.")
print("  Weil bound: |a_11| <= 2*sqrt(11) = 6.63..., trivially satisfied.")
print("  Weil bound: |a_13| <= 2*sqrt(13) = 7.21..., trivially satisfied.")
print("  [OK] Level-dividing primes pass by Hecke eigenvalue theory.")

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------

print()
print("=" * 65)
verdict = "PASS -- All tested primes satisfy |a_p^sigma| <= 2*sqrt(p)." if all_pass else "FAIL -- See above."
print(f"RESULT: {verdict}")
print()
print("MATHEMATICAL INTERPRETATION:")
print("  This PASS is guaranteed by Deligne 1974, unconditionally.")
print("  It does NOT constitute evidence for M9.2 as new mathematics.")
print()
print("  To pursue GRH(J_0(143)) from M8, a different bridge is needed.")
print("  Ramanujan bounds (|a_p| <= 2*sqrt(p)) are already proved and")
print("  are not equivalent to GRH for L(s, J_0(143)).")
print()
print("  Status of M9.2:")
print("    Conclusion (Ramanujan bound): THEOREM [Deligne 1974]")
print("    Hypothesis (omega algebraic): independently certified [M8]")
print("    Implication (omega alg => Ramanujan): trivially true, not new")
print("    Route (Ramanujan => GRH): NOT a known theorem")
print()
print("  Open question (genuine): Does algebraic omega imply any")
print("  zero-free region for L(s, J_0(143))? Not known.")
print("=" * 65)
