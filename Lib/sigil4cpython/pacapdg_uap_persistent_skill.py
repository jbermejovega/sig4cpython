"""PACAPDG-typed UAP lift for persistent PACAIoGame skills.

The module wraps the existing persistent PACA skill compiler, preserves its
three V1 artifacts, and emits three source-bound V2 candidates.  It compiles
metadata and replay witnesses only; it does not start Godot, allocate tensors,
execute models, merge branches, deploy a runtime, or promote candidates.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
import re
from typing import Mapping


SCHEMA_ID = "SIGIL4CPYTHON_PACAPDG_UAP_PERSISTENT_PACAIOGAME_SKILL_V1"
SOURCE_SCHEMA_ID = "SIGIL4CPYTHON_PERSISTENT_PACAIOGAME_SKILL_COMPILER_V1"
SOURCE_AST_ID = "SIGIL_AST_V1"
SOURCE_SYNTACTICAL_KERNEL_ID = "SIGIL_SYNTACTICAL_KERNEL_V1"
SOURCE_SEMANTICAL_KERNEL_ID = "SIGIL_SEMANTICAL_KERNEL_V1"
CANDIDATE_AST_ID = "SIGIL_AST_PACAPDG_UAP_V2"
CANDIDATE_SYNTACTICAL_KERNEL_ID = (
    "SIGIL_SYNTACTICAL_KERNEL_PACAPDG_UAP_V2"
)
CANDIDATE_SEMANTICAL_KERNEL_ID = (
    "SIGIL_SEMANTICAL_KERNEL_PACAPDG_UAP_V2"
)
INPUT_PACKET_TYPE = "PERSISTENT_PACA_SKILL_PACKET"
PACAPDG_IR_TYPE = "PACAPDG_TYPED_IR"
UAP_ENVELOPE_TYPE = "UAP_ADMISSION_ENVELOPE"
UAP_WITNESS_TYPE = "UAP_ADMISSION_WITNESS"

REQUIRED_FACETS = (
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
)
REQUIRED_STAGE_ORDER = (
    "PACAPDG_PARSE",
    "QUNOTYPED_ROUTE",
    "PYDANTIKA_ANNOTATE",
    "DISKOTIKA_COMPOSE",
    "SIGIL_AST_COMPILE",
    "SIGIL_SYNTACTICAL_KERNEL_COMPILE",
    "QUAZRIS_LOCALIZE",
    "SIGIL_SEMANTICAL_KERNEL_COMPILE",
    "PACA_ANTORCHA_NORMALIZE",
    "ARAKNE_REWRITE",
    "LENA_LEAN4_VALIDATE",
    "STRIKK_VALIDATE",
    "UAP_ADMIT",
)
SOURCE_REQUIRED_VALIDATORS = {
    "PYDANTIKA",
    "DISKOTIKA",
    "LENA_LEAN4",
    "ARAKNE_REWRITE",
    "PACA_ANTORCHA",
    "QUAZRIS",
    "STRIKK",
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
HEX64 = re.compile(r"^[a-f0-9]{64}$")


class UapCompileState(str, Enum):
    ADMIT_PLAN_ONLY = "ADMIT_PLAN_ONLY"
    HOLD_WITH_OBSTRUCTION = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT"


class ValidatorStatus(str, Enum):
    DECLARED = "DECLARED"
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"


class UapArtifactKind(str, Enum):
    SIGIL_AST = "SIGIL_AST"
    SIGIL_SYNTACTICAL_KERNEL = "SIGIL_SYNTACTICAL_KERNEL"
    SIGIL_SEMANTICAL_KERNEL = "SIGIL_SEMANTICAL_KERNEL"


@dataclass(frozen=True, slots=True)
class PacapdgUapTypeContract:
    contract_id: str
    input_type: str
    pacapdg_ir_type: str
    uap_envelope_type: str
    output_type: str
    facets: tuple[str, ...]
    stage_order: tuple[str, ...]
    source_bound: bool = True
    trace_preserved: bool = True
    no_identity_transport: bool = True
    no_plural_collapse: bool = True
    pi_fixed_or_hold: bool = True
    execution_authority: bool = False


@dataclass(frozen=True, slots=True)
class PersistentPacaHabilidad:
    ability_id: str
    source_skill_id: str
    annotated_type_id: str
    surfaces: tuple[str, ...]
    persistence_key: str
    replay_entrypoint: str
    source_bound: bool = True
    trace_preserved: bool = True
    no_identity_transport: bool = True
    runtime_executed: bool = False
    deployment_executed: bool = False


@dataclass(frozen=True, slots=True)
class CandidateKernelArtifact:
    artifact_id: str
    kind: UapArtifactKind
    version: int
    input_artifact_ids: tuple[str, ...]
    type_signature: str
    facets: tuple[str, ...]
    source_bound: bool = True
    canonical_candidate: bool = True
    promoted: bool = False


@dataclass(frozen=True, slots=True)
class TypedValidatorBinding:
    validator_id: str
    validator_kind: str
    status: ValidatorStatus
    source_ref: str
    stage_ids: tuple[str, ...]
    preserves_trace: bool = True
    no_identity_transport: bool = True


@dataclass(frozen=True, slots=True)
class PacapdgUapPersistentSkillBundle:
    source_compiler_id: str
    source_compiler_digest: str
    source_compile_state: str
    source_artifact_ids: tuple[str, ...]
    source_validator_states: tuple[tuple[str, str], ...]
    contract: PacapdgUapTypeContract
    ability: PersistentPacaHabilidad
    candidate_artifacts: tuple[CandidateKernelArtifact, ...]
    validators: tuple[TypedValidatorBinding, ...]
    schema_id: str = SCHEMA_ID
    source_bound: bool = True
    runtime_executed: bool = False
    deployment_executed: bool = False
    git_merge_executed: bool = False
    branch_rewrite_executed: bool = False
    uap_execution_authorized: bool = False
    final_kapsyla: bool = False


def stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _source_payload() -> dict[str, object]:
    from .persistent_pacaiogame_skill import (
        build_persistent_pacaiogame_skill_compiler,
        compile_persistent_pacaiogame_skill_compiler,
    )

    return compile_persistent_pacaiogame_skill_compiler(
        build_persistent_pacaiogame_skill_compiler()
    )


def _source_summary(
    source: Mapping[str, object],
) -> tuple[str, str, tuple[str, ...], tuple[tuple[str, str], ...]]:
    raw_artifacts = source.get("canonical_artifacts", ())
    artifacts = (
        tuple(
            str(item.get("artifact_id", ""))
            for item in raw_artifacts
            if isinstance(item, Mapping)
        )
        if isinstance(raw_artifacts, (list, tuple))
        else ()
    )
    raw_validators = source.get("validator_states", {})
    validators = (
        tuple(
            sorted(
                (str(key), str(value))
                for key, value in raw_validators.items()
            )
        )
        if isinstance(raw_validators, Mapping)
        else ()
    )
    return (
        str(source.get("compiler_id", "")),
        str(source.get("compiler_sha256", "")),
        artifacts,
        validators,
    )


def _candidate(
    kind: UapArtifactKind,
    artifact_id: str,
    inputs: tuple[str, ...],
    signature: str,
) -> CandidateKernelArtifact:
    return CandidateKernelArtifact(
        artifact_id=artifact_id,
        kind=kind,
        version=2,
        input_artifact_ids=inputs,
        type_signature=signature,
        facets=(
            "PACAPDG_TYPED",
            "UAP_TYPED",
            "QUNOTYPED",
            "TRACE_PRESERVED",
            "NO_IDENTITY_TRANSPORT",
            "NO_PLURAL_COLLAPSE",
            "SOURCE_BOUND",
            "PI_FIXED_OR_HOLD",
        ),
    )


def _validator(
    kind: str,
    source_ref: str,
    stages: tuple[str, ...],
    status: ValidatorStatus = ValidatorStatus.DECLARED,
) -> TypedValidatorBinding:
    return TypedValidatorBinding(
        validator_id=f"validator:{kind.lower()}:pacapdg-uap",
        validator_kind=kind,
        status=status,
        source_ref=source_ref,
        stage_ids=stages,
    )


def build_pacapdg_uap_persistent_skill_bundle(
    source_payload: Mapping[str, object] | None = None,
) -> PacapdgUapPersistentSkillBundle:
    """Build the source-bound PACAPDG/UAP persistent skill bundle."""

    source = dict(
        _source_payload() if source_payload is None else source_payload
    )
    compiler_id, digest, artifact_ids, validator_states = _source_summary(
        source
    )
    return PacapdgUapPersistentSkillBundle(
        source_compiler_id=compiler_id,
        source_compiler_digest=digest,
        source_compile_state=str(source.get("compile_state", "")),
        source_artifact_ids=artifact_ids,
        source_validator_states=validator_states,
        contract=PacapdgUapTypeContract(
            contract_id="contract:pacapdg-uap-persistent-paca-habilidad",
            input_type=INPUT_PACKET_TYPE,
            pacapdg_ir_type=PACAPDG_IR_TYPE,
            uap_envelope_type=UAP_ENVELOPE_TYPE,
            output_type=UAP_WITNESS_TYPE,
            facets=REQUIRED_FACETS,
            stage_order=REQUIRED_STAGE_ORDER,
        ),
        ability=PersistentPacaHabilidad(
            ability_id="habilidad:persistent-pacaiogame-sigil4godot-uap",
            source_skill_id="skill:persistent-pacaiogame-sigil4godot",
            annotated_type_id=(
                "PydantikaAnnotatedPacapdgUapPersistentPacaHabilidad"
            ),
            surfaces=("PACAIOGAMES", "SIGIL4GODOT", "SIGIL4CPYTHON"),
            persistence_key=(
                "paca.habilidad.pacaiogames.sigil4godot.uap.v1"
            ),
            replay_entrypoint=(
                "compile_pacapdg_uap_persistent_skill_bundle"
            ),
        ),
        candidate_artifacts=(
            _candidate(
                UapArtifactKind.SIGIL_AST,
                CANDIDATE_AST_ID,
                (SOURCE_AST_ID,),
                "SIGIL_AST_V1 -> PACAPDG_TYPED_UAP -> SIGIL_AST_V2",
            ),
            _candidate(
                UapArtifactKind.SIGIL_SYNTACTICAL_KERNEL,
                CANDIDATE_SYNTACTICAL_KERNEL_ID,
                (CANDIDATE_AST_ID,),
                "SIGIL_AST_V2 -> SIGIL_SYNTACTICAL_KERNEL_V2",
            ),
            _candidate(
                UapArtifactKind.SIGIL_SEMANTICAL_KERNEL,
                CANDIDATE_SEMANTICAL_KERNEL_ID,
                (CANDIDATE_SYNTACTICAL_KERNEL_ID,),
                "SIGIL_SYNTAX_V2 -> QUAZRIS -> SIGIL_SEMANTICS_V2",
            ),
        ),
        validators=(
            _validator(
                "PACAPDG_UAP",
                "Lib/sigil4cpython/pacapdg_uap_persistent_skill.py",
                ("PACAPDG_PARSE", "QUNOTYPED_ROUTE", "UAP_ADMIT"),
            ),
            _validator(
                "PYDANTIKA",
                "Tools/sigil4cpython/pacapdg_uap_persistent_skill_models.py",
                ("PYDANTIKA_ANNOTATE",),
            ),
            _validator(
                "DISKOTIKA",
                "Tools/sigil4cpython/diskotika_pacapdg_uap.py",
                ("DISKOTIKA_COMPOSE",),
            ),
            _validator(
                "LENA_LEAN4",
                "formal/sigil4cpython/PersistentPacaSkillUAP.lean",
                ("LENA_LEAN4_VALIDATE",),
            ),
            _validator(
                "ARAKNE_REWRITE",
                "source-bound-open-pr-ledger",
                ("ARAKNE_REWRITE",),
            ),
            _validator(
                "PACA_ANTORCHA",
                "source-paca-antorcha-plan",
                ("PACA_ANTORCHA_NORMALIZE",),
            ),
            _validator(
                "QUAZRIS",
                "Lib/sigil4cpython/localization_polyglot.py",
                ("QUAZRIS_LOCALIZE",),
            ),
            _validator(
                "STRIKK",
                "actions/runs/30654349949/job/91234960898",
                ("STRIKK_VALIDATE",),
                ValidatorStatus.PASS,
            ),
        ),
    )


def _validate_contract(contract: PacapdgUapTypeContract) -> list[str]:
    errors: list[str] = []
    if contract.input_type != INPUT_PACKET_TYPE:
        errors.append("pacapdg_uap_input_type_mismatch")
    if contract.pacapdg_ir_type != PACAPDG_IR_TYPE:
        errors.append("pacapdg_typed_ir_missing")
    if contract.uap_envelope_type != UAP_ENVELOPE_TYPE:
        errors.append("uap_envelope_type_missing")
    if contract.output_type != UAP_WITNESS_TYPE:
        errors.append("uap_witness_type_mismatch")
    if contract.stage_order != REQUIRED_STAGE_ORDER:
        errors.append("pacapdg_uap_stage_order_mismatch")
    missing = sorted(set(REQUIRED_FACETS) - set(contract.facets))
    if missing:
        errors.append("pacapdg_uap_facets_missing:" + ",".join(missing))
    if len(set(contract.facets)) != len(contract.facets):
        errors.append("pacapdg_uap_duplicate_facet")
    if not contract.source_bound:
        errors.append("pacapdg_uap_not_source_bound")
    if not contract.trace_preserved:
        errors.append("pacapdg_uap_trace_drift")
    if not contract.no_identity_transport:
        errors.append("pacapdg_uap_identity_transport")
    if not contract.no_plural_collapse:
        errors.append("pacapdg_uap_plural_collapse")
    if not contract.pi_fixed_or_hold:
        errors.append("pacapdg_uap_pi_drift")
    if contract.execution_authority:
        errors.append("pacapdg_uap_execution_authority")
    return errors


def _validate_bundle(bundle: PacapdgUapPersistentSkillBundle) -> list[str]:
    errors = _validate_contract(bundle.contract)
    if bundle.schema_id != SCHEMA_ID:
        errors.append("pacapdg_uap_schema_mismatch")
    if bundle.source_compiler_id != SOURCE_SCHEMA_ID:
        errors.append("pacapdg_uap_source_schema_mismatch")
    if not HEX64.fullmatch(bundle.source_compiler_digest):
        errors.append("pacapdg_uap_source_digest_invalid")
    if bundle.source_compile_state not in {
        UapCompileState.ADMIT_PLAN_ONLY.value,
        UapCompileState.HOLD_WITH_OBSTRUCTION.value,
    }:
        errors.append("pacapdg_uap_source_rejected")
    if set(bundle.source_artifact_ids) != {
        SOURCE_AST_ID,
        SOURCE_SYNTACTICAL_KERNEL_ID,
        SOURCE_SEMANTICAL_KERNEL_ID,
    }:
        errors.append("pacapdg_uap_source_artifact_family_mismatch")
    source_validators = dict(bundle.source_validator_states)
    if not SOURCE_REQUIRED_VALIDATORS.issubset(source_validators):
        errors.append("pacapdg_uap_source_validator_family_incomplete")
    if any(value == "FAIL" for value in source_validators.values()):
        errors.append("pacapdg_uap_source_validator_failed")
    if any(value == "HOLD" for value in source_validators.values()):
        errors.append("pacapdg_uap_source_validator_held")

    ability = bundle.ability
    required_surfaces = {"PACAIOGAMES", "SIGIL4GODOT", "SIGIL4CPYTHON"}
    if not required_surfaces.issubset(ability.surfaces):
        errors.append("persistent_paca_habilidad_surface_missing")
    if not ability.source_bound or not ability.trace_preserved:
        errors.append("persistent_paca_habilidad_trace_or_source_boundary")
    if not ability.no_identity_transport:
        errors.append("persistent_paca_habilidad_identity_transport")
    if ability.runtime_executed or ability.deployment_executed:
        errors.append("persistent_paca_habilidad_runtime_execution")

    candidates = {item.kind: item for item in bundle.candidate_artifacts}
    if set(candidates) != set(UapArtifactKind):
        errors.append("uap_candidate_artifact_family_incomplete")
    expected = {
        UapArtifactKind.SIGIL_AST: (CANDIDATE_AST_ID, (SOURCE_AST_ID,)),
        UapArtifactKind.SIGIL_SYNTACTICAL_KERNEL: (
            CANDIDATE_SYNTACTICAL_KERNEL_ID,
            (CANDIDATE_AST_ID,),
        ),
        UapArtifactKind.SIGIL_SEMANTICAL_KERNEL: (
            CANDIDATE_SEMANTICAL_KERNEL_ID,
            (CANDIDATE_SYNTACTICAL_KERNEL_ID,),
        ),
    }
    for kind, (artifact_id, inputs) in expected.items():
        item = candidates.get(kind)
        if item is None:
            continue
        if item.artifact_id != artifact_id or item.input_artifact_ids != inputs:
            errors.append(
                f"uap_candidate_id_or_input_mismatch:{kind.value}"
            )
        if item.version != 2 or not item.canonical_candidate:
            errors.append(f"uap_candidate_version_or_flag:{item.artifact_id}")
        if not {"PACAPDG_TYPED", "UAP_TYPED"}.issubset(item.facets):
            errors.append(f"uap_candidate_facets_missing:{item.artifact_id}")
        if item.promoted:
            errors.append(
                f"uap_candidate_premature_promotion:{item.artifact_id}"
            )

    validator_kinds = {item.validator_kind for item in bundle.validators}
    if validator_kinds != REQUIRED_VALIDATORS:
        errors.append("pacapdg_uap_validator_family_incomplete")
    if len(validator_kinds) != len(bundle.validators):
        errors.append("duplicate_pacapdg_uap_validator")
    for item in bundle.validators:
        if not item.source_ref or not item.stage_ids:
            errors.append(
                f"uap_validator_source_or_stage_missing:{item.validator_kind}"
            )
        if not item.preserves_trace or not item.no_identity_transport:
            errors.append(
                f"uap_validator_identity_transport:{item.validator_kind}"
            )
        if item.status == ValidatorStatus.FAIL:
            errors.append(f"uap_validator_failed:{item.validator_kind}")
        if item.status == ValidatorStatus.HOLD:
            errors.append(f"uap_validator_held:{item.validator_kind}")

    if not bundle.source_bound:
        errors.append("pacapdg_uap_bundle_not_source_bound")
    if bundle.runtime_executed or bundle.deployment_executed:
        errors.append("pacapdg_uap_runtime_execution")
    if bundle.git_merge_executed:
        errors.append("pacapdg_uap_git_merge")
    if bundle.branch_rewrite_executed:
        errors.append("pacapdg_uap_branch_rewrite")
    if bundle.uap_execution_authorized:
        errors.append("pacapdg_uap_execution_authorized_without_gate")
    if bundle.final_kapsyla:
        errors.append("pacapdg_uap_final_kapsyla_forbidden")
    return errors


def _diskotika_route() -> list[dict[str, str]]:
    objects = (
        INPUT_PACKET_TYPE,
        PACAPDG_IR_TYPE,
        UAP_ENVELOPE_TYPE,
        CANDIDATE_AST_ID,
        CANDIDATE_SYNTACTICAL_KERNEL_ID,
        CANDIDATE_SEMANTICAL_KERNEL_ID,
        UAP_WITNESS_TYPE,
    )
    relations = (
        "PACAPDG_TYPED_PARSE",
        "QUNOTYPED_UAP_ENVELOPE",
        "SIGIL_AST_PLURAL_COMPILE",
        "SIGIL_SYNTACTICAL_COMPILE",
        "QUAZRIS_CONTEXTUAL_LOWERING",
        "STRIKK_TYPED_UAP_ADMISSION",
    )
    return [
        {
            "morphism_id": f"route:{index}",
            "source_type": source,
            "target_type": target,
            "relation_type": relation,
        }
        for index, (source, target, relation) in enumerate(
            zip(objects, objects[1:], relations), start=1
        )
    ]


def compile_pacapdg_uap_persistent_skill_bundle(
    bundle: PacapdgUapPersistentSkillBundle,
) -> dict[str, object]:
    """Validate the bundle and emit a deterministic UAP admission payload."""

    errors = _validate_bundle(bundle)
    reject_markers = (
        "schema_mismatch",
        "source_schema_mismatch",
        "digest_invalid",
        "artifact_family_mismatch",
        "facets_missing",
        "validator_family_incomplete",
        "source_rejected",
        "identity_transport",
        "plural_collapse",
        "pi_drift",
        "runtime_execution",
        "deployment",
        "git_merge",
        "branch_rewrite",
        "execution_authority",
        "execution_authorized_without_gate",
        "premature_promotion",
        "validator_failed",
        "final_kapsyla",
    )
    if any(any(marker in error for marker in reject_markers) for error in errors):
        state = UapCompileState.REJECT
    elif (
        bundle.source_compile_state
        == UapCompileState.HOLD_WITH_OBSTRUCTION.value
    ):
        errors.append("pacapdg_uap_source_held")
        state = UapCompileState.HOLD_WITH_OBSTRUCTION
    elif errors:
        state = UapCompileState.HOLD_WITH_OBSTRUCTION
    else:
        state = UapCompileState.ADMIT_PLAN_ONLY

    payload = asdict(bundle)
    payload["source_validator_states"] = dict(bundle.source_validator_states)
    payload["candidate_artifacts"] = []
    for artifact in bundle.candidate_artifacts:
        item = asdict(artifact)
        item["artifact_sha256"] = stable_digest(item)
        payload["candidate_artifacts"].append(item)
    payload["compile_state"] = state.value
    payload["promotion_state"] = "CANDIDATE_CANONICAL_NOT_PROMOTED"
    payload["obstruction_ledger"] = errors
    payload["validator_states"] = {
        item.validator_kind: item.status.value for item in bundle.validators
    }
    payload["hosted_validation_required"] = any(
        item.status == ValidatorStatus.DECLARED for item in bundle.validators
    )
    payload["diskotika_route"] = _diskotika_route()
    payload["runtime_executed"] = False
    payload["deployment_executed"] = False
    payload["git_merge_executed"] = False
    payload["branch_rewrite_executed"] = False
    payload["uap_execution_authorized"] = False
    payload["candidate_promoted"] = False
    payload["final_kapsyla"] = False
    payload["bundle_sha256"] = stable_digest(payload)
    return payload


__all__ = [
    "CANDIDATE_AST_ID",
    "CANDIDATE_SEMANTICAL_KERNEL_ID",
    "CANDIDATE_SYNTACTICAL_KERNEL_ID",
    "CandidateKernelArtifact",
    "PacapdgUapPersistentSkillBundle",
    "PacapdgUapTypeContract",
    "PersistentPacaHabilidad",
    "REQUIRED_FACETS",
    "REQUIRED_STAGE_ORDER",
    "SCHEMA_ID",
    "TypedValidatorBinding",
    "UapArtifactKind",
    "UapCompileState",
    "ValidatorStatus",
    "build_pacapdg_uap_persistent_skill_bundle",
    "compile_pacapdg_uap_persistent_skill_bundle",
    "stable_digest",
]
