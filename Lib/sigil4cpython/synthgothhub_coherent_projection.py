"""Dependency-free SIGIL4CPython projection of the SynthGothHub coherent sheaf."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Final

SCHEMA_ID: Final = "SIGIL4CPYTHON_SYNTHGOTHHUB_COHERENT_CYTHON_PROJECTION_V1"
AUTHOR_OWNER: Final = "Jara Juana Bermejo-Vega / JJBV"
SIGILBOOK_PR: Final = 695
SIGILBOOK_PAYLOAD_HEAD: Final = "3eaa72173eba1f91627c80b5e8359adeb140994e"
SEMANTIC_KERNEL_ID: Final = "SIGIL_PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK_KERNEL_V1"
PI_REF: Final = "PI:SYNTHGOTHHUB:COHERENT_SHEAF:CYTHON:V1"
PROJECTION_ID: Final = "SYNTHGOTHHUB_SIGIL4CPYTHON_PROJECTION_V1"
EXPECTED_END_LINE: Final = f"end {PROJECTION_ID}"
CYTHON_SOURCE_SHA256: Final = "71245c28f42685dde8531a96647b2c508517cd9885ac6492f450beb721560bfb"


@dataclass(frozen=True, slots=True)
class ProjectionReceipt:
    schema_id: str
    author_owner: str
    source_pull_request: int
    source_head: str
    target_repository: str
    projection_id: str
    semantic_kernel_id: str
    pi_ref: str
    end_line: str
    cython_source_sha256: str
    dependency_free_runtime: bool
    pydantic_stdlib_dependency_added: bool
    cython_stdlib_dependency_added: bool
    interpreter_semantics_changed: bool
    identity_transport: bool
    plural_collapse: bool
    runtime_executed: bool
    final_kapsyla: bool
    fixed_point_sha256: str


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def validate_projection_document(document: str) -> tuple[str, ...]:
    errors: list[str] = []
    lines = document.rstrip("\n").splitlines()
    if not lines or lines[-1] != EXPECTED_END_LINE:
        errors.append("EXACT_END_LINE_MISSING")
    if document.count(EXPECTED_END_LINE) != 1:
        errors.append("END_LINE_NOT_UNIQUE")
    required = {
        f"projection {PROJECTION_ID}",
        f"author {AUTHOR_OWNER}",
        f"source sigilbook#{SIGILBOOK_PR}@{SIGILBOOK_PAYLOAD_HEAD}",
        "target jbermejovega/sigil4cpython",
        f"kernel {SEMANTIC_KERNEL_ID}",
        f"pi {PI_REF}",
        "invariant NO_IDENTITY_TRANSPORT",
        "invariant NO_PLURAL_COLLAPSE",
        "invariant TRACE_PRESERVED",
        "invariant OBSTRUCTION_PRESERVED",
    }
    missing = sorted(required - set(lines))
    errors.extend(f"MISSING_LINE:{line}" for line in missing)
    return tuple(errors)


def build_receipt(document: str) -> ProjectionReceipt:
    errors = validate_projection_document(document)
    if errors:
        raise ValueError(";".join(errors))
    payload = {
        "schema_id": SCHEMA_ID,
        "author_owner": AUTHOR_OWNER,
        "source_pull_request": SIGILBOOK_PR,
        "source_head": SIGILBOOK_PAYLOAD_HEAD,
        "target_repository": "jbermejovega/sigil4cpython",
        "projection_id": PROJECTION_ID,
        "semantic_kernel_id": SEMANTIC_KERNEL_ID,
        "pi_ref": PI_REF,
        "end_line": EXPECTED_END_LINE,
        "cython_source_sha256": CYTHON_SOURCE_SHA256,
        "dependency_free_runtime": True,
        "pydantic_stdlib_dependency_added": False,
        "cython_stdlib_dependency_added": False,
        "interpreter_semantics_changed": False,
        "identity_transport": False,
        "plural_collapse": False,
        "runtime_executed": False,
        "final_kapsyla": False,
    }
    fixed = sha256(_canonical(payload).encode("utf-8")).hexdigest()
    return ProjectionReceipt(**payload, fixed_point_sha256=fixed)


def verify_fixed_point(receipt: ProjectionReceipt) -> bool:
    payload = {
        key: value
        for key, value in asdict(receipt).items()
        if key != "fixed_point_sha256"
    }
    return sha256(_canonical(payload).encode("utf-8")).hexdigest() == receipt.fixed_point_sha256
