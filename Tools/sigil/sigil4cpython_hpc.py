#!/usr/bin/env python3
# SPDX-License-Identifier: PSF-2.0
"""SIGIL4CPython PYPL/HPC/OpenMPI compatibility contract.

The tool records an isolated, replay-safe compatibility surface for the
SIG4PYPL compiled/parallel projection layer. It does not modify CPython
interpreter semantics, launch a scheduler job, or claim performance results.
MPI execution occurs only when ``--mpi-smoke`` is explicitly requested.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

SCHEMA_VERSION = "sigil4cpython.pypl_hpc_openmpi.v1"
CONTRACT_ID = "SIGIL4CPYTHON_PYPL_HPC_OPENMPI_V1"
KERNEL_ID = "JARRAMPLAS_KERNEL"


@dataclass(frozen=True)
class CompatibilityProfile:
    """Explicit compatibility declaration; no implicit backend promotion."""

    implementation: str = "CPython"
    sigil_surface: str = "SIGIL4CPython"
    pypl_profile: str = "SIG4PYPL"
    hpc_profile: str = "optional_host_parallel_runtime"
    mpi_profile: str = "OpenMPI_via_mpi4py_optional"
    identity_kernel: str = KERNEL_ID
    replay_safe: bool = True
    no_identity_transport: bool = True
    no_scheduler_mutation: bool = True


def repository_root() -> Path:
    """Return the checked-out CPython repository root."""

    return Path(__file__).resolve().parents[2]


def source_tree_state(root: Optional[Path] = None) -> dict[str, Any]:
    """Inspect only stable source-tree witnesses required by this adapter."""

    root = (root or repository_root()).resolve()
    expected = {
        "readme": root / "README.rst",
        "configure": root / "configure",
        "interpreter_loop": root / "Python" / "ceval.c",
        "license": root / "LICENSE",
    }
    present = {name: path.is_file() for name, path in expected.items()}
    version_banner = "unknown"
    if expected["readme"].is_file():
        first_line = expected["readme"].read_text(encoding="utf-8").splitlines()[0].strip()
        if first_line:
            version_banner = first_line
    return {
        "root": str(root),
        "present": present,
        "complete": all(present.values()),
        "version_banner": version_banner,
    }


def host_parallel_state() -> dict[str, Any]:
    """Record optional host capabilities without treating them as authority."""

    return {
        "platform": platform.platform(),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "mpiexec": shutil.which("mpiexec") or shutil.which("mpirun"),
        "mpicc": shutil.which("mpicc"),
        "openmpi_visible": bool(
            shutil.which("mpiexec") or shutil.which("mpirun") or shutil.which("mpicc")
        ),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
        "scheduler_job_id_visible": any(
            os.environ.get(name)
            for name in ("SLURM_JOB_ID", "PBS_JOBID", "LSB_JOBID", "COBALT_JOBID")
        ),
    }


def build_contract(root: Optional[Path] = None) -> dict[str, Any]:
    """Build a deterministic compatibility contract."""

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID,
        "profile": asdict(CompatibilityProfile()),
        "source_tree": source_tree_state(root),
        "host_parallel_state": host_parallel_state(),
        "pypl_definition": {
            "name": "SIG4PYPL",
            "meaning": "SIGIL compiled and parallel Python projection layer",
            "boundary": "internal SIGIL profile; not PyPI and not an upstream CPython standard",
            "requirements": [
                "explicit_types",
                "trace_preserved",
                "pi_fixed",
                "projection_not_identity_transport",
                "backend_capabilities_recorded",
            ],
        },
        "hpc_boundary": {
            "single_rank_fallback": True,
            "openmp_optional": True,
            "openmpi_optional": True,
            "mpi4py_adapter_optional": True,
            "scheduler_mutation": False,
            "performance_claim_without_benchmark": False,
        },
        "jarramplas_boundary": {
            "kernel_id": KERNEL_ID,
            "jarrampli_role": "local_typed_projection",
            "identity_seed_transport": False,
            "plural_type_collapse": False,
        },
        "invariants": [
            "PI_FIXED",
            "SAFE_REPLAY",
            "TRACE_PRESERVED",
            "NO_IDENTITY_TRANSPORT",
            "NO_PLURAL_COLLAPSE",
            "NO_SCHEDULER_MUTATION",
            "CPYTHON_UPSTREAM_BOUNDARY_PRESERVED",
            "PSF_LICENSE_BOUNDARY_PRESERVED",
        ],
        "not_claimed": [
            "upstream_CPython_acceptance",
            "interpreter_semantics_changed",
            "OpenMPI_present_on_every_host",
            "cluster_scheduler_integration",
            "parallel_speedup",
            "scaling_efficiency",
            "physical_topological_protection",
        ],
    }
    body["contract_hash"] = _digest(body)
    return body


def verify_contract(document: Mapping[str, Any]) -> bool:
    """Verify the deterministic hash and hard contract boundaries."""

    try:
        body = dict(document)
        observed_hash = body.pop("contract_hash")
        if _digest(body) != observed_hash:
            return False
        profile = body["profile"]
        hpc = body["hpc_boundary"]
        jarramplas = body["jarramplas_boundary"]
        return all(
            (
                profile["replay_safe"],
                profile["no_identity_transport"],
                profile["no_scheduler_mutation"],
                hpc["single_rank_fallback"],
                hpc["scheduler_mutation"] is False,
                hpc["performance_claim_without_benchmark"] is False,
                jarramplas["identity_seed_transport"] is False,
                jarramplas["plural_type_collapse"] is False,
            )
        )
    except (KeyError, TypeError, ValueError):
        return False


def mpi_smoke() -> dict[str, Any]:
    """Run one explicit, finite mpi4py collective and emit its rank witness."""

    try:
        from mpi4py import MPI  # type: ignore
    except ImportError as exc:
        raise RuntimeError("mpi4py is required for --mpi-smoke") from exc

    comm = MPI.COMM_WORLD
    rank = int(comm.Get_rank())
    size = int(comm.Get_size())
    local = {
        "rank": rank,
        "size": size,
        "kernel_id": KERNEL_ID,
        "projection": "jarrampli_rank_%d" % rank,
        "projection_only": True,
        "replay_safe": True,
    }
    gathered = comm.allgather(local)
    ranks = sorted(int(item["rank"]) for item in gathered)
    valid = (
        size >= 1
        and len(gathered) == size
        and ranks == list(range(size))
        and all(item["kernel_id"] == KERNEL_ID for item in gathered)
        and all(item["projection_only"] and item["replay_safe"] for item in gathered)
    )
    result = {
        "schema_version": SCHEMA_VERSION,
        "kind": "explicit_openmpi_smoke_witness",
        "size": size,
        "ranks": gathered,
        "valid": valid,
        "collective": "allgather",
        "scheduler_mutated": False,
        "performance_claimed": False,
    }
    result["witness_hash"] = _digest(result)
    if not valid:
        raise RuntimeError("MPI rank witness failed validation")
    return result


def _digest(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print the compatibility contract")
    parser.add_argument(
        "--require-source-tree",
        action="store_true",
        help="fail unless the expected CPython source witnesses are present",
    )
    parser.add_argument(
        "--require-openmpi",
        action="store_true",
        help="fail unless an OpenMPI-compatible launcher/compiler is visible",
    )
    parser.add_argument(
        "--mpi-smoke",
        action="store_true",
        help="run the explicit finite mpi4py allgather witness",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parser().parse_args(argv)
    if args.mpi_smoke:
        document = mpi_smoke()
    else:
        document = build_contract()
        if args.require_source_tree and not document["source_tree"]["complete"]:
            print("incomplete CPython source tree", file=sys.stderr)
            return 2
        if args.require_openmpi and not document["host_parallel_state"]["openmpi_visible"]:
            print("OpenMPI-compatible runtime not visible", file=sys.stderr)
            return 3
        if not verify_contract(document):
            print("contract verification failed", file=sys.stderr)
            return 4
    if args.json or args.mpi_smoke:
        print(json.dumps(document, sort_keys=True, indent=2))
    else:
        print("%s: verified" % CONTRACT_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
