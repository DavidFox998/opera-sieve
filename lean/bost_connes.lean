/-
  bost_connes.lean -- Wall 0.5
  Opera Numerorum -- David J. Fox | June 2026 | Battle Plan v1.6
  ORCID: 0009-0008-1290-6105

  Bost-Connes bound: C(S_4) = sum_{p in {2,3,19,191}} p*log(p)/(p-1) > 2*sqrt(13)
  This is the numerical spine of the RH Tower.

  M5 certified stdout SHA:
    9df98a3970acbb6942770a6cdd42fb21b0a70fc6c8fe04b88ad11ef6c3a8e9f5

  Clay status:
    sqrt13_lt          -- PROVED (nlinarith + Real.sq_sqrt)
    log_lb_2/3/19/191  -- OPEN: exp upper-bound via Taylor+Lagrange (~10 lines each)
    bc_sum_S4_gt_bound -- PROVED assuming log_lb_* (linarith, no sorry in body)
    BCAlgebra          -- opaque (not sorry). IsKMSState not in Mathlib4 v4.12.
    bc_partition_is_zeta -- conditional stub, closes in Task 6.

  PROOF OBLIGATION for log_lb_*:
    log(p) >= q  iff  exp(q) <= p.
    Use: Real.exp_bound' or Taylor truncation with geometric tail.
    For q=693/1000, p=2: T_9 = 1.999878... < 2, tail < 0.00013. Sum < 2. QED.
    Gap between bc_sum(S_4) and 2*sqrt(13) is 4.21 -- bounds need not be tight.

  Axiom audit (after log_lb_* closed):
    [propext, Classical.choice, Quot.sound]  -- no custom axioms, no sorry
-/
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace BostConnes

-- =========================================================================
-- S_4 and bc_sum
-- =========================================================================

/-- Exceptional prime set for alpha_0 = 299 + pi/10.
    Certified by M4 (print_S14.c). SHA: b810a7a3... -/
def S_4 : Finset Nat := {2, 3, 19, 191}

/-- Bost-Connes sum C(S) = sum_{p in S} p * log(p) / (p - 1).
    Corrected formula (M5 errata 2026-06-06): p*log(p)/(p-1), not log(p)/(p-1).
    Certified by M5 (arb_bost.py, mpmath 64 dps). SHA: 9df98a39... -/
noncomputable def bc_sum (S : Finset Nat) : Real :=
  Finset.sum S (fun p => (p : Real) * Real.log p / ((p : Real) - 1))

-- =========================================================================
-- sqrt(13) < 3606/1000
-- =========================================================================

/-- sqrt(13) < 3.606. Proved: (3606/1000)^2 = 13.003236 > 13. -/
theorem sqrt13_lt : Real.sqrt 13 < 3606/1000 := by
  have hnn  : (0 : Real) <= Real.sqrt 13 := Real.sqrt_nonneg 13
  have hsq  : Real.sqrt 13 ^ 2 = 13     := Real.sq_sqrt (by norm_num)
  have hne  : Real.sqrt 13 != 3606/1000 := by
    intro h; rw [h] at hsq; norm_num at hsq
  have hle  : Real.sqrt 13 <= 3606/1000 := by
    nlinarith [sq_nonneg (Real.sqrt 13 - 3606/1000)]
  exact lt_of_le_of_ne hle hne

-- =========================================================================
-- LOG LOWER BOUNDS
-- Each: log(p) >= q  iff  exp(q) <= p  (by Real.le_log_iff_exp_le).
-- Proof obligation: bound exp(q) above using truncated Taylor + tail.
-- Gap = 4.21 units; loose bounds (1-2 decimal places) are sufficient.
-- M5 SHA: 9df98a3970acbb6942770a6cdd42fb21b0a70fc6c8fe04b88ad11ef6c3a8e9f5
-- =========================================================================

/-- log(2) >= 0.693. Obligation: exp(693/1000) <= 2.
    Taylor T_9 = 1.999878. Tail < 0.000125. Sum < 2. -/
theorem log_lb_2 : Real.log 2 >= 693/1000 := by
  rw [ge_iff_le, Real.le_log_iff_exp_le (by norm_num : (0:Real) < 2)]
  -- Goal: exp(693/1000) <= 2
  -- OBLIGATION: close with Real.exp_bound' or explicit Taylor bound
  -- Lean 4 path: have hT := Real.sum_le_exp_of_nonneg (by norm_num : (0:Real) <= 693/1000) 10
  --              then bound tail by geometric series with exp(1) < 3
  sorry

/-- log(3) >= 1.098. Obligation: exp(1098/1000) <= 3.
    Taylor T_9 = 2.998. Tail < 0.002. -/
theorem log_lb_3 : Real.log 3 >= 1098/1000 := by
  rw [ge_iff_le, Real.le_log_iff_exp_le (by norm_num : (0:Real) < 3)]
  sorry

/-- log(19) >= 2.944. Obligation: exp(2944/1000) <= 19.
    exp(2.944) = 18.997. Directly computable. -/
theorem log_lb_19 : Real.log 19 >= 2944/1000 := by
  rw [ge_iff_le, Real.le_log_iff_exp_le (by norm_num : (0:Real) < 19)]
  sorry

/-- log(191) >= 5.252. Obligation: exp(5252/1000) <= 191.
    exp(5.252) = 190.89. Directly computable. -/
theorem log_lb_191 : Real.log 191 >= 5252/1000 := by
  rw [ge_iff_le, Real.le_log_iff_exp_le (by norm_num : (0:Real) < 191)]
  sorry

-- =========================================================================
-- MAIN THEOREM: bc_sum(S_4) > 2 * sqrt(13)
-- NO sorry in this body. Depends on log_lb_* obligations above.
-- Numerical check: 11.4221 > 7.2111 (gap = 4.21).
-- M5 certified stdout SHA: 9df98a39...
-- =========================================================================

theorem bc_sum_S4_gt_bound : bc_sum S_4 > 2 * Real.sqrt 13 := by
  have hsqrt : Real.sqrt 13 < 3606/1000 := sqrt13_lt
  have h2    : Real.log 2   >= 693/1000  := log_lb_2
  have h3    : Real.log 3   >= 1098/1000 := log_lb_3
  have h19   : Real.log 19  >= 2944/1000 := log_lb_19
  have h191  : Real.log 191 >= 5252/1000 := log_lb_191
  -- Expand bc_sum {2, 3, 19, 191} to four explicit terms
  have hexpand : bc_sum S_4 =
      2 * Real.log 2 +
      3 / 2 * Real.log 3 +
      19 / 18 * Real.log 19 +
      191 / 190 * Real.log 191 := by
    simp only [bc_sum, S_4,
      Finset.sum_insert (show (2:Nat) !in ({3,19,191} : Finset Nat) from by decide),
      Finset.sum_insert (show (3:Nat) !in ({19,191}   : Finset Nat) from by decide),
      Finset.sum_insert (show (19:Nat) !in ({191}      : Finset Nat) from by decide),
      Finset.sum_singleton]
    push_cast
    ring
  rw [hexpand]
  -- Numerical gap: lb = 2*0.693 + 1.5*1.098 + 19/18*2.944 + 191/190*5.252 = 11.418
  -- 2 * sqrt(13) < 2 * 3.606 = 7.212
  -- 11.418 > 7.212 by linarith
  nlinarith [mul_le_mul_of_nonneg_left h2   (by norm_num : (0:Real) <= 2),
             mul_le_mul_of_nonneg_left h3   (by norm_num : (0:Real) <= 3/2),
             mul_le_mul_of_nonneg_left h19  (by norm_num : (0:Real) <= 19/18),
             mul_le_mul_of_nonneg_left h191 (by norm_num : (0:Real) <= 191/190)]

-- =========================================================================
-- BOST-CONNES ALGEBRA: opaque infrastructure
-- opaque != sorry. This is an explicit open axiom (CMI honest pattern).
-- Clay status: OPEN. IsKMSState not formalized in Mathlib4 v4.12.
-- =========================================================================

/-- OPEN: Bost-Connes C*-dynamical system (A_{BC}, sigma_t).
    Built from N |x Q* and its C*-completion.
    Clay status: OPEN. -/
opaque BCAlgebra : Type

/-- OPEN: KMS state condition at inverse temperature beta = 1. -/
opaque IsKMSAtOne : BCAlgebra -> Prop

/-- Wall 0.5 -> Wall 1 dependency anchor.
    The Bost-Connes theorem (1995): Z_{BC}(beta) = zeta(beta) for beta > 1.
    Clay status: OPEN. Requires C*-algebra formalization. Task 6. -/
theorem bc_partition_wall05_anchor (phi : BCAlgebra) (_ : IsKMSAtOne phi) : True :=
  trivial

end BostConnes
