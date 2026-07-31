"""Strict Pydantika models for HPC-localized SIGIL FPGA kernels."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


SCHEMA_ID = "SIGIL4CPYTHON_HPC_LOCALIZED_QUAZRIS_FPGA_KERNELS_V1"
SIGILITAS_CONTEXT = "SIGILITAS_SEMANTIC_OPERATING_SYSTEM"
VOID_VORTEX_CONTEXT = "SIGIL_VOID_VORTEX_ALHAMBRA"
COHERENT_SHEAF_SCHEMA_ID = "SIGIL4CPYTHON_PYDANTIKA_COHERENT_SHEAF_KERNELS_V1"
VIRTUAL_IO_SCHEMA_ID = "SIGIL4CPYTHON_VIRTUAL_REST_IO_KERNELS_V1"

REQUIRED_DSL_FORMS = {
    "QUAZRIS_DATAFLOW_DSL",
    "DISCOPY_TYPED_CATEGORICAL_DSL",
    "TWISTED_K_TYPED_CONTEXTUAL_DSL",
}
REQUIRED_FPGA_RESOURCES = {
    "PROCESSING_ELEMENT",
    "FIFO_STREAM",
    "HBM_MEMORY",
    "NETWORK_ON_CHIP",
    "DSP_TILE",
}
REQUIRED_MORPHISMS = {
    "PROCESSING_ELEMENT",
    "STREAM_CHANNEL",
    "MEMORY_MOVER",
    "NOC_ROUTE",
    "SHEAF_FLOW",
    "VOID_OUROBOROS",
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


class QuazrisTypeModel(StrictModel):
    type_id: str = Field(min_length=1, max_length=192)
    carrier: str = Field(min_length=1, max_length=192)
    semantic_type: str = Field(min_length=1, max_length=192)
    twisted_k_type: str = Field(min_length=1, max_length=192)
    discopy_object: str = Field(min_length=1, max_length=192)
    cellular_dimension: int = Field(ge=0, le=32)
    context_id: Literal[SIGILITAS_CONTEXT, VOID_VORTEX_CONTEXT] = (
        SIGILITAS_CONTEXT
    )


class QuazrisMorphismModel(StrictModel):
    morphism_id: str = Field(min_length=1, max_length=192)
    kind: Literal[
        "PROCESSING_ELEMENT",
        "STREAM_CHANNEL",
        "MEMORY_MOVER",
        "NOC_ROUTE",
        "HLS_LOWERING",
        "SHEAF_FLOW",
        "VOID_OUROBOROS",
    ]
    source_type_ids: StringTuple = Field(min_length=1, max_length=64)
    target_type_ids: StringTuple = Field(min_length=1, max_length=64)
    categorical_law: str = Field(min_length=1, max_length=256)
    strikk_witness: str = Field(min_length=1, max_length=192)
    data_activated: Literal[True] = True
    no_global_program_counter: Literal[True] = True
    preserves_discopy_typing: Literal[True] = True
    preserves_twisted_k_type: Literal[True] = True


class DataflowChannelModel(StrictModel):
    channel_id: str = Field(min_length=1, max_length=192)
    channel_kind: Literal["FIFO", "AXI_STREAM", "HBM_STREAM", "NOC_STREAM"]
    source_morphism_id: str = Field(min_length=1, max_length=192)
    target_morphism_id: str = Field(min_length=1, max_length=192)
    type_id: str = Field(min_length=1, max_length=192)
    backpressure_policy: str = Field(min_length=1, max_length=192)
    depth_policy: str = Field(min_length=1, max_length=192)
    preserves_order: Literal[True] = True
    deadlock_checked: Literal[True] = True
    overflow_checked: Literal[True] = True


class FPGAResourceProfileModel(StrictModel):
    resource_id: str = Field(min_length=1, max_length=192)
    kind: Literal[
        "PROCESSING_ELEMENT",
        "FIFO_STREAM",
        "HBM_MEMORY",
        "NETWORK_ON_CHIP",
        "DSP_TILE",
        "PCIE_ENDPOINT",
        "NETWORK_ENDPOINT",
        "HLS_TOOLCHAIN",
        "SCHEDULER_QUEUE",
    ]
    target_id: str = Field(min_length=1, max_length=192)
    descriptor: str = Field(min_length=1, max_length=256)
    owning_space: Literal["VIRTUAL_KRONE_SPACE", "VIRTUAL_CRONE_SPACE"] = (
        "VIRTUAL_KRONE_SPACE"
    )
    virtualized: Literal[True] = True
    direct_user_access: Literal[False] = False


ResourceTuple = Annotated[
    tuple[FPGAResourceProfileModel, ...],
    BeforeValidator(_json_array_to_tuple),
]


class FPGATargetProfileModel(StrictModel):
    target_id: str = Field(min_length=1, max_length=192)
    family: Literal[
        "VERSAL_INSPIRED",
        "AMD_ALVEO_V80_INSPIRED",
        "SIMULATED_FPGA",
    ]
    architecture_tags: StringTuple = Field(min_length=1, max_length=64)
    resources: ResourceTuple = Field(min_length=1, max_length=128)
    scheduler_interface: str = Field(min_length=1, max_length=192)
    hls_flow: str = Field(min_length=1, max_length=192)
    virtualized: Literal[True] = True
    physical_instantiation_attached: Literal[False] = False

    @model_validator(mode="after")
    def validate_target(self) -> "FPGATargetProfileModel":
        resource_ids = tuple(resource.resource_id for resource in self.resources)
        if len(resource_ids) != len(set(resource_ids)):
            raise ValueError("duplicate_fpga_resource")
        if any(resource.target_id != self.target_id for resource in self.resources):
            raise ValueError("fpga_resource_target_mismatch")
        kinds = {resource.kind for resource in self.resources}
        if not REQUIRED_FPGA_RESOURCES.issubset(kinds):
            raise ValueError("fpga_target_required_resource_missing")
        return self


class CellularFlowMoveModel(StrictModel):
    move_id: str = Field(min_length=1, max_length=192)
    kind: Literal[
        "TWISTED_K_REWRITE",
        "DATAFLOW_FUSION",
        "BACKPRESSURE_INSERT",
        "RESOURCE_LOCALIZATION",
        "VOID_RECURSION",
    ]
    source_morphism_id: str = Field(min_length=1, max_length=192)
    target_morphism_id: str = Field(min_length=1, max_length=192)
    cellular_dimension: int = Field(ge=0, le=32)
    strikk_witness: str = Field(min_length=1, max_length=192)
    preserves_dataflow_activation: Literal[True] = True
    preserves_backpressure: Literal[True] = True
    preserves_chiral_boundary: Literal[True] = True
    preserves_twisted_k_type: Literal[True] = True


class SigilAPIInterfaceModel(StrictModel):
    api_id: str = Field(min_length=1, max_length=192)
    protocols: StringTuple = Field(min_length=1, max_length=64)
    virtual_io_schema_id: Literal[VIRTUAL_IO_SCHEMA_ID] = VIRTUAL_IO_SCHEMA_ID
    coherent_sheaf_schema_id: Literal[COHERENT_SHEAF_SCHEMA_ID] = (
        COHERENT_SHEAF_SCHEMA_ID
    )
    sigilitas_context: Literal[SIGILITAS_CONTEXT] = SIGILITAS_CONTEXT
    direct_hardware_calls: Literal[False] = False
    scheduler_submission_requires_krone: Literal[True] = True
    physical_resource_handles_exposed: Literal[False] = False


TypeTuple = Annotated[
    tuple[QuazrisTypeModel, ...],
    BeforeValidator(_json_array_to_tuple),
]
MorphismTuple = Annotated[
    tuple[QuazrisMorphismModel, ...],
    BeforeValidator(_json_array_to_tuple),
]
ChannelTuple = Annotated[
    tuple[DataflowChannelModel, ...],
    BeforeValidator(_json_array_to_tuple),
]
MoveTuple = Annotated[
    tuple[CellularFlowMoveModel, ...],
    BeforeValidator(_json_array_to_tuple),
]


class HPCLocalizedKernelModel(StrictModel):
    kernel_id: str = Field(min_length=1, max_length=192)
    dsl_forms: StringTuple = Field(min_length=1, max_length=16)
    target: FPGATargetProfileModel
    quazris_types: TypeTuple = Field(min_length=1, max_length=256)
    morphisms: MorphismTuple = Field(min_length=1, max_length=512)
    channels: ChannelTuple = Field(min_length=1, max_length=512)
    cellular_moves: MoveTuple = Field(default=(), max_length=512)
    sigil_api: SigilAPIInterfaceModel
    plural_sheaf_sections: StringTuple = Field(min_length=1, max_length=64)
    pydantika_annotation_flow_ids: StringTuple = Field(min_length=1, max_length=64)
    kokompile_plan_id: str = Field(min_length=1, max_length=192)
    authorial_context: Literal["JJBV_AUTHORED_SIGIL_ALGORITHMS"] = (
        "JJBV_AUTHORED_SIGIL_ALGORITHMS"
    )
    void_vortex_context: Literal[VOID_VORTEX_CONTEXT] = VOID_VORTEX_CONTEXT
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    source_bound: Literal[True] = True
    fully_factorizable: Literal[True] = True
    conformal_architecture: Literal[True] = True
    pydantika_annotations_required: Literal[True] = True
    runtime_executed: Literal[False] = False
    hardware_synthesis_performed: Literal[False] = False
    scheduler_job_submitted: Literal[False] = False
    pydantika_is_tooling_not_stdlib_dependency: Literal[True] = True
    virtual_plan_is_not_hardware_authority: Literal[True] = True
    human_review_required: Literal[True] = True

    @model_validator(mode="after")
    def validate_kernel(self) -> "HPCLocalizedKernelModel":
        if not REQUIRED_DSL_FORMS.issubset(set(self.dsl_forms)):
            raise ValueError("hpc_localized_kernel_dsl_forms_incomplete")
        type_ids = tuple(item.type_id for item in self.quazris_types)
        if len(type_ids) != len(set(type_ids)):
            raise ValueError("duplicate_quazris_type")
        known_type_ids = set(type_ids)
        morphism_ids = tuple(item.morphism_id for item in self.morphisms)
        if len(morphism_ids) != len(set(morphism_ids)):
            raise ValueError("duplicate_quazris_morphism")
        known_morphism_ids = set(morphism_ids)
        for morphism in self.morphisms:
            if set(morphism.source_type_ids) - known_type_ids:
                raise ValueError("quazris_morphism_unknown_source")
            if set(morphism.target_type_ids) - known_type_ids:
                raise ValueError("quazris_morphism_unknown_target")
        channel_ids = tuple(channel.channel_id for channel in self.channels)
        if len(channel_ids) != len(set(channel_ids)):
            raise ValueError("duplicate_dataflow_channel")
        for channel in self.channels:
            if channel.source_morphism_id not in known_morphism_ids:
                raise ValueError("dataflow_channel_unknown_source")
            if channel.target_morphism_id not in known_morphism_ids:
                raise ValueError("dataflow_channel_unknown_target")
            if channel.type_id not in known_type_ids:
                raise ValueError("dataflow_channel_unknown_type")
        for move in self.cellular_moves:
            if move.source_morphism_id not in known_morphism_ids:
                raise ValueError("cellular_flow_move_unknown_source")
            if move.target_morphism_id not in known_morphism_ids:
                raise ValueError("cellular_flow_move_unknown_target")
        kinds = {morphism.kind for morphism in self.morphisms}
        if not REQUIRED_MORPHISMS.issubset(kinds):
            raise ValueError("hpc_localized_kernel_morphism_missing")
        return self

    def canonical_digest(self) -> str:
        encoded = json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


class PydantikaHPCLocalizedKernelCertificate(StrictModel):
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    model_name: Literal["HPCLocalizedKernelModel"] = "HPCLocalizedKernelModel"
    payload_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    serialization_round_trip_verified: Literal[True] = True
    runtime_executed: Literal[False] = False
    hardware_synthesis_performed: Literal[False] = False
    scheduler_job_submitted: Literal[False] = False
    human_review_required: Literal[True] = True


def compile_pydantika_hpc_localized_kernel(
    payload: dict[str, object],
) -> PydantikaHPCLocalizedKernelCertificate:
    model = HPCLocalizedKernelModel.model_validate(payload)
    encoded = model.model_dump_json()
    reconstructed = HPCLocalizedKernelModel.model_validate_json(encoded)
    if reconstructed.model_dump(mode="json") != model.model_dump(mode="json"):
        raise ValueError("hpc_localized_kernel_round_trip_failed")
    return PydantikaHPCLocalizedKernelCertificate(
        payload_digest=model.canonical_digest()
    )


__all__ = [
    "HPCLocalizedKernelModel",
    "PydantikaHPCLocalizedKernelCertificate",
    "SCHEMA_ID",
    "compile_pydantika_hpc_localized_kernel",
]
