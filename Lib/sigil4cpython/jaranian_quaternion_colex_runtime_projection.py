"""Dependency-free projection of the Jaranian Godot quaternion colex runtime."""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
from hashlib import sha256
import json

SCHEMA_ID = "SIGIL4CPYTHON_JARANIAN_QUATERNION_COLEX_RUNTIME_PROJECTION_V1"
CANON = "PIORNALEGO_ES_CANON"
SIGILBOOK_PULL_REQUEST = 746
SIGILBOOK_RUNTIME_HEAD = "28fd3f150fb1520ea322b35d4d6542a7738ae11d"


class RuntimeProjectionState(str, Enum):
    ADMIT_SOURCE_RUNTIME_PROJECTION = "ADMIT_SOURCE_RUNTIME_PROJECTION"
    REJECT = "REJECT"


@dataclass(frozen=True, slots=True)
class GodotSourceFile:
    path: str
    role: str
    source_only: bool = True
    parser_observed: bool = False
    runtime_executed: bool = False


@dataclass(frozen=True, slots=True)
class QuaternionEquation:
    equation_id: str
    left: tuple[str, ...]
    right: str
    expected_sign: int = 1
    source_checked: bool = True
    runtime_observed: bool = False


@dataclass(frozen=True, slots=True)
class ContextRule:
    axis: str
    context_id: str
    identity_visible: bool
    stabilizer_visible: bool
    chirality_layers_visible: bool
    held_axes: tuple[str, ...]
    all_relations_jointly_measurable: bool = False
    physical_measurement_executed: bool = False


@dataclass(frozen=True, slots=True)
class JaranianQuaternionColexRuntimeProjection:
    source_files: tuple[GodotSourceFile, ...]
    equations: tuple[QuaternionEquation, ...]
    contexts: tuple[ContextRule, ...]
    schema_id: str = SCHEMA_ID
    source_repository: str = "jbermejovega/sigilbook"
    source_pull_request: int = SIGILBOOK_PULL_REQUEST
    source_head_sha: str = SIGILBOOK_RUNTIME_HEAD
    identity_cell_id: str = "cell.identity"
    identity_relation_id: str = "rel.identity"
    stabilizer_polytope_id: str = "StabilizerOctahedron_Gold"
    identity_anchor_id: str = "Identity_ONE_Gold"
    colors: tuple[tuple[str, str], ...] = (
        ("BRANE_CYAN", "#22D3EE"),
        ("KINK_MAGENTA", "#F472B6"),
        ("PIORNALEGO_GOLD", "#F5C542"),
        ("PARCHMENT_CREAM", "#F8F6E8"),
    )
    opposite_phase_operation: str = "QUATERNION_ANTIPODE"
    composite_states_normalized: bool = True
    phase_projection_radius: str = "sqrt(3)"
    parity_layers_are_pauli_contexts: bool = False
    render_is_projection: bool = True
    dependency_free: bool = True
    cpython_semantics_changed: bool = False
    abi_changed: bool = False
    godot_started: bool = False
    scene_instantiated: bool = False
    physical_measurement_executed: bool = False
    runtime_executed: bool = False
    identity_transport: bool = False
    trace_preserved: bool = True
    pi_fixed: bool = True
    final_kapsyla: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.source_repository != "jbermejovega/sigilbook":
            errors.append("runtime_source_repository_mismatch")
        if self.source_pull_request != SIGILBOOK_PULL_REQUEST:
            errors.append("runtime_source_pull_request_mismatch")
        if self.source_head_sha != SIGILBOOK_RUNTIME_HEAD:
            errors.append("runtime_source_head_drift")
        expected_paths = {
            "godot/sigil4godot/jaranian/JaranianQuaternionColex.gd",
            "godot/sigil4godot/jaranian/JaranianBasisRenderer.gd",
            "godot/sigil4godot/jaranian/JaranianQuaternionColex.tscn",
        }
        if {item.path for item in self.source_files} != expected_paths:
            errors.append("godot_source_inventory_mismatch")
        if any(not item.source_only or item.parser_observed or item.runtime_executed for item in self.source_files):
            errors.append("godot_source_execution_boundary_broken")
        expected_equations = {
            "X2_NEG_ONE", "Y2_NEG_ONE", "Z2_NEG_ONE",
            "XY_Z", "YZ_X", "ZX_Y",
            "YX_NEG_Z", "ZY_NEG_X", "XZ_NEG_Y",
            "XYZ_NEG_ONE", "ONE_X_X",
        }
        if {item.equation_id for item in self.equations} != expected_equations:
            errors.append("quaternion_equation_inventory_mismatch")
        if any(not item.source_checked or item.runtime_observed for item in self.equations):
            errors.append("quaternion_equation_runtime_boundary_broken")
        if {item.axis for item in self.contexts} != {"GLOBAL", "X", "Y", "Z"}:
            errors.append("context_inventory_mismatch")
        for context in self.contexts:
            if not context.identity_visible or not context.stabilizer_visible or not context.chirality_layers_visible:
                errors.append(f"context_erases_required_geometry:{context.axis}")
            if context.axis != "GLOBAL" and not context.held_axes:
                errors.append(f"context_held_axis_inventory_missing:{context.axis}")
            if context.all_relations_jointly_measurable or context.physical_measurement_executed:
                errors.append(f"context_overclaims_measurement:{context.axis}")
        if self.identity_anchor_id == self.stabilizer_polytope_id:
            errors.append("identity_silently_collapsed_into_stabilizer_polytope")
        if self.opposite_phase_operation != "QUATERNION_ANTIPODE":
            errors.append("opposite_phase_must_use_antipode")
        if not self.composite_states_normalized or self.phase_projection_radius != "sqrt(3)":
            errors.append("quaternion_phase_projection_mismatch")
        if self.parity_layers_are_pauli_contexts:
            errors.append("parity_context_collapse")
        if not self.render_is_projection or not self.dependency_free:
            errors.append("projection_or_dependency_boundary_broken")
        if self.cpython_semantics_changed or self.abi_changed:
            errors.append("cpython_boundary_broken")
        if self.godot_started or self.scene_instantiated or self.physical_measurement_executed or self.runtime_executed:
            errors.append("runtime_execution_claim_forbidden")
        if self.identity_transport or not self.trace_preserved or not self.pi_fixed or self.final_kapsyla:
            errors.append("replay_identity_or_kapsyla_boundary_broken")
        return tuple(errors)

    @property
    def state(self) -> RuntimeProjectionState:
        return RuntimeProjectionState.ADMIT_SOURCE_RUNTIME_PROJECTION if not self.validate() else RuntimeProjectionState.REJECT

    @property
    def projection_sha256(self) -> str:
        payload = _encode(asdict(self))
        return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def receipt(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "canon": CANON,
            "state": self.state.value,
            "source_head_sha": self.source_head_sha,
            "projection_sha256": self.projection_sha256,
            "source_file_count": len(self.source_files),
            "equation_count": len(self.equations),
            "context_count": len(self.contexts),
            "identity_anchor_distinct": self.identity_anchor_id != self.stabilizer_polytope_id,
            "runtime_executed": False,
            "godot_started": False,
            "physical_measurement_executed": False,
            "cpython_semantics_changed": False,
            "final_kapsyla": False,
            "errors": list(self.validate()),
        }


def _encode(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_encode(item) for item in value]
    return value


def _equation(equation_id: str, left: tuple[str, ...], right: str, sign: int = 1) -> QuaternionEquation:
    return QuaternionEquation(equation_id, left, right, sign)


def build_reference_runtime_projection() -> JaranianQuaternionColexRuntimeProjection:
    files = (
        GodotSourceFile("godot/sigil4godot/jaranian/JaranianQuaternionColex.gd", "QUATERNION_MESH_AND_CONTEXT_RUNTIME"),
        GodotSourceFile("godot/sigil4godot/jaranian/JaranianBasisRenderer.gd", "IMMEDIATE_MESH_BASIS_OVERLAY"),
        GodotSourceFile("godot/sigil4godot/jaranian/JaranianQuaternionColex.tscn", "SCENE_BINDING"),
    )
    equations = (
        _equation("X2_NEG_ONE", ("X", "X"), "ONE", -1),
        _equation("Y2_NEG_ONE", ("Y", "Y"), "ONE", -1),
        _equation("Z2_NEG_ONE", ("Z", "Z"), "ONE", -1),
        _equation("XY_Z", ("X", "Y"), "Z"),
        _equation("YZ_X", ("Y", "Z"), "X"),
        _equation("ZX_Y", ("Z", "X"), "Y"),
        _equation("YX_NEG_Z", ("Y", "X"), "Z", -1),
        _equation("ZY_NEG_X", ("Z", "Y"), "X", -1),
        _equation("XZ_NEG_Y", ("X", "Z"), "Y", -1),
        _equation("XYZ_NEG_ONE", ("X", "Y", "Z"), "ONE", -1),
        _equation("ONE_X_X", ("ONE", "X"), "X"),
    )
    contexts = (
        ContextRule("GLOBAL", "ctx.qubit.GLOBAL", True, True, True, ()),
        ContextRule("X", "ctx.qubit.X", True, True, True, ("Y", "Z")),
        ContextRule("Y", "ctx.qubit.Y", True, True, True, ("X", "Z")),
        ContextRule("Z", "ctx.qubit.Z", True, True, True, ("X", "Y")),
    )
    return JaranianQuaternionColexRuntimeProjection(
        source_files=files,
        equations=equations,
        contexts=contexts,
    )


def compile_reference_runtime_projection_json() -> str:
    projection = build_reference_runtime_projection()
    if projection.validate():
        raise ValueError("invalid_runtime_projection:" + ",".join(projection.validate()))
    return json.dumps(projection.receipt(), indent=2, sort_keys=True)


__all__ = [
    "SCHEMA_ID", "CANON", "SIGILBOOK_PULL_REQUEST", "SIGILBOOK_RUNTIME_HEAD",
    "RuntimeProjectionState", "GodotSourceFile", "QuaternionEquation", "ContextRule",
    "JaranianQuaternionColexRuntimeProjection", "build_reference_runtime_projection",
    "compile_reference_runtime_projection_json", "replace",
]
