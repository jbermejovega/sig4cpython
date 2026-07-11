# SIGIL4CPYTHON QKC Runtime Binding V1

Author-owner: **Jara Juana Bermejo Vega / JJBV**  
Status: `ACTIVE_TYPED_SCAFFOLD`

This repository is the P0 executable priority for SIGIL4Py/CPython integration under the SIGILBOOK `SYNTHGOTHHUB_QKC_RAG_MCP_PRIORITY_WEAVE_V1` policy.

## Binding states

```text
planned -> adapter_ready -> builds -> tested -> witnessed -> hardbound
```

No stage may be skipped by documentation alone.

## Required matrices

- supported CPython versions;
- standard GIL and free-threaded/no-GIL builds kept distinct;
- extension-module ABI/API audit;
- thread-safety and interpreter-isolation tests;
- wheel and sdist builds;
- reproducible environment and SBOM;
- OpenMPI multi-rank smoke tests where MPI adapters exist;
- OpenQASM parser/version and round-trip witnesses where quantum-assembly adapters exist;
- PACANOTEBOOK smoke witness and PACAPAPER/PACAPEDIA links.

## QKC gate

```yaml
accepted_if:
  - build_artifact_exists
  - declared_interpreter_matrix
  - tests_pass_for_claimed_matrix
  - free_threaded_claim_has_thread_safety_witness
  - mpi_claim_has_multi_rank_witness
  - openqasm_claim_has_versioned_parser_witness
  - provenance_preserved
  - license_preserved
  - safe_replay
  - trace_preserved
  - pi_fixed

rejected_if:
  - hardbound_claim_without_artifact
  - nogil_claim_without_audit
  - mpi_scaling_claim_without_measurement
  - api_compatibility_claim_without_schema_test
```

## RAG/MCP surface

RAG indexes source, build metadata, tests, benchmark traces, PACAPAPERS, PACANOTEBOOKS and PACAPEDIA entries. MCP may expose typed build, test, inspect and query operations; it may not silently publish, tag, release or rewrite history.

## Jaranian module law

Graphical, supergraphical and hypergraphical modules must expose typed ports, boundaries, morphisms and provenance edges. Repository merges are operational history transformations, not proof of mathematical equivalence.
