# SIG4PY EXTERNAL GLUE LAYER V1

Status: canonical, NF, sealed, interoperability, external_glue.

## Core principle

sig4py does not absorb ecosystems.
sig4py orchestrates ecosystems through typed glue layers.

## Architecture

### Internal core

sig4py.core contains:
- typing
- orchestration
- gates
- trace
- runtime kernel
- quo
- Pi
- kapsyla

### External glue layer

sig4py.glue contains adapters for:
- scientific runtimes
- tensor libraries
- HPC systems
- quantum SDKs
- simulation frameworks
- orchestration tools

## Recommended structure

sig4py/
├── core/
├── gates/
├── projection/
├── runtime/
├── trace/
├── orchestration/
├── glue/
│   ├── qiskit/
│   ├── cirq/
│   ├── pennylane/
│   ├── pyzx/
│   ├── mitiq/
│   ├── tensor_networks/
│   ├── cudaq/
│   ├── mpi/
│   ├── openmp/
│   ├── hpc/
│   └── external/
├── benchmarks/
├── adapters/
└── manifests/

## External repository law

External repositories remain sovereign.
SIG4Py adds:
- adapters
- manifests
- orchestration
- interoperability
- benchmarks
- typed wrappers

## Canonical integration theorem

SIG4Py grows by adding bridges, not by collapsing ecosystems.

## Runtime philosophy

core stays minimal
glue stays modular
plurality stays external

## Compression

core computes
glue connects
ecosystems remain sovereign
