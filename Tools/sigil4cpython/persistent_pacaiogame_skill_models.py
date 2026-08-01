"""Strict Pydantika models for the persistent PACAIoGames skill compiler."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


SCHEMA_ID = "SIGIL4CPYTHON_PERSISTENT_PACAIOGAME_SKILL_COMPILER_V1"
CANONICAL_IDS = {
    "SIGIL_AST": "SIGIL_AST_V1",
    "SIGIL_SYNTACTICAL_KERNEL": "SIGIL_SYNTACTICAL_KERNEL_V1",
    "SIGIL_SEMANTICAL_KERNEL": "SIGIL_SEMANTICAL_KERNEL_V1",
}
REQUIRED_VALIDATORS = {
    "PYDANTIKA",
    "DISKOTIKA",
    "LENA_LEAN4",
    "ARAKNE_REWRITE",
    "PACA_ANTORCHA",
    "QUAZRIS",
    "STRIKK",
}
REQUIRED_SEMANTIC_TYPES = {
    "PERSISTENT_PACA_SKILL",
    "PACAIOGAMES_SKILL",
    "SIGIL4GODOT_RUNTIME_PLAN",
    "DISKOTIKA_TYPED_RELATION",
    "PACA_ANTORCHA_NORMALIZER_PLAN",
    "QUAZRIS_LOCALIZED_VIEW",
}
REQUIRED_SURFACES = {"PACAIOGAMES", "SIGIL4GODOT", "SIGIL4CPYTHON"}


def _list_to_tuple(value: object) -> object:
    if isinstance(value, list):
        return tuple(value)
    return value


StringTuple = Annotated[tuple[str, ...], BeforeValidator(_list_to_tuple)]
Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
Identifier = Annotated[str, Field(min_length=1, max_length=256)]


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        allow_inf_nan=False,
    )


class AnnotatedTypeBindingModel(StrictModel):
    binding_id: Identifier
    python_type: Identifier
    semantic_types: StringTuple = Field(min_length=2, max_length=64)
    annotation_ids: StringTuple = Field(min_length=1, max_length=64)
    strict: Literal[True] = True
    plural_typed: Literal[True] = True
    source_bound: Literal[True] = True


class PersistentPacaSkillModel(StrictModel):
    skill_id: Identifier
    surfaces: StringTuple = Field(min_length=3, max_length=16)
    annotated_type_binding_id: Identifier
    persistence_key: Identifier
    replay_entrypoint: Identifier
    resource_bound: Identifier
    trace_preserved: Literal[True] = True
    no_identity_transport: Literal[True] = True
    runtime_executed: Literal[False] = False
    deployment_executed: Literal[False] = False


class CanonicalArtifactModel(StrictModel):
    artifact_id: Identifier
    kind: Literal[
        "SIGIL_AST",
        "SIGIL_SYNTACTICAL_KERNEL",
        "SIGIL_SEMANTICAL_KERNEL",
    ]
    version: Annotated[int, Field(ge=1)]
    input_artifact_ids: StringTuple
    type_signature: Identifier
    invariants: StringTuple = Field(min_length=3, max_length=32)
    source_bound: Literal[True] = True
    canonical: Literal[True] = True


class CanonicalArtifactCertificateModel(CanonicalArtifactModel):
    artifact_sha256: Digest


AnnotationTuple = Annotated[
    tuple[AnnotatedTypeBindingModel, ...],
    BeforeValidator(_list_to_tuple),
]
SkillTuple = Annotated[
    tuple[PersistentPacaSkillModel, ...],
    BeforeValidator(_list_to_tuple),
]
ArtifactTuple = Annotated[
    tuple[CanonicalArtifactModel, ...],
    BeforeValidator(_list_to_tuple),
]
CertifiedArtifactTuple = Annotated[
    tuple[CanonicalArtifactCertificateModel, ...],
    BeforeValidator(_list_to_tuple),
]
DictionaryTuple = Annotated[
    tuple[dict[str, object], ...],
    BeforeValidator(_list_to_tuple),
]


class PersistentPacaSkillCompilerPayloadModel(StrictModel):
    compiler_id: Literal[SCHEMA_ID]
    annotations: AnnotationTuple = Field(min_length=1, max_length=16)
    skills: SkillTuple = Field(min_length=1, max_length=32)
    artifacts: ArtifactTuple = Field(min_length=3, max_length=3)
    diskotika: dict[str, object]
    paca_antorcha: dict[str, object]
    quazris: dict[str, object]
    arakne: dict[str, object]
    validators: DictionaryTuple = Field(min_length=7, max_length=7)
    schema_id: Literal[SCHEMA_ID]
    linked_validator_baseline: Identifier
    source_bound: Literal[True] = True
    runtime_executed: Literal[False] = False
    deployment_executed: Literal[False] = False
    git_merge_executed: Literal[False] = False
    cpython_semantics_changed: Literal[False] = False
    final_kapsyla: Literal[False] = False
    canonical_artifacts: CertifiedArtifactTuple = Field(min_length=3, max_length=3)
    compile_state: Literal[
        "ADMIT_PLAN_ONLY",
        "HOLD_WITH_OBSTRUCTION",
        "REJECT",
    ]
    obstruction_ledger: StringTuple
    validator_states: dict[
        str,
        Literal["DECLARED", "PASS", "HOLD", "FAIL"],
    ]
    hosted_validation_required: bool
    branch_rewrite_executed: Literal[False] = False
    compiler_sha256: Digest

    @model_validator(mode="after")
    def validate_plural_compiler(self) -> "PersistentPacaSkillCompilerPayloadModel":
        canonical = {item.kind: item.artifact_id for item in self.canonical_artifacts}
        if canonical != CANONICAL_IDS:
            raise ValueError("canonical_artifact_family_mismatch")
        if {item.kind: item.artifact_id for item in self.artifacts} != CANONICAL_IDS:
            raise ValueError("source_artifact_family_mismatch")
        if set(self.validator_states) != REQUIRED_VALIDATORS:
            raise ValueError("persistent_validator_family_incomplete")
        if self.compile_state == "ADMIT_PLAN_ONLY" and self.obstruction_ledger:
            raise ValueError("admitted_payload_has_obstruction")

        binding_ids = {item.binding_id for item in self.annotations}
        if len(binding_ids) != len(self.annotations):
            raise ValueError("duplicate_annotated_binding")
        if not any(
            REQUIRED_SEMANTIC_TYPES.issubset(set(item.semantic_types))
            for item in self.annotations
        ):
            raise ValueError("pydantika_required_plural_types_missing")
        for skill in self.skills:
            if skill.annotated_type_binding_id not in binding_ids:
                raise ValueError("skill_annotation_binding_missing")
            if not REQUIRED_SURFACES.issubset(set(skill.surfaces)):
                raise ValueError("skill_runtime_surface_missing")

        if self.arakne.get("git_merge_executed") is not False:
            raise ValueError("arakne_git_merge_boundary_broken")
        if self.arakne.get("branch_rewrite_executed") is not False:
            raise ValueError("arakne_branch_rewrite_boundary_broken")
        if self.arakne.get("branch_identities_preserved") is not True:
            raise ValueError("arakne_branch_identity_collapse")
        if self.paca_antorcha.get("model_executed") is not False:
            raise ValueError("paca_antorcha_execution_boundary_broken")
        if self.paca_antorcha.get("tensor_allocated") is not False:
            raise ValueError("paca_antorcha_allocation_boundary_broken")
        if self.quazris.get("runtime_executed") is not False:
            raise ValueError("quazris_runtime_boundary_broken")
        return self

    def canonical_digest(self) -> str:
        encoded = json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


class PydantikaPersistentSkillCertificate(StrictModel):
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    model_name: Literal["PersistentPacaSkillCompilerPayloadModel"] = (
        "PersistentPacaSkillCompilerPayloadModel"
    )
    payload_digest: Digest
    compiler_digest_verified: Literal[True] = True
    serialization_round_trip_verified: Literal[True] = True
    artifact_digests: Annotated[tuple[Digest, ...], BeforeValidator(_list_to_tuple)]
    canonical_artifact_count: Literal[3] = 3
    runtime_executed: Literal[False] = False
    deployment_executed: Literal[False] = False
    git_merge_executed: Literal[False] = False
    final_kapsyla: Literal[False] = False


def _stable_digest(payload: dict[str, object]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def compile_pydantika_persistent_skill(
    payload: dict[str, object],
) -> PydantikaPersistentSkillCertificate:
    """Strictly validate the dependency-free compiler payload."""

    unsigned = dict(payload)
    supplied_compiler_digest = unsigned.pop("compiler_sha256", None)
    if not isinstance(supplied_compiler_digest, str):
        raise ValueError("compiler_digest_missing")
    if _stable_digest(unsigned) != supplied_compiler_digest:
        raise ValueError("compiler_digest_mismatch")

    model = PersistentPacaSkillCompilerPayloadModel.model_validate(payload)
    encoded = model.model_dump_json()
    reconstructed = PersistentPacaSkillCompilerPayloadModel.model_validate_json(encoded)
    if reconstructed.model_dump(mode="json") != model.model_dump(mode="json"):
        raise ValueError("persistent_skill_round_trip_failed")

    return PydantikaPersistentSkillCertificate(
        payload_digest=model.canonical_digest(),
        artifact_digests=tuple(
            item.artifact_sha256 for item in model.canonical_artifacts
        ),
    )


__all__ = [
    "CANONICAL_IDS",
    "PersistentPacaSkillCompilerPayloadModel",
    "PydantikaPersistentSkillCertificate",
    "REQUIRED_VALIDATORS",
    "SCHEMA_ID",
    "compile_pydantika_persistent_skill",
]
