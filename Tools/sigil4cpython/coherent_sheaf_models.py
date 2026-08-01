"""Strict Pydantika models for the SIGIL coherent-sheaf kernel upgrade."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


SCHEMA_ID = "SIGIL4CPYTHON_PYDANTIKA_COHERENT_SHEAF_KERNELS_V1"
TOTAL_CONTEXT = "TOTAL_JARANIAN_WEAVE_CATEGORY"
KERNEL_SURFACES = {
    "SIGILBOOK",
    "SIGIL4PY",
    "SIGIL4GODOT",
    "SIGIL4CPYTHON",
    "PACA_ESTACA",
    "SYNTHGOTHHUB",
    "PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK",
}


def _json_array_to_tuple(value: object) -> object:
    if isinstance(value, list):
        return tuple(value)
    return value


StringTuple = Annotated[tuple[str, ...], BeforeValidator(_json_array_to_tuple)]


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        allow_inf_nan=False,
    )


class PydantikaAnnotationModel(StrictModel):
    annotation_id: str = Field(min_length=1, max_length=192)
    kernel_id: str = Field(min_length=1, max_length=192)
    python_type: str = Field(min_length=1, max_length=192)
    semantic_type: str = Field(min_length=1, max_length=192)
    context_id: str = Field(min_length=1, max_length=192)
    optional: bool = False
    source_bound: Literal[True] = True


class KernelAgentModel(StrictModel):
    agent_id: str = Field(min_length=1, max_length=192)
    kernel_id: str = Field(min_length=1, max_length=192)
    space: Literal[
        "VIRTUAL_USER_SPACE",
        "VIRTUAL_KRONE_SPACE",
        "VIRTUAL_CRONE_SPACE",
    ]
    permission: Literal[
        "USER_LEFT",
        "KRONE_RIGHT",
        "CRONE_RIGHT",
        "BRIDGE_GUARD",
    ]
    may_cross_space: Literal[False] = False
    may_attach_resource: bool = False

    @model_validator(mode="after")
    def validate_chirality(self) -> "KernelAgentModel":
        if self.space == "VIRTUAL_USER_SPACE" and self.permission not in {
            "USER_LEFT",
            "BRIDGE_GUARD",
        }:
            raise ValueError("user_agent_permission_not_left")
        if self.space in {
            "VIRTUAL_KRONE_SPACE",
            "VIRTUAL_CRONE_SPACE",
        } and self.permission not in {
            "KRONE_RIGHT",
            "CRONE_RIGHT",
            "BRIDGE_GUARD",
        }:
            raise ValueError("krone_agent_permission_not_right")
        if self.space == "VIRTUAL_USER_SPACE" and self.may_attach_resource:
            raise ValueError("user_agent_resource_attachment_forbidden")
        return self


class IrreducibleResourceModel(StrictModel):
    resource_id: str = Field(min_length=1, max_length=192)
    kernel_id: str = Field(min_length=1, max_length=192)
    resource_type: str = Field(min_length=1, max_length=192)
    owning_space: Literal["VIRTUAL_KRONE_SPACE", "VIRTUAL_CRONE_SPACE"]
    release_scale: Literal["MICROCANONICAL", "MACROCANONICAL"]
    context_id: str = Field(min_length=1, max_length=192)
    direct_user_access: Literal[False] = False


AnnotationTuple = Annotated[
    tuple[PydantikaAnnotationModel, ...], BeforeValidator(_json_array_to_tuple)
]
AgentTuple = Annotated[
    tuple[KernelAgentModel, ...], BeforeValidator(_json_array_to_tuple)
]
ResourceTuple = Annotated[
    tuple[IrreducibleResourceModel, ...], BeforeValidator(_json_array_to_tuple)
]


class CoherentSheafKernelModel(StrictModel):
    kernel_id: str = Field(min_length=1, max_length=192)
    surface: Literal[
        "SIGILBOOK",
        "SIGIL4PY",
        "SIGIL4GODOT",
        "SIGIL4CPYTHON",
        "PACA_ESTACA",
        "SYNTHGOTHHUB",
        "PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK",
    ]
    context_id: str = Field(min_length=1, max_length=192)
    annotations: AnnotationTuple = Field(min_length=1, max_length=128)
    agents: AgentTuple = Field(min_length=1, max_length=64)
    resources: ResourceTuple = Field(min_length=1, max_length=64)
    local_sections: StringTuple = Field(min_length=1, max_length=128)
    release_scale: Literal["MICROCANONICAL"] = "MICROCANONICAL"

    @model_validator(mode="after")
    def validate_kernel(self) -> "CoherentSheafKernelModel":
        if any(item.kernel_id != self.kernel_id for item in self.annotations):
            raise ValueError("annotation_kernel_mismatch")
        if any(item.kernel_id != self.kernel_id for item in self.agents):
            raise ValueError("agent_kernel_mismatch")
        if any(item.kernel_id != self.kernel_id for item in self.resources):
            raise ValueError("resource_kernel_mismatch")
        spaces = {agent.space for agent in self.agents}
        if "VIRTUAL_USER_SPACE" not in spaces:
            raise ValueError("kernel_user_space_agent_missing")
        if not spaces & {"VIRTUAL_KRONE_SPACE", "VIRTUAL_CRONE_SPACE"}:
            raise ValueError("kernel_krone_space_agent_missing")
        return self


class SheafGluingModel(StrictModel):
    gluing_id: str = Field(min_length=1, max_length=192)
    source_kernel_id: str = Field(min_length=1, max_length=192)
    target_kernel_id: str = Field(min_length=1, max_length=192)
    context_id: str = Field(min_length=1, max_length=192)
    shared_annotation_ids: StringTuple = Field(min_length=1, max_length=128)
    preserves_user_krone_factorization: Literal[True] = True
    preserves_release_scale_boundary: Literal[True] = True

    @model_validator(mode="after")
    def distinct_kernels(self) -> "SheafGluingModel":
        if self.source_kernel_id == self.target_kernel_id:
            raise ValueError("sheaf_gluing_identity_collapse")
        return self


class OuroborosFlowModel(StrictModel):
    flow_id: str = Field(min_length=1, max_length=192)
    kernel_ids: StringTuple = Field(min_length=1, max_length=128)
    phases: StringTuple = Field(min_length=1, max_length=32)
    error_budget: int = Field(ge=0, le=1_000_000)
    recurrent: Literal[True] = True
    compositional_contextual_lwe: Literal[True] = True
    preserves_void_boundary: Literal[True] = True

    @model_validator(mode="after")
    def validate_phases(self) -> "OuroborosFlowModel":
        required = {
            "VOID_TYPED_SOURCE",
            "LEARN_WITH_ERRORS",
            "VOID_TYPED_RETURN",
        }
        if not required.issubset(set(self.phases)):
            raise ValueError("ouroboros_flow_phase_incomplete")
        return self


class ReleasePolicyModel(StrictModel):
    policy_id: str = Field(min_length=1, max_length=192)
    release_scale: Literal["MICROCANONICAL", "MACROCANONICAL"]
    applies_to_kernel_ids: StringTuple = Field(min_length=1, max_length=128)
    context_id: str = Field(min_length=1, max_length=192)
    strikk_type: str = Field(min_length=1, max_length=192)
    global_policy: bool

    @model_validator(mode="after")
    def validate_scale(self) -> "ReleasePolicyModel":
        if self.release_scale == "MACROCANONICAL" and not (
            self.global_policy and self.context_id == TOTAL_CONTEXT
        ):
            raise ValueError("macrocanonical_policy_not_global")
        if self.release_scale == "MICROCANONICAL" and self.global_policy:
            raise ValueError("microcanonical_policy_marked_global")
        return self


KernelTuple = Annotated[
    tuple[CoherentSheafKernelModel, ...], BeforeValidator(_json_array_to_tuple)
]
GluingTuple = Annotated[
    tuple[SheafGluingModel, ...], BeforeValidator(_json_array_to_tuple)
]
FlowTuple = Annotated[
    tuple[OuroborosFlowModel, ...], BeforeValidator(_json_array_to_tuple)
]
PolicyTuple = Annotated[
    tuple[ReleasePolicyModel, ...], BeforeValidator(_json_array_to_tuple)
]


class PydantikaCoherentSheafModel(StrictModel):
    sheaf_id: str = Field(min_length=1, max_length=192)
    kernels: KernelTuple = Field(min_length=1, max_length=64)
    gluings: GluingTuple = Field(default=(), max_length=256)
    ouroboros_flows: FlowTuple = Field(min_length=1, max_length=64)
    release_policies: PolicyTuple = Field(min_length=1, max_length=64)
    context_id: Literal[TOTAL_CONTEXT] = TOTAL_CONTEXT
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    source_bound: Literal[True] = True
    runtime_executed: Literal[False] = False
    resource_access_performed: Literal[False] = False
    pydantika_is_tooling_not_stdlib_dependency: Literal[True] = True
    human_review_required: Literal[True] = True

    @model_validator(mode="after")
    def validate_sheaf(self) -> "PydantikaCoherentSheafModel":
        kernel_ids = tuple(kernel.kernel_id for kernel in self.kernels)
        if len(kernel_ids) != len(set(kernel_ids)):
            raise ValueError("duplicate_coherent_kernel_id")
        surfaces = {kernel.surface for kernel in self.kernels}
        if surfaces != KERNEL_SURFACES:
            raise ValueError("coherent_sheaf_required_surface_missing")

        known_kernel_ids = set(kernel_ids)
        annotation_ids = {
            annotation.annotation_id
            for kernel in self.kernels
            for annotation in kernel.annotations
        }
        for gluing in self.gluings:
            if {
                gluing.source_kernel_id,
                gluing.target_kernel_id,
            } - known_kernel_ids:
                raise ValueError("sheaf_gluing_unknown_kernel")
            if set(gluing.shared_annotation_ids) - annotation_ids:
                raise ValueError("sheaf_gluing_unknown_annotation")
        for flow in self.ouroboros_flows:
            if set(flow.kernel_ids) - known_kernel_ids:
                raise ValueError("ouroboros_flow_unknown_kernel")
        for policy in self.release_policies:
            if set(policy.applies_to_kernel_ids) - known_kernel_ids:
                raise ValueError("release_policy_unknown_kernel")
        if not any(
            policy.release_scale == "MACROCANONICAL"
            for policy in self.release_policies
        ):
            raise ValueError("macrocanonical_policy_missing")
        return self

    def canonical_digest(self) -> str:
        encoded = json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


class PydantikaCoherentSheafCertificate(StrictModel):
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    model_name: Literal["PydantikaCoherentSheafModel"] = (
        "PydantikaCoherentSheafModel"
    )
    payload_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    serialization_round_trip_verified: Literal[True] = True
    runtime_executed: Literal[False] = False
    resource_access_performed: Literal[False] = False
    human_review_required: Literal[True] = True


def compile_pydantika_coherent_sheaf_model(
    payload: dict[str, object],
) -> PydantikaCoherentSheafCertificate:
    model = PydantikaCoherentSheafModel.model_validate(payload)
    encoded = model.model_dump_json()
    reconstructed = PydantikaCoherentSheafModel.model_validate_json(encoded)
    if reconstructed.model_dump(mode="json") != model.model_dump(mode="json"):
        raise ValueError("pydantika_coherent_sheaf_round_trip_failed")
    return PydantikaCoherentSheafCertificate(
        payload_digest=model.canonical_digest()
    )


__all__ = [
    "PydantikaCoherentSheafCertificate",
    "PydantikaCoherentSheafModel",
    "SCHEMA_ID",
    "TOTAL_CONTEXT",
    "compile_pydantika_coherent_sheaf_model",
]
