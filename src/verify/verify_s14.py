#!/usr/bin/env python3
"""
verify_s14.py -- Canon S_14 Python Verification
Algorithm v1.6 | David Fox | 2026-06-09

Canon SHA-256 (v1.6 large-prime set, comma-joined, no trailing newline):
  1e21ff0b85ab3700357e6bf7e6dea02c01ed03b3603ebd16f81811228401c5ea

Omitted: SHA 197ef385... was computed for a different (pre-v1.6) sieve set.
This script verifies ONLY the Algorithm v1.6 canonical primes.

Chain: Algorithm v1.6 -> p5_bridge_certificate -> C01 -> C07 -> M1-M6 -> M7 manifest

Check #1 = bash scripts/verify.sh
Check #2 = this script (mpmath 4010 dps)
Check #3 = BPSW certificates (pending)

Rule: If this fails, fix the data, not the code.

Usage: python3 scripts/verify_s14.py
Exit 0 = PASS, 1 = FAIL
"""
import csv
import sys
import hashlib
from mpmath import mp, mpf, floor

mp.dps = 4010

CANON_SHA = "1e21ff0b85ab3700357e6bf7e6dea02c01ed03b3603ebd16f81811228401c5ea"
ALGORITHM = "v1.6"
SCRIPT_SHA = "594de23659bdeccc5bbf51b25fae78b05b92bf351b8a13eff33b563bbf487010"
ALPHA_0 = mpf(299) + mp.pi / 10


def dist_to_nearest_int(x):
    frac = x - floor(x)
    return min(frac, 1 - frac)


def sha256_of_primes():
    """SHA-256 of 14 primes comma-joined, no trailing newline."""
    with open('data/exceptional_primes.txt', 'r') as f:
        primes = [line.strip() for line in f if line.strip()]
    s = ','.join(primes)
    return hashlib.sha256(s.encode('utf-8')).hexdigest(), len(primes)


def main():
    print("Opera Numerorum -- S_14 Canon Verification (Algorithm v1.6)")
    print(f"Canon SHA-256 : {CANON_SHA}")
    print(f"Algorithm     : {ALGORITHM}")
    print(f"Script SHA    : {SCRIPT_SHA}")
    print(f"mpmath dps    : {mp.dps}")
    print(f"alpha_0       : 299 + pi/10")
    print("-" * 70)

    actual_sha, count = sha256_of_primes()
    if actual_sha != CANON_SHA:
        print(f"SHA MISMATCH: FAIL", file=sys.stderr)
        print(f"Expected : {CANON_SHA}", file=sys.stderr)
        print(f"Got      : {actual_sha}", file=sys.stderr)
        print(f"Count    : {count}", file=sys.stderr)
        return 1
    print(f"SHA check : PASS ({count} primes)")

    fails = 0
    with open('data/exceptional_primes.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            i = int(row['rank'])
            p = mpf(row['prime'])
            p_alpha = p * ALPHA_0
            d = dist_to_nearest_int(p_alpha)
            thresh = 1 / p
            ok = bool(d < thresh)

            status = "PASS" if ok else "FAIL"
            if not ok:
                fails += 1

            p_str = row['prime']
            if len(p_str) > 22:
                p_str = p_str[:22] + "..."
            print(f"p_{i:2d} = {p_str:<25} ||p*a||<1/p : {status}")

    print("-" * 70)
    if fails == 0:
        print("CANON LOCKED: PASS -- All 14 primes verified to 4010 digits")
        print("Chain: Algorithm v1.6 -> p5_bridge -> C01 -> C07 -> M1-M6 -> M7")
        return 0
    else:
        print(f"CANON FAIL -- {fails}/14 primes failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
