# SIGIL4CPython PYPL / HPC / OpenMPI compatibility surface

This directory adds an isolated compatibility and replay witness layer to the
`jbermejovega/sigil4cpython` CPython fork.

It does **not** modify interpreter semantics, claim upstream CPython acceptance,
or treat a parallel runtime as canonical authority.

## PYPL meaning

Within this repository contract, `PYPL` means **SIG4PYPL**, the internal SIGIL
compiled/parallel Python projection profile already used by SIGILBOOK. It is not
PyPI and it is not an official CPython standard.

The profile requires:

- explicit SIGIL/QUNOTYPE types;
- preserved provenance and replay traces;
- Π-fixed identity references;
- no identity transport;
- no plural-type collapse;
- explicit declaration of optional HPC backends.

## Runtime boundary

```text
JARRAMPLAS_KERNEL
  -> Jarrampli local typed projection
  -> SIG4PYPL compatibility contract
  -> optional single-process execution
  -> optional explicit mpi4py / OpenMPI smoke witness
```

OpenMPI is optional. A host without MPI remains valid for deterministic
single-rank replay. A distributed witness is generated only after an explicit
`mpiexec` invocation.

## Commands

Validate the source tree and print the contract:

```bash
python Tools/sigil/sigil4cpython_hpc.py --require-source-tree --json
```

Run the focused unit tests:

```bash
python Tools/sigil/test_sigil4cpython_hpc.py
```

After installing OpenMPI and `mpi4py`, run a finite two-rank witness:

```bash
mpiexec -n 2 python Tools/sigil/sigil4cpython_hpc.py --mpi-smoke
```

The same command can use a locally built interpreter:

```bash
mpiexec -n 2 ./python Tools/sigil/sigil4cpython_hpc.py --mpi-smoke
```

## Authority partition

| Surface | Role |
|---|---|
| CPython source tree | interpreter implementation and upstream-compatible source boundary |
| SIG4PYPL | internal compiled/parallel projection profile |
| HPC host | optional execution capability |
| OpenMPI / mpi4py | optional explicit rank transport and collective witness |
| scheduler | external capability; never mutated by this tool |
| Git | reviewed persistence surface |

## Hard invariants

```text
PI_FIXED
SAFE_REPLAY
TRACE_PRESERVED
NO_IDENTITY_TRANSPORT
NO_PLURAL_COLLAPSE
NO_SCHEDULER_MUTATION
CPYTHON_UPSTREAM_BOUNDARY_PRESERVED
PSF_LICENSE_BOUNDARY_PRESERVED
```

## Claim boundary

The compatibility tool records capabilities and runs a bounded `allgather`
smoke test. It does not establish performance, scalability, fault tolerance,
physical topological protection, or compatibility with every cluster.

The mask is projected; the kernel reference holds. 🌀
