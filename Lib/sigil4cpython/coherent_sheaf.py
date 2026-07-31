"""Pydantika coherent-sheaf contracts for SIGIL kernel families.

This module models a reviewable metadata sheaf spanning SIGILBook, SIGIL4Py,
SIGIL4Godot, SIGIL4CPython, PACA Estaca, SynthGothHub, and the
plural-universal-abstrakta-aesthetik surface.  It is dependency-free and does
not execute kernels, call services, or grant resource authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping


SCHEMA_ID = "SIGIL4CPYTHON_PYDANTIKA_COHERENT_SHEAF_KERNELS_V1"
TOTAL_CONTEXT = "TOTAL_JARANIAN_WEAVE_CATEGORY"


class CoherentSheafState(str, Enum):
    ADMIT = "ADMIT"
    HOLD_WITH_OBSTRUCTION = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT"


class KernelSurface(str, Enum):
    SIGILBOOK = "SIGILBOOK"
    SIGIL4PY = "SIGIL4PY"
    SIGIL4GODOT = "SIGIL4GODOT"
    SIGIL4CPYTHON = "SIGIL4CPYTHON"
    PACA_ESTACA = "PACA_ESTACA"
    SYNTHGOTHHUB = "SYNTHGOTHHUB"
    PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK = (
        "PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK"
    )


class AgentSpace(str, Enum):
    VIRTUAL_USER_SPACE = "VIRTUAL_USER_SPACE"
    VIRTUAL_KRONE_SPACE = "VIRTUAL_KRONE_SPACE"
    VIRTUAL_CRONE_SPACE = "VIRTUAL_CRONE_SPACE"


class ChiralPermission(str, Enum):
    USER_LEFT = "USER_LEFT"
    KRONE_RIGHT = "KRONE_RIGHT"
    CRONE_RIGHT = "CRONE_RIGHT"
    BRIDGE_GUARD = "BRIDGE_GUARD"


class ReleaseScale(str, Enum):
    MICROCANONICAL = "MICROCANONICAL"
    MACROCANONICAL = "MACROCANONICAL"


class OuroborosPhase(str, Enum):
    VOID_TYPED_SOURCE = "VOID_TYPED_SOURCE"
    ANNOTATE = "ANNOTATE"
    FORGET = "FORGET"
    TRACE = "TRACE"
    RECUR = "RECUR"
    LEARN_WITH_ERRORS = "LEARN_WITH_ERRORS"
    VOID_TYPED_RETURN = "VOID_TYPED_RETURN"


@dataclass(frozen=True, slots=True)
class PydantikaAnnotation:
    annotation_id: str
    kernel_id: str
    python_type: str
    semantic_type: str
    context_id: str
    optional: bool = False
    source_bound: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.annotation_id:
            errors.append("pydantika_annotation_id_missing")
        if not self.kernel_id:
            errors.append(f"pydantika_annotation_kernel_missing:{self.annotation_id}")
        if not self.python_type or not self.semantic_type:
            errors.append(f"pydantika_annotation_type_missing:{self.annotation_id}")
        if not self.context_id:
            errors.append(f"pydantika_annotation_context_missing:{self.annotation_id}")
        if not self.source_bound:
            errors.append(f"pydantika_annotation_not_source_bound:{self.annotation_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class KernelAgent:
    agent_id: str
    kernel_id: str
    space: AgentSpace
    permission: ChiralPermission
    may_cross_space: bool = False
    may_attach_resource: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.agent_id:
            errors.append("kernel_agent_id_missing")
        if not self.kernel_id:
            errors.append(f"kernel_agent_kernel_missing:{self.agent_id}")
        if self.space == AgentSpace.VIRTUAL_USER_SPACE and self.permission not in {
            ChiralPermission.USER_LEFT,
            ChiralPermission.BRIDGE_GUARD,
        }:
            errors.append(f"user_agent_permission_not_left:{self.agent_id}")
        if self.space in {
            AgentSpace.VIRTUAL_KRONE_SPACE,
            AgentSpace.VIRTUAL_CRONE_SPACE,
        } and self.permission not in {
            ChiralPermission.KRONE_RIGHT,
            ChiralPermission.CRONE_RIGHT,
            ChiralPermission.BRIDGE_GUARD,
        }:
            errors.append(f"krone_agent_permission_not_right:{self.agent_id}")
        if self.may_cross_space:
            errors.append(f"agent_space_crossing_forbidden:{self.agent_id}")
        if self.space == AgentSpace.VIRTUAL_USER_SPACE and self.may_attach_resource:
            errors.append(f"user_agent_resource_attachment_forbidden:{self.agent_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class IrreducibleResource:
    resource_id: str
    kernel_id: str
    resource_type: str
    owning_space: AgentSpace
    release_scale: ReleaseScale
    context_id: str
    direct_user_access: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.resource_id:
            errors.append("irreducible_resource_id_missing")
        if not self.kernel_id:
            errors.append(f"irreducible_resource_kernel_missing:{self.resource_id}")
        if not self.resource_type:
            errors.append(f"irreducible_resource_type_missing:{self.resource_id}")
        if not self.context_id:
            errors.append(f"irreducible_resource_context_missing:{self.resource_id}")
        if self.owning_space == AgentSpace.VIRTUAL_USER_SPACE:
            errors.append(f"resource_owned_by_user_space:{self.resource_id}")
        if self.direct_user_access:
            errors.append(f"direct_user_resource_access_forbidden:{self.resource_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class ReleasePolicy:
    policy_id: str
    release_scale: ReleaseScale
    applies_to_kernel_ids: tuple[str, ...]
    context_id: str
    strikk_type: str
    global_policy: bool

    def validate(self, known_kernel_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.policy_id:
            errors.append("release_policy_id_missing")
        if not self.applies_to_kernel_ids:
            errors.append(f"release_policy_empty_scope:{self.policy_id}")
        if not set(self.applies_to_kernel_ids).issubset(known_kernel_ids):
            errors.append(f"release_policy_unknown_kernel:{self.policy_id}")
        if not self.context_id or not self.strikk_type:
            errors.append(f"release_policy_type_boundary_missing:{self.policy_id}")
        if self.release_scale == ReleaseScale.MACROCANONICAL and not (
            self.global_policy and self.context_id == TOTAL_CONTEXT
        ):
            errors.append(f"macrocanonical_policy_not_global:{self.policy_id}")
        if self.release_scale == ReleaseScale.MICROCANONICAL and self.global_policy:
            errors.append(f"microcanonical_policy_marked_global:{self.policy_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class CoherentSheafKernel:
    kernel_id: str
    surface: KernelSurface
    context_id: str
    annotations: tuple[PydantikaAnnotation, ...]
    agents: tuple[KernelAgent, ...]
    resources: tuple[IrreducibleResource, ...]
    local_sections: tuple[str, ...]
    release_scale: ReleaseScale = ReleaseScale.MICROCANONICAL

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.kernel_id:
            errors.append("coherent_kernel_id_missing")
        if not self.context_id:
            errors.append(f"coherent_kernel_context_missing:{self.kernel_id}")
        if self.release_scale != ReleaseScale.MICROCANONICAL:
            errors.append(f"coherent_kernel_not_microcanonical:{self.kernel_id}")
        if not self.annotations:
            errors.append(f"coherent_kernel_annotations_missing:{self.kernel_id}")
        if not self.agents:
            errors.append(f"coherent_kernel_agents_missing:{self.kernel_id}")
        if not self.resources:
            errors.append(f"coherent_kernel_resources_missing:{self.kernel_id}")
        if not self.local_sections:
            errors.append(f"coherent_kernel_sections_missing:{self.kernel_id}")

        for item in self.annotations:
            errors.extend(item.validate())
            if item.kernel_id != self.kernel_id:
                errors.append(f"annotation_kernel_mismatch:{item.annotation_id}")
        for agent in self.agents:
            errors.extend(agent.validate())
            if agent.kernel_id != self.kernel_id:
                errors.append(f"agent_kernel_mismatch:{agent.agent_id}")
        for resource in self.resources:
            errors.extend(resource.validate())
            if resource.kernel_id != self.kernel_id:
                errors.append(f"resource_kernel_mismatch:{resource.resource_id}")

        spaces = {agent.space for agent in self.agents}
        if AgentSpace.VIRTUAL_USER_SPACE not in spaces:
            errors.append(f"kernel_user_space_agent_missing:{self.kernel_id}")
        if not spaces & {
            AgentSpace.VIRTUAL_KRONE_SPACE,
            AgentSpace.VIRTUAL_CRONE_SPACE,
        }:
            errors.append(f"kernel_krone_space_agent_missing:{self.kernel_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class SheafGluing:
    gluing_id: str
    source_kernel_id: str
    target_kernel_id: str
    context_id: str
    shared_annotation_ids: tuple[str, ...]
    preserves_user_krone_factorization: bool = True
    preserves_release_scale_boundary: bool = True

    def validate(
        self,
        known_kernel_ids: set[str],
        known_annotation_ids: set[str],
    ) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.gluing_id:
            errors.append("sheaf_gluing_id_missing")
        if self.source_kernel_id == self.target_kernel_id:
            errors.append(f"sheaf_gluing_identity_collapse:{self.gluing_id}")
        if not {self.source_kernel_id, self.target_kernel_id}.issubset(
            known_kernel_ids
        ):
            errors.append(f"sheaf_gluing_unknown_kernel:{self.gluing_id}")
        if not self.shared_annotation_ids:
            errors.append(f"sheaf_gluing_shared_annotation_missing:{self.gluing_id}")
        if not set(self.shared_annotation_ids).issubset(known_annotation_ids):
            errors.append(f"sheaf_gluing_unknown_annotation:{self.gluing_id}")
        if not self.context_id:
            errors.append(f"sheaf_gluing_context_missing:{self.gluing_id}")
        if not self.preserves_user_krone_factorization:
            errors.append(f"sheaf_gluing_space_factorization_drift:{self.gluing_id}")
        if not self.preserves_release_scale_boundary:
            errors.append(f"sheaf_gluing_release_scale_drift:{self.gluing_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class OuroborosFlow:
    flow_id: str
    kernel_ids: tuple[str, ...]
    phases: tuple[OuroborosPhase, ...]
    error_budget: int
    recurrent: bool = True
    compositional_contextual_lwe: bool = True
    preserves_void_boundary: bool = True

    def validate(self, known_kernel_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.flow_id:
            errors.append("ouroboros_flow_id_missing")
        if not self.kernel_ids or not set(self.kernel_ids).issubset(
            known_kernel_ids
        ):
            errors.append(f"ouroboros_flow_unknown_kernel:{self.flow_id}")
        if self.error_budget < 0:
            errors.append(f"ouroboros_flow_negative_error_budget:{self.flow_id}")
        phase_set = set(self.phases)
        required = {
            OuroborosPhase.VOID_TYPED_SOURCE,
            OuroborosPhase.LEARN_WITH_ERRORS,
            OuroborosPhase.VOID_TYPED_RETURN,
        }
        if not required.issubset(phase_set):
            errors.append(f"ouroboros_flow_phase_incomplete:{self.flow_id}")
        if not self.recurrent:
            errors.append(f"ouroboros_flow_not_recurrent:{self.flow_id}")
        if not self.compositional_contextual_lwe:
            errors.append(f"ouroboros_flow_not_contextual_lwe:{self.flow_id}")
        if not self.preserves_void_boundary:
            errors.append(f"ouroboros_flow_void_boundary_drift:{self.flow_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PydantikaCoherentSheaf:
    sheaf_id: str
    kernels: tuple[CoherentSheafKernel, ...]
    gluings: tuple[SheafGluing, ...]
    ouroboros_flows: tuple[OuroborosFlow, ...]
    release_policies: tuple[ReleasePolicy, ...]
    context_id: str = TOTAL_CONTEXT
    schema_id: str = SCHEMA_ID
    source_bound: bool = True
    runtime_executed: bool = False
    resource_access_performed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.sheaf_id:
            errors.append("pydantika_coherent_sheaf_id_missing")
        if self.schema_id != SCHEMA_ID:
            errors.append("pydantika_coherent_sheaf_schema_mismatch")
        if self.context_id != TOTAL_CONTEXT:
            errors.append("pydantika_coherent_sheaf_context_not_total")
        if not self.source_bound:
            errors.append("pydantika_coherent_sheaf_not_source_bound")
        if self.runtime_executed:
            errors.append("pydantika_coherent_sheaf_runtime_execution_forbidden")
        if self.resource_access_performed:
            errors.append("pydantika_coherent_sheaf_resource_access_forbidden")

        kernel_ids = {kernel.kernel_id for kernel in self.kernels}
        if len(kernel_ids) != len(self.kernels):
            errors.append("duplicate_coherent_kernel_id")
        required_surfaces = set(KernelSurface)
        actual_surfaces = {kernel.surface for kernel in self.kernels}
        missing_surfaces = sorted(
            required_surfaces - actual_surfaces,
            key=lambda item: item.value,
        )
        if missing_surfaces:
            labels = ",".join(item.value for item in missing_surfaces)
            errors.append(f"coherent_sheaf_required_surface_missing:{labels}")

        known_annotation_ids: set[str] = set()
        for kernel in self.kernels:
            errors.extend(kernel.validate())
            known_annotation_ids.update(
                annotation.annotation_id for annotation in kernel.annotations
            )

        for gluing in self.gluings:
            errors.extend(gluing.validate(kernel_ids, known_annotation_ids))
        for flow in self.ouroboros_flows:
            errors.extend(flow.validate(kernel_ids))
        for policy in self.release_policies:
            errors.extend(policy.validate(kernel_ids))

        if not any(
            policy.release_scale == ReleaseScale.MACROCANONICAL
            for policy in self.release_policies
        ):
            errors.append("macrocanonical_policy_missing")
        if not all(
            kernel.release_scale == ReleaseScale.MICROCANONICAL
            for kernel in self.kernels
        ):
            errors.append("microcanonical_kernel_boundary_missing")
        return tuple(errors)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["kernels"] = [asdict(kernel) for kernel in self.kernels]
        payload["gluings"] = [asdict(gluing) for gluing in self.gluings]
        payload["ouroboros_flows"] = [
            asdict(flow) for flow in self.ouroboros_flows
        ]
        payload["release_policies"] = [
            asdict(policy) for policy in self.release_policies
        ]
        payload["sheaf_sha256"] = stable_digest(payload)
        return payload


def stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return sha256(encoded).hexdigest()


def _kernel(
    kernel_id: str,
    surface: KernelSurface,
    *,
    semantic_type: str,
) -> CoherentSheafKernel:
    return CoherentSheafKernel(
        kernel_id=kernel_id,
        surface=surface,
        context_id=f"context:{kernel_id}",
        annotations=(
            PydantikaAnnotation(
                f"ann:{kernel_id}:typed-kernel",
                kernel_id,
                "AnnotatedKernel",
                semantic_type,
                f"context:{kernel_id}",
            ),
            PydantikaAnnotation(
                f"ann:{kernel_id}:paca-estaca",
                kernel_id,
                "PacaEstacaSection",
                "PACA_ESTACA_SHARED_SECTION",
                f"context:{kernel_id}",
            ),
        ),
        agents=(
            KernelAgent(
                f"agent:{kernel_id}:user",
                kernel_id,
                AgentSpace.VIRTUAL_USER_SPACE,
                ChiralPermission.USER_LEFT,
            ),
            KernelAgent(
                f"agent:{kernel_id}:krone",
                kernel_id,
                AgentSpace.VIRTUAL_KRONE_SPACE,
                ChiralPermission.KRONE_RIGHT,
                may_attach_resource=True,
            ),
        ),
        resources=(
            IrreducibleResource(
                f"res:{kernel_id}:component",
                kernel_id,
                "PACA_ESTACA_COMPONENT",
                AgentSpace.VIRTUAL_KRONE_SPACE,
                ReleaseScale.MICROCANONICAL,
                f"context:{kernel_id}",
            ),
        ),
        local_sections=(
            f"section:{kernel_id}:annotations",
            f"section:{kernel_id}:resources",
        ),
    )


def build_pydantika_coherent_sheaf() -> PydantikaCoherentSheaf:
    """Build the canonical multi-kernel coherent sheaf candidate."""

    kernels = (
        _kernel("sigilbook", KernelSurface.SIGILBOOK, semantic_type="SIGILBOOK"),
        _kernel("sigil4py", KernelSurface.SIGIL4PY, semantic_type="SIGIL4PY"),
        _kernel(
            "sigil4godot",
            KernelSurface.SIGIL4GODOT,
            semantic_type="SIGIL4GODOT",
        ),
        _kernel(
            "sigil4cpython",
            KernelSurface.SIGIL4CPYTHON,
            semantic_type="SIGIL4CPYTHON",
        ),
        _kernel(
            "paca-estaca",
            KernelSurface.PACA_ESTACA,
            semantic_type="PACA_ESTACA",
        ),
        _kernel(
            "synthgothub",
            KernelSurface.SYNTHGOTHHUB,
            semantic_type="SYNTHGOTHHUB",
        ),
        _kernel(
            "plural-universal-abstrakta-aesthetik",
            KernelSurface.PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK,
            semantic_type="PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK",
        ),
    )
    kernel_ids = tuple(kernel.kernel_id for kernel in kernels)
    gluings = tuple(
        SheafGluing(
            f"glue:{left.kernel_id}:{right.kernel_id}",
            left.kernel_id,
            right.kernel_id,
            TOTAL_CONTEXT,
            (
                f"ann:{left.kernel_id}:paca-estaca",
                f"ann:{right.kernel_id}:paca-estaca",
            ),
        )
        for left, right in zip(kernels, kernels[1:])
    )
    phases = (
        OuroborosPhase.VOID_TYPED_SOURCE,
        OuroborosPhase.ANNOTATE,
        OuroborosPhase.FORGET,
        OuroborosPhase.TRACE,
        OuroborosPhase.RECUR,
        OuroborosPhase.LEARN_WITH_ERRORS,
        OuroborosPhase.VOID_TYPED_RETURN,
    )
    return PydantikaCoherentSheaf(
        "SIGIL4CPYTHON_PYDANTIKA_COHERENT_SHEAF_KERNELS_V1",
        kernels,
        gluings,
        (
            OuroborosFlow(
                "flow:void-typed-ouroboros-contextual-lwe",
                kernel_ids,
                phases,
                error_budget=7,
            ),
        ),
        (
            ReleasePolicy(
                "policy:macrocanonical-total-jaranian-weave",
                ReleaseScale.MACROCANONICAL,
                kernel_ids,
                TOTAL_CONTEXT,
                "STRIKK::TOTAL_JARANIAN_WEAVE_POLICY",
                global_policy=True,
            ),
        ),
    )


def compile_pydantika_coherent_sheaf(
    sheaf: PydantikaCoherentSheaf,
) -> dict[str, object]:
    """Validate a coherent sheaf and return a canonical admission payload."""

    errors = sheaf.validate()
    reject_markers = (
        "runtime_execution_forbidden",
        "resource_access_forbidden",
        "direct_user_resource_access_forbidden",
        "resource_owned_by_user_space",
        "agent_space_crossing_forbidden",
    )
    if any(any(marker in error for marker in reject_markers) for error in errors):
        state = CoherentSheafState.REJECT
    elif errors:
        state = CoherentSheafState.HOLD_WITH_OBSTRUCTION
    else:
        state = CoherentSheafState.ADMIT
    payload = sheaf.to_dict()
    payload["uap_state"] = state.value
    payload["obstruction_ledger"] = list(errors)
    payload["runtime_executed"] = False
    payload["resource_access_performed"] = False
    payload["human_review_required"] = True
    return payload


__all__ = [
    "AgentSpace",
    "ChiralPermission",
    "CoherentSheafKernel",
    "CoherentSheafState",
    "IrreducibleResource",
    "KernelAgent",
    "KernelSurface",
    "OuroborosFlow",
    "OuroborosPhase",
    "PydantikaAnnotation",
    "PydantikaCoherentSheaf",
    "ReleasePolicy",
    "ReleaseScale",
    "SCHEMA_ID",
    "SheafGluing",
    "TOTAL_CONTEXT",
    "build_pydantika_coherent_sheaf",
    "compile_pydantika_coherent_sheaf",
    "stable_digest",
]
