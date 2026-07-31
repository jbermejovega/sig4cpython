"""Coherent presheaf kernel for PACA Estaca and Universal Abstrakta.

This dependency-free module compiles a source-bound metadata plan joining the
SIGIL4CPython coherent-sheaf surface to the PACA Estaca / Universal Abstrakta
pipeline and a Pydantika view of open pull-request epochs.

"Merge" in this module means a deterministic ledger view. It never performs a
Git merge, changes CPython semantics, starts a runtime, or absorbs authority
from an open pull request.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping


SCHEMA_ID = "SIGIL4CPYTHON_PACA_ESTACA_UNIVERSAL_PRESHEAF_V1"
GLOBAL_SECTION_ID = "SIGIL4CPYTHON_GLOBAL_UNIVERSAL_ABSTRAKTA_SECTION"
RULEZERO = "PIORNALEGO_ES_CANON"


class PresheafState(str, Enum):
    ADMIT = "ADMIT"
    HOLD_WITH_OBSTRUCTION = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT"


class PullRequestState(str, Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"
    CLOSED = "CLOSED"


class SectionKind(str, Enum):
    GLOBAL = "GLOBAL"
    PACA_BASE = "PACA_BASE"
    PACA_CODE_BASE = "PACA_CODE_BASE"
    PACA_KNOWLEDGE_BASE = "PACA_KNOWLEDGE_BASE"
    PACA_ESTACA = "PACA_ESTACA"
    UNIVERSAL_ABSTRAKTA_PIPELINE = "UNIVERSAL_ABSTRAKTA_PIPELINE"
    QUNO_NORMA_ADJOINT_EPOCHS = "QUNO_NORMA_ADJOINT_EPOCHS"
    SIGIL4CPYTHON_PROJECTION = "SIGIL4CPYTHON_PROJECTION"


class PipelinePhase(str, Enum):
    INGEST_LEDGER = "INGEST_LEDGER"
    PYDANTIKA_VALIDATE = "PYDANTIKA_VALIDATE"
    RESTRICT_GLOBAL_TO_LOCAL = "RESTRICT_GLOBAL_TO_LOCAL"
    GLUE_OVERLAPS = "GLUE_OVERLAPS"
    KOKOMPILE_UAP = "KOKOMPILE_UAP"
    EMIT_REPLAY = "EMIT_REPLAY"


@dataclass(frozen=True, slots=True)
class PullRequestEpoch:
    epoch_id: str
    repository: str
    pull_request: int
    state: PullRequestState
    head_sha: str
    branch: str
    draft: bool
    mergeable_observed: bool
    source_role: str
    identity_transport: bool = False
    authority_absorbed: bool = False
    git_merge_executed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.epoch_id or not self.repository or self.pull_request <= 0:
            errors.append(f"pr_epoch_identity_missing:{self.epoch_id}")
        if len(self.head_sha) != 40 or any(ch not in "0123456789abcdef" for ch in self.head_sha):
            errors.append(f"pr_epoch_head_sha_invalid:{self.epoch_id}")
        if not self.branch or not self.source_role:
            errors.append(f"pr_epoch_metadata_missing:{self.epoch_id}")
        if self.identity_transport:
            errors.append(f"pr_epoch_identity_transport:{self.epoch_id}")
        if self.authority_absorbed:
            errors.append(f"pr_epoch_authority_absorption:{self.epoch_id}")
        if self.git_merge_executed:
            errors.append(f"pr_epoch_git_merge_forbidden:{self.epoch_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PresheafSection:
    section_id: str
    kind: SectionKind
    context_id: str
    semantic_type: str
    source_epoch_ids: tuple[str, ...]
    local: bool
    plural_typed: bool = True
    mild_context_sensitive: bool = True
    provenance_preserved: bool = True
    identity_transport: bool = False

    def validate(self, known_epoch_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.section_id or not self.context_id or not self.semantic_type:
            errors.append(f"presheaf_section_metadata_missing:{self.section_id}")
        if not self.source_epoch_ids:
            errors.append(f"presheaf_section_source_missing:{self.section_id}")
        if not set(self.source_epoch_ids).issubset(known_epoch_ids):
            errors.append(f"presheaf_section_unknown_epoch:{self.section_id}")
        if self.kind == SectionKind.GLOBAL and self.local:
            errors.append(f"global_section_marked_local:{self.section_id}")
        if self.kind != SectionKind.GLOBAL and not self.local:
            errors.append(f"local_section_marked_global:{self.section_id}")
        if not self.plural_typed or not self.mild_context_sensitive:
            errors.append(f"presheaf_section_type_policy_missing:{self.section_id}")
        if not self.provenance_preserved:
            errors.append(f"presheaf_section_provenance_loss:{self.section_id}")
        if self.identity_transport:
            errors.append(f"presheaf_section_identity_transport:{self.section_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class RestrictionMap:
    restriction_id: str
    source_section_id: str
    target_section_id: str
    witness_id: str
    contravariant: bool = True
    preserves_trace: bool = True
    preserves_plural_identity: bool = True
    identity_transport: bool = False

    def validate(self, sections: Mapping[str, PresheafSection]) -> tuple[str, ...]:
        errors: list[str] = []
        source = sections.get(self.source_section_id)
        target = sections.get(self.target_section_id)
        if source is None or target is None:
            errors.append(f"restriction_unknown_section:{self.restriction_id}")
            return tuple(errors)
        if source.kind != SectionKind.GLOBAL or target.kind == SectionKind.GLOBAL:
            errors.append(f"restriction_not_global_to_local:{self.restriction_id}")
        if not self.witness_id or not self.contravariant:
            errors.append(f"restriction_witness_or_variance_missing:{self.restriction_id}")
        if not self.preserves_trace or not self.preserves_plural_identity:
            errors.append(f"restriction_preservation_failure:{self.restriction_id}")
        if self.identity_transport:
            errors.append(f"restriction_identity_transport:{self.restriction_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class OverlapWitness:
    overlap_id: str
    left_section_id: str
    right_section_id: str
    compatibility_witness_id: str
    seam_visible: bool = True
    replay_safe: bool = True
    silent_overwrite: bool = False

    def validate(self, section_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if self.left_section_id == self.right_section_id:
            errors.append(f"overlap_identity_collapse:{self.overlap_id}")
        if not {self.left_section_id, self.right_section_id}.issubset(section_ids):
            errors.append(f"overlap_unknown_section:{self.overlap_id}")
        if not self.compatibility_witness_id:
            errors.append(f"overlap_witness_missing:{self.overlap_id}")
        if not self.seam_visible or not self.replay_safe or self.silent_overwrite:
            errors.append(f"overlap_replay_or_seam_failure:{self.overlap_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PipelineStage:
    stage_id: str
    phase: PipelinePhase
    dependency_ids: tuple[str, ...]
    input_types: tuple[str, ...]
    output_types: tuple[str, ...]
    executable: bool = False

    def validate(self, stage_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.stage_id or not self.input_types or not self.output_types:
            errors.append(f"pipeline_stage_metadata_missing:{self.stage_id}")
        if self.stage_id in self.dependency_ids:
            errors.append(f"pipeline_stage_self_cycle:{self.stage_id}")
        if not set(self.dependency_ids).issubset(stage_ids):
            errors.append(f"pipeline_stage_unknown_dependency:{self.stage_id}")
        if self.executable:
            errors.append(f"pipeline_stage_execution_forbidden:{self.stage_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PydantikaLedgerMerge:
    merge_id: str
    input_epoch_ids: tuple[str, ...]
    output_epoch_ids: tuple[str, ...]
    mode: str = "PYDANTIKA_LEDGER_VIEW_ONLY"
    preserves_cardinality: bool = True
    open_epochs_remain_open: bool = True
    git_merge_executed: bool = False
    branch_rewritten: bool = False
    authority_expansion: bool = False

    def validate(self, epochs: Mapping[str, PullRequestEpoch]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.merge_id or self.mode != "PYDANTIKA_LEDGER_VIEW_ONLY":
            errors.append("ledger_merge_mode_invalid")
        if set(self.input_epoch_ids) != set(epochs):
            errors.append("ledger_merge_input_family_mismatch")
        if self.output_epoch_ids != self.input_epoch_ids:
            errors.append("ledger_merge_reordered_or_collapsed_epochs")
        if not self.preserves_cardinality or not self.open_epochs_remain_open:
            errors.append("ledger_merge_preservation_failure")
        if self.git_merge_executed or self.branch_rewritten or self.authority_expansion:
            errors.append("ledger_merge_forbidden_effect")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class UniversalPresheafKernel:
    kernel_id: str
    epochs: tuple[PullRequestEpoch, ...]
    sections: tuple[PresheafSection, ...]
    restrictions: tuple[RestrictionMap, ...]
    overlaps: tuple[OverlapWitness, ...]
    stages: tuple[PipelineStage, ...]
    ledger_merge: PydantikaLedgerMerge
    schema_id: str = SCHEMA_ID
    rulezero: str = RULEZERO
    coherent_presheaf: bool = True
    full_paca_estaca: bool = True
    universal_abstracta_pipeline: bool = True
    pacapdg_uap_typed: bool = True
    runtime_executed: bool = False
    repository_mutated: bool = False
    final_kapsyla: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.schema_id != SCHEMA_ID or self.rulezero != RULEZERO:
            errors.append("universal_presheaf_schema_or_rulezero_mismatch")
        if not self.kernel_id:
            errors.append("universal_presheaf_kernel_id_missing")
        if not all((self.coherent_presheaf, self.full_paca_estaca,
                    self.universal_abstracta_pipeline, self.pacapdg_uap_typed)):
            errors.append("universal_presheaf_feature_family_incomplete")
        if self.runtime_executed or self.repository_mutated or self.final_kapsyla:
            errors.append("universal_presheaf_execution_boundary_violated")

        epoch_map = {item.epoch_id: item for item in self.epochs}
        if len(epoch_map) != len(self.epochs):
            errors.append("duplicate_pr_epoch_identity")
        for epoch in self.epochs:
            errors.extend(epoch.validate())

        section_map = {item.section_id: item for item in self.sections}
        if len(section_map) != len(self.sections):
            errors.append("duplicate_presheaf_section_identity")
        required_kinds = set(SectionKind)
        if {item.kind for item in self.sections} != required_kinds:
            errors.append("presheaf_section_family_incomplete")
        if sum(item.kind == SectionKind.GLOBAL for item in self.sections) != 1:
            errors.append("presheaf_requires_exactly_one_global_section")
        for section in self.sections:
            errors.extend(section.validate(set(epoch_map)))

        for restriction in self.restrictions:
            errors.extend(restriction.validate(section_map))
        restricted_targets = {item.target_section_id for item in self.restrictions}
        local_ids = {item.section_id for item in self.sections if item.local}
        if restricted_targets != local_ids:
            errors.append("presheaf_restriction_family_incomplete")

        for overlap in self.overlaps:
            errors.extend(overlap.validate(set(section_map)))

        stage_map = {item.stage_id: item for item in self.stages}
        if len(stage_map) != len(self.stages):
            errors.append("duplicate_pipeline_stage_identity")
        for stage in self.stages:
            errors.extend(stage.validate(set(stage_map)))
        errors.extend(_validate_dag(self.stages))

        errors.extend(self.ledger_merge.validate(epoch_map))
        return tuple(errors)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["kernel_sha256"] = stable_digest(payload)
        return payload


def _validate_dag(stages: tuple[PipelineStage, ...]) -> tuple[str, ...]:
    incoming = {stage.stage_id: set(stage.dependency_ids) for stage in stages}
    ready = sorted(stage_id for stage_id, deps in incoming.items() if not deps)
    visited: list[str] = []
    while ready:
        current = ready.pop(0)
        visited.append(current)
        for stage_id, deps in incoming.items():
            if current in deps:
                deps.remove(current)
                if not deps and stage_id not in visited and stage_id not in ready:
                    ready.append(stage_id)
                    ready.sort()
    return () if len(visited) == len(stages) else ("pipeline_scheduler_cycle",)


def stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _epoch(
    epoch_id: str,
    repository: str,
    pull_request: int,
    head_sha: str,
    branch: str,
    *,
    draft: bool,
    role: str,
) -> PullRequestEpoch:
    return PullRequestEpoch(
        epoch_id=epoch_id,
        repository=repository,
        pull_request=pull_request,
        state=PullRequestState.OPEN,
        head_sha=head_sha,
        branch=branch,
        draft=draft,
        mergeable_observed=True,
        source_role=role,
    )


def build_universal_presheaf_kernel() -> UniversalPresheafKernel:
    epochs = (
        _epoch(
            "sigilbook-pr-661",
            "jbermejovega/sigilbook",
            661,
            "f7fa58d0ade34f9780939d3b961cafc7d64801d6",
            "agent/quno-norma-adjoint-epochs-v1",
            draft=True,
            role="QUNO_NORMA_ADJOINT_GRANNY_EPOCHS",
        ),
        _epoch(
            "sigilbook-pr-668",
            "jbermejovega/sigilbook",
            668,
            "7ed6a43b02309c929909b4447266c96d0d92e9c9",
            "agent/universal-abstrakta-cellular-pipeline-dsl-v1",
            draft=True,
            role="UNIVERSAL_ABSTRAKTA_CELLULAR_PIPELINE",
        ),
        _epoch(
            "sigilbook-pr-669",
            "jbermejovega/sigilbook",
            669,
            "f018e136899f2f2d6d709778db08a943550f7af5",
            "agent/pydantika-quasarpi-aesthetic-awakening-runtime-v1",
            draft=True,
            role="QUASARPI_AESTHETIC_AWAKENING",
        ),
        _epoch(
            "sigil4cpython-pr-7",
            "jbermejovega/sigil4cpython",
            7,
            "54efbe9fd41c58aae68401d99b40ec48c2d3084e",
            "agent/virtual-rest-io-kernels-v1",
            draft=False,
            role="SIGIL4CPYTHON_TYPED_RUNTIME_PROJECTION",
        ),
    )
    epoch_ids = tuple(item.epoch_id for item in epochs)
    global_sources = epoch_ids
    sections = (
        PresheafSection(
            GLOBAL_SECTION_ID,
            SectionKind.GLOBAL,
            "context:global:universal-abstrakta",
            "SIGIL4CPYTHON::GLOBAL_COHERENT_PRESHEAF",
            global_sources,
            local=False,
        ),
        PresheafSection(
            "section:paca-base",
            SectionKind.PACA_BASE,
            "context:paca-base",
            "PACA::BASE_SECTION",
            ("sigilbook-pr-668",),
            local=True,
        ),
        PresheafSection(
            "section:paca-code-base",
            SectionKind.PACA_CODE_BASE,
            "context:paca-code-base",
            "PACA::CODE_BASE_SECTION",
            ("sigilbook-pr-668", "sigil4cpython-pr-7"),
            local=True,
        ),
        PresheafSection(
            "section:paca-knowledge-base",
            SectionKind.PACA_KNOWLEDGE_BASE,
            "context:paca-knowledge-base",
            "PACA::KNOWLEDGE_BASE_SECTION",
            ("sigilbook-pr-668",),
            local=True,
        ),
        PresheafSection(
            "section:paca-estaca",
            SectionKind.PACA_ESTACA,
            "context:paca-estaca",
            "PACA::ESTACA_FULL_SECTION",
            ("sigilbook-pr-661", "sigilbook-pr-668"),
            local=True,
        ),
        PresheafSection(
            "section:universal-abstrakta",
            SectionKind.UNIVERSAL_ABSTRAKTA_PIPELINE,
            "context:universal-abstrakta",
            "SIGIL::UNIVERSAL_ABSTRAKTA_PIPELINE",
            ("sigilbook-pr-668", "sigilbook-pr-669"),
            local=True,
        ),
        PresheafSection(
            "section:quno-norma",
            SectionKind.QUNO_NORMA_ADJOINT_EPOCHS,
            "context:quno-norma",
            "QUNO::NORMA_ADJOINT_EPOCHS",
            ("sigilbook-pr-661",),
            local=True,
        ),
        PresheafSection(
            "section:sigil4cpython",
            SectionKind.SIGIL4CPYTHON_PROJECTION,
            "context:sigil4cpython",
            "SIGIL4CPYTHON::PUBLIC_TYPED_PROJECTION",
            ("sigil4cpython-pr-7",),
            local=True,
        ),
    )
    restrictions = tuple(
        RestrictionMap(
            f"restriction:global:{section.section_id}",
            GLOBAL_SECTION_ID,
            section.section_id,
            f"witness:restriction:{section.section_id}",
        )
        for section in sections
        if section.local
    )
    overlaps = (
        OverlapWitness(
            "overlap:paca-estaca:quno-norma",
            "section:paca-estaca",
            "section:quno-norma",
            "witness:quno-norma-paca-estaca:v1",
        ),
        OverlapWitness(
            "overlap:paca-estaca:universal-abstrakta",
            "section:paca-estaca",
            "section:universal-abstrakta",
            "witness:paca-estaca-universal-abstrakta:v1",
        ),
        OverlapWitness(
            "overlap:universal-abstrakta:sigil4cpython",
            "section:universal-abstrakta",
            "section:sigil4cpython",
            "witness:universal-abstrakta-cpython:v1",
        ),
    )
    stages = (
        PipelineStage(
            "ledger-ingest",
            PipelinePhase.INGEST_LEDGER,
            (),
            ("OPEN_PR_EPOCHS",),
            ("SOURCE_BOUND_LEDGER",),
        ),
        PipelineStage(
            "pydantika-validate",
            PipelinePhase.PYDANTIKA_VALIDATE,
            ("ledger-ingest",),
            ("SOURCE_BOUND_LEDGER",),
            ("STRICT_LEDGER_VIEW",),
        ),
        PipelineStage(
            "restrict-sections",
            PipelinePhase.RESTRICT_GLOBAL_TO_LOCAL,
            ("pydantika-validate",),
            ("STRICT_LEDGER_VIEW",),
            ("LOCAL_PRESHEAF_SECTIONS",),
        ),
        PipelineStage(
            "glue-overlaps",
            PipelinePhase.GLUE_OVERLAPS,
            ("restrict-sections",),
            ("LOCAL_PRESHEAF_SECTIONS",),
            ("COHERENT_GLUE_CANDIDATE",),
        ),
        PipelineStage(
            "kokompile-uap",
            PipelinePhase.KOKOMPILE_UAP,
            ("glue-overlaps",),
            ("COHERENT_GLUE_CANDIDATE",),
            ("UAP_KERNEL_PLAN",),
        ),
        PipelineStage(
            "emit-replay",
            PipelinePhase.EMIT_REPLAY,
            ("kokompile-uap",),
            ("UAP_KERNEL_PLAN",),
            ("SAFE_REPLAY_CERTIFICATE",),
        ),
    )
    return UniversalPresheafKernel(
        kernel_id="SIGIL4CPYTHON_PACA_ESTACA_UNIVERSAL_PRESHEAF_KERNEL_V1",
        epochs=epochs,
        sections=sections,
        restrictions=restrictions,
        overlaps=overlaps,
        stages=stages,
        ledger_merge=PydantikaLedgerMerge(
            merge_id="PYDANTIKA_OPEN_PR_LEDGER_VIEW_V1",
            input_epoch_ids=epoch_ids,
            output_epoch_ids=epoch_ids,
        ),
    )


def compile_universal_presheaf_kernel() -> tuple[PresheafState, dict[str, object]]:
    kernel = build_universal_presheaf_kernel()
    errors = kernel.validate()
    if errors:
        return PresheafState.REJECT, {
            "schema_id": SCHEMA_ID,
            "state": PresheafState.REJECT.value,
            "errors": list(errors),
        }
    obstructions = (
        "SOURCE_PULL_REQUESTS_REMAIN_OPEN",
        "HOSTED_VALIDATION_NOT_OBSERVED_FOR_CURRENT_EPOCH",
        "RUNTIME_EXECUTION_NOT_REQUESTED",
    )
    return PresheafState.HOLD_WITH_OBSTRUCTION, {
        "schema_id": SCHEMA_ID,
        "state": PresheafState.HOLD_WITH_OBSTRUCTION.value,
        "kernel": kernel.to_dict(),
        "obstructions": list(obstructions),
        "git_merge_executed": False,
        "main_mutated": False,
        "runtime_executed": False,
        "final_kapsyla": False,
    }


__all__ = [
    "GLOBAL_SECTION_ID",
    "OverlapWitness",
    "PipelinePhase",
    "PipelineStage",
    "PresheafSection",
    "PresheafState",
    "PullRequestEpoch",
    "PullRequestState",
    "PydantikaLedgerMerge",
    "RestrictionMap",
    "SCHEMA_ID",
    "SectionKind",
    "UniversalPresheafKernel",
    "build_universal_presheaf_kernel",
    "compile_universal_presheaf_kernel",
    "stable_digest",
]
