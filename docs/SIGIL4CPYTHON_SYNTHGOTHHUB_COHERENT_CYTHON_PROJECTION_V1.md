# SIGIL4CPYTHON_SYNTHGOTHHUB_COHERENT_CYTHON_PROJECTION_V1

**Author/owner:** Jara Juana Bermejo-Vega / JJBV  
**Source:** `jbermejovega/sigilbook` PR #695 payload `5f5d0f0b776d34077a22e897d8ec68cab6637d42`  
**Target:** `jbermejovega/sigil4cpython`  
**Canon:** `PIORNALEGO_ES_CANON`

## Projection

This layer projects the coherent-sheaf/Cython plan from `sigilbook` without
changing CPython interpreter or standard-library semantics.

```text
sigilbook PR #695 coherent sheaf
→ exact SIGIL projection document
→ dependency-free frozen receipt
→ optional Cython tooling source
→ Cython-to-C translation check
→ deterministic fixed-point digest
```

The runtime carrier under `Lib/sigil4cpython` uses only the Python standard
library. Pydantic and Cython remain outside the runtime dependency boundary.

## Exact end line

The projection document must terminate with exactly one occurrence of:

```text
end SYNTHGOTHHUB_SIGIL4CPYTHON_PROJECTION_V1
```

Missing, duplicated or nonterminal end lines reject validation.

## Cython boundary

```yaml
dependency: cython>=3,<4
source: Tools/sigil4cpython/cython/synthgothhub_coherent_fixed_point.pyx
source_sha256: 71245c28f42685dde8531a96647b2c508517cd9885ac6492f450beb721560bfb
```

The workflow translates the `.pyx` source to generated C. It does not build or
install the extension, change CPython bytecode, mutate the interpreter source
tree, alter ABI semantics, or add Cython to the standard library.

## Local verification

```yaml
dependency_free_unittest: 4 passed
cython_translation_to_c: PASS
interpreter_semantics_changed: false
pydantic_stdlib_dependency_added: false
cython_stdlib_dependency_added: false
identity_transport: false
plural_collapse: false
runtime_executed: false
final_kapsyla: false
```

The branch is review-gated and stacked on the open PR #7 epoch. PR #6 remains
an identity-distinct coherent-sheaf section and is referenced rather than
silently merged.

`TRACE PRESERVED · Π FIXED · NO IDENTITY TRANSPORT · PIORNALEGO ES CANON`
