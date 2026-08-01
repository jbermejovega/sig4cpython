"""Dependency-free STRIKK/KQC publication-sheaf contract.

This module models review-gated transport from a source repository into a public
experimental mirror and, separately, into an upstream contribution candidate.
It does not copy files, push branches, open upstream pull requests, execute JIT
code, or change CPython interpreter semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
import re
from typing import Mapping


SCHEMA_ID = "STRIKK_KQC_PUBLICATION_SHEAF_V1"
STRIKK_TYPE = "STRIKK::KQC_PUBLICATION_SHEAF"
_SHA1_RE = re.compile(r"^[a-f0-9]{40}$")


class CompilerStrategy(str, Enum):
    """Plural compiler/runtime classes; no two values are aliases."""

    SCHEMA_AOT = "SCHEMA_AOT"
    BYTECODE_COMPILE = "BYTECODE_COMPILE"
    ADAPTIVE_INTERPRETER = "ADAPTIVE_INTERPRETER"
    EXPERIMENTAL_JIT = "EXPERIMENTAL_JIT"
    EXTERNAL_JIT = "EXTERNAL_JIT"
    NATIVE_AOT = "NATIVE_AOT"
    PYBIND_BINDING = "PYBIND_BINDING"
    OPENMP_BINDING = "OPENMP_BINDING"
    PLAN_ONLY = "PLAN_ONLY"


class UAPState(str, Enum):
    ADMIT = "ADMIT"
    HOLD_WITH_OBSTRUCTION = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT"


class PublicationAuthority(str, Enum):
    WRITE_OWN_REPOSITORY = "WRITE_OWN_REPOSITORY"
    OPEN_REVIEW_CANDIDATE = "OPEN_REVIEW_CANDIDATE"
    PLAN_ONLY = "PLAN_ONLY"


class RelationKind(str, Enum):
    STATIC = "STATIC"
    DYNAMIC = "DYNAMIC"
    PULLBACK = "PULLBACK"
    TRANADA = "TRANADA"
    THIRD_WHEEL = "THIRD_WHEEL"
    PUBLICATION = "PUBLICATION"


@dataclass(frozen=True, slots=True)
class RepositorySection:
    repository: str
    ref: str
    commit_sha: str
    visibility: str
    role: str

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if "/" not in self.repository:
            errors.append(f"repository_name_invalid:{self.repository}")
        if not self.ref:
            errors.append(f"repository_ref_missing:{self.repository}")
        if not _SHA1_RE.fullmatch(self.commit_sha):
            errors.append(f"repository_sha_invalid:{self.repository}")
        if self.visibility not in {"private", "public"}:
            errors.append(f"repository_visibility_invalid:{self.repository}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class KQCKernelType:
    c_typed: bool
    q_typed: bool
    k_typed: bool
    context_type: str
    quoquantum_type: str
    no_identity_transport: bool = True
    no_plural_collapse: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not (self.c_typed and self.q_typed and self.k_typed):
            errors.append("incomplete_KQC_kernel_type")
        if not self.context_type:
            errors.append("missing_context_type")
        if not self.quoquantum_type:
            errors.append("missing_quoquantum_type")
        if not self.no_identity_transport:
            errors.append("identity_transport_forbidden")
        if not self.no_plural_collapse:
            errors.append("plural_collapse_forbidden")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PullbackWitness:
    witness_id: str
    left_object: str
    right_object: str
    base_object: str
    commutes: bool
    trace_id: str

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not all(
            (self.witness_id, self.left_object, self.right_object, self.base_object, self.trace_id)
        ):
            errors.append("incomplete_pullback_witness")
        if self.left_object == self.right_object:
            errors.append(f"pullback_identity_collapse:{self.witness_id}")
        if not self.commutes:
            errors.append(f"noncommuting_pullback:{self.witness_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class CompilerKernel:
    kernel_id: str
    strategy: CompilerStrategy
    source_type: str
    target_type: str
    context_id: str
    backend: str
    kqc_type: KQCKernelType
    source_paths: tuple[str, ...]
    dependency_ids: tuple[str, ...] = ()
    pullback_ids: tuple[str, ...] = ()
    binding_kinds: tuple[str, ...] = ()
    resource_calls_bounded: bool = True
    max_resource_calls: int = 1
    runtime_execution_claimed: bool = False
    physical_execution_claimed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors = list(self.kqc_type.validate())
        if not self.kernel_id:
            errors.append("kernel_id_missing")
        if not self.source_type or not self.target_type or not self.context_id:
            errors.append(f"kernel_type_boundary_missing:{self.kernel_id}")
        if not self.backend:
            errors.append(f"kernel_backend_missing:{self.kernel_id}")
        if not self.source_paths:
            errors.append(f"kernel_source_paths_missing:{self.kernel_id}")
        if not self.resource_calls_bounded or self.max_resource_calls < 1:
            errors.append(f"unbounded_bunched_resource_calls:{self.kernel_id}")
        if self.strategy == CompilerStrategy.EXPERIMENTAL_JIT and self.backend != "CPYTHON_JIT":
            errors.append(f"experimental_jit_backend_mismatch:{self.kernel_id}")
        if self.physical_execution_claimed:
            errors.append(f"physical_execution_claim_forbidden:{self.kernel_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class TypedRelation:
    relation_id: str
    kind: RelationKind
    source_ids: tuple[str, ...]
    target_ids: tuple[str, ...]
    context_id: str
    witness_ids: tuple[str, ...]
    obstruction_ids: tuple[str, ...] = ()
    identity_transport: bool = False

    def validate(self, known_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.source_ids or not self.target_ids:
            errors.append(f"empty_relation_boundary:{self.relation_id}")
        if not set(self.source_ids + self.target_ids).issubset(known_ids):
            errors.append(f"relation_unknown_endpoint:{self.relation_id}")
        if set(self.source_ids) & set(self.target_ids):
            errors.append(f"relation_identity_collapse:{self.relation_id}")
        if self.kind in {RelationKind.DYNAMIC, RelationKind.PULLBACK, RelationKind.TRANADA}:
            if not self.witness_ids:
                errors.append(f"relation_witness_missing:{self.relation_id}")
        if self.identity_transport:
            errors.append(f"relation_identity_transport:{self.relation_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PublicationHop:
    hop_id: str
    source_repository: str
    target_repository: str
    source_sha: str
    target_base_sha: str
    authority: PublicationAuthority
    required_reviews: tuple[str, ...]
    copies_source_identity: bool = False
    direct_upstream_write: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.source_repository == self.target_repository:
            errors.append(f"publication_self_hop:{self.hop_id}")
        if not _SHA1_RE.fullmatch(self.source_sha):
            errors.append(f"publication_source_sha_invalid:{self.hop_id}")
        if not _SHA1_RE.fullmatch(self.target_base_sha):
            errors.append(f"publication_target_sha_invalid:{self.hop_id}")
        if not self.required_reviews:
            errors.append(f"publication_reviews_missing:{self.hop_id}")
        if self.copies_source_identity:
            errors.append(f"publication_identity_transport:{self.hop_id}")
        if self.target_repository == "python/cpython":
            if self.authority != PublicationAuthority.PLAN_ONLY:
                errors.append("upstream_authority_must_be_plan_only")
            if self.direct_upstream_write:
                errors.append("direct_upstream_write_forbidden")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class ThirdWheelFactor:
    factor_id: str
    parent_id: str
    left_id: str
    right_id: str
    obstruction_id: str
    remaining_budget: int
    terminal: bool = False

    def validate(self, known_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if self.parent_id not in known_ids:
            errors.append(f"third_wheel_unknown_parent:{self.factor_id}")
        if self.left_id == self.right_id:
            errors.append(f"third_wheel_factor_collapse:{self.factor_id}")
        if self.remaining_budget < 0:
            errors.append(f"third_wheel_negative_budget:{self.factor_id}")
        if not self.obstruction_id:
            errors.append(f"third_wheel_obstruction_missing:{self.factor_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class HarmonicConstraint:
    object_id: str
    group_action_declared: bool
    locally_compact_t2: bool
    commutative_hyperoperation: bool
    signed_dual_declared: bool
    characters_separate_points: bool
    fourier_invertible: bool
    haar_plancherel_witnesses: tuple[str, ...]
    claim_scope: str = "declared_model_only"

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.fourier_invertible and not (
            self.group_action_declared
            and self.locally_compact_t2
            and self.commutative_hyperoperation
            and self.characters_separate_points
            and self.haar_plancherel_witnesses
        ):
            errors.append(f"fourier_invertibility_underwitnessed:{self.object_id}")
        if self.claim_scope != "declared_model_only":
            errors.append(f"harmonic_claim_scope_too_strong:{self.object_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class MeasurementProfile:
    profile_id: str
    measured_basis: str
    dual_basis: str
    repeatable_for_measured_basis: bool
    destroys_dual_coherence: bool
    demolition_for_dual_basis: bool
    physical_execution_claimed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.measured_basis == self.dual_basis:
            errors.append(f"measurement_basis_collapse:{self.profile_id}")
        if self.physical_execution_claimed:
            errors.append(f"measurement_execution_unwitnessed:{self.profile_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class TQFTCoherenceProfile:
    profile_id: str
    associativity_witness: str
    pentagon_witness: str
    trace_cyclicity_witness: str
    three_cocycle_witness: str
    twisted_injection_witnesses: tuple[str, ...]
    pullback_ids: tuple[str, ...]
    spatial_resource_claimed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        required = (
            self.associativity_witness,
            self.pentagon_witness,
            self.trace_cyclicity_witness,
            self.three_cocycle_witness,
        )
        if not all(required):
            errors.append(f"tqft_coherence_incomplete:{self.profile_id}")
        if not self.twisted_injection_witnesses:
            errors.append(f"twisted_injection_witness_missing:{self.profile_id}")
        if not self.pullback_ids:
            errors.append(f"tqft_pullback_family_missing:{self.profile_id}")
        if self.spatial_resource_claimed:
            errors.append(f"spatial_resource_claim_forbidden:{self.profile_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class KQCPublicationSheaf:
    report_id: str
    source: RepositorySection
    public_mirror: RepositorySection
    upstream: RepositorySection
    kernels: tuple[CompilerKernel, ...]
    relations: tuple[TypedRelation, ...]
    pullbacks: tuple[PullbackWitness, ...]
    publication_hops: tuple[PublicationHop, ...]
    third_wheel_factors: tuple[ThirdWheelFactor, ...]
    harmonic_constraints: tuple[HarmonicConstraint, ...]
    measurement_profiles: tuple[MeasurementProfile, ...]
    tqft_profiles: tuple[TQFTCoherenceProfile, ...]
    replay_trace: tuple[str, ...]
    source_bound: bool = True
    strikk_type: str = STRIKK_TYPE
    schema_id: str = SCHEMA_ID
    pydantika_is_tooling_not_stdlib_dependency: bool = True
    discopy_is_optional_projection: bool = True
    lean4_is_proof_scaffold_not_kernel_proof: bool = True
    void_is_semantic_kernel_role_not_literal_K_dual: bool = True
    quotient_isomorphism_claimed: bool = False
    aperiodic_compression_theorem_claimed: bool = False
    human_review_required: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        errors.extend(self.source.validate())
        errors.extend(self.public_mirror.validate())
        errors.extend(self.upstream.validate())

        if self.schema_id != SCHEMA_ID or self.strikk_type != STRIKK_TYPE:
            errors.append("strikk_or_schema_identity_mismatch")
        if self.source.repository != "jbermejovega/sigilbook":
            errors.append("unexpected_source_repository")
        if self.public_mirror.repository != "jbermejovega/sigil4cpython":
            errors.append("unexpected_public_mirror_repository")
        if self.upstream.repository != "python/cpython":
            errors.append("unexpected_upstream_repository")
        if self.source.visibility != "private":
            errors.append("sigilbook_source_visibility_must_be_private")
        if self.public_mirror.visibility != "public" or self.upstream.visibility != "public":
            errors.append("public_repository_visibility_required")
        if not self.source_bound or not self.replay_trace:
            errors.append("source_binding_and_replay_required")
        if not self.pydantika_is_tooling_not_stdlib_dependency:
            errors.append("pydantika_stdlib_dependency_forbidden")
        if not self.discopy_is_optional_projection:
            errors.append("discopy_core_dependency_forbidden")
        if not self.lean4_is_proof_scaffold_not_kernel_proof:
            errors.append("lean4_scaffold_promoted_to_proof")
        if not self.void_is_semantic_kernel_role_not_literal_K_dual:
            errors.append("void_K_dual_overclaim")
        if self.quotient_isomorphism_claimed:
            errors.append("quotient_isomorphism_requires_proof")
        if self.aperiodic_compression_theorem_claimed:
            errors.append("aperiodic_compression_requires_proof")
        if not self.human_review_required:
            errors.append("human_review_required")

        kernel_ids = [kernel.kernel_id for kernel in self.kernels]
        if len(kernel_ids) != len(set(kernel_ids)):
            errors.append("duplicate_kernel_identity")
        pullback_ids = [item.witness_id for item in self.pullbacks]
        if len(pullback_ids) != len(set(pullback_ids)):
            errors.append("duplicate_pullback_identity")
        relation_ids = [item.relation_id for item in self.relations]
        if len(relation_ids) != len(set(relation_ids)):
            errors.append("duplicate_relation_identity")
        hop_ids = [item.hop_id for item in self.publication_hops]
        if len(hop_ids) != len(set(hop_ids)):
            errors.append("duplicate_publication_hop_identity")

        for kernel in self.kernels:
            errors.extend(kernel.validate())
            unknown_pullbacks = set(kernel.pullback_ids) - set(pullback_ids)
            if unknown_pullbacks:
                errors.append(f"kernel_unknown_pullback:{kernel.kernel_id}")
        for pullback in self.pullbacks:
            errors.extend(pullback.validate())

        known_ids = set(kernel_ids)
        known_ids.update({self.source.repository, self.public_mirror.repository, self.upstream.repository})
        for relation in self.relations:
            errors.extend(relation.validate(known_ids))
        for factor in self.third_wheel_factors:
            errors.extend(factor.validate(known_ids))
        for item in self.harmonic_constraints:
            errors.extend(item.validate())
        for item in self.measurement_profiles:
            errors.extend(item.validate())
        for item in self.tqft_profiles:
            errors.extend(item.validate())
            if not set(item.pullback_ids).issubset(set(pullback_ids)):
                errors.append(f"tqft_unknown_pullback:{item.profile_id}")
        for hop in self.publication_hops:
            errors.extend(hop.validate())

        expected_hops = {
            ("jbermejovega/sigilbook", "jbermejovega/sigil4cpython"),
            ("jbermejovega/sigil4cpython", "python/cpython"),
        }
        actual_hops = {(hop.source_repository, hop.target_repository) for hop in self.publication_hops}
        if expected_hops != actual_hops:
            errors.append("publication_chain_incomplete")

        if not any(kernel.strategy == CompilerStrategy.BYTECODE_COMPILE for kernel in self.kernels):
            errors.append("cpython_bytecode_profile_missing")
        if not any(kernel.strategy == CompilerStrategy.ADAPTIVE_INTERPRETER for kernel in self.kernels):
            errors.append("cpython_adaptive_interpreter_profile_missing")
        if not any(kernel.strategy == CompilerStrategy.EXPERIMENTAL_JIT for kernel in self.kernels):
            errors.append("cpython_experimental_jit_profile_missing")
        if not any(kernel.strategy == CompilerStrategy.NATIVE_AOT for kernel in self.kernels):
            errors.append("native_AOT_profile_missing")

        return tuple(dict.fromkeys(errors))

    def to_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    def canonical_digest(self) -> str:
        return stable_digest(self.to_dict())



def _jsonable(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value



def stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        _jsonable(dict(payload)),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()



def compile_publication_sheaf(sheaf: KQCPublicationSheaf) -> dict[str, object]:
    """Validate and serialize a publication candidate without performing a push."""

    obstructions = sheaf.validate()
    if any(
        item.startswith(
            (
                "identity_transport",
                "plural_collapse",
                "relation_identity_transport",
                "publication_identity_transport",
                "direct_upstream_write_forbidden",
            )
        )
        for item in obstructions
    ):
        state = UAPState.REJECT
    elif obstructions:
        state = UAPState.HOLD_WITH_OBSTRUCTION
    else:
        state = UAPState.ADMIT

    payload = sheaf.to_dict()
    payload.update(
        {
            "uap_state": state.value,
            "obstruction_ledger": list(obstructions),
            "sheaf_sha256": sheaf.canonical_digest(),
            "source_files_copied": False,
            "upstream_write_performed": False,
            "pull_request_opened": False,
            "runtime_executed": False,
        }
    )
    return payload


__all__ = [
    "CompilerKernel",
    "CompilerStrategy",
    "HarmonicConstraint",
    "KQCKernelType",
    "KQCPublicationSheaf",
    "MeasurementProfile",
    "PublicationAuthority",
    "PublicationHop",
    "PullbackWitness",
    "RelationKind",
    "RepositorySection",
    "SCHEMA_ID",
    "STRIKK_TYPE",
    "TQFTCoherenceProfile",
    "ThirdWheelFactor",
    "TypedRelation",
    "UAPState",
    "compile_publication_sheaf",
    "stable_digest",
]
