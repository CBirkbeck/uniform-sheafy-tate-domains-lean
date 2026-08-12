# Uniform sheafy Tate rings that are not stably uniform — the Lean formalisation

Lean 4 formalisation of the two counterexamples in
**[*Uniform sheafy Tate rings that are not stably uniform*](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/)**
(Birkbeck–Torzewski).

The paper answers **Question 7 of Kedlaya's *Nonarchimedean Scottish Book***:

> Let `(A, A⁺)` be a sheafy uniform Huber pair. Is `(A, A⁺)` necessarily stably uniform?

The answer is no. Buzzard–Verberkmoes and Mihara showed that a stably uniform Tate Huber ring
is sheafy; the paper constructs two uniform, strongly sheafy Tate rings that are **not** stably
uniform. In the first, a rational localisation is non-reduced; in the second, the rational
localisation is an integral domain but is not uniform.

Both constructions, the rational localisations witnessing the failure, and their sheafiness are
formalised here — and the two headline theorems are **kernel-certified**: each statement is
pinned in a file that cannot see its own proof, the proofs are replayed through the Lean
kernel, and the axiom budget is exactly `propext`, `Quot.sound`, `Classical.choice`. Nothing is
assumed, and no certified proof contains a `sorry`.

The paper's own account of the formalisation is
[Appendix A](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-formalisation).

---

## The two theorems

### [Theorem 1.1](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#thm-main-1-1) — the finite-jet ring

*Paper:* [§3, The finite-jet ring](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-the-global-ring)
· [§4, A rational localisation which is not uniform](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-a-rational-localisation-which-is)
· [§6, Milnor descent and strong sheafiness](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-milnor-descent-and-strong-sheafiness)

`A` is a complete uniform non-noetherian Tate `k`-algebra and an integral domain, with
`A° = A₀`. It is strongly sheafy — in particular `(A, A°)` is sheafy. But

```
A⟨W/ϖ⟩ ≅ k⟨X, Q⟩/(Q²),   X = W/ϖ,
```

which is non-reduced, so `A` is not stably uniform.

In Lean, `A` is the pullback `𝓐 = 𝓑 ×_𝓓 𝓒` of the pinching (Milnor) square

| ring | |
|---|---|
| `L = k⟨W, W⁻¹⟩` | radius-one restricted Laurent algebra |
| `𝓑 = k⟨W, Q⟩/(Q²)` | realised norm-faithfully as `DualNumber (k⟨W⟩)` |
| `𝓒 = L⟨Q⟩` | |
| `𝓓 = L⟨Q⟩/(Q²)` | |

realised concretely as the closed subring of `𝓒` of series whose `Q⁰`- and `Q¹`-coefficients
have nonnegative `W`-support.

*Definition:* `FiniteJetOver.JetA K` in `Adic spaces/FJP/Over/JetRings.lean`, over an
arbitrary complete ultrametric nontrivially-normed field `K`.
*Endpoints:* `Adic spaces/FJP/Over/SheafyEndpoints.lean` and `Over/StrongSheafy.lean`, at the
layer-2 (`_of_dvr`) form where the valuation ring of `K` is a DVR.

| paper | Lean | certified |
|---|---|---|
| sheafy | `FiniteJetOver.isSheafy_JetA_of_dvr` | ✓ |
| uniform | `FiniteJetOver.finiteJet_isUniform_of_dvr` | ✓ |
| integral domain | `FiniteJetOver.finiteJet_isDomain` | ✓ |
| non-noetherian | `FiniteJetOver.finiteJet_not_noetherian` | ✓ |
| `A° = A₀` | `FiniteJetOver.finiteJet_powerBounded_eq_unitBall_of_dvr` | ✓ |
| strongly sheafy | `FiniteJetOver.finiteJet_tateExt_isSheafyComplete_of_dvr` | ✓ |
| not stably uniform | `FiniteJetOver.finiteJet_not_stablyUniform_of_dvr` | ✓ |

These are the declarations the paper's own `<lean>` references for Theorem 1.1 point at. A
parallel development over the concrete witness base `k = F((t))` lives in
`Adic spaces/FJP/` (`FiniteJet.JetA F`, endpoints in `FJP/FiniteJetMain.lean`); the
general-base statements above specialise to it.

### [Theorem 8.1](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#thm-second-example-1-1) — the weighted-parity algebra

*Paper:* [§8, A second example](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-second-example)
· [§8.1, The weighted-parity algebra](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-second-example-the-weighted-parity-algebra)
· [§8.4, A reduced rational chart which is not uniform](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-second-example-a-reduced-rational-chart-which)
· [§8.5, Strong sheafiness](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-second-example-strong-sheafiness)

For a weight `w : ℕ_{>0} → ℕ` with `w(n) ≥ 1` and unbounded, the complete Tate `k`-algebra
`𝒜_w` satisfies:

1. `𝒜_w` is a uniform, non-noetherian integral domain with `𝒜_w° = 𝒜_{w,0}`;
2. `𝒜_w` is strongly sheafy — in particular `(𝒜_w, 𝒜_w°)` is sheafy;
3. the rational localisation `ℬ_w = 𝒜_w⟨W/ϖ⟩` is an **integral domain** but is not uniform.

Hence `𝒜_w` is not stably uniform — and this time the failure is not explained away by a
nilpotent, which is what makes this example sharper than Theorem 1.1.

In Lean, `𝒜_w` is the subring of the countable restricted Tate algebra `k⟨W, U₁, U₂, …⟩` of
series supported on the weighted-parity monoid of `w`.

*Definition:* `WeightedParity.WPA K w` in `Adic spaces/WP/Algebra.lean`, for a general weight.
*Endpoints:* `Adic spaces/WP/Main.lean`, at the paper's weight `w = id`
(`WeightedParity.idWeight`).

| paper | Lean | certified |
|---|---|---|
| uniform | `WeightedParity.weightedParity_isUniform_of_dvr` | ✓ |
| integral domain | `WeightedParity.weightedParity_isDomain` | ✓ |
| non-noetherian | `WeightedParity.weightedParity_not_noetherian` | ✓ |
| `𝒜° = 𝒜₀` | `WeightedParity.weightedParity_powerBounded_eq_unitBall` | ✓ |
| sheafy | `WeightedParity.weightedParity_isSheafyComplete_of_dvr` | ✓ |
| strongly sheafy | `WeightedParity.weightedParity_stronglySheafy_of_dvr` | ✓ |
| not stably uniform | `WeightedParity.weightedParity_not_stablyUniform_of_dvr` | ✓ |

The base is an abstract complete ultrametric nonarchimedean field whose valuation ring is a
DVR, rather than a fixed witness field.

### Scope of the certificate

Fourteen statements are certified — seven per theorem — and together they are exactly the
conclusions of the two theorems as the paper states them. Both certificates are over a
general base: an arbitrary complete ultrametric nontrivially-normed field whose valuation
ring is a discrete valuation ring. Neither is pinned to a concrete witness field.

The challenge files state all of this from the **definition layer** alone. For the finite-jet
ring that required one refactor: the uniformizer-free `IsHuberRing`/`IsTateRing` instances,
without which `¬ IsStablyUniform (JetA K)` does not even elaborate, used to live in
`Over/Functoriality.lean` — a module whose import closure contains `Over/Chart.lean`, and so
the proof of `not_isStablyUniform_JetA`. They now live in
`Adic spaces/FJP/Over/TateInstances.lean`, whose closure is the definition layer plus the
base-agnostic `FaithfulLocLift`, so the challenge can state the conclusions without seeing
any proof of them.

---

## Check it yourself

### Build

```sh
lake exe cache get   # mathlib oleans for v4.33.0
lake build           # the library — it is this repository's only build target
```

mathlib is the only dependency. The first build compiles the library from source and takes a
while; after that it is incremental.

### Kernel certification

The two theorems are certified with [`leanprover/comparator`](https://github.com/leanprover/comparator).
One-time setup — comparator and `lean4export` must be built on the *same* toolchain as this
repository, `leanprover/lean4:v4.33.0`:

```sh
git clone https://github.com/leanprover/comparator /tmp/comparator
cd /tmp/comparator && lake build

# the lean4export artifact lake fetches is a Linux ELF; build it natively instead
git clone https://github.com/leanprover/lean4export /tmp/lean4export
cd /tmp/lean4export && git checkout \
  $(python3 -c "import json;print([p['rev'] for p in \
    json.load(open('/tmp/comparator/lake-manifest.json'))['packages'] \
    if p['name']=='lean4export'][0])") && lake build
```

Then, from this repository's root:

```sh
bash scripts/certify.sh                                     # Theorem 1.1 — seven statements
CONFIG="Adic spaces/Comparator/wp-config.json" \
  bash scripts/certify.sh                                   # Theorem 8.1 — seven statements
```

Each run ends `Your solution is okay!`.

On Linux, install [landrun](https://github.com/Zouuup/landrun) for real sandboxing. On macOS
the script falls back to comparator's `fake-landrun.sh` shim — acceptable here, since the
"submission" being judged is this repository's own code rather than an adversarial one.

### What certification buys over `#print axioms`

For each certified name, comparator

1. rebuilds the solution module in a sandbox,
2. checks that the solution's statement is **structurally identical** to the challenge's — and
   the challenge is a file the solution does not get to edit,
3. checks the axiom set is within `propext`, `Quot.sound`, `Classical.choice`, and
4. replays the proof through the Lean kernel.

`#print axioms` answers only (3), and only relative to whatever statement the library happens
to declare — it cannot tell you that the theorem says what you think it says. The trust
boundary is the point: each challenge file imports only the **definition** layer, and its
import closure provably contains none of the modules that prove the result. See
`Adic spaces/Comparator/README.md` for the full argument.

**Numbering note.** The Lean docstrings were written against an earlier revision of the paper
and cite these results as `[FJP] Thm 1.3` and `[WP] thm 6.2`. In the current revision they are
Theorem 1.1 and Theorem 8.1; the certificate names (`fjp_1_1_*`, `wp_8_1_*`) follow the current
numbering.

---

## Repository map

| path | what it is |
|---|---|
| `Adic spaces/FJP/` | Theorem 1.1 — the finite-jet ring |
| `Adic spaces/FJP/Over/` | the same over a general complete discretely valued base |
| `Adic spaces/WP/` | Theorem 8.1 — the weighted-parity algebra |
| `Adic spaces/Comparator/` | the challenge/solution certificate pairs and their configs |
| `Adic spaces/` (rest) | the supporting adic-spaces library the examples are built on: continuous valuations, `Spa`, Tate rings, rational subsets, the structure presheaf, completions, Čech cohomology, Milnor squares |
| `Adic spaces/ScottishBook/` | the [Nonarchimedean Scottish Book](https://scripts.mit.edu/~kedlaya/wiki/index.php?title=The_Nonarchimedean_Scottish_Book) — Kedlaya's open-problem list, one module per problem, *statements only* |
| `scripts/certify.sh` | the comparator run, plus its one-time setup instructions |
| [`formalization.yaml`](formalization.yaml) | the formalisation self-report (below) |

### The manifest

[`formalization.yaml`](formalization.yaml) is a self-report in the
[mathlib-initiative schema](https://github.com/mathlib-initiative/formalization.yaml)
(v0.3): the sources and their licences, the scope of what is formalised, the per-result
axiom status and comparator config for each headline theorem, the automation provenance
with its cost caveats, and the fidelity divergences from the paper. Fields that need a human
answer are left blank rather than guessed. It is a page long and is the right place to start
if you want the claims without reading Lean.

A handful of docstrings in the supporting library (25 files) point at AINTLIB's internal
planning notes — paths like `.mathlib-quality/…` or `docs/plans/…`. Those files are development
process rather than mathematics, so they are not carried here; they live
[upstream](https://github.com/CBirkbeck/AINTLIB). None of the certified results depend on them.

---

## Toolchain

Lean `v4.33.0` (stable) and mathlib release tag `v4.33.0` (`db584cd6d46c`).

This is deliberate. The `v4.33` line is the first stable release line carrying the fix for
kernel soundness bug [leanprover/lean4#14576](https://github.com/leanprover/lean4/issues/14576)
— an axiom-free proof of `False` via unchecked projections on phantom-parameter nested
inductives, reported 2026-07-28 and fixed the same day in
[#14577](https://github.com/leanprover/lean4/pull/14577). Comparator is built on the same
toolchain, so the judging kernel and the judged development agree.

---

## On `sorry`

**Every certified statement — all fourteen — has a `sorry`-free proof closure.** This is not a
claim you have to take on trust: a `sorry` anywhere in a proof's closure shows up as the axiom
`sorryAx`, and both comparator runs pass with an axiom set of exactly
`[propext, Quot.sound, Classical.choice]`.

The wider library does contain `sorry`s, none of them on the certified results' path:

* the **Nonarchimedean Scottish Book** modules, which are open-problem *statements* by design;
* `Adic spaces/WP/HeadReduced.lean`, a quarantined conditional route to a rational stable
  reducedness claim that the current revision of the paper no longer makes;
* work-in-progress frontiers of the general adic-spaces development (the Wedhorn 8.28(b)
  campaign) that the two examples do not depend on.

As of this commit that is 155 declarations across the tree, none of them in the finite-jet
group and none on a certified proof's closure.

---

## Provenance

From the paper's abstract: *"The two main results are due to ChatGPT 5.6 Sol."* The Lean
formalisation was carried out by Claude Code. The paper's
[§9, How the examples were found](https://cbirkbeck.github.io/uniform-sheafy-tate-domains/#sec-discovery)
tells that story; `formalization.yaml` records the model, framework and cost caveats for the
formalisation side.

This repository is a standalone extract of the adic-spaces development in
[AINTLIB](https://github.com/CBirkbeck/AINTLIB), an AI-built and AI-maintained number-theory
library, where the work continues on the `announce/sheafy-not-stably-uniform` branch. The
extract carries the library and the certificates, and drops the monorepo's other projects and
its internal process files. It differs from the AINTLIB tree in exactly one mathematical
respect: the instance `Module.Flat.pi` (finite products of flat modules are flat), which
AINTLIB factors out into its shared `Common` library, is declared inline in
`Adic spaces/FlatnessResults.lean` here so that this repository has mathlib as its only
dependency.

## Licence

Apache 2.0 — see [`LICENSE`](LICENSE).
