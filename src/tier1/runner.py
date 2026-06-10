#!/usr/bin/env python3
"""
Opera Numerorum -- Tier 1 runner
Executes each M1-M23 compute script, captures stdout, computes SHA-256,
and compares against data/certified_hashes.json.

Usage:
    python3 src/tier1/runner.py          # prints table, returns exit code
"""
import hashlib, json, subprocess, sys, os, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HASHES = json.loads((ROOT / "data" / "certified_hashes.json").read_text())["tier1"]

# Map: key -> (command, cwd)
# Commands run relative to repo root so existing source paths work unchanged.
SCRIPTS = {
    "m1":    (["python3", "certificates/alpha0.py"], str(ROOT)),
    "m2":    (["./bin/print_kappa"],                 str(ROOT)),
    "m3":    (["python3", "cf_pi10.py"],             str(ROOT)),
    "m4":    (["python3", "verify/bound_10_4000.py"],str(ROOT)),
    "m5":    (["python3", "arb_bost.py"],            str(ROOT)),
    "m6":    (["python3", "x0_143.py"],              str(ROOT)),
    "m9all": (["python3", "certificates/build_module_9_all.py"], str(ROOT)),
    "m10":   (["python3", "certificates/build_module_10.py"],    str(ROOT)),
    "m21":   (["python3", "certificates/m21_h4_invariant.py"],   str(ROOT)),
    "m22":   (["python3", "certificates/m22_mstar_definition.py"],str(ROOT)),
    "m23":   (["python3", "certificates/m23_bsd_j0_143.py"],     str(ROOT)),
    "m8a":   (["python3", "certificates/build_module_m8a.py"],   str(ROOT)),
}

GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
RESET  = "\033[0m"

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run_script(key, cmd, cwd):
    t0 = time.time()
    try:
        result = subprocess.run(
            cmd, cwd=cwd,
            capture_output=True, timeout=600
        )
        elapsed = time.time() - t0
        if result.returncode != 0:
            return None, result.stderr.decode(errors="replace"), elapsed
        return result.stdout, None, elapsed
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT after 600s", time.time() - t0
    except FileNotFoundError:
        return None, f"COMMAND NOT FOUND: {cmd[0]}", time.time() - t0

def main():
    print()
    print("=" * 72)
    print("OPERA NUMERORUM -- TIER 1: RECOMPUTE VERIFICATION")
    print("=" * 72)
    print(f"{'MODULE':<8} {'CLAIM':<42} {'STATUS':<10} SHA (first 16)")
    print("-" * 72)

    results = {}
    for key, (cmd, cwd) in SCRIPTS.items():
        entry = HASHES.get(key, {})
        expected = entry.get("sha256_stdout", "")
        claim    = entry.get("claim", "")[:40]

        stdout, err, elapsed = run_script(key, cmd, cwd)
        if err:
            status  = f"{RED}ERROR{RESET}"
            got_sha = "N/A"
            ok      = False
        else:
            got_sha = sha256_bytes(stdout)
            if got_sha == expected:
                status = f"{GREEN}PASS{RESET}"
                ok     = True
            else:
                status = f"{RED}FAIL{RESET}"
                ok     = False

        results[key] = ok
        print(f"{key.upper():<8} {claim:<42} {status:<10} {got_sha[:16]}...")
        if not ok and err:
            print(f"         ERROR: {err[:60]}")
        if not ok and not err:
            print(f"         EXPECTED: {expected[:16]}...")
            print(f"         GOT:      {got_sha[:16]}...")

    print("-" * 72)
    passed = sum(1 for v in results.values() if v)
    total  = len(results)
    print(f"T1 result: {passed}/{total}")
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
