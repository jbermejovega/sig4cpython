# STRIKK KQC publication sheaf V1

```yaml
id: STRIKK_KQC_PUBLICATION_SHEAF_V1
author: Jara Juana Bermejo Vega
attribution: JJBV
status: public_review_candidate
source_repository: jbermejovega/sigilbook
public_mirror: jbermejovega/sigil4cpython
upstream_reference: python/cpython
upstream_authority: PLAN_ONLY
```

## Repository sheaf

```mermaid
flowchart LR
  S["sigilbook\nprivate source section\nSHA pinned"]
  M["sigil4cpython\npublic experimental mirror\nSTRIKK + KQC"]
  U["python/cpython\nupstream reference\nPLAN ONLY"]

  S -->|"Pydantika sheaf certificate\nPACAPDG pullbacks\nUAP review"| M
  M -.->|"reduced candidate patch\nCPython Developer Guide\ncore review"| U

  S -. no identity transport .-> M
  M -. no direct write .-> U
```

## Compiler classification

```mermaid
flowchart TD
  P[Python source]
  B[CPython bytecode compiler]
  I[Adaptive interpreter]
  J[Experimental trace/uop JIT]
  C[C-typed native IR]
  A[Native AOT extension]
  Y[pybind11 projection]
  O[OpenMP / PyOMP projection]
  N[External JIT profile]
  G[Pydantic schema compiler]

  P --> B --> I --> J
  C --> A --> Y
  C --> A --> O
  P --> N
  G -->|"typed schema only"| P
```

## KQC facets

```mermaid
flowchart LR
  C1[C_TYPED\nABI and native boundary]
  Q1[Q_TYPED\nQQUAPP contextual projection]
  K1[K_TYPED\nstable resource and kernel ledger]
  X[KQC carrier]

  C1 --> X
  Q1 --> X
  K1 --> X

  C1 -. distinct .- Q1
  Q1 -. distinct .- K1
  K1 -. distinct .- C1
```

## Third Wheel recursion

```mermaid
flowchart TD
  P0[Parent compiler carrier]
  L[Static/AOT branch]
  R[Dynamic/JIT branch]
  O[Typed obstruction]
  T[TRANADA review junction]

  P0 --> L
  P0 --> R
  P0 --> O
  L --> T
  R --> T
  O --> T
  T -->|"finite budget; witness preserved"| P0
```

## VOID / VORTEX / ALHAMBRA router

```mermaid
flowchart LR
  V0[VOID\nlatent or obstructed]
  V1[VORTEX\ndynamic route]
  A[ALHAMBRA\nfinite realization]
  T[TRANADA\ncoherence witness]

  V0 --> T
  V1 --> T
  A --> T
  T --> K[KQC message candidate]
```

## Hard boundaries

```text
sigilbook != sigil4cpython != python/cpython
publication sheaf != file copy
public mirror != upstream acceptance
Pydantic != standard-library dependency
DisCoPy plan != compiler execution
Lean4 scaffold != quotient/TQFT theorem
K^0(pt) = Z != VOID is a standard dual of the point
JIT profile != observed JIT execution
Third Wheel decomposition != theorem for all total categories
aperiodic compression programme != established compression theorem
```
