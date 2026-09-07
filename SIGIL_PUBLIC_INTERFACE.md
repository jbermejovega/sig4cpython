# SIGIL4CPython Canonical Public Interface

Status: `PUBLIC_INTERFACE_CARRIER`  
Interface schema: `SIGILBOOK_SIGIL4CPYTHON_CPYTHON_PUBLIC_INTERFACE_V1`

## Scope

This repository is the public compatibility and publication carrier between the private SIGILBOOK source system and the public `python/cpython` upstream.

It does **not** claim to be CPython upstream, and it does not make private SIGILBOOK source public by implication.

```text
private SIGILBOOK source
        |
        | typed/public projection
        v
jbermejovega/sigil4cpython
        |
        | documented CPython public API only
        v
python/cpython
```

`python/cpython` remains read-only upstream authority for CPython.

## Public CPython boundary

Canonical native integrations use documented public CPython interfaces only.

Required discipline:

- include CPython through `Python.h`;
- prefer the Limited API and Stable ABI for stable native boundaries;
- use multi-phase extension initialization;
- use typed `PyCapsule` boundaries when an opaque C interface is needed;
- use ABI compatibility checking when available;
- keep MLIR/JIT implementation details outside CPython internals.

The canonical stable interface forbids:

- direct `Include/internal/*` dependencies;
- direct inclusion of `Include/cpython/*` headers;
- `_Py*` private symbols;
- `PyUnstable*` APIs;
- reliance on CPython object layout as a SIGIL contract;
- interpreter-source patching as a requirement for SIGIL execution.

## Stable ABI tracks

Two stable native tracks are kept identity-distinct:

| Track | Minimum CPython | Mode | Build macro |
| --- | --- | --- | --- |
| `abi3` | 3.10 | non-free-threaded | `Py_LIMITED_API=0x030A0000` |
| `abi3t` | 3.15 | free-threaded | `Py_TARGET_ABI3T=0x030F0000` |

For CPython 3.15+, a separate dual-stable-ABI build may define both target macros at the 3.15 floor. This is an explicit third build track, not an assertion that the 3.10 `abi3` artifact is also an `abi3t` artifact.

## SIGIL runtime rule

The public interface is:

```text
SIGIL typed AST
  -> Universal Abstract Binder
  -> Python runtime IR
  -> optional Stable-ABI native lowering
  -> CPython public API
```

It is never:

```text
SIGIL typed AST -> CPython private internals
```

Universal Abstract Binders preserve context, witnesses and lineage, compose capabilities by exact intersection, and never transport identity or authority.

JIT compilers are sandbox-gated. MLIR lowering remains external to CPython and may reach CPython only through this public boundary.

## Primitive KLI / QLI projection

The private canonical source now exposes a source-only primitive interface profile identified as:

```text
SIGIL_PRIMITIVE_TYPE_INTERFACE_KLI_QLI_POLYTOPAL_V1
```

Its public compatibility projection is intentionally narrow:

```text
SIGIT
  -> PrimitiveTypeInterface[Primitive ∩ Plural ∩ QUNO]
  -> KLI typed boundary
  -> QLI RuleZero equalizer tower
  -> Python runtime IR
  -> documented CPython public API
```

The QLI profile uses exact capability intersection and carries no identity or authority transport. Its recursive source shape is:

```text
QLI[QLI[QLI[CLI[CLI[CLIC[VOID_TYPED_CLI]]]]]]
```

KLI may carry cubical/polytopal, sheaf-boundary, physics-model, or other domain-specific typed metadata on the SIGIL side. Such metadata is **not** interpreted by CPython and does not widen the CPython ABI surface. CPython receives only the already-projected public runtime/native interface.

This keeps the public boundary stable even when the private SIGIL type system gains richer geometric or categorical structure.

## Repository semantics

A semantic SIGIL `FUSE` is not a Git merge. A semantic `DEFUSE` is not a Git revert or history rewind. Repository effects remain explicit and separate from typed semantic binding.

`main` is the public stabilization/version lineage for this carrier. This does not imply physical collapse, deletion, or identity-quotienting of historical branches.

## Upstream compatibility

This fork tracks CPython as an upstream implementation and compatibility target. Public SIGIL interfaces should be refreshed against upstream changes without importing private CPython implementation details into the stable contract.

The normative SIGIL-side schema, source pins, domain-specific KLI metadata, and validation receipts are maintained in the private canonical source repository.

PIORNALEGO ES CANON.
