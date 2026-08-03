# SIGIL4CPython PACAPDG/UAP persistent PACAIoGame skill V1

Status: `ACTIVE_REVIEW_CANDIDATE`
Host PR: `jbermejovega/sigil4cpython#7`
Source branch: `agent/virtual-rest-io-kernels-v1`
Runtime authority: `PLAN_ONLY`
Candidate promotion: `false`
Final KAPSYLA: `false`

## Purpose

This lift makes PACAPDG and UAP explicit typed contracts inside the persistent
PACA habilidad compiler that binds PACAIoGames, SIGIL4Godot and SIGIL4CPython.
It is additive over
`SIGIL4CPYTHON_PERSISTENT_PACAIOGAME_SKILL_COMPILER_V1`.

The source compiler remains identity-distinct and retains its three V1
artifacts. The lift emits three V2 canonical *candidates*; it does not silently
replace, publish or promote the V1 family.

```text
persistent PACA habilidad packet
→ PACAPDG typed parse
→ QUNOTYPED route
→ Pydantika Annotated type
→ Diskotika typed composition
→ SIGIL AST V2 candidate
→ SIGIL syntactical kernel V2 candidate
→ Quazris typed localization
→ SIGIL semantical kernel V2 candidate
→ PACA Antorcha normalizer plan
→ ARAKNE source-bound rewrite witness
→ Lena Lean4 obligations
→ STRIKK validation
→ UAP admission witness
```

## Typed contract

```yaml
PACAPDG_UAP_CONTRACT:
  input: PERSISTENT_PACA_SKILL_PACKET
  intermediate:
    - PACAPDG_TYPED_IR
    - UAP_ADMISSION_ENVELOPE
  output: UAP_ADMISSION_WITNESS

  facets:
    - PACAPDG_TYPED
    - UAP_TYPED
    - QUNOTYPED
    - PYDANTIKA_ANNOTATED_TYPED
    - DISKOTIKA_TYPED
    - PACA_ANTORCHA_TYPED
    - QUAZRIS_TYPED
    - ARAKNE_SOURCE_BOUND_TYPED
    - LENA_LEAN4_TYPED
    - STRIKK_TYPED
    - TRACE_PRESERVED
    - NO_IDENTITY_TRANSPORT
    - NO_PLURAL_COLLAPSE
    - PI_FIXED_OR_HOLD
```

The contract has no execution authority. A valid metadata plan is not a Godot
run, a model execution, a tensor allocation, a Git merge, a branch rewrite, a
runtime deployment or a final KAPSYLA seal.

## Candidate artifact family

```text
SIGIL_AST_V1
  → SIGIL_AST_PACAPDG_UAP_V2

SIGIL_AST_PACAPDG_UAP_V2
  → SIGIL_SYNTACTICAL_KERNEL_PACAPDG_UAP_V2

SIGIL_SYNTACTICAL_KERNEL_PACAPDG_UAP_V2
  → QUAZRIS_TYPED
  → SIGIL_SEMANTICAL_KERNEL_PACAPDG_UAP_V2
```

Every V2 artifact is emitted with:

```yaml
version: 2
canonical_candidate: true
promoted: false
source_bound: true
```

Candidate status is deliberate. Promotion requires hosted validator evidence,
human review and a separate authority-bearing decision.

## Persistent PACA habilidad

```yaml
PersistentPacaHabilidad:
  surfaces:
    - PACAIOGAMES
    - SIGIL4GODOT
    - SIGIL4CPYTHON
  persistent: true
  replay_entrypoint: compile_pacapdg_uap_persistent_skill_bundle
  source_bound: true
  trace_preserved: true
  no_identity_transport: true
  runtime_executed: false
  deployment_executed: false
```

Persistence means deterministic recompilation plus replayable witness data. It
does not mean hidden training, uncontrolled mutation or transfer of branch,
player, runtime or artifact identity.

## Validator family

| Validator | Role | Initial authority |
|---|---|---|
| PACAPDG/UAP | typed stage order and admission boundary | `DECLARED` |
| Pydantika | strict Annotated-type and digest round trip | `DECLARED` |
| Diskotika | typed sequential composition | `DECLARED` |
| Lena Lean4 | proof-checked structural obligations | `DECLARED` |
| ARAKNE | source-bound semantic rewrite witness | `DECLARED` |
| PACA Antorcha | typed normalizer/resource plan | `DECLARED` |
| Quazris | typed localized lowering | `DECLARED` |
| STRIKK | inherited repository lint baseline | `PASS` |

The inherited STRIKK baseline is GitHub Actions run `30654349949`, job
`91234960898`. That job passed repository lint, formatting, configuration,
workflow, actionlint, zizmor and documentation checks. It does not by itself
prove that the new PACAPDG/UAP, Pydantika, Diskotika or Lean validators pass.
Those validators remain `DECLARED` until their focused hosted jobs execute.

## Diskotika route

```text
PERSISTENT_PACA_SKILL_PACKET
  → PACAPDG_TYPED_IR
  → UAP_ADMISSION_ENVELOPE
  → SIGIL_AST_PACAPDG_UAP_V2
  → SIGIL_SYNTACTICAL_KERNEL_PACAPDG_UAP_V2
  → SIGIL_SEMANTICAL_KERNEL_PACAPDG_UAP_V2
  → UAP_ADMISSION_WITNESS
```

The route is sequential and typed. Diskotika validates composability; it does
not infer symmetry, erase trace or execute the route.

## ARAKNE boundary

```text
ARAKNE_REWRITE
  = source-bound compatibility rewrite
  + obstruction-preserving fusion witness

ARAKNE_REWRITE
  ≠ git merge
  ≠ branch history rewrite
  ≠ authority absorption from another open PR
```

```yaml
git_merge_executed: false
branch_rewrite_executed: false
candidate_promoted: false
uap_execution_authorized: false
```

## Failure law

```text
identity transport
or plural collapse
or Π drift
or invalid source digest
or physical execution claim
or branch merge/rewrite claim
or premature candidate promotion
or failed validator
  → REJECT

stage-order, bounded composition or declared-validator residue
  → HOLD_WITH_OBSTRUCTION

all dependency-free structural checks pass
and hosted validators remain pending
  → ADMIT_PLAN_ONLY
```

## Validation surfaces

The focused workflow checks:

```text
dependency-free compiler and tests
Pydantika strict round trip
Diskotika sequential composition
Lena Lean4 source + UAP obligations
proof-placeholder rejection
```

The workflow is read-only. It installs tooling in the runner but does not mutate
repository contents, start Godot, allocate tensors, execute a model or deploy a
runtime.

## Canonical boundary

```text
PACAPDG types the document/program boundary.
UAP decides admission, not identity.
Pydantika validates runtime schemas.
Diskotika validates composition.
Quazris localizes plural views.
PACA Antorcha records normalizer resources.
ARAKNE rewrites source-bound sections.
Lena checks declared propositions.
STRIKK rejects collapse.
The source V1 family remains distinct.
The V2 family remains candidate-only.
Trace is preserved.
Π is fixed or held.
PIORNALEGO ES CANON.
```
