# SIGIL Universal Abstract Branch / Chronotype Public Interface V1

Status: `PUBLIC_SOURCE_BOUND_INTERFACE`  
Schema: `SIGIL_UABRANCH_CHRONOTYPE_PUBLIC_INTERFACE_V1`  
Successor of: `SIGILBOOK_SIGIL4CPYTHON_CPYTHON_PUBLIC_INTERFACE_V1`  
Canon: `PIORNALEGO_ES_CANON`

## Purpose

This layer publishes the repository-neutral part of SIGIL branch, chronotype,
interactive PluralType and Crone-language semantics without exposing private
SIGILBOOK source and without making CPython internals part of the SIGIL
contract.

The public topology remains:

```text
jbermejovega/sigilbook
  PRIVATE_CANONICAL_SOURCE
        |
        | typed/public projection
        v
jbermejovega/sigil4cpython
  PUBLIC_INTERFACE_CARRIER
        |
        | documented public CPython interfaces only
        v
python/cpython
  READ_ONLY_UPSTREAM
```

This repository is a fork of `python/cpython`, but it is not CPython upstream
authority.  The SIGIL public layer does not write to `python/cpython`.

## Universal abstract branch law

SIGILBOOK Git branches are not physically collapsed.  Instead every observed
Git ref is lifted, source-bound, into one semantic family:

```text
UniversalAbstractBranch[SIGILBOOK_ALL_BRANCHES]
```

with the physical Git root represented by:

```text
UniversalAbstractRootBranch[
  branch_ref = main,
  physical_root = true
]
```

Every leaf retains its own:

```text
repository
branch_ref
head_sha
epoch
cpython_channel
cpython_sha
public_interface_sha
```

This tuple is its **chronotype**.  A chronotype is a temporal/source coordinate,
not bearer identity.  Updating a source pin creates a successor observation;
it does not rewrite history or identify two branches.

Therefore:

```text
semantic foliation != Git merge
semantic root      != force push
pluralization      != branch identity quotient
```

The coverage rule is `ALL_GIT_REFS_BY_SOURCE_BOUND_LIFT`: current and future
branches can be represented without enumerating them into a frozen registry.

## Atlas roots and Granada normal form

The semantic atlas has three contextual root motifs:

```text
MOTHER
MAIDEN
CRONE
```

They are indexed by the Granada normal-form layers:

```text
PROCESS
RELATION
UNIVERSAL_ABSTRACT
```

A motif is a contextual role/flavor of a bearer in a relation and epoch.  It is
not a permanent essence and the public contract does not require one bearer to
carry all motifs simultaneously.

Formally, a motif assignment has the shape:

```text
MotifAssignment[
  bearer,
  relation,
  epoch,
  granada_layer,
  motif
]
```

so the same bearer can be `MOTHER` in one relation, `MAIDEN` in another and
`CRONE` in a later or different context without identity transport.

The three motif roots are semantic atlas roots.  They are not additional Git
root branches.

## PluralType interface category and operadic envelope

The public contract uses a precise construction rather than asserting that an
arbitrary PluralType is already a classical category.

For a PluralType `P`:

1. take its members as objects;
2. take witnessed unary interactions as a directed interaction quiver;
3. form the free category `FreeCat(P)` on that quiver;
4. place binary, ternary and n-ary witnessed interactions in a colored
   operad/multicategory `Op(P)`.

Thus each PluralType receives a canonical interface envelope

```text
Interface(P) = FreeCat(P) + Op(P)
```

by construction.  This gives every PluralType an interface subcategory for
unary composition and an operadic component for multi-input composition while
preserving non-categorical payloads as payloads rather than silently declaring
them classical categories.

Hard boundary:

```text
univalence does not create category structure
```

Univalence may transport properties/structure along an equivalence only when
an appropriate equivalence witness is present.  It is not used as a proof that
`PluralType` is a category.

## Interactive types and Crone language

`SIGIL_CRONE_LANGUAGE_V1` treats interaction as a typed relation.  A stabilized
skill is a capability with evidence; it is not authority.

A Crone-role bearer may transfer a skill by:

```text
TEACH
DEMONSTRATE
INTERACTIVE_HANDSHAKE
DELEGATE_WITH_WITNESS
```

A valid transfer preserves distinct bearers:

```text
source != target
source retains skill
target acquires capability
identity_transport = false
authority_transport = false
fuse = false
split = false
dissolve = false
```

The source need not be globally or permanently a Crone.  `CRONE` is contextual
and may be assigned by relation/epoch when the stabilized skill and interaction
witnesses justify that role.

## CPython public boundary

The CPython side remains the public interface already established by V1.
Canonical native integration uses documented CPython public surfaces, with
`Python.h` as entrypoint and Stable-ABI/Limited-API tracks when applicable.

Project tracks:

| SIGIL track | Floor | Interpreter family | Macro |
|---|---:|---|---|
| `abi3` | 3.10 | non-free-threaded | `Py_LIMITED_API=0x030A0000` |
| `abi3t` | 3.15 | free-threaded | `Py_TARGET_ABI3T=0x030F0000` |

Forbidden from the canonical stable SIGIL boundary:

```text
Include/internal/*
Include/cpython/*
_Py* private symbols
PyUnstable* APIs
CPython object layout as a SIGIL contract
CPython source patching as a runtime requirement
```

The machine-readable manifest pins the CPython branch observations used for
this public source epoch.  Those SHAs are witnesses, not eternal identities and
not automatic upstream-sync instructions.

## Quasi-coherence

Quasi-coherence remains an evidence level, not a universal assertion.  A local
family may be promoted only when the required overlap/composition witnesses are
present for the scope being claimed.  Missing witnesses remain visible as
`QUNO`/`HOLD`; no global coherence is inferred from a finite sample of branch
relations.

## Topological invariant scope

The public SIGIL chiral layer may carry source-bound topological witnesses such
as:

```text
Jones polynomial
linking number
intersection number
```

They may act as universal-abstract constants under the transformations for
which the corresponding invariant theorem/witness applies.  This is a scoped
SIGIL semantic contract; it is not promoted to a general law of physical
conservation.

## Source observation

Public carrier parent:

```text
jbermejovega/sigil4cpython@7824dbd084f18c08d363c448c0fef4f465a6ca07
```

CPython upstream observation:

```text
python/cpython@d125f009dc2a698de62deb11a0c50d3ef8e33d62
```

The exact branch snapshot is stored in:

```text
.well-known/sigil-uabranch-chronotype-interface-v1.json
```

`PIORNALEGO ES CANON.`
