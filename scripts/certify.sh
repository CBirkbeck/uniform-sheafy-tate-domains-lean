#!/usr/bin/env bash
# Kernel-level certification of the paper's headline theorems via leanprover/comparator:
# statement-identity against `Adic spaces/Comparator/Challenge.lean`, axiom budget
# [propext, Quot.sound, Classical.choice], and kernel acceptance.
#
# Prerequisites (one-time):
#   git clone https://github.com/leanprover/comparator /tmp/comparator
#   cd /tmp/comparator && lake build            # its toolchain matches this project exactly
#   # the lean4export artifact lake fetches is a Linux ELF; build it natively instead:
#   git clone https://github.com/leanprover/lean4export /tmp/lean4export
#   cd /tmp/lean4export && git checkout \
#     $(python3 -c "import json;print([p['rev'] for p in \
#       json.load(open('/tmp/comparator/lake-manifest.json'))['packages'] \
#       if p['name']=='lean4export'][0])") && lake build
#
# On Linux, install the real landrun (github.com/Zouuup/landrun) for sandboxing.
# On macOS, comparator's own scripts/fake-landrun.sh shim is used (no sandbox — acceptable
# here: the "solution" is this repository's own code, not an adversarial submission).
#
# The script cds to the repo root itself, so it can be invoked from anywhere.
#
# CONFIG selects which certificate to run; the challenge/solution modules are read from it:
#   default  — comparator.json                                  the Palomar submission:
#              [FJP] Theorem 1.1 stated self-containedly on Mathlib (`Palomar/Challenge.lean`)
#   also     — Adic spaces/Comparator/comparator-config.json   ([FJP] Theorem 1.1, the
#              in-library certificate whose challenge imports the library's definition layer)
#            — Adic spaces/Comparator/wp-config.json           ([WP] Theorem 8.1, likewise)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${CONFIG:-comparator.json}"

COMPARATOR_DIR="${COMPARATOR_DIR:-/tmp/comparator}"
export COMPARATOR_LEAN4EXPORT="${COMPARATOR_LEAN4EXPORT:-/tmp/lean4export/.lake/build/bin/lean4export}"
if ! command -v landrun >/dev/null 2>&1; then
  export COMPARATOR_LANDRUN="${COMPARATOR_LANDRUN:-$COMPARATOR_DIR/scripts/fake-landrun.sh}"
fi

cd "$REPO_ROOT"

# For the Palomar config, `Palomar/Defs.lean` must be the Challenge's definitions verbatim.
if [ "$CONFIG" = "comparator.json" ]; then python3 scripts/gen-defs.py --check; fi

# Both modules are deliberately outside defaultTargets (the challenge is full of `sorry`), so
# they must be built by name. Build the challenge FIRST: comparator's guarantee assumes the
# challenge's oleans were not produced by a run that had already seen the solution.
#
# Comparator itself re-runs `lake build` on each module inside landrun (`safeLakeBuild`), which
# is why `Solution.lean` is a small forwarding file rather than a library module: only the
# untrusted submission belongs in the sandboxed build, not the whole project.
CHALLENGE_MOD="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['challenge_module'])" "$CONFIG")"
SOLUTION_MOD="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['solution_module'])" "$CONFIG")"
lake build "$CHALLENGE_MOD"
lake build "$SOLUTION_MOD"

exec lake env "$COMPARATOR_DIR/.lake/build/bin/comparator" "$CONFIG"
