"""Dependency-free SIGIL4CPython projection of the Jaranian Total Colex Atlas."""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
from hashlib import sha256
import json

SCHEMA_ID = "SIGIL4CPYTHON_JARANIAN_TOTAL_COLEX_ATLAS_PROJECTION_V1"
CANON = "PIORNALEGO_ES_CANON"
PARENT_PULL_REQUEST = 7
PARENT_HEAD = "afa45481401555a07c90f6ee670deab653a1b50f"
SIGILBOOK_SOURCE_PULL_REQUEST = 746
SIGILBOOK_SOURCE_HEAD = "5ef828c5df04f77a64c66dd5a4b940588cef3bd2"
SOURCE_AST_SHA256 = "d1aae3a8873097086120b1c3bfa885ae4f4c807720c5bef66af006a1bb8df238"
SOURCE_ALLEGORICAL_KERNEL_SHA256 = "ab611bb85e69352ee5f103edfb90bc39e611e64f13ef94615b174fd14d9167af"
SOURCE_BUNDLE_SHA256 = "06dcf4061d299fe9efc821b15c563aa2ae34160ebc592a668fae446a8e3b20c2"


class ProjectionState(str, Enum):
    ADMIT_DEPENDENCY_FREE_PROJECTION = "ADMIT_DEPENDENCY_FREE_PROJECTION"
    REJECT = "REJECT"


class PanelId(str, Enum):
    BRANE = "panel.brane"
    TOTALIZATION = "panel.totalization"
    HK_FM = "panel.hk_fm"
    DUAL_SOLIDS = "panel.dual_solids"
    SCUTOID = "panel.scutoid"
    QUBIT = "panel.qubit"


class ColexLayer(str, Enum):
    H1_OBJECTS = "H1_OBJECTS"
    H2_FUNCTORS = "H2_FUNCTORS"
    H3_NATURAL_TRANSFORMATIONS = "H3_NATURAL_TRANSFORMATIONS"
    H4_COHERENCE = "H4_COHERENCE"


class ChiralAxis(str, Enum):
    X = "X"
    Y = "Y"
    Z = "Z"


@dataclass(frozen=True, slots=True)
class SourceBinding:
    repository: str = "jbermejovega/sigilbook"
    pull_request: int = SIGILBOOK_SOURCE_PULL_REQUEST
    head_sha: str = SIGILBOOK_SOURCE_HEAD
    payload_sha256: str = SOURCE_BUNDLE_SHA256
    identity_distinct: bool = True
    authority_transferred: bool = False


@dataclass(frozen=True, slots=True)
class PanelProjection:
    panel_id: PanelId
    ordinal: int
    slug: str
    render_role: str
    render_is_projection: bool = True
    canonical_authority: bool = False


@dataclass(frozen=True, slots=True)
class ChiralContextProjection:
    axis: ChiralAxis
    context_id: str
    identity_cell_id: str
    measurable_relation_ids: tuple[str, ...]
    held_relation_ids: tuple[str, ...]
    all_relations_jointly_measurable: bool = False
    physical_measurement_executed: bool = False


@dataclass(frozen=True, slots=True)
class HeldClaimProjection:
    relation_id: str
    reason: str
    promoted: bool = False


@dataclass(frozen=True, slots=True)
class JaranianTotalColexProjection:
    source: SourceBinding
    panels: tuple[PanelProjection, ...]
    layers: tuple[ColexLayer, ...]
    chiral_contexts: tuple[ChiralContextProjection, ...]
    held_claims: tuple[HeldClaimProjection, ...]
    projection_id: str = SCHEMA_ID
    identity_cell_id: str = "cell.identity"
    identity_relation_id: str = "rel.identity"
    ast_sha256: str = SOURCE_AST_SHA256
    allegorical_kernel_sha256: str = SOURCE_ALLEGORICAL_KERNEL_SHA256
    source_bundle_sha256: str = SOURCE_BUNDLE_SHA256
    dependency_free: bool = True
    pydantic_imported: bool = False
    discopy_imported: bool = False
    cpython_semantics_changed: bool = False
    abi_changed: bool = False
    stdlib_semantics_changed: bool = False
    godot_started: bool = False
    runtime_executed: bool = False
    deployment_executed: bool = False
    identity_transport: bool = False
    plural_collapse: bool = False
    trace_preserved: bool = True
    pi_fixed: bool = True
    final_kapsyla: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.source.repository != "jbermejovega/sigilbook":
            errors.append("source_repository_mismatch")
        if self.source.pull_request != SIGILBOOK_SOURCE_PULL_REQUEST:
            errors.append("source_pull_request_mismatch")
        if self.source.head_sha != SIGILBOOK_SOURCE_HEAD:
            errors.append("source_head_drift")
        if self.source.payload_sha256 != SOURCE_BUNDLE_SHA256:
            errors.append("source_bundle_digest_drift")
        if not self.source.identity_distinct or self.source.authority_transferred:
            errors.append("source_identity_or_authority_boundary_broken")
        if self.projection_id != SCHEMA_ID:
            errors.append("projection_schema_id_mismatch")
        if len(self.panels) != 6 or {p.panel_id for p in self.panels} != set(PanelId):
            errors.append("projection_panel_inventory_mismatch")
        if {p.ordinal for p in self.panels} != set(range(1, 7)):
            errors.append("projection_panel_order_mismatch")
        if any(not p.slug or not p.render_is_projection or p.canonical_authority for p in self.panels):
            errors.append("panel_render_boundary_broken")
        if len(self.layers) != 4 or set(self.layers) != set(ColexLayer):
            errors.append("projection_requires_H1_H2_H3_H4")
        if len(self.chiral_contexts) != 3 or {c.axis for c in self.chiral_contexts} != set(ChiralAxis):
            errors.append("projection_chiral_context_inventory_mismatch")
        for context in self.chiral_contexts:
            if context.identity_cell_id != "cell.identity" or "rel.identity" not in context.measurable_relation_ids:
                errors.append(f"context_identity_missing:{context.axis.value}")
            if not context.held_relation_ids or context.all_relations_jointly_measurable:
                errors.append(f"single_context_claims_global_completeness:{context.axis.value}")
            if context.physical_measurement_executed:
                errors.append(f"physical_measurement_execution_forbidden:{context.axis.value}")
        expected_held = {"rel.fm.reverse", "rel.hk.preservation", "rel.scutoid.intercalation"}
        if {h.relation_id for h in self.held_claims} != expected_held:
            errors.append("held_claim_inventory_mismatch")
        if any(not h.reason or h.promoted for h in self.held_claims):
            errors.append("held_claim_silently_promoted")
        if self.identity_cell_id != "cell.identity" or self.identity_relation_id != "rel.identity":
            errors.append("pacacore_identity_mismatch")
        if (self.ast_sha256, self.allegorical_kernel_sha256, self.source_bundle_sha256) != (
            SOURCE_AST_SHA256,
            SOURCE_ALLEGORICAL_KERNEL_SHA256,
            SOURCE_BUNDLE_SHA256,
        ):
            errors.append("source_digest_drift")
        if not self.dependency_free or self.pydantic_imported or self.discopy_imported:
            errors.append("dependency_free_boundary_broken")
        if self.cpython_semantics_changed or self.abi_changed or self.stdlib_semantics_changed:
            errors.append("cpython_semantic_boundary_broken")
        if self.godot_started or self.runtime_executed or self.deployment_executed:
            errors.append("runtime_execution_forbidden")
        if self.identity_transport or self.plural_collapse:
            errors.append("identity_or_plurality_boundary_broken")
        if not self.trace_preserved or not self.pi_fixed or self.final_kapsyla:
            errors.append("replay_or_kapsyla_boundary_broken")
        return tuple(errors)

    @property
    def state(self) -> ProjectionState:
        return ProjectionState.ADMIT_DEPENDENCY_FREE_PROJECTION if not self.validate() else ProjectionState.REJECT

    @property
    def projection_sha256(self) -> str:
        payload = _encode(asdict(self))
        return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def receipt(self) -> dict[str, object]:
        return {
            "schema_id": SCHEMA_ID,
            "canon": CANON,
            "state": self.state.value,
            "projection_sha256": self.projection_sha256,
            "source_head": self.source.head_sha,
            "source_bundle_sha256": self.source_bundle_sha256,
            "panel_count": len(self.panels),
            "layer_count": len(self.layers),
            "chiral_context_count": len(self.chiral_contexts),
            "identity_cell_count": 1,
            "held_claim_ids": sorted(h.relation_id for h in self.held_claims),
            "errors": list(self.validate()),
            "runtime_executed": False,
            "cpython_semantics_changed": False,
            "final_kapsyla": False,
        }


def _encode(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): _encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_encode(v) for v in value]
    return value


def build_reference_projection() -> JaranianTotalColexProjection:
    panels = tuple(
        PanelProjection(panel, index, slug, role)
        for index, (panel, slug, role) in enumerate(
            (
                (PanelId.BRANE, "braided-brane-of-branes-and-sigil-typing", "BRAIDED_BRANE_VIEW"),
                (PanelId.TOTALIZATION, "weak-three-dimensional-graphical-calculus-totalization", "TOTALIZATION_VIEW"),
                (PanelId.HK_FM, "hyperkaehler-and-fourier-mukai-deep-colex", "HK_FM_VIEW"),
                (PanelId.DUAL_SOLIDS, "global-quasi-category-dual-solids-and-momentum", "DUAL_SOLIDS_VIEW"),
                (PanelId.SCUTOID, "scutoid-geometry-and-packing", "SCUTOID_VIEW"),
                (PanelId.QUBIT, "chiral-qubit-polytope-colex-eight-state-model", "CHIRAL_QUBIT_VIEW"),
            ),
            start=1,
        )
    )
    contexts = (
        ChiralContextProjection(ChiralAxis.X, "ctx.qubit.X", "cell.identity", ("rel.identity", "rel.measure.X", "rel.glue.XY", "rel.glue.ZX"), ("rel.measure.Y", "rel.measure.Z", "rel.glue.YZ")),
        ChiralContextProjection(ChiralAxis.Y, "ctx.qubit.Y", "cell.identity", ("rel.identity", "rel.measure.Y", "rel.glue.XY", "rel.glue.YZ"), ("rel.measure.X", "rel.measure.Z", "rel.glue.ZX")),
        ChiralContextProjection(ChiralAxis.Z, "ctx.qubit.Z", "cell.identity", ("rel.identity", "rel.measure.Z", "rel.glue.YZ", "rel.glue.ZX"), ("rel.measure.X", "rel.measure.Y", "rel.glue.XY")),
    )
    held = (
        HeldClaimProjection("rel.fm.reverse", "reverse transform remains an adjoint/equivalence candidate"),
        HeldClaimProjection("rel.hk.preservation", "derived equivalence does not prove Hyperkaehler preservation"),
        HeldClaimProjection("rel.scutoid.intercalation", "render does not prove a physical tissue-energy model"),
    )
    return JaranianTotalColexProjection(
        source=SourceBinding(),
        panels=panels,
        layers=tuple(ColexLayer),
        chiral_contexts=contexts,
        held_claims=held,
    )


def compile_reference_projection_json() -> str:
    projection = build_reference_projection()
    if projection.validate():
        raise ValueError("invalid_reference_projection:" + ",".join(projection.validate()))
    return json.dumps(projection.receipt(), indent=2, sort_keys=True)


__all__ = [
    "SCHEMA_ID", "CANON", "PARENT_PULL_REQUEST", "PARENT_HEAD",
    "SIGILBOOK_SOURCE_PULL_REQUEST", "SIGILBOOK_SOURCE_HEAD",
    "SOURCE_AST_SHA256", "SOURCE_ALLEGORICAL_KERNEL_SHA256", "SOURCE_BUNDLE_SHA256",
    "ProjectionState", "PanelId", "ColexLayer", "ChiralAxis", "SourceBinding",
    "PanelProjection", "ChiralContextProjection", "HeldClaimProjection",
    "JaranianTotalColexProjection", "build_reference_projection",
    "compile_reference_projection_json", "replace",
]
