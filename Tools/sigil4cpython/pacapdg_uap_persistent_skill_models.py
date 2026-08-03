"""Strict Pydantika models for the PACAPDG/UAP persistent skill lift."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


SCHEMA_ID = "SIGIL4CPYTHON_PACAPDG_UAP_PERSISTENT_PACAIOGAME_SKILL_V1"
SOURCE_SCHEMA_ID = "SIGIL4CPYTHON_PERSISTENT_PACAIOGAME_SKILL_COMPILER_V1"
CANDIDATE_IDS = {
    "SIGIL_AST": "SIGIL_AST_PACAPDG_UAP_V2",
    "SIGIL_SYNTACTICAL_KERNEL": "SIGIL_SYNTACTICAL_KERNEL_PACAPDG_UAP_V2",
    "SIGIL_SEMANTICAL_KERNEL": "SIGIL_SEMANTICAL_KERNEL_PACAPDG_UAP_V2",
}
SOURCE_IDS = {
    "SIGIL_AST_V1",
    "SIGIL_SYNTACTICAL_KERNEL_V1",
    "SIGIL_SEMANTICAL_KERNEL_V1",
}
REQUIRED_FACETS = {
    "PACAPDG_TYPED",
    "UAP_TYPED",
    "QUNOTYPED",
    "PYDANTIKA_ANNOTATED_TYPED",
    "DISKOTIKA_TYPED",
    "PACA_ANTORCHA_TYPED",
    "QUAZRIS_TYPED",
    "ARAKNE_SOURCE_BOUND_TYPED",
    "LENA_LEAN4_TYPED",
    "STRIKK_TYPED",
    "TRACE_PRESERVED",
    "NO_IDENTITY_TRANSPORT",
    "NO_PLURAL_COLLAPSE",
    "PI_FIXED_OR_HOLD",
}
REQUIRED_VALIDATORS = {
    "PACAPDG_UAP",
    "PYDANTIKA",
    "DISKOTIKA",
    "LENA_LEAN4",
    "ARAKNE_REWRITE",
    "PACA_ANTORCHA",
    "QUAZRIS",
    "STRIKK",
}
REQUIRED_SURFACES = {"PACAIOGAMES", "SIGIL4GODOT", "SIGIL4CPYTHON"}


def _list_to_tuple(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


StringTuple = Annotated[tuple[str, ...], BeforeValidator(_list_to_tuple)]
Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
Identifier = Annotated[str, Field(min_length=1, max_length=512)]


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        allow_inf_nan=False,
    )


class PacapdgUapTypeContractModel(StrictModel):
    contract_id: Identifier
    input_type: Literal["PERSISTENT_PACA_SKILL_PACKET"]
    pacapdg_ir_type: Literal["PACAPDG_TYPED_IR"]
    uap_envelope_type: Literal["UAP_ADMISSION_ENVELOPE"]
    output_type: Literal["UAP_ADMISSION_WITNESS"]
    facets: StringTuple = Field(min_length=1, max_length=64)
    stage_order: StringTuple = Field(min_length=13, max_length=32)
    source_bound: Literal[True] = True
    trace_preserved: Literal[True] = True
    no_identity_transport: Literal[True] = True
    no_plural_collapse: Literal[True] = True
    pi_fixed_or_hold: Literal[True] = True
    execution_authority: Literal[False] = False


class PersistentPacaHabilidadModel(StrictModel):
    ability_id: Identifier
    source_skill_id: Identifier
    annotated_type_id: Identifier
    surfaces: StringTuple = Field(min_length=3, max_length=16)
    persistence_key: Identifier
    replay_entrypoint: Identifier
    source_bound: Literal[True] = True
    trace_preserved: Literal[True] = True
    no_identity_transport: Literal[True] = True
    runtime_executed: Literal[False] = False
    deployment_executed: Literal[False] = False


class CandidateKernelArtifactModel(StrictModel):
    artifact_id: Identifier
    kind: Literal[
        "SIGIL_AST",
        "SIGIL_SYNTACTICAL_KERNEL",
        "SIGIL_SEMANTICAL_KERNEL",
    ]
    version: Literal[2]
    input_artifact_ids: StringTuple = Field(min_length=1, max_length=4)
    type_signature: Identifier
    facets: StringTuple = Field(min_length=2, max_length=32)
    source_bound: Literal[True] = True
    canonical_candidate: Literal[True] = True
    promoted: Literal[False] = False
    artifact_sha256: Digest


class TypedValidatorBindingModel(StrictModel):
    validator_id: Identifier
    validator_kind: Identifier
    status: Literal["DECLARED", "PASS", "HOLD", "FAIL"]
    source_ref: Identifier
    stage_ids: StringTuple = Field(min_length=1, max_length=16)
    preserves_trace: Literal[True] = True
    no_identity_transport: Literal[True] = True


CandidateTuple = Annotated[
    tuple[CandidateKernelArtifactModel, ...], BeforeValidator(_list_to_tuple)
]
ValidatorTuple = Annotated[
    tuple[TypedValidatorBindingModel, ...], BeforeValidator(_list_to_tuple)
]
RouteTuple = Annotated[
    tuple[dict[str, str], ...], BeforeValidator(_list_to_tuple)
]


class PacapdgUapPersistentSkillPayloadModel(StrictModel):
    source_compiler_id: Literal[SOURCE_SCHEMA_ID]
    source_compiler_digest: Digest
    source_compile_state: Literal["ADMIT_PLAN_ONLY", "HOLD_WITH_OBSTRUCTION"]
    source_artifact_ids: StringTuple = Field(min_length=3, max_length=3)
    source_validator_states: dict[
        str, Literal["DECLARED", "PASS", "HOLD", "FAIL"]
    ]
    contract: PacapdgUapTypeContractModel
    ability: PersistentPacaHabilidadModel
    candidate_artifacts: CandidateTuple = Field(min_length=3, max_length=3)
    validators: ValidatorTuple = Field(min_length=8, max_length=8)
    schema_id: Literal[SCHEMA_ID]
    source_bound: Literal[True] = True
    runtime_executed: Literal[False] = False
    deployment_executed: Literal[False] = False
    git_merge_executed: Literal[False] = False
    branch_rewrite_executed: Literal[False] = False
    uap_execution_authorized: Literal[False] = False
    final_kapsyla: Literal[False] = False
    compile_state: Literal[
        "ADMIT_PLAN_ONLY", "HOLD_WITH_OBSTRUCTION", "REJECT"
    ]
    promotion_state: Literal["CANDIDATE_CANONICAL_NOT_PROMOTED"]
    obstruction_ledger: StringTuple
    validator_states: dict[
        str, Literal["DECLARED", "PASS", "HOLD", "FAIL"]
    ]
    hosted_validation_required: bool
    diskotika_route: RouteTuple = Field(min_length=6, max_length=6)
    candidate_promoted: Literal[False] = False
    bundle_sha256: Digest

    @model_validator(mode="after")
    def validate_bundle(self) -> "PacapdgUapPersistentSkillPayloadModel":
        if set(self.source_artifact_ids) != SOURCE_IDS:
            raise ValueError("pacapdg_uap_source_artifact_family_mismatch")
        if not REQUIRED_FACETS.issubset(self.contract.facets):
            raise ValueError("pacapdg_uap_required_facets_missing")
        if not REQUIRED_SURFACES.issubset(self.ability.surfaces):
            raise ValueError("pacapdg_uap_runtime_surface_missing")
        family = {item.kind: item.artifact_id for item in self.candidate_artifacts}
        if family != CANDIDATE_IDS:
            raise ValueError("pacapdg_uap_candidate_family_mismatch")
        validator_family = {item.validator_kind for item in self.validators}
        if validator_family != REQUIRED_VALIDATORS:
            raise ValueError("pacapdg_uap_validator_family_incomplete")
        if set(self.validator_states) != REQUIRED_VALIDATORS:
            raise ValueError("pacapdg_uap_validator_state_family_incomplete")
        if self.compile_state == "ADMIT_PLAN_ONLY" and self.obstruction_ledger:
            raise ValueError("pacapdg_uap_admitted_payload_has_obstruction")
        if self.compile_state == "ADMIT_PLAN_ONLY" and not self.hosted_validation_required:
            raise ValueError("pacapdg_uap_hosted_validation_boundary_missing")
        for left, right in zip(self.diskotika_route, self.diskotika_route[1:]):
            if left.get("target_type") != right.get("source_type"):
                raise ValueError("pacapdg_uap_noncomposable_route")
        if self.diskotika_route[0].get("source_type") != (
            "PERSISTENT_PACA_SKILL_PACKET"
        ):
            raise ValueError("pacapdg_uap_route_domain_mismatch")
        if self.diskotika_route[-1].get("target_type") != (
            "UAP_ADMISSION_WITNESS"
        ):
            raise ValueError("pacapdg_uap_route_codomain_mismatch")
        return self

    def canonical_digest(self) -> str:
        return _stable_digest(self.model_dump(mode="json"))


class PydantikaPacapdgUapCertificate(StrictModel):
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    model_name: Literal["PacapdgUapPersistentSkillPayloadModel"] = (
        "PacapdgUapPersistentSkillPayloadModel"
    )
    payload_digest: Digest
    source_compiler_digest: Digest
    artifact_digests: Annotated[
        tuple[Digest, ...], BeforeValidator(_list_to_tuple)
    ]
    artifact_count: Literal[3] = 3
    pydantika_round_trip_verified: Literal[True] = True
    pacapdg_typed: Literal[True] = True
    uap_typed: Literal[True] = True
    candidate_promoted: Literal[False] = False
    runtime_executed: Literal[False] = False
    deployment_executed: Literal[False] = False
    final_kapsyla: Literal[False] = False


def _stable_digest(payload: dict[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def compile_pydantika_pacapdg_uap(
    payload: dict[str, object],
) -> PydantikaPacapdgUapCertificate:
    unsigned = dict(payload)
    supplied = unsigned.pop("bundle_sha256", None)
    if not isinstance(supplied, str):
        raise ValueError("pacapdg_uap_bundle_digest_missing")
    if _stable_digest(unsigned) != supplied:
        raise ValueError("pacapdg_uap_bundle_digest_mismatch")
    model = PacapdgUapPersistentSkillPayloadModel.model_validate(payload)
    encoded = model.model_dump_json()
    reconstructed = PacapdgUapPersistentSkillPayloadModel.model_validate_json(
        encoded
    )
    if reconstructed.model_dump(mode="json") != model.model_dump(mode="json"):
        raise ValueError("pacapdg_uap_round_trip_failed")
    return PydantikaPacapdgUapCertificate(
        payload_digest=model.canonical_digest(),
        source_compiler_digest=model.source_compiler_digest,
        artifact_digests=tuple(
            item.artifact_sha256 for item in model.candidate_artifacts
        ),
    )


__all__ = [
    "CANDIDATE_IDS",
    "PacapdgUapPersistentSkillPayloadModel",
    "PydantikaPacapdgUapCertificate",
    "REQUIRED_FACETS",
    "REQUIRED_VALIDATORS",
    "SCHEMA_ID",
    "_stable_digest",
    "compile_pydantika_pacapdg_uap",
]
