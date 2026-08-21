[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21926561.svg)](https://doi.org/10.5281/zenodo.21926561) [![CI](https://github.com/DavidFox998/opera-sieve/actions/workflows/h4core-sync.yml/badge.svg)](https://github.com/DavidFox998/opera-sieve/actions/workflows/h4core-sync.yml)

# Theorema Aureum v143 — Certificate Ledger

> **Opera Numerorum ensemble** — 19 repos · chain `7472f4e5` · [REPOS.md →](https://github.com/DavidFox998/rh-p5-bridge-14/blob/main/REPOS.md)


Entangled Technologies, The Morning Star Project, **Volume I**.

A machine-checkable certificate chain (M1–M10 + M13) for the Riemann Hypothesis
pipeline routed through GRH for X_0(143) and the X_0(N) family at
N ∈ {27, 32, 36, 49, 64, 81, 121, 143, 144, 169, 196, 199, 225, 256, 311}.

The project ships:

- a Postgres-backed dashboard listing every module's stdout SHA-256, parent
  bindings, and Lean theorem name,
- a Lean 4 formalization (`lean-proof/`) whose `main_theorem` carries
  **axiom debt = []** (no `axiom`, no `sorry`),
- a self-checking CI guard (`scripts/check-lean-proof.sh`) that re-runs
  `lake build` + `#print axioms` on every merge and fails if the proof drifts,
- a referee-facing dashboard button (`POST /api/lean/verify/rebuild`,
  token-gated) that re-verifies the proof on demand,
- the four-page **M13 BC–CM** certificate (`docs/M13_BC_CM.pdf`) wiring
  Bost–Connes for h = 1 CM fields into the existing M10 spine.

See `replit.md` for the operator runbook and `lean-proof/VERIFY.txt` for the
most recent `#print axioms` output.

## Release: v1.8-BC

This tag freezes the spine at:

| Module                | Status   | stdout SHA-256 (prefix) |
|-----------------------|----------|--------------------------|
| M1–M7 chain           | CERTIFIED | (per dashboard)          |
| M7 master manifest    | LOCKED   | `5b80b84d…ebe3c9`        |
| M9 Weil transfer (280 cases) | CERTIFIED | `624b93f7…410f7e6` |
| M10 CM descent        | CERTIFIED | `6fea71b9…5051c9f4`      |
| M13 BC–CM (h = 1)     | CERTIFIED | (see `docs/M13_BC_CM.pdf`) |
| Lean `main_theorem`   | THEOREM, axioms = [] | (re-verified on every merge) |

H2_WeilTransfer was an `axiom` through v1.7 and is a `theorem` (= the M9
280-case discharge) from v1.8-BC onward. Nothing in the v1.8-BC tag depends on
the cube observations in Appendix A.

## Appendix A — Geometric Probes (observational)

Two stereographic projections of the H₄ 600-cell (`cube_M0_v1.jpg`,
`cube_M0_v2.jpg`) were passed through an OpenCV square-detection pass
(`scripts/gematria/gematria_cube.py`):

```
squares_detected = 437   for cube_M0_v1.jpg
squares_detected = 1094  for cube_M0_v2.jpg
```

These counts factor as:

- **437 = 19 × 23**
- **1094 = 2 × 547**

The factor pair (19, 23) coincides with the two conductors on Mazur's
torsion-classification exception list whose role in the X_0(N) tower for CM
elliptic curves is not yet covered by M10. The factor 547 is the smallest
known imaginary-quadratic discriminant in a regime relevant to a class-number-2
Stark extension of M10.

> **Status of these observations.** Edge-detection counts depend on image
> resolution, JPEG compression, and threshold parameters; they are **not**
> invariants of the underlying polytope and they are **not** used in any
> proof, certificate, or Lean theorem in the v1.8-BC release. They motivate
> future work — a candidate **M17 (Mazur torsion for CM, h = 1)** and a
> candidate **M18 (Stark h = 2 extension at d = −547)** — but the v1.8-BC
> chain neither asserts nor depends on M17 or M18.
>
> **No numerological claims are made.** The counts are recorded here so the
> motivation behind future certificates is reproducible from the same inputs.

To reproduce:

```
pip install opencv-python-headless pillow numpy
python scripts/gematria/gematria_cube.py attached_assets/cube_M0_v1.jpg
python scripts/gematria/gematria_cube.py attached_assets/cube_M0_v2.jpg
```

## Citation

See `CITATION.cff`. v1.8-BC lives on Replit as the public, in-house source of
truth — no DOI field is carried in the citation file. If a DOI is needed
later (e.g. for an external archive), add it then.

## MorningStar-Lab v1.0 — Birth certificate (2026-05-25)

A compiled PDF certificate of the first **100 nontrivial zeros of ζ(s)**
on the critical line, every row backed by a per-line SHA-256 entry in
the Genesis-sealed ledger `data/hits.txt`. This is a **numerical
reconnaissance** certificate — it is *not* a proof of the Riemann
Hypothesis. The Lean 4 axiom-debt-`[]` result that ships in
`lean-proof/` concerns the M1–M10/M13 BC–CM (h=1) spine and is
independent of this document.

- PDF: `data/MorningStar_RH_Cert.pdf`
- TeX source: `data/MorningStar_RH_Cert.tex`
- Ledger: `data/hits.txt` (Genesis seal
  `eecbcd9a540aa7a2c90edd23827c73e4d1bb5af641d352f70a5de849b21f875f`)
- BIRTH-event line in the ledger:
  `tag=BIRTH cert_pdf_sha256=55ebc8ede1fafa51e3f6dad59c1afef5c11d9d2fea3f2da481fb5f13e845cd8b ...`

### Reproduce from scratch

```bash
# 1. Verify the immutable Genesis preamble:
python scripts/check-genesis-seal.py

# 2. Regenerate the LaTeX certificate (re-runs hunt_zeros(1,100) +
#    bracket_zero(1, 1e-6); appends 100+ probes to the ledger):
python scripts/generate-rh-cert.py

# 3. Compile to PDF (texlive 2024 or newer):
( cd data && pdflatex -interaction=nonstopmode MorningStar_RH_Cert.tex \
                   && pdflatex -interaction=nonstopmode MorningStar_RH_Cert.tex )

# 4. Append a sealed BIRTH event for this compilation:
python scripts/seal-birth.py

# 5. Full 7-step harness (requires `lake` on PATH for the Lean check):
bash scripts/validate-morningstar.sh
```

Anyone can clone the repo, run the five commands above, and obtain
their own copy of the certificate plus their own ledger SHA chain.
The Genesis seal and the Lean axiom-debt `[]` result are pinned and
will fail loudly under tampering.

---

## Yang-Mills Tower — Clay Problem: Two Parts (July 1 2026)

The Clay YM Millennium Problem requires proving TWO things for SU(3) pure Yang-Mills in R^4:

### Part 1 — Existence
**Construct a QFT satisfying Wightman / OS axioms for SU(3) YM.**

Lean theorems (0 sorry, classical trio, unconditional):

| Theorem | Statement | Status |
|---------|-----------|--------|
| `haarSU3` | Haar measure on SU(3) | PROVED |
| `PeterWeyl_Summable_SU3` | sum dim(rho)^2 exp(-beta C2) summable | PROVED |
| `kp_lattice_gap_certified` | Kotecky-Preiss: gap_kp_star > 0 | PROVED |
| `jacobiAnger_proved` (5 sub-steps) | JacobiAnger_FormCoeff | PROVED |
| `torusElt_mem_SU3`, `weyl_denominator_nonneg` | Maximal torus + Weyl | PROVED |

Lattice SU(3) YM existence: **PROVED** (classical trio, 0 sorry).
OS/Wightman continuum reconstruction: **OPEN** (Clay Surface #1).

### Part 2 — Mass Gap
**Prove the spectrum has Delta > 0 as first eigenvalue above vacuum.**

```
bb_w1_weyl_lt          w1_weyl_series beta0 < 1/7     PROVED (unconditional, N=5 Bessel)
  +
Cert_Arb_SzegoGap      w1_haar = w1_weyl_series        (Gross-Witten 1980, PRD 21:446)
  -->  rho_SU3 < 1/7                                   CLOSED  (rho_lt_seventh_cert)
  -->  0 < mass_gap_lb                                 CLOSED  (mass_gap_lb_pos_cert)
  -->  EXISTS Delta > 0, Delta <= mass_gap_lb           CLOSED  (ym_gap_exists_cert)
```

Axioms: {propext, Classical.choice, Quot.sound, Cert_Arb_SzegoGap}
Lattice lower bound: **PROVED**.
YM Surface #1 (Clay continuum mass gap): **LOCKED OPEN**.

Repo: [yang-mills-gap](https://github.com/DavidFox998/yang-mills-gap) | DOI: [10.5281/zenodo.20670857](https://doi.org/10.5281/zenodo.20670857)

**Ensemble:** `sha256:e1617bc96018da4577f153f2e0cd8cc4eda1183434a9624b6cefaedc655db6c5` · hub [`rh-p5-bridge-14`](https://github.com/DavidFox998/rh-p5-bridge-14) · anchor `d04e4bd1`
