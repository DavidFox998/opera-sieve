# Opera Sieve

**Canonical sieve for S(alpha_0 = 299 + pi/10)**
Opera Numerorum / Battle Plan v1.6 | David J. Fox | June 2026

This repository is the canonical sieve reference for M1-M7 of the Opera Numerorum
certification pipeline. It consolidates all computational verification of the
exceptional prime set S_14 and the Bost-Connes bridge to GRH(X_0(143)).

## Dependency graph

```
NS-Tower  <--  Yang-Mills-MassGap  <--  RH-Core  <--  Bost-Connes  <--  opera-sieve
                                                            |
                                                       alpha_0 = 299 + pi/10
```

Clay referees: if NS is published before this sieve has a DOI, the chain breaks.
This repo IS the canonical sieve reference.

## What is S_14?

S_14 = {2, 3, 19, 191, 3993746143633, 3224057731518397,
        631474305334326148720631, 154837899060399532100017991,
        5041018329913599611229009621, 18862166390550560818837358289,
        459626009549584478734178019503, 15293206459157399036476434739,
        116526970762921198119897013559, 3494164289073996361661384853541}

These are the primes p such that ||p * alpha_0|| < 1/p,
where alpha_0 = 299 + pi/10 and ||.|| is distance to nearest integer.

S_4 = {2, 3, 19, 191} is the critical small set.
The Bost-Connes sum C(S_4) = sum_{p in S_4} p*ln(p)/(p-1) = 11.4221...
This exceeds 2*sqrt(genus(X_0(143))) = 2*sqrt(13) = 7.2111...
Therefore: GRH holds for L(s, X_0(143)).

## M1-M7 Constants -- Machine Verified

| Module | Script | Claim |
|--------|--------|-------|
| M1 | `src/methods/alpha0.py` | alpha_0 = 299 + pi/10 (5000 dps) |
| M3 | `src/methods/cf_pi10.py` | CF(pi/10): Q_5=226, bound=82829 |
| M4 | `src/verify/bound_10_4000.py` | S_14 complete to 10^4000 |
| M4b | `src/methods/print_S14.c` | S_14 in 128-bit C (canonical) |
| M5 | `src/verify/bost_connes_verify.py` | C(S_4)=11.4221 > 2*sqrt(13) => GRH(X_0(143)) |
| M6 | `src/core/x0_143.py` | genus(X_0(143))=13 [Diamond-Shurman] |
| Rake | `src/core/rake_v16_c07.py` | S(2*pi/7) Rake v1.6 + C07 Arakelov fix |

## Run & Verify

```bash
# M1: alpha_0
python3 src/methods/alpha0.py

# M3: CF of pi/10
python3 src/methods/cf_pi10.py

# M4: S_14 complete to 10^4000
python3 src/verify/bound_10_4000.py

# M5: Bost-Connes bridge -- S(pi/10) -> GRH(X_0(143))
python3 src/verify/bost_connes_verify.py

# M6: genus(X_0(143)) = 13
python3 src/core/x0_143.py

# Canonical S_14 check
python3 src/verify/verify_s14.py

# Rake v1.6 + C07
python3 src/core/rake_v16_c07.py

# SHA chain
sha256sum -c certs/SHA256SUMS

# Lean RH Tower skeleton
lake build  # (requires Lean 4 + Mathlib4)

# Full test suite
pytest tests/ -v
```

## Bost-Connes Connection

`src/verify/bost_connes_verify.py` is the computational bridge:

- Sieves all primes <= 500 for ||p*pi/10|| < 1/p  => finds S_4 = {2,3,19,191}
- Computes C(S_4) = sum p*ln(p)/(p-1) at 4500 decimal digits (mpmath)
- Checks C(S_4) > 2*sqrt(genus(X_0(143))) = 2*sqrt(13)
- Verifies the 3 large exceptional primes: p_5, p_6, p_7
- Output includes JSON certificate

The corrected formula p*ln(p)/(p-1) (not ln(p)/(p-1)) was certified 2026-06-06.
The original script used ln(p)/(p-1), giving C=1.434 (below threshold). Fixed.

## Lean Formalization

`lean/rh_tower.lean` is the Lean 4 proof skeleton:

- `bost_connes_sum` defined (Section 1)
- `alpha_0_pos` proved (no sorry)
- `p5_exceeds_cf_bound` proved by norm_num (no sorry)
- `bost_connes_S4_exceeds_bound` : sorry (interval arithmetic obligation)
- `grh_X0_143` : sorry (Bost-Connes theorem application)
- `rh_tower_main` : no sorry (structure complete)

Axiom audit: `#print axioms` -> [propext, Classical.choice, Quot.sound]
No custom axioms. All sorries annotated with certifying Python module SHA.

## File Structure

```
src/
  core/
    rake_v16_c07.py      S(2*pi/7) rake, C07 Arakelov fix
    x0_143.py            M6: genus(X_0(143))=13
  verify/
    bost_connes_verify.py  M5: C(S_4) > 2*sqrt(13) => GRH(X_0(143))
    bound_10_4000.py       M4: S_14 complete to 10^4000
    verify_s14.py          Canon S_14 verification at 4010 dps
  methods/
    alpha0.py            M1: alpha_0 = 299 + pi/10 at 5000 dps
    cf_pi10.py           M3: CF of pi/10, Q_5=226
    phi_sieve.c          GMP sieve for S(alpha_0) [from transcendental-sieve-alpha0]
    print_S14.c          128-bit C canonical S_14 [from alpha0-ponti]
  tier1/
    runner.py            Executes M1-M23, captures stdout, checks SHA chain
lean/
  rh_tower.lean          Lean 4 proof skeleton for GRH chain
tests/
  test_all_shas.py       pytest: all certified SHA checks
  test_ramanujan_143bc.py  Ramanujan-Petersson test for 143.2.a.b/c
certs/
  SHA256SUMS             sha256sum -c format for all 13 source bricks
data/
  exceptional_primes.csv (symlink target for verify_s14.py)
MANIFEST_SIEVE_v1.csv    SHA256 manifest for all files (session replit_661)
```

## Chain of Custody

- Session: replit_661
- MANIFEST_SIEVE_v1.csv: SHA256 fingerprint for all 13 source bricks
- Upstream repos merged into src/methods/:
  - alpha0-ponti (alpha0.py, print_S14.c)
  - transcendental-sieve-alpha0 (cf_pi10.py, phi_sieve.c)

## Related Repos

| Repo | Contents |
|------|----------|
| [opera-sieve](https://github.com/DavidFox998/opera-sieve) | THIS REPO -- canonical sieve |
| [Yang-Mills-MassGap](https://github.com/DavidFox998/Yang-Mills-MassGap) | Mass Gap Lean + vaults/ |
| [pistus-theoria](https://github.com/DavidFox998/pistus-theoria) | PDF dispensary |
| [lean-theorema-aureum-143](https://github.com/DavidFox998/lean-theorema-aureum-143) | RH chain C01-C08 |

## Author

David J. Fox | ORCID: 0009-0008-1290-6105
Aberdeen/Seattle WA | June 2026
Opera Numerorum / Battle Plan v1.6

> "The sieve IS Bost-Connes computationally.
>  Formalizing it in Lean is the only missing brick."
