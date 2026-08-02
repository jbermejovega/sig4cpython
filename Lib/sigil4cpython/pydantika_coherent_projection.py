"""Dependency-free Annotated projection of the Pydantika coherent sheaf.

The canonical validator remains in sigilbook/SIGIL4Py. This module projects its
finite schema into the public SIGIL4CPython mirror using only the Python
standard library. It does not import Pydantic and does not alter CPython
interpreter, bytecode, compiler, ABI, or standard-library semantics.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
from hashlib import sha256
import json
import re
from typing import Annotated, Literal


SCHEMA_ID = "SIGIL4CPYTHON_PYDANTIKA_COHERENT_SHEAF_PROJECTION_V1"
SEMANTIC_KERNEL_ID = "SIGILITAS_PYDANTIKA_COHERENT_SHEAF_KERNEL_V1"
AUTHOR = "Jara Juana Bermejo Vega / JJBV"
SOURCE_REPOSITORY = "jbermejovega/sigilbook"
SOURCE_BRANCH = "agent/sigilitas-vortice-taller-twerk-canonical-release-v1"
SOURCE_SHA = "040117f2620b517182b7eb7d551d27b05ac0216d"
TARGET_REPOSITORY = "jbermejovega/sigil4cpython"
_SHA1 = re.compile(r"^[a-f0-9]{40}$")

Identifier = Annotated[str, "pydantika:identifier", "min_length=1"]
TraceRef = Annotated[str, "pydantika:trace_ref", "min_length=1"]
GitSha = Annotated[str, "pydantika:git_sha", "pattern=^[a-f0-9]{40}$"]


class ProjectionVerdict(str, Enum):
    ADMIT = "ADMIT_ANNOTATED_COHERENT_PROJECTION"
    HOLD = "HOLD_WITH_PROJECTION_OBSTRUCTION"
    REJECT = "REJECT_INVALID_ANNOTATED_PROJECTION"


@dataclass(frozen=True, slots=True)
class AnnotatedKernelSection:
    section_id: Identifier
    kernel_kind: Identifier
    context_id: Identifier
    semantic_kernel_id: Literal[
        "SIGILITAS_PYDANTIKA_COHERENT_SHEAF_KERNEL_V1"
    ]
    trace_ref: TraceRef
    projection_only: bool
    pi_fixed: bool = True
    no_identity_transport: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not all(
            (
                self.section_id,
                self.kernel_kind,
                self.context_id,
                self.semantic_kernel_id,
                self.trace_ref,
            )
        ):
            errors.append(f"incomplete_section:{self.section_id}")
        if self.semantic_kernel_id != SEMANTIC_KERNEL_ID:
            errors.append(f"semantic_kernel_mismatch:{self.section_id}")
        if not self.pi_fixed:
            errors.append(f"pi_not_fixed:{self.section_id}")
        if not self.no_identity_transport:
            errors.append(f"identity_transport:{self.section_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class AnnotatedRestriction:
    witness_id: Identifier
    source_section: Identifier
    target_section: Identifier
    trace_ref: TraceRef
    preserves_annotations: bool = True
    preserves_trace: bool = True
    pi_fixed: bool = True
    identity_transport: bool = False

    def validate(self, known: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if self.source_section not in known or self.target_section not in known:
            errors.append(f"unknown_endpoint:{self.witness_id}")
        if self.source_section == self.target_section:
            errors.append(f"self_projection:{self.witness_id}")
        if not all(
            (
                self.preserves_annotations,
                self.preserves_trace,
                self.pi_fixed,
            )
        ):
            errors.append(f"restriction_invariant_failure:{self.witness_id}")
        if self.identity_transport:
            errors.append(f"restriction_identity_transport:{self.witness_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class VoidOuroborosProjection:
    flow_id: Literal["PYDANTIKA_VOID_TYPED_OUROBOROS_FLOW_V1"]
    void_type: Literal["VOID"]
    finite_budget: int
    recur_requires_decreasing_residue: bool
    error_history_append_only: bool
    budget_reset_allowed: bool
    runtime_executed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.finite_budget < 1:
            errors.append("ouroboros_budget_must_be_positive")
        if not self.recur_requires_decreasing_residue:
            errors.append("ouroboros_requires_decreasing_residue")
        if not self.error_history_append_only:
            errors.append("ouroboros_error_history_must_be_append_only")
        if self.budget_reset_allowed:
            errors.append("ouroboros_budget_reset_forbidden")
        if self.runtime_executed:
            errors.append("projection_does_not_execute_ouroboros")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PydantikaCoherentProjection:
    schema_id: Literal[
        "SIGIL4CPYTHON_PYDANTIKA_COHERENT_SHEAF_PROJECTION_V1"
    ]
    author_owner: Literal["Jara Juana Bermejo Vega / JJBV"]
    source_repository: Literal["jbermejovega/sigilbook"]
    source_branch: Literal[
        "agent/sigilitas-vortice-taller-twerk-canonical-release-v1"
    ]
    source_sha: GitSha
    target_repository: Literal["jbermejovega/sigil4cpython"]
    sections: tuple[AnnotatedKernelSection, ...]
    restrictions: tuple[AnnotatedRestriction, ...]
    ouroboros: VoidOuroborosProjection
    dependency_free: bool = True
    interpreter_semantics_changed: bool = False
    runtime_executed: bool = False
    upstream_write: bool = False
    trace_preserved: bool = True
    pi_fixed: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.schema_id != SCHEMA_ID or self.author_owner != AUTHOR:
            errors.append("schema_or_author_mismatch")
        if (
            self.source_repository != SOURCE_REPOSITORY
            or self.source_branch != SOURCE_BRANCH
            or self.source_sha != SOURCE_SHA
        ):
            errors.append("source_pin_mismatch")
        if not _SHA1.fullmatch(self.source_sha):
            errors.append("invalid_source_sha")
        if self.target_repository != TARGET_REPOSITORY:
            errors.append("target_repository_mismatch")

        ids = [section.section_id for section in self.sections]
        if len(ids) != len(set(ids)):
            errors.append("section_ids_not_unique")
        required = {
            "SIGILBOOK_KERNEL",
            "SIGIL4PY_KERNEL",
            "SIGIL4GODOT_KERNEL",
            "PACA_ESTACA_KERNEL_FAMILY",
            "SIGIL4CPYTHON_KERNEL",
            "UNIVERSAL_ABSTRAKTA_AESTHETIK_KERNEL",
            "SYNTHGOTHHUB_ROUTER",
        }
        if set(ids) != required:
            errors.append("finite_cover_mismatch")

        known = set(ids)
        for section in self.sections:
            errors.extend(section.validate())
        for restriction in self.restrictions:
            errors.extend(restriction.validate(known))
        errors.extend(self.ouroboros.validate())

        if not all(
            (
                self.dependency_free,
                self.trace_preserved,
                self.pi_fixed,
            )
        ):
            errors.append("projection_boundary_missing")
        if any(
            (
                self.interpreter_semantics_changed,
                self.runtime_executed,
                self.upstream_write,
            )
        ):
            errors.append("forbidden_projection_effect")
        return tuple(errors)

    def digest(self) -> str:
        payload = json.dumps(
            asdict(self),
            sort_keys=True,
            separators=(",", ":"),
        )
        return sha256(payload.encode()).hexdigest()


def build_pydantika_coherent_projection() -> PydantikaCoherentProjection:
    specifications = (
        ("SIGILBOOK_KERNEL", "SIGILBOOK", "SIGILITAS_SOURCE_CONTEXT", False),
        ("SIGIL4PY_KERNEL", "SIGIL4PY", "SIGIL4PY_RUNTIME_CONTEXT", False),
        (
            "SIGIL4GODOT_KERNEL",
            "SIGIL4GODOT",
            "SIGIL4GODOT_RENDER_CONTEXT",
            True,
        ),
        (
            "PACA_ESTACA_KERNEL_FAMILY",
            "PACA_ESTACA",
            "PACA_ESTACA_CELL_CONTEXT",
            True,
        ),
        (
            "SIGIL4CPYTHON_KERNEL",
            "SIGIL4CPYTHON",
            "SIGIL4CPYTHON_PROJECTION_CONTEXT",
            True,
        ),
        (
            "UNIVERSAL_ABSTRAKTA_AESTHETIK_KERNEL",
            "UNIVERSAL_ABSTRAKTA_PLURAL_AESTHETIK",
            "PLURAL_AESTHETIK_CONTEXT",
            True,
        ),
        (
            "SYNTHGOTHHUB_ROUTER",
            "SYNTHGOTHHUB",
            "QQUAPP_CROSS_REPOSITORY_CONTEXT",
            True,
        ),
    )
    sections = tuple(
        AnnotatedKernelSection(
            section_id=section_id,
            kernel_kind=kind,
            context_id=context,
            semantic_kernel_id=SEMANTIC_KERNEL_ID,
            trace_ref=f"trace://sigil4cpython/{section_id.lower()}",
            projection_only=projection_only,
        )
        for section_id, kind, context, projection_only in specifications
    )
    restrictions = tuple(
        AnnotatedRestriction(
            witness_id=f"R_CPYTHON_{index}",
            source_section=sections[0].section_id,
            target_section=target.section_id,
            trace_ref=f"trace://sigil4cpython/restriction/{index}",
        )
        for index, target in enumerate(sections[1:], start=1)
    )
    return PydantikaCoherentProjection(
        schema_id=SCHEMA_ID,
        author_owner=AUTHOR,
        source_repository=SOURCE_REPOSITORY,
        source_branch=SOURCE_BRANCH,
        source_sha=SOURCE_SHA,
        target_repository=TARGET_REPOSITORY,
        sections=sections,
        restrictions=restrictions,
        ouroboros=VoidOuroborosProjection(
            flow_id="PYDANTIKA_VOID_TYPED_OUROBOROS_FLOW_V1",
            void_type="VOID",
            finite_budget=42,
            recur_requires_decreasing_residue=True,
            error_history_append_only=True,
            budget_reset_allowed=False,
        ),
    )


def compile_pydantika_coherent_projection(
    projection: PydantikaCoherentProjection | None = None,
) -> dict[str, object]:
    model = projection or build_pydantika_coherent_projection()
    errors = model.validate()
    return {
        "schema_id": model.schema_id,
        "source_sha": model.source_sha,
        "verdict": (
            ProjectionVerdict.ADMIT
            if not errors
            else ProjectionVerdict.REJECT
        ).value,
        "errors": errors,
        "projection_sha256": model.digest(),
        "dependency_free": True,
        "interpreter_semantics_changed": False,
        "runtime_executed": False,
    }


def with_identity_transport(
    projection: PydantikaCoherentProjection,
) -> PydantikaCoherentProjection:
    broken = replace(projection.sections[0], no_identity_transport=False)
    return replace(projection, sections=(broken, *projection.sections[1:]))


__all__ = [
    "AUTHOR",
    "AnnotatedKernelSection",
    "AnnotatedRestriction",
    "PydantikaCoherentProjection",
    "ProjectionVerdict",
    "SCHEMA_ID",
    "SEMANTIC_KERNEL_ID",
    "SOURCE_BRANCH",
    "SOURCE_REPOSITORY",
    "SOURCE_SHA",
    "TARGET_REPOSITORY",
    "VoidOuroborosProjection",
    "build_pydantika_coherent_projection",
    "compile_pydantika_coherent_projection",
    "with_identity_transport",
]
