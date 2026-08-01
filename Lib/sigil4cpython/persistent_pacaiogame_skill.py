"""Persistent PACA skill compiler contracts for SIGIL4CPython.

The module binds PACAIoGames and SIGIL4Godot to source-bound plural types and
compiles three canonical metadata artifacts: the SIGIL AST, syntactical kernel,
and semantical kernel.  It is deliberately dependency free.  Pydantika and
DisCoPy validators live under ``Tools/sigil4cpython``.

Compilation here means deterministic validation and witness emission.  It does
not start Godot, execute PyTorch, merge Git branches, deploy a runtime, or alter
CPython interpreter semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping


SCHEMA_ID = "SIGIL4CPYTHON_PERSISTENT_PACAIOGAME_SKILL_COMPILER_V1"
CANONICAL_AST_ID = "SIGIL_AST_V1"
CANONICAL_SYNTACTICAL_KERNEL_ID = "SIGIL_SYNTACTICAL_KERNEL_V1"
CANONICAL_SEMANTICAL_KERNEL_ID = "SIGIL_SEMANTICAL_KERNEL_V1"
LINKED_VALIDATOR_BASELINE = (
    "https://github.com/jbermejovega/sigil4cpython/actions/runs/"
    "30654349949/job/91234960898"
)


class SkillCompileState(str, Enum):
    ADMIT_PLAN_ONLY = "ADMIT_PLAN_ONLY"
    HOLD_WITH_OBSTRUCTION = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT"


class CanonicalArtifactKind(str, Enum):
    SIGIL_AST = "SIGIL_AST"
    SIGIL_SYNTACTICAL_KERNEL = "SIGIL_SYNTACTICAL_KERNEL"
    SIGIL_SEMANTICAL_KERNEL = "SIGIL_SEMANTICAL_KERNEL"


class RuntimeSurface(str, Enum):
    PACAIOGAMES = "PACAIOGAMES"
    SIGIL4GODOT = "SIGIL4GODOT"
    SIGIL4CPYTHON = "SIGIL4CPYTHON"


class ValidatorKind(str, Enum):
    PYDANTIKA = "PYDANTIKA"
    DISKOTIKA = "DISKOTIKA"
    LENA_LEAN4 = "LENA_LEAN4"
    ARAKNE_REWRITE = "ARAKNE_REWRITE"
    PACA_ANTORCHA = "PACA_ANTORCHA"
    QUAZRIS = "QUAZRIS"
    STRIKK = "STRIKK"


class ValidatorStatus(str, Enum):
    DECLARED = "DECLARED"
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"


class BranchFusionMode(str, Enum):
    SOURCE_BOUND_SEMANTIC_FUSION = "SOURCE_BOUND_SEMANTIC_FUSION"


@dataclass(frozen=True, slots=True)
class AnnotatedTypeBinding:
    binding_id: str
    python_type: str
    semantic_types: tuple[str, ...]
    annotation_ids: tuple[str, ...]
    strict: bool = True
    plural_typed: bool = True
    source_bound: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.binding_id:
            errors.append("annotated_type_binding_id_missing")
        if not self.python_type:
            errors.append(f"annotated_python_type_missing:{self.binding_id}")
        if len(set(self.semantic_types)) < 2:
            errors.append(f"annotated_plural_types_missing:{self.binding_id}")
        if not self.annotation_ids:
            errors.append(f"annotated_metadata_missing:{self.binding_id}")
        if not self.strict:
            errors.append(f"annotated_type_not_strict:{self.binding_id}")
        if not self.plural_typed:
            errors.append(f"annotated_type_plural_collapse:{self.binding_id}")
        if not self.source_bound:
            errors.append(f"annotated_type_not_source_bound:{self.binding_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PersistentPacaSkill:
    skill_id: str
    surfaces: tuple[RuntimeSurface, ...]
    annotated_type_binding_id: str
    persistence_key: str
    replay_entrypoint: str
    resource_bound: str
    trace_preserved: bool = True
    no_identity_transport: bool = True
    runtime_executed: bool = False
    deployment_executed: bool = False

    def validate(self, known_binding_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.skill_id:
            errors.append("persistent_skill_id_missing")
        required = {
            RuntimeSurface.PACAIOGAMES,
            RuntimeSurface.SIGIL4GODOT,
            RuntimeSurface.SIGIL4CPYTHON,
        }
        if not required.issubset(set(self.surfaces)):
            errors.append(f"persistent_skill_surface_missing:{self.skill_id}")
        if self.annotated_type_binding_id not in known_binding_ids:
            errors.append(f"persistent_skill_unknown_annotation:{self.skill_id}")
        if not self.persistence_key:
            errors.append(f"persistent_skill_key_missing:{self.skill_id}")
        if not self.replay_entrypoint:
            errors.append(f"persistent_skill_replay_missing:{self.skill_id}")
        if not self.resource_bound:
            errors.append(f"persistent_skill_resource_bound_missing:{self.skill_id}")
        if not self.trace_preserved:
            errors.append(f"persistent_skill_trace_drift:{self.skill_id}")
        if not self.no_identity_transport:
            errors.append(f"persistent_skill_identity_transport:{self.skill_id}")
        if self.runtime_executed:
            errors.append(f"persistent_skill_runtime_execution:{self.skill_id}")
        if self.deployment_executed:
            errors.append(f"persistent_skill_deployment:{self.skill_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class DiskotikaMorphism:
    morphism_id: str
    source_type: str
    target_type: str
    relation_type: str
    preserves_trace: bool = True
    preserves_plural_type: bool = True

    def validate(self, known_types: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.morphism_id:
            errors.append("diskotika_morphism_id_missing")
        if self.source_type not in known_types or self.target_type not in known_types:
            errors.append(f"diskotika_unknown_object:{self.morphism_id}")
        if not self.relation_type:
            errors.append(f"diskotika_relation_type_missing:{self.morphism_id}")
        if not self.preserves_trace:
            errors.append(f"diskotika_trace_drift:{self.morphism_id}")
        if not self.preserves_plural_type:
            errors.append(f"diskotika_plural_collapse:{self.morphism_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class DiskotikaDiagram:
    diagram_id: str
    object_types: tuple[str, ...]
    morphisms: tuple[DiskotikaMorphism, ...]
    optional_runtime_dependency: bool = True
    diagram_executed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.diagram_id:
            errors.append("diskotika_diagram_id_missing")
        known_types = set(self.object_types)
        required = {
            CANONICAL_AST_ID,
            CANONICAL_SYNTACTICAL_KERNEL_ID,
            CANONICAL_SEMANTICAL_KERNEL_ID,
        }
        if not required.issubset(known_types):
            errors.append("diskotika_canonical_objects_missing")
        if len(self.morphisms) < 2:
            errors.append("diskotika_composition_chain_missing")
        for morphism in self.morphisms:
            errors.extend(morphism.validate(known_types))
        for left, right in zip(self.morphisms, self.morphisms[1:]):
            if left.target_type != right.source_type:
                errors.append(
                    "diskotika_noncomposable_chain:"
                    f"{left.morphism_id}->{right.morphism_id}"
                )
        if self.diagram_executed:
            errors.append("diskotika_runtime_execution_forbidden")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PacaAntorchaPlan:
    plan_id: str
    tensor_types: tuple[str, ...]
    normalization_strategy: str
    resource_budget: str
    device_authority: str = "PLAN_ONLY"
    resource_budget_declared: bool = True
    model_executed: bool = False
    tensor_allocated: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.plan_id:
            errors.append("paca_antorcha_plan_id_missing")
        if not self.tensor_types:
            errors.append(f"paca_antorcha_tensor_types_missing:{self.plan_id}")
        if not self.normalization_strategy:
            errors.append(f"paca_antorcha_normalizer_missing:{self.plan_id}")
        if not self.resource_budget or not self.resource_budget_declared:
            errors.append(f"paca_antorcha_resource_bound_missing:{self.plan_id}")
        if self.device_authority != "PLAN_ONLY":
            errors.append(f"paca_antorcha_device_authority:{self.plan_id}")
        if self.model_executed:
            errors.append(f"paca_antorcha_model_execution:{self.plan_id}")
        if self.tensor_allocated:
            errors.append(f"paca_antorcha_tensor_allocation:{self.plan_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class QuazrisLoweringPlan:
    plan_id: str
    source_artifact_id: str
    output_types: tuple[str, ...]
    localization_type: str
    backend_identity_preserved: bool = True
    resource_cost_preserved: bool = True
    runtime_executed: bool = False

    def validate(self, known_artifact_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.plan_id:
            errors.append("quazris_plan_id_missing")
        if self.source_artifact_id not in known_artifact_ids:
            errors.append(f"quazris_unknown_source:{self.plan_id}")
        required_outputs = {
            "PYTHON_TYPED_IR",
            "SIGIL4GODOT_RUNTIME_PLAN",
            "PACAIOGAMES_SKILL_PLAN",
            "SIGIL_AST_IR",
        }
        if not required_outputs.issubset(set(self.output_types)):
            errors.append(f"quazris_output_missing:{self.plan_id}")
        if not self.localization_type:
            errors.append(f"quazris_localization_type_missing:{self.plan_id}")
        if not self.backend_identity_preserved:
            errors.append(f"quazris_backend_identity_collapse:{self.plan_id}")
        if not self.resource_cost_preserved:
            errors.append(f"quazris_resource_cost_erasure:{self.plan_id}")
        if self.runtime_executed:
            errors.append(f"quazris_runtime_execution:{self.plan_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class ArakneFusionPlan:
    plan_id: str
    source_branch_refs: tuple[str, ...]
    target_branch_ref: str
    rewrite_rules: tuple[str, ...]
    mode: BranchFusionMode = BranchFusionMode.SOURCE_BOUND_SEMANTIC_FUSION
    source_bound: bool = True
    branch_identities_preserved: bool = True
    open_pr_authority_absorbed: bool = False
    git_merge_executed: bool = False
    branch_rewrite_executed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.plan_id:
            errors.append("arakne_plan_id_missing")
        if len(set(self.source_branch_refs)) < 2:
            errors.append(f"arakne_plural_branch_refs_missing:{self.plan_id}")
        if not self.target_branch_ref:
            errors.append(f"arakne_target_branch_missing:{self.plan_id}")
        if not self.rewrite_rules:
            errors.append(f"arakne_rewrite_rules_missing:{self.plan_id}")
        if not self.source_bound:
            errors.append(f"arakne_source_boundary_missing:{self.plan_id}")
        if not self.branch_identities_preserved:
            errors.append(f"arakne_branch_identity_collapse:{self.plan_id}")
        if self.open_pr_authority_absorbed:
            errors.append(f"arakne_open_pr_authority_absorbed:{self.plan_id}")
        if self.git_merge_executed:
            errors.append(f"arakne_git_merge_executed:{self.plan_id}")
        if self.branch_rewrite_executed:
            errors.append(f"arakne_branch_rewrite_executed:{self.plan_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class ValidatorWitness:
    witness_id: str
    validator: ValidatorKind
    status: ValidatorStatus
    artifact_kinds: tuple[CanonicalArtifactKind, ...]
    source_ref: str
    preserves_trace: bool = True
    no_identity_transport: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.witness_id:
            errors.append("validator_witness_id_missing")
        if not self.artifact_kinds:
            errors.append(f"validator_artifacts_missing:{self.witness_id}")
        if not self.source_ref:
            errors.append(f"validator_source_ref_missing:{self.witness_id}")
        if not self.preserves_trace:
            errors.append(f"validator_trace_drift:{self.witness_id}")
        if not self.no_identity_transport:
            errors.append(f"validator_identity_transport:{self.witness_id}")
        if self.status == ValidatorStatus.FAIL:
            errors.append(f"validator_failed:{self.validator.value}")
        if self.status == ValidatorStatus.HOLD:
            errors.append(f"validator_held:{self.validator.value}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class CanonicalKernelArtifact:
    artifact_id: str
    kind: CanonicalArtifactKind
    version: int
    input_artifact_ids: tuple[str, ...]
    type_signature: str
    invariants: tuple[str, ...]
    source_bound: bool = True
    canonical: bool = True

    def validate(self, known_artifact_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        expected_ids = {
            CanonicalArtifactKind.SIGIL_AST: CANONICAL_AST_ID,
            CanonicalArtifactKind.SIGIL_SYNTACTICAL_KERNEL: (
                CANONICAL_SYNTACTICAL_KERNEL_ID
            ),
            CanonicalArtifactKind.SIGIL_SEMANTICAL_KERNEL: (
                CANONICAL_SEMANTICAL_KERNEL_ID
            ),
        }
        if self.artifact_id != expected_ids[self.kind]:
            errors.append(f"canonical_artifact_id_mismatch:{self.kind.value}")
        if self.version < 1:
            errors.append(f"canonical_artifact_version_invalid:{self.artifact_id}")
        if set(self.input_artifact_ids) - known_artifact_ids:
            errors.append(f"canonical_artifact_unknown_input:{self.artifact_id}")
        if not self.type_signature:
            errors.append(f"canonical_artifact_signature_missing:{self.artifact_id}")
        required_invariants = {
            "TRACE_PRESERVED",
            "NO_IDENTITY_TRANSPORT",
            "NO_PLURAL_COLLAPSE",
        }
        if not required_invariants.issubset(set(self.invariants)):
            errors.append(f"canonical_artifact_invariants_missing:{self.artifact_id}")
        if not self.source_bound:
            errors.append(f"canonical_artifact_not_source_bound:{self.artifact_id}")
        if not self.canonical:
            errors.append(f"canonical_artifact_not_canonical:{self.artifact_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PersistentPacaSkillCompiler:
    compiler_id: str
    annotations: tuple[AnnotatedTypeBinding, ...]
    skills: tuple[PersistentPacaSkill, ...]
    artifacts: tuple[CanonicalKernelArtifact, ...]
    diskotika: DiskotikaDiagram
    paca_antorcha: PacaAntorchaPlan
    quazris: QuazrisLoweringPlan
    arakne: ArakneFusionPlan
    validators: tuple[ValidatorWitness, ...]
    schema_id: str = SCHEMA_ID
    linked_validator_baseline: str = LINKED_VALIDATOR_BASELINE
    source_bound: bool = True
    runtime_executed: bool = False
    deployment_executed: bool = False
    git_merge_executed: bool = False
    cpython_semantics_changed: bool = False
    final_kapsyla: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.compiler_id:
            errors.append("persistent_compiler_id_missing")
        if self.schema_id != SCHEMA_ID:
            errors.append("persistent_compiler_schema_mismatch")
        if self.linked_validator_baseline != LINKED_VALIDATOR_BASELINE:
            errors.append("persistent_compiler_baseline_mismatch")
        if not self.source_bound:
            errors.append("persistent_compiler_not_source_bound")
        if self.runtime_executed:
            errors.append("persistent_compiler_runtime_execution")
        if self.deployment_executed:
            errors.append("persistent_compiler_deployment")
        if self.git_merge_executed:
            errors.append("persistent_compiler_git_merge")
        if self.cpython_semantics_changed:
            errors.append("persistent_compiler_cpython_semantics_changed")
        if self.final_kapsyla:
            errors.append("persistent_compiler_final_kapsyla_forbidden")

        binding_ids = {item.binding_id for item in self.annotations}
        if len(binding_ids) != len(self.annotations):
            errors.append("duplicate_annotated_type_binding")
        for item in self.annotations:
            errors.extend(item.validate())

        skill_ids = {item.skill_id for item in self.skills}
        if len(skill_ids) != len(self.skills):
            errors.append("duplicate_persistent_skill")
        for item in self.skills:
            errors.extend(item.validate(binding_ids))

        artifact_ids = {item.artifact_id for item in self.artifacts}
        artifact_kinds = {item.kind for item in self.artifacts}
        if len(artifact_ids) != len(self.artifacts):
            errors.append("duplicate_canonical_artifact_id")
        if artifact_kinds != set(CanonicalArtifactKind):
            errors.append("canonical_artifact_family_incomplete")
        for item in self.artifacts:
            errors.extend(item.validate(artifact_ids))

        by_kind = {item.kind: item for item in self.artifacts}
        ast = by_kind.get(CanonicalArtifactKind.SIGIL_AST)
        syntactical = by_kind.get(CanonicalArtifactKind.SIGIL_SYNTACTICAL_KERNEL)
        semantical = by_kind.get(CanonicalArtifactKind.SIGIL_SEMANTICAL_KERNEL)
        if ast is not None and ast.input_artifact_ids:
            errors.append("sigil_ast_must_be_root_artifact")
        if syntactical is not None and syntactical.input_artifact_ids != (
            CANONICAL_AST_ID,
        ):
            errors.append("sigil_syntactical_kernel_input_mismatch")
        if semantical is not None and semantical.input_artifact_ids != (
            CANONICAL_SYNTACTICAL_KERNEL_ID,
        ):
            errors.append("sigil_semantical_kernel_input_mismatch")

        errors.extend(self.diskotika.validate())
        errors.extend(self.paca_antorcha.validate())
        errors.extend(self.quazris.validate(artifact_ids))
        errors.extend(self.arakne.validate())

        validator_kinds = {item.validator for item in self.validators}
        if len(validator_kinds) != len(self.validators):
            errors.append("duplicate_validator_kind")
        if validator_kinds != set(ValidatorKind):
            errors.append("persistent_validator_family_incomplete")
        for item in self.validators:
            errors.extend(item.validate())
        return tuple(errors)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["annotations"] = [asdict(item) for item in self.annotations]
        payload["skills"] = [asdict(item) for item in self.skills]
        payload["artifacts"] = [asdict(item) for item in self.artifacts]
        payload["diskotika"] = asdict(self.diskotika)
        payload["paca_antorcha"] = asdict(self.paca_antorcha)
        payload["quazris"] = asdict(self.quazris)
        payload["arakne"] = asdict(self.arakne)
        payload["validators"] = [asdict(item) for item in self.validators]
        return payload


def stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _artifact(
    kind: CanonicalArtifactKind,
    artifact_id: str,
    inputs: tuple[str, ...],
    signature: str,
) -> CanonicalKernelArtifact:
    return CanonicalKernelArtifact(
        artifact_id=artifact_id,
        kind=kind,
        version=1,
        input_artifact_ids=inputs,
        type_signature=signature,
        invariants=(
            "TRACE_PRESERVED",
            "NO_IDENTITY_TRANSPORT",
            "NO_PLURAL_COLLAPSE",
            "SOURCE_BOUND",
            "PI_FIXED_OR_HOLD",
        ),
    )


def build_persistent_pacaiogame_skill_compiler() -> PersistentPacaSkillCompiler:
    """Build the canonical persistent PACAIoGames skill compiler."""

    annotation = AnnotatedTypeBinding(
        binding_id="annotation:persistent-pacaiogame-sigil4godot",
        python_type="PydantikaAnnotatedPersistentPacaSkill",
        semantic_types=(
            "PERSISTENT_PACA_SKILL",
            "PACAIOGAMES_SKILL",
            "SIGIL4GODOT_RUNTIME_PLAN",
            "DISKOTIKA_TYPED_RELATION",
            "PACA_ANTORCHA_NORMALIZER_PLAN",
            "QUAZRIS_LOCALIZED_VIEW",
        ),
        annotation_ids=(
            "ann:persistent",
            "ann:plural-typed",
            "ann:pacaiogames",
            "ann:sigil4godot",
            "ann:source-bound",
        ),
    )
    artifacts = (
        _artifact(
            CanonicalArtifactKind.SIGIL_AST,
            CANONICAL_AST_ID,
            (),
            "PersistentPacaSkillPacket -> SIGIL_AST",
        ),
        _artifact(
            CanonicalArtifactKind.SIGIL_SYNTACTICAL_KERNEL,
            CANONICAL_SYNTACTICAL_KERNEL_ID,
            (CANONICAL_AST_ID,),
            "SIGIL_AST -> SIGIL_SYNTACTICAL_KERNEL",
        ),
        _artifact(
            CanonicalArtifactKind.SIGIL_SEMANTICAL_KERNEL,
            CANONICAL_SEMANTICAL_KERNEL_ID,
            (CANONICAL_SYNTACTICAL_KERNEL_ID,),
            "SIGIL_SYNTACTICAL_KERNEL -> SIGIL_SEMANTICAL_KERNEL",
        ),
    )
    all_kinds = tuple(CanonicalArtifactKind)
    validators = (
        ValidatorWitness(
            "witness:pydantika:annotated-round-trip",
            ValidatorKind.PYDANTIKA,
            ValidatorStatus.DECLARED,
            all_kinds,
            "Tools/sigil4cpython/persistent_pacaiogame_skill_models.py",
        ),
        ValidatorWitness(
            "witness:diskotika:typed-composition",
            ValidatorKind.DISKOTIKA,
            ValidatorStatus.DECLARED,
            all_kinds,
            "Tools/sigil4cpython/diskotika_persistent_skill.py",
        ),
        ValidatorWitness(
            "witness:lena:lean4-kernel-check",
            ValidatorKind.LENA_LEAN4,
            ValidatorStatus.DECLARED,
            all_kinds,
            "formal/sigil4cpython/PersistentPacaSkill.lean",
        ),
        ValidatorWitness(
            "witness:arakne:semantic-fusion",
            ValidatorKind.ARAKNE_REWRITE,
            ValidatorStatus.DECLARED,
            all_kinds,
            "source-bound-open-pr-ledger",
        ),
        ValidatorWitness(
            "witness:paca-antorcha:normalizer-plan",
            ValidatorKind.PACA_ANTORCHA,
            ValidatorStatus.DECLARED,
            all_kinds,
            "dependency-free-resource-plan",
        ),
        ValidatorWitness(
            "witness:quazris:polyglot-lowering",
            ValidatorKind.QUAZRIS,
            ValidatorStatus.DECLARED,
            all_kinds,
            "Lib/sigil4cpython/localization_polyglot.py",
        ),
        ValidatorWitness(
            "witness:strikk:linked-successful-lint",
            ValidatorKind.STRIKK,
            ValidatorStatus.PASS,
            all_kinds,
            LINKED_VALIDATOR_BASELINE,
        ),
    )
    return PersistentPacaSkillCompiler(
        compiler_id=SCHEMA_ID,
        annotations=(annotation,),
        skills=(
            PersistentPacaSkill(
                skill_id="skill:persistent-pacaiogame-sigil4godot",
                surfaces=(
                    RuntimeSurface.PACAIOGAMES,
                    RuntimeSurface.SIGIL4GODOT,
                    RuntimeSurface.SIGIL4CPYTHON,
                ),
                annotated_type_binding_id=annotation.binding_id,
                persistence_key="paca.skill.pacaiogames.sigil4godot.v1",
                replay_entrypoint="compile_persistent_pacaiogame_skill_compiler",
                resource_bound="PLAN_ONLY_NO_NATIVE_RUNTIME",
            ),
        ),
        artifacts=artifacts,
        diskotika=DiskotikaDiagram(
            diagram_id="diskotika:persistent-sigil-kernel-chain",
            object_types=(
                CANONICAL_AST_ID,
                CANONICAL_SYNTACTICAL_KERNEL_ID,
                CANONICAL_SEMANTICAL_KERNEL_ID,
            ),
            morphisms=(
                DiskotikaMorphism(
                    "morphism:ast-to-syntactical",
                    CANONICAL_AST_ID,
                    CANONICAL_SYNTACTICAL_KERNEL_ID,
                    "PLURAL_TYPED_PARSE_AND_TYPE",
                ),
                DiskotikaMorphism(
                    "morphism:syntactical-to-semantical",
                    CANONICAL_SYNTACTICAL_KERNEL_ID,
                    CANONICAL_SEMANTICAL_KERNEL_ID,
                    "CONTEXTUAL_INTERPRETATION",
                ),
            ),
        ),
        paca_antorcha=PacaAntorchaPlan(
            plan_id="paca-antorcha:persistent-skill-normalizer",
            tensor_types=(
                "ANNOTATED_SKILL_TENSOR",
                "PLURAL_RELATION_TENSOR",
                "RESOURCE_OBSTRUCTION_TENSOR",
            ),
            normalization_strategy="REPLAY_SAFE_LOCAL_NORMAL_FORM",
            resource_budget="NO_ALLOCATION_PLAN_ONLY",
        ),
        quazris=QuazrisLoweringPlan(
            plan_id="quazris:persistent-skill-polyglot-lowering",
            source_artifact_id=CANONICAL_AST_ID,
            output_types=(
                "PYTHON_TYPED_IR",
                "SIGIL4GODOT_RUNTIME_PLAN",
                "PACAIOGAMES_SKILL_PLAN",
                "SIGIL_AST_IR",
                "RESOURCE_OBSTRUCTION_IR",
            ),
            localization_type="PLURAL_TYPED_FOCAL_LOCALIZATION",
        ),
        arakne=ArakneFusionPlan(
            plan_id="arakne:source-bound-open-pr-semantic-fusion",
            source_branch_refs=(
                "sigil4cpython#7:agent/virtual-rest-io-kernels-v1",
                "sigilbook:open-pr-ledger-view",
            ),
            target_branch_ref="agent/virtual-rest-io-kernels-v1",
            rewrite_rules=(
                "normalize_lexical_aliases_without_erasure",
                "preserve_open_pr_epoch_identity",
                "fuse_compatible_local_sections_only",
                "emit_obstruction_on_noncommuting_overlap",
            ),
        ),
        validators=validators,
    )


def compile_persistent_pacaiogame_skill_compiler(
    compiler: PersistentPacaSkillCompiler,
) -> dict[str, object]:
    """Validate and plural-compile the canonical SIGIL metadata artifacts."""

    errors = compiler.validate()
    reject_markers = (
        "identity_transport",
        "plural_collapse",
        "runtime_execution",
        "deployment",
        "git_merge",
        "branch_rewrite_executed",
        "authority_absorbed",
        "cpython_semantics_changed",
        "model_execution",
        "tensor_allocation",
        "device_authority",
        "validator_failed",
    )
    if any(any(marker in error for marker in reject_markers) for error in errors):
        state = SkillCompileState.REJECT
    elif errors:
        state = SkillCompileState.HOLD_WITH_OBSTRUCTION
    else:
        state = SkillCompileState.ADMIT_PLAN_ONLY

    payload = compiler.to_dict()
    canonical_artifacts: list[dict[str, object]] = []
    for artifact in compiler.artifacts:
        artifact_payload = asdict(artifact)
        artifact_payload["artifact_sha256"] = stable_digest(artifact_payload)
        canonical_artifacts.append(artifact_payload)
    payload["canonical_artifacts"] = canonical_artifacts
    payload["compile_state"] = state.value
    payload["obstruction_ledger"] = list(errors)
    payload["validator_states"] = {
        item.validator.value: item.status.value for item in compiler.validators
    }
    payload["hosted_validation_required"] = any(
        item.status == ValidatorStatus.DECLARED for item in compiler.validators
    )
    payload["runtime_executed"] = False
    payload["deployment_executed"] = False
    payload["git_merge_executed"] = False
    payload["branch_rewrite_executed"] = False
    payload["cpython_semantics_changed"] = False
    payload["final_kapsyla"] = False
    payload["compiler_sha256"] = stable_digest(payload)
    return payload


__all__ = [
    "AnnotatedTypeBinding",
    "ArakneFusionPlan",
    "BranchFusionMode",
    "CANONICAL_AST_ID",
    "CANONICAL_SEMANTICAL_KERNEL_ID",
    "CANONICAL_SYNTACTICAL_KERNEL_ID",
    "CanonicalArtifactKind",
    "CanonicalKernelArtifact",
    "DiskotikaDiagram",
    "DiskotikaMorphism",
    "LINKED_VALIDATOR_BASELINE",
    "PacaAntorchaPlan",
    "PersistentPacaSkill",
    "PersistentPacaSkillCompiler",
    "QuazrisLoweringPlan",
    "RuntimeSurface",
    "SCHEMA_ID",
    "SkillCompileState",
    "ValidatorKind",
    "ValidatorStatus",
    "ValidatorWitness",
    "build_persistent_pacaiogame_skill_compiler",
    "compile_persistent_pacaiogame_skill_compiler",
    "stable_digest",
]
