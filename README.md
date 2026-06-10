# opera-sieve -- Wall 0 / Wall 0.5

Bost-Connes bridge and classical trio source code for Opera Numerorum.

Depends on: mathlib @ v4.12.0

## Lean

```
lean/bost_connes.lean   -- Wall 0.5: bc_sum_S4_gt_bound PROVED
```

## Scripts (Wall 0 classical trio)

```
scripts/alpha0.py           -- M1: alpha_0 = sum_{p in S4} p*log(p)/(p-1)
scripts/cf_pi10.py          -- M3: continued fraction of pi/10, finds S14 bound 82829
scripts/bound_10_4000.py    -- M4: verifies S14 complete to 10^4000
scripts/arb_bost.py         -- M5: Bost bound C(S4) > 2*sqrt(g)
scripts/x0_143.py           -- M6: GRH for X_0(143) via Diamond-Shurman
```

## Binaries

```
bin/print_S14.c / bin/print_S14     -- M4: outputs S14 prime list (C, 80-bit)
bin/print_kappa.c / bin/print_kappa -- M2: kappa = phi(143)*c_lemma/1e10
```

## Data

```
data/exceptional_primes.csv    -- S14 = 14 exceptional primes
data/exceptional_primes.json
data/exceptional_primes.txt
```

## Downstream

- [RH-Core](https://github.com/DavidFox998/RH-Core) -- Wall 1: C01-C08
- [NS-Tower](https://github.com/DavidFox998/NS-Tower) -- Wall 4.5: YM + NS

Opera Numerorum / Battle Plan v1.6 | David J. Fox | ORCID: 0009-0008-1290-6105
