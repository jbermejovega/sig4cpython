"""Tooling-only Pydantika models for the universal presheaf kernel."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

sys.path.append(str(Path(__file__).resolve().parents[2] / "Lib"))

from sigil4cpython.universal_presheaf_pipeline import (  # noqa: E402
    SCHEMA_ID,
    build_universal_presheaf_kernel,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class PullRequestEpochModel(StrictModel):
    epoch_id: str = Field(min_length=1)
    repository: str = Field(min_length=3)
    pull_request: int = Field(gt=0)
    state: Literal["OPEN", "MERGED", "CLOSED"]
    head_sha: str = Field(pattern=r"^[a-f0-9]{40}$")
    branch: str = Field(min_length=1)
    draft: bool
    mergeable_observed: bool
    source_role: str = Field(min_length=1)
    identity_transport: Literal[False] = False
    authority_absorbed: Literal[False] = False
    git_merge_executed: Literal[False] = False


class SectionModel(StrictModel):
    section_id: str = Field(min_length=1)
    kind: Literal[
        "GLOBAL",
        "PACA_BASE",
        "PACA_CODE_BASE",
        "PACA_KNOWLEDGE_BASE",
        "PACA_ESTACA",
        "UNIVERSAL_ABSTRAKTA_PIPELINE",
        "QUNO_NORMA_ADJOINT_EPOCHS",
        "SIGIL4CPYTHON_PROJECTION",
    ]
    context_id: str = Field(min_length=1)
    semantic_type: str = Field(min_length=1)
    source_epoch_ids: tuple[str, ...] = Field(min_length=1)
    local: bool
    plural_typed: Literal[True] = True
    mild_context_sensitive: Literal[True] = True
    provenance_preserved: Literal[True] = True
    identity_transport: Literal[False] = False


class RestrictionModel(StrictModel):
    restriction_id: str
    source_section_id: str
    target_section_id: str
    witness_id: str
    contravariant: Literal[True] = True
    preserves_trace: Literal[True] = True
    preserves_plural_identity: Literal[True] = True
    identity_transport: Literal[False] = False


class OverlapModel(StrictModel):
    overlap_id: str
    left_section_id: str
    right_section_id: str
    compatibility_witness_id: str
    seam_visible: Literal[True] = True
    replay_safe: Literal[True] = True
    silent_overwrite: Literal[False] = False


class StageModel(StrictModel):
    stage_id: str
    phase: Literal[
        "INGEST_LEDGER",
        "PYDANTIKA_VALIDATE",
        "RESTRICT_GLOBAL_TO_LOCAL",
        "GLUE_OVERLAPS",
        "KOKOMPILE_UAP",
        "EMIT_REPLAY",
    ]
    dependency_ids: tuple[str, ...]
    input_types: tuple[str, ...] = Field(min_length=1)
    output_types: tuple[str, ...] = Field(min_length=1)
    executable: Literal[False] = False


class LedgerMergeModel(StrictModel):
    merge_id: str
    input_epoch_ids: tuple[str, ...]
    output_epoch_ids: tuple[str, ...]
    mode: Literal["PYDANTIKA_LEDGER_VIEW_ONLY"]
    preserves_cardinality: Literal[True] = True
    open_epochs_remain_open: Literal[True] = True
    git_merge_executed: Literal[False] = False
    branch_rewritten: Literal[False] = False
    authority_expansion: Literal[False] = False


class UniversalPresheafModel(StrictModel):
    kernel_id: str
    epochs: tuple[PullRequestEpochModel, ...] = Field(min_length=4)
    sections: tuple[SectionModel, ...] = Field(min_length=8)
    restrictions: tuple[RestrictionModel, ...] = Field(min_length=7)
    overlaps: tuple[OverlapModel, ...] = Field(min_length=3)
    stages: tuple[StageModel, ...] = Field(min_length=6, max_length=6)
    ledger_merge: LedgerMergeModel
    schema_id: Literal["SIGIL4CPYTHON_PACA_ESTACA_UNIVERSAL_PRESHEAF_V1"]
    rulezero: Literal["PIORNALEGO_ES_CANON"]
    coherent_presheaf: Literal[True]
    full_paca_estaca: Literal[True]
    universal_abstracta_pipeline: Literal[True]
    pacapdg_uap_typed: Literal[True]
    runtime_executed: Literal[False]
    repository_mutated: Literal[False]
    final_kapsyla: Literal[False]

    @model_validator(mode="after")
    def validate_plural_cover(self) -> "UniversalPresheafModel":
        epoch_ids = tuple(item.epoch_id for item in self.epochs)
        if len(epoch_ids) != len(set(epoch_ids)):
            raise ValueError("duplicate_open_pr_epoch")
        if self.ledger_merge.input_epoch_ids != epoch_ids:
            raise ValueError("ledger_merge_input_order_mismatch")
        if self.ledger_merge.output_epoch_ids != epoch_ids:
            raise ValueError("ledger_merge_output_order_mismatch")

        section_ids = {item.section_id for item in self.sections}
        global_ids = {item.section_id for item in self.sections if item.kind == "GLOBAL"}
        local_ids = {item.section_id for item in self.sections if item.local}
        if len(global_ids) != 1:
            raise ValueError("exactly_one_global_section_required")
        if {item.target_section_id for item in self.restrictions} != local_ids:
            raise ValueError("restriction_cover_incomplete")
        if not all(item.source_section_id in global_ids for item in self.restrictions):
            raise ValueError("restriction_source_not_global")
        if not all(
            {item.left_section_id, item.right_section_id}.issubset(section_ids)
            for item in self.overlaps
        ):
            raise ValueError("overlap_unknown_section")
        return self


class CompilationCertificate(StrictModel):
    schema_id: Literal["SIGIL4CPYTHON_PACA_ESTACA_UNIVERSAL_PRESHEAF_V1"]
    payload_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    schema_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    state: Literal["HOLD_WITH_OBSTRUCTION"]
    epoch_count: Literal[4]
    section_count: Literal[8]
    git_merge_executed: Literal[False] = False
    runtime_executed: Literal[False] = False
    final_kapsyla: Literal[False] = False


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def compile_universal_presheaf_models() -> tuple[
    UniversalPresheafModel,
    CompilationCertificate,
]:
    runtime_kernel = build_universal_presheaf_kernel()
    errors = runtime_kernel.validate()
    if errors:
        raise ValueError(";".join(errors))
    payload = runtime_kernel.to_dict()
    payload.pop("kernel_sha256")
    model = UniversalPresheafModel.model_validate(payload)
    round_trip = UniversalPresheafModel.model_validate_json(model.model_dump_json())
    if round_trip != model:
        raise ValueError("universal_presheaf_pydantika_round_trip_mismatch")
    certificate = CompilationCertificate(
        schema_id=SCHEMA_ID,
        payload_digest=_digest(model.model_dump(mode="json")),
        schema_digest=_digest(UniversalPresheafModel.model_json_schema()),
        state="HOLD_WITH_OBSTRUCTION",
        epoch_count=len(model.epochs),
        section_count=len(model.sections),
    )
    return model, certificate


__all__ = [
    "CompilationCertificate",
    "LedgerMergeModel",
    "PullRequestEpochModel",
    "SectionModel",
    "UniversalPresheafModel",
    "compile_universal_presheaf_models",
]
