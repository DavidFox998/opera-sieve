"""
Opera Numerorum -- pytest suite
Verifies every artifact in data/certified_hashes.json.

Run:
    pip install pytest mpmath
    pytest tests/test_all_shas.py -v
"""
import hashlib, json, os, subprocess, sys
from pathlib import Path
import pytest

ROOT   = Path(__file__).resolve().parent.parent
DATA   = json.loads((ROOT / "data" / "certified_hashes.json").read_text())
T2     = DATA["tier2"]
T3     = DATA["tier3"]
MANIF  = DATA["manifest"]["M7"]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

# ── T2: artifact SHA tests (one per artifact file) ──────────────────────────
@pytest.mark.parametrize("key,entry", T2.items())
def test_t2_artifact(key, entry):
    """Shipped artifact must match certified SHA."""
    artifacts_dir = ROOT          # .out files live at repo root
    fp = artifacts_dir / key
    if not fp.exists():
        # Try source_file name directly
        alt = artifacts_dir / Path(entry.get("source_file", key)).name
        fp  = alt if alt.exists() else fp
    assert fp.exists(), f"Artifact missing: {fp}"
    got = sha256_file(fp)
    assert got == entry["sha256"], (
        f"{key}: SHA mismatch\n"
        f"  expected: {entry['sha256']}\n"
        f"  got:      {got}"
    )

# ── T3: Lean source SHA tests ────────────────────────────────────────────────
@pytest.mark.parametrize("cn,entry", T3.items())
def test_t3_lean_source(cn, entry):
    """Lean source file must match certified SHA."""
    fp = ROOT / entry["source_file"]
    assert fp.exists(), f"Lean source missing: {fp}"
    got = sha256_file(fp)
    assert got == entry["sha256_source"], (
        f"{cn}: source SHA mismatch\n"
        f"  expected: {entry['sha256_source']}\n"
        f"  got:      {got}"
    )

# ── Manifest: verify M7 hash from shipped .out files ────────────────────────
def test_m7_manifest():
    """M7 manifest = SHA256(cat m1.out...m6.out) must match certified value."""
    out_files = [ROOT / f"m{i}.out" for i in range(1, 7)]
    for fp in out_files:
        assert fp.exists(), f"Missing for manifest: {fp}"
    combined = b"".join(fp.read_bytes() for fp in out_files)
    got = hashlib.sha256(combined).hexdigest()
    assert got == MANIF["sha"], (
        f"M7 manifest mismatch\n"
        f"  expected: {MANIF['sha']}\n"
        f"  got:      {got}"
    )

# ── T4: physics self-consistency (runs check_physics.py as subprocess) ───────
def test_t4_physics_consistency():
    """All 13 physics constant assertions must pass."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "src" / "tier4" / "check_physics.py")],
        capture_output=True, text=True
    )
    assert result.returncode == 0, (
        "T4 physics consistency FAILED:\n" + result.stdout + result.stderr
    )
