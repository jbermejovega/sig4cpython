"""Strict Pydantika models for the SIGIL4CPython KQC publication sheaf.

This tooling layer may depend on Pydantic.  It is intentionally not imported by
``Lib/sigil4cpython`` and is not proposed as a CPython standard-library
dependency.
"""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


SCHEMA_ID = "STRIKK_KQC_PUBLICATION_SHEAF_V1"
STRIKK_TYPE = "STRIKK::KQC_PUBLICATION_SHEAF"
SHA1_PATTERN = r"^[a-f0-9]{40}$"


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        allow_inf_nan=False,
    )


class RepositorySectionModel(StrictModel):
    repository: str = Field(pattern=r"^[^/]+/[^/]+$")
    ref: str = Field(min_length=1, max_length=256)
    commit_sha: str = Field(pattern=SHA1_PATTERN)
    visibility: Literal["private", "public"]
    role: str = Field(min_length=1, max_length=192)


class KQCKernelTypeModel(StrictModel):
    c_typed: Literal[True] = True
    q_typed: Literal[True] = True
    k_typed: Literal[True] = True
    context_type: str = Field(min_length=1, max_length=192)
    quoquantum_type: str = Field(min_length=1, max_length=192)
    no_identity_transport: Literal[True] = True
    no_plural_collapse: Literal[True] = True


class PullbackWitnessModel(StrictModel):
    witness_id: str = Field(min_length=1, max_length=192)
    left_object: str = Field(min_length=1, max_length=192)
    right_object: str = Field(min_length=1, max_length=192)
    base_object: str = Field(min_length=1, max_length=192)
    commutes: bool
    trace_id: str = Field(min_length=1, max_length=192)

    @model_validator(mode="after")
    def distinct_legs(self) -> "PullbackWitnessModel":
        if self.left_object == self.right_object:
            raise ValueError("pullback_identity_collapse")
        return self


class CompilerKernelModel(StrictModel):
    kernel_id: str = Field(min_length=1, max_length=192)
    strategy: Literal[
        "SCHEMA_AOT",
        "BYTECODE_COMPILE",
        "ADAPTIVE_INTERPRETER",
        "EXPERIMENTAL_JIT",
        "EXTERNAL_JIT",
        "NATIVE_AOT",
        "PYBIND_BINDING",
        "OPENMP_BINDING",
        "PLAN_ONLY",
    ]
    source_type: str = Field(min_length=1, max_length=192)
    target_type: str = Field(min_length=1, max_length=192)
    context_id: str = Field(min_length=1, max_length=192)
    backend: str = Field(min_length=1, max_length=192)
    kqc_type: KQCKernelTypeModel
    source_paths: tuple[str, ...] = Field(min_length=1, max_length=256)
    dependency_ids: tuple[str, ...] = Field(default=(), max_length=256)
    pullback_ids: tuple[str, ...] = Field(default=(), max_length=256)
    binding_kinds: tuple[str, ...] = Field(default=(), max_length=64)
    resource_calls_bounded: Literal[True] = True
    max_resource_calls: int = Field(ge=1, le=1_000_000)
    runtime_execution_claimed: Literal[False] = False
    physical_execution_claimed: Literal[False] = False

    @model_validator(mode="after")
    def validate_strategy(self) -> "CompilerKernelModel":
        if self.strategy == "EXPERIMENTAL_JIT" and self.backend != "CPYTHON_JIT":
            raise ValueError("experimental_jit_backend_mismatch")
        return self


class TypedRelationModel(StrictModel):
    relation_id: str = Field(min_length=1, max_length=192)
    kind: Literal["STATIC", "DYNAMIC", "PULLBACK", "TRANADA", "THIRD_WHEEL", "PUBLICATION"]
    source_ids: tuple[str, ...] = Field(min_length=1, max_length=128)
    target_ids: tuple[str, ...] = Field(min_length=1, max_length=128)
    context_id: str = Field(min_length=1, max_length=192)
    witness_ids: tuple[str, ...] = Field(default=(), max_length=256)
    obstruction_ids: tuple[str, ...] = Field(default=(), max_length=256)
    identity_transport: Literal[False] = False

    @model_validator(mode="after")
    def validate_relation(self) -> "TypedRelationModel":
        if set(self.source_ids) & set(self.target_ids):
            raise ValueError("relation_identity_collapse")
        if self.kind in {"DYNAMIC", "PULLBACK", "TRANADA"} and not self.witness_ids:
            raise ValueError("relation_witness_missing")
        return self


class PublicationHopModel(StrictModel):
    hop_id: str = Field(min_length=1, max_length=192)
    source_repository: str = Field(pattern=r"^[^/]+/[^/]+$")
    target_repository: str = Field(pattern=r"^[^/]+/[^/]+$")
    source_sha: str = Field(pattern=SHA1_PATTERN)
    target_base_sha: str = Field(pattern=SHA1_PATTERN)
    authority: Literal["WRITE_OWN_REPOSITORY", "OPEN_REVIEW_CANDIDATE", "PLAN_ONLY"]
    required_reviews: tuple[str, ...] = Field(min_length=1, max_length=64)
    copies_source_identity: Literal[False] = False
    direct_upstream_write: Literal[False] = False

    @model_validator(mode="after")
    def upstream_is_plan_only(self) -> "PublicationHopModel":
        if self.source_repository == self.target_repository:
            raise ValueError("publication_self_hop")
        if self.target_repository == "python/cpython" and self.authority != "PLAN_ONLY":
            raise ValueError("upstream_authority_must_be_plan_only")
        return self


class ThirdWheelFactorModel(StrictModel):
    factor_id: str = Field(min_length=1, max_length=192)
    parent_id: str = Field(min_length=1, max_length=192)
    left_id: str = Field(min_length=1, max_length=192)
    right_id: str = Field(min_length=1, max_length=192)
    obstruction_id: str = Field(min_length=1, max_length=192)
    remaining_budget: int = Field(ge=0, le=1_000_000)
    terminal: bool = False

    @model_validator(mode="after")
    def distinct_factors(self) -> "ThirdWheelFactorModel":
        if self.left_id == self.right_id:
            raise ValueError("third_wheel_factor_collapse")
        return self


class HarmonicConstraintModel(StrictModel):
    object_id: str = Field(min_length=1, max_length=192)
    group_action_declared: bool
    locally_compact_t2: bool
    commutative_hyperoperation: bool
    signed_dual_declared: bool
    characters_separate_points: bool
    fourier_invertible: bool
    haar_plancherel_witnesses: tuple[str, ...] = Field(default=(), max_length=128)
    claim_scope: Literal["declared_model_only"] = "declared_model_only"

    @model_validator(mode="after")
    def validate_fourier_claim(self) -> "HarmonicConstraintModel":
        if self.fourier_invertible and not (
            self.group_action_declared
            and self.locally_compact_t2
            and self.commutative_hyperoperation
            and self.characters_separate_points
            and self.haar_plancherel_witnesses
        ):
            raise ValueError("fourier_invertibility_underwitnessed")
        return self


class MeasurementProfileModel(StrictModel):
    profile_id: str = Field(min_length=1, max_length=192)
    measured_basis: str = Field(min_length=1, max_length=192)
    dual_basis: str = Field(min_length=1, max_length=192)
    repeatable_for_measured_basis: bool
    destroys_dual_coherence: bool
    demolition_for_dual_basis: bool
    physical_execution_claimed: Literal[False] = False

    @model_validator(mode="after")
    def bases_are_distinct(self) -> "MeasurementProfileModel":
        if self.measured_basis == self.dual_basis:
            raise ValueError("measurement_basis_collapse")
        return self


class TQFTCoherenceProfileModel(StrictModel):
    profile_id: str = Field(min_length=1, max_length=192)
    associativity_witness: str = Field(min_length=1, max_length=192)
    pentagon_witness: str = Field(min_length=1, max_length=192)
    trace_cyclicity_witness: str = Field(min_length=1, max_length=192)
    three_cocycle_witness: str = Field(min_length=1, max_length=192)
    twisted_injection_witnesses: tuple[str, ...] = Field(min_length=1, max_length=128)
    pullback_ids: tuple[str, ...] = Field(min_length=1, max_length=128)
    spatial_resource_claimed: Literal[False] = False


class KQCPublicationSheafModel(StrictModel):
    report_id: str = Field(min_length=1, max_length=192)
    source: RepositorySectionModel
    public_mirror: RepositorySectionModel
    upstream: RepositorySectionModel
    kernels: tuple[CompilerKernelModel, ...] = Field(min_length=1, max_length=4096)
    relations: tuple[TypedRelationModel, ...] = Field(default=(), max_length=8192)
    pullbacks: tuple[PullbackWitnessModel, ...] = Field(default=(), max_length=4096)
    publication_hops: tuple[PublicationHopModel, ...] = Field(min_length=2, max_length=16)
    third_wheel_factors: tuple[ThirdWheelFactorModel, ...] = Field(default=(), max_length=4096)
    harmonic_constraints: tuple[HarmonicConstraintModel, ...] = Field(default=(), max_length=4096)
    measurement_profiles: tuple[MeasurementProfileModel, ...] = Field(default=(), max_length=4096)
    tqft_profiles: tuple[TQFTCoherenceProfileModel, ...] = Field(default=(), max_length=4096)
    replay_trace: tuple[str, ...] = Field(min_length=1, max_length=4096)
    source_bound: Literal[True] = True
    strikk_type: Literal[STRIKK_TYPE] = STRIKK_TYPE
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    pydantika_is_tooling_not_stdlib_dependency: Literal[True] = True
    discopy_is_optional_projection: Literal[True] = True
    lean4_is_proof_scaffold_not_kernel_proof: Literal[True] = True
    void_is_semantic_kernel_role_not_literal_K_dual: Literal[True] = True
    quotient_isomorphism_claimed: Literal[False] = False
    aperiodic_compression_theorem_claimed: Literal[False] = False
    human_review_required: Literal[True] = True

    @model_validator(mode="after")
    def validate_sheaf(self) -> "KQCPublicationSheafModel":
        if self.source.repository != "jbermejovega/sigilbook":
            raise ValueError("unexpected_source_repository")
        if self.public_mirror.repository != "jbermejovega/sigil4cpython":
            raise ValueError("unexpected_public_mirror_repository")
        if self.upstream.repository != "python/cpython":
            raise ValueError("unexpected_upstream_repository")
        if self.source.visibility != "private":
            raise ValueError("sigilbook_source_visibility_must_be_private")
        if self.public_mirror.visibility != "public" or self.upstream.visibility != "public":
            raise ValueError("public_repository_visibility_required")

        kernel_ids = tuple(item.kernel_id for item in self.kernels)
        if len(kernel_ids) != len(set(kernel_ids)):
            raise ValueError("duplicate_kernel_identity")
        pullback_ids = tuple(item.witness_id for item in self.pullbacks)
        if len(pullback_ids) != len(set(pullback_ids)):
            raise ValueError("duplicate_pullback_identity")
        known_pullbacks = set(pullback_ids)
        if any(not set(item.pullback_ids).issubset(known_pullbacks) for item in self.kernels):
            raise ValueError("kernel_unknown_pullback")
        if any(not set(item.pullback_ids).issubset(known_pullbacks) for item in self.tqft_profiles):
            raise ValueError("tqft_unknown_pullback")

        expected_hops = {
            ("jbermejovega/sigilbook", "jbermejovega/sigil4cpython"),
            ("jbermejovega/sigil4cpython", "python/cpython"),
        }
        actual_hops = {(item.source_repository, item.target_repository) for item in self.publication_hops}
        if actual_hops != expected_hops:
            raise ValueError("publication_chain_incomplete")

        strategies = {item.strategy for item in self.kernels}
        required = {
            "BYTECODE_COMPILE",
            "ADAPTIVE_INTERPRETER",
            "EXPERIMENTAL_JIT",
            "NATIVE_AOT",
        }
        if not required.issubset(strategies):
            raise ValueError("compiler_taxonomy_incomplete")
        return self

    def canonical_digest(self) -> str:
        encoded = json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


class PydantikaPublicationCertificate(StrictModel):
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    model_name: Literal["KQCPublicationSheafModel"] = "KQCPublicationSheafModel"
    payload_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    serialization_round_trip_verified: Literal[True] = True
    source_files_copied: Literal[False] = False
    upstream_write_performed: Literal[False] = False
    runtime_executed: Literal[False] = False
    human_review_required: Literal[True] = True


def compile_pydantika_publication_sheaf(payload: dict[str, object]) -> PydantikaPublicationCertificate:
    """Validate and round-trip one publication sheaf without publishing it."""

    model = KQCPublicationSheafModel.model_validate(payload)
    encoded = model.model_dump_json()
    reconstructed = KQCPublicationSheafModel.model_validate_json(encoded)
    if reconstructed.model_dump(mode="json") != model.model_dump(mode="json"):
        raise ValueError("publication_sheaf_round_trip_failed")
    return PydantikaPublicationCertificate(payload_digest=model.canonical_digest())


__all__ = [
    "KQCPublicationSheafModel",
    "PydantikaPublicationCertificate",
    "SCHEMA_ID",
    "STRIKK_TYPE",
    "compile_pydantika_publication_sheaf",
]
