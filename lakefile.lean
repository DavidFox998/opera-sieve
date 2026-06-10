import Lake
open Lake DSL

package opera_sieve

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.12.0"

@[default_target]
lean_lib OperaSieve where
  srcDir := "lean"
  globs := #[.path `bost_connes]
