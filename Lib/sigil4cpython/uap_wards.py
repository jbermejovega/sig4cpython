"""Kokompiled UAP ward kernels for SIGIL4CPython.

The module provides a small, deterministic metadata kernel for SIGIL runtime
guardrails.  It deliberately stays out of CPython's evaluator and object model:
the output is a canonical dictionary that agents, CI and MCP surfaces can check
before they reuse generated review or research artifacts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Mapping, Sequence


DEFAULT_CLAIM_BOUNDARY = (
    "diagnostic_kernel_not_final_grade",
    "ci_pass_not_scientific_certification",
    "similarity_not_misconduct_evidence",
    "missing_trace_preserved_as_obstruction",
    "human_review_required_for_assessment",
)


@dataclass(frozen=True, slots=True)
class UAPWard:
    """A typed guardrail attached to a kokompiled kernel."""

    ward_id: str
    invariant: str
    source: str
    status: str = "active"
    witness: str = ""


@dataclass(frozen=True, slots=True)
class UAPWardVerdict:
    """Result of a single ward check."""

    ward_id: str
    passed: bool
    reason: str


@dataclass(frozen=True, slots=True)
class KokompiledKernel:
    """Canonical SIGIL kernel payload.

    Vertices and hyperedges are metadata only.  They model UAP boundaries and
    review-flow incidence; they do not assert mathematical certification by
    themselves.
    """

    kernel_id: str
    vertices: tuple[str, ...]
    hyperedges: tuple[tuple[str, ...], ...]
    wards: tuple[UAPWard, ...]
    claim_boundary: tuple[str, ...]
    max_duality_vertices: int = 16

    def to_dict(self) -> dict[str, object]:
        payload = {
            "kernel_id": self.kernel_id,
            "vertices": list(self.vertices),
            "hyperedges": [list(edge) for edge in self.hyperedges],
            "wards": [asdict(ward) for ward in self.wards],
            "claim_boundary": list(self.claim_boundary),
            "max_duality_vertices": self.max_duality_vertices,
        }
        payload["kernel_sha256"] = stable_digest(payload)
        return payload


def _normalize_tokens(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(value).strip() for value in values if str(value).strip()}))


def _normalize_edges(edges: Iterable[Iterable[str]]) -> tuple[tuple[str, ...], ...]:
    normalized = {_normalize_tokens(edge) for edge in edges}
    normalized.discard(())
    return tuple(sorted(normalized, key=lambda edge: (len(edge), edge)))


def stable_digest(payload: Mapping[str, object]) -> str:
    """Return a stable digest for JSON-compatible kernel metadata."""

    encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def kokompile_kernel(
    kernel_id: str,
    vertices: Iterable[str],
    hyperedges: Iterable[Iterable[str]],
    wards: Sequence[UAPWard],
    claim_boundary: Iterable[str] = DEFAULT_CLAIM_BOUNDARY,
    max_duality_vertices: int = 16,
) -> KokompiledKernel:
    """Normalize a SIGIL/UAP kernel into canonical immutable form."""

    normalized_vertices = _normalize_tokens(vertices)
    vertex_set = set(normalized_vertices)
    normalized_edges = _normalize_edges(hyperedges)
    unknown = sorted({vertex for edge in normalized_edges for vertex in edge if vertex not in vertex_set})
    if unknown:
        raise ValueError(f"hyperedge references unknown vertices: {', '.join(unknown)}")
    if max_duality_vertices < 1:
        raise ValueError("max_duality_vertices must be positive")
    return KokompiledKernel(
        kernel_id=str(kernel_id).strip(),
        vertices=normalized_vertices,
        hyperedges=normalized_edges,
        wards=tuple(wards),
        claim_boundary=_normalize_tokens(claim_boundary),
        max_duality_vertices=max_duality_vertices,
    )


def check_uap_wards(kernel: KokompiledKernel) -> tuple[UAPWardVerdict, ...]:
    """Check core UAP ward invariants for a kokompiled kernel."""

    boundary = set(kernel.claim_boundary)
    ward_ids = [ward.ward_id for ward in kernel.wards]
    verdicts = [
        UAPWardVerdict("kernel_id_present", bool(kernel.kernel_id), "kernel_id must be non-empty"),
        UAPWardVerdict("vertices_present", bool(kernel.vertices), "kernel must have vertices"),
        UAPWardVerdict("wards_present", bool(kernel.wards), "kernel must have wards"),
        UAPWardVerdict("ward_ids_unique", len(ward_ids) == len(set(ward_ids)), "ward ids must be unique"),
        UAPWardVerdict(
            "ward_trace_complete",
            all(ward.invariant and ward.source for ward in kernel.wards),
            "each ward needs invariant and source",
        ),
        UAPWardVerdict(
            "obstructions_keep_witness",
            all(ward.witness for ward in kernel.wards if ward.status in {"blocked", "obstruction"}),
            "blocked or obstruction wards must keep a witness",
        ),
        UAPWardVerdict(
            "no_grade_authority",
            "diagnostic_kernel_not_final_grade" in boundary,
            "kernel must not finalize grades",
        ),
        UAPWardVerdict(
            "no_similarity_misconduct_claim",
            "similarity_not_misconduct_evidence" in boundary,
            "similarity is context, not misconduct evidence",
        ),
        UAPWardVerdict(
            "bounded_duality",
            len(kernel.vertices) <= kernel.max_duality_vertices,
            "finite guardrail must stay within the declared duality bound",
        ),
    ]
    return tuple(verdicts)


def validate_kokompiled_kernel(kernel: KokompiledKernel) -> dict[str, object]:
    """Return a validated kernel dictionary or raise ``ValueError``."""

    verdicts = check_uap_wards(kernel)
    failures = [verdict for verdict in verdicts if not verdict.passed]
    if failures:
        reasons = "; ".join(f"{item.ward_id}: {item.reason}" for item in failures)
        raise ValueError(f"UAP ward validation failed: {reasons}")
    payload = kernel.to_dict()
    payload["uap_wards"] = [asdict(verdict) for verdict in verdicts]
    payload["accepted"] = True
    return payload


def build_pacadocencia_uap_kernel() -> KokompiledKernel:
    """Build the PACA DOCENCIA bridge kernel used by sigilbook review flows."""

    vertices = (
        "student_identity",
        "repository_identity",
        "evidence_trace",
        "rubric_boundary",
        "execution_status",
        "embargo_boundary",
        "human_review",
        "diagnostic_embedding",
        "hypergraph_duality",
        "annihilator_guardrail",
        "mcp_resource",
        "n8n_resource",
    )
    hyperedges = (
        ("student_identity", "repository_identity", "evidence_trace"),
        ("rubric_boundary", "human_review", "embargo_boundary"),
        ("diagnostic_embedding", "human_review"),
        ("hypergraph_duality", "annihilator_guardrail", "evidence_trace"),
        ("mcp_resource", "n8n_resource", "execution_status"),
        ("execution_status", "evidence_trace"),
    )
    wards = (
        UAPWard(
            "safe_replay",
            "diagnostic artifacts do not finalize grades",
            "sigilbook:pacadocencia",
        ),
        UAPWard(
            "trace_preservation",
            "missing execution traces remain visible obstructions",
            "sigilbook:COMPU2526_REVIEW_HYPERDAG",
        ),
        UAPWard(
            "duality_bound",
            "bounded hypergraph duality stays below max_duality_vertices",
            "sigil4py.pacadocencia.duality",
        ),
    )
    return kokompile_kernel(
        "SIGIL4CPYTHON_PACADOCENCIA_UAP_WARDS_V1",
        vertices,
        hyperedges,
        wards,
    )
