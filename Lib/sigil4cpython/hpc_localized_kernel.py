"""HPC-localized Quazris/FPGA flow contracts for SIGIL4CPython.

This module models a virtual SIGIL API interface for categorical dataflow
kernels targeting Versal-inspired FPGA families.  It is dependency-free
metadata: it does not synthesize hardware, submit scheduler jobs, call vendor
tools, open devices, or change CPython interpreter semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping


SCHEMA_ID = "SIGIL4CPYTHON_HPC_LOCALIZED_QUAZRIS_FPGA_KERNELS_V1"
SIGILITAS_CONTEXT = "SIGILITAS_SEMANTIC_OPERATING_SYSTEM"
VOID_VORTEX_CONTEXT = "SIGIL_VOID_VORTEX_ALHAMBRA"
COHERENT_SHEAF_SCHEMA_ID = "SIGIL4CPYTHON_PYDANTIKA_COHERENT_SHEAF_KERNELS_V1"
VIRTUAL_IO_SCHEMA_ID = "SIGIL4CPYTHON_VIRTUAL_REST_IO_KERNELS_V1"


class HPCLocalizedState(str, Enum):
    ADMIT = "ADMIT"
    HOLD_WITH_OBSTRUCTION = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT"


class QuazrisDSLForm(str, Enum):
    DATAFLOW = "QUAZRIS_DATAFLOW_DSL"
    DISCOPY_TYPED = "DISCOPY_TYPED_CATEGORICAL_DSL"
    TWISTED_K_TYPED = "TWISTED_K_TYPED_CONTEXTUAL_DSL"


class KernelSpace(str, Enum):
    VIRTUAL_USER_SPACE = "VIRTUAL_USER_SPACE"
    VIRTUAL_KRONE_SPACE = "VIRTUAL_KRONE_SPACE"
    VIRTUAL_CRONE_SPACE = "VIRTUAL_CRONE_SPACE"


class FPGATargetFamily(str, Enum):
    VERSAL_INSPIRED = "VERSAL_INSPIRED"
    AMD_ALVEO_V80_INSPIRED = "AMD_ALVEO_V80_INSPIRED"
    SIMULATED_FPGA = "SIMULATED_FPGA"


class FPGAResourceKind(str, Enum):
    PROCESSING_ELEMENT = "PROCESSING_ELEMENT"
    FIFO_STREAM = "FIFO_STREAM"
    HBM_MEMORY = "HBM_MEMORY"
    NETWORK_ON_CHIP = "NETWORK_ON_CHIP"
    DSP_TILE = "DSP_TILE"
    PCIE_ENDPOINT = "PCIE_ENDPOINT"
    NETWORK_ENDPOINT = "NETWORK_ENDPOINT"
    HLS_TOOLCHAIN = "HLS_TOOLCHAIN"
    SCHEDULER_QUEUE = "SCHEDULER_QUEUE"


class MorphismKind(str, Enum):
    PROCESSING_ELEMENT = "PROCESSING_ELEMENT"
    STREAM_CHANNEL = "STREAM_CHANNEL"
    MEMORY_MOVER = "MEMORY_MOVER"
    NOC_ROUTE = "NOC_ROUTE"
    HLS_LOWERING = "HLS_LOWERING"
    SHEAF_FLOW = "SHEAF_FLOW"
    VOID_OUROBOROS = "VOID_OUROBOROS"


class ChannelKind(str, Enum):
    FIFO = "FIFO"
    AXI_STREAM = "AXI_STREAM"
    HBM_STREAM = "HBM_STREAM"
    NOC_STREAM = "NOC_STREAM"


class CellularMoveKind(str, Enum):
    TWISTED_K_REWRITE = "TWISTED_K_REWRITE"
    DATAFLOW_FUSION = "DATAFLOW_FUSION"
    BACKPRESSURE_INSERT = "BACKPRESSURE_INSERT"
    RESOURCE_LOCALIZATION = "RESOURCE_LOCALIZATION"
    VOID_RECURSION = "VOID_RECURSION"


@dataclass(frozen=True, slots=True)
class QuazrisType:
    type_id: str
    carrier: str
    semantic_type: str
    twisted_k_type: str
    discopy_object: str
    cellular_dimension: int
    context_id: str = SIGILITAS_CONTEXT

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.type_id:
            errors.append("quazris_type_id_missing")
        if not self.carrier or not self.semantic_type:
            errors.append(f"quazris_type_boundary_missing:{self.type_id}")
        if not self.twisted_k_type:
            errors.append(f"quazris_type_twisted_k_missing:{self.type_id}")
        if not self.discopy_object:
            errors.append(f"quazris_type_discopy_object_missing:{self.type_id}")
        if self.cellular_dimension < 0:
            errors.append(f"quazris_type_negative_dimension:{self.type_id}")
        if self.context_id not in {SIGILITAS_CONTEXT, VOID_VORTEX_CONTEXT}:
            errors.append(f"quazris_type_context_unknown:{self.type_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class QuazrisMorphism:
    morphism_id: str
    kind: MorphismKind
    source_type_ids: tuple[str, ...]
    target_type_ids: tuple[str, ...]
    categorical_law: str
    strikk_witness: str
    data_activated: bool = True
    no_global_program_counter: bool = True
    preserves_discopy_typing: bool = True
    preserves_twisted_k_type: bool = True

    def validate(self, known_type_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.morphism_id:
            errors.append("quazris_morphism_id_missing")
        if not self.source_type_ids:
            errors.append(f"quazris_morphism_source_missing:{self.morphism_id}")
        if not self.target_type_ids:
            errors.append(f"quazris_morphism_target_missing:{self.morphism_id}")
        if set(self.source_type_ids) - known_type_ids:
            errors.append(f"quazris_morphism_unknown_source:{self.morphism_id}")
        if set(self.target_type_ids) - known_type_ids:
            errors.append(f"quazris_morphism_unknown_target:{self.morphism_id}")
        if not self.categorical_law:
            errors.append(f"quazris_morphism_law_missing:{self.morphism_id}")
        if not self.strikk_witness:
            errors.append(f"quazris_morphism_strikk_missing:{self.morphism_id}")
        if not self.data_activated:
            errors.append(f"quazris_morphism_not_dataflow:{self.morphism_id}")
        if not self.no_global_program_counter:
            errors.append(f"quazris_morphism_von_neumann_drift:{self.morphism_id}")
        if not self.preserves_discopy_typing:
            errors.append(f"quazris_morphism_discopy_drift:{self.morphism_id}")
        if not self.preserves_twisted_k_type:
            errors.append(f"quazris_morphism_twisted_k_drift:{self.morphism_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class DataflowChannel:
    channel_id: str
    channel_kind: ChannelKind
    source_morphism_id: str
    target_morphism_id: str
    type_id: str
    backpressure_policy: str
    depth_policy: str
    preserves_order: bool = True
    deadlock_checked: bool = True
    overflow_checked: bool = True

    def validate(
        self,
        known_morphism_ids: set[str],
        known_type_ids: set[str],
    ) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.channel_id:
            errors.append("dataflow_channel_id_missing")
        if self.source_morphism_id not in known_morphism_ids:
            errors.append(f"dataflow_channel_unknown_source:{self.channel_id}")
        if self.target_morphism_id not in known_morphism_ids:
            errors.append(f"dataflow_channel_unknown_target:{self.channel_id}")
        if self.type_id not in known_type_ids:
            errors.append(f"dataflow_channel_unknown_type:{self.channel_id}")
        if not self.backpressure_policy:
            errors.append(f"dataflow_channel_backpressure_missing:{self.channel_id}")
        if not self.depth_policy:
            errors.append(f"dataflow_channel_depth_missing:{self.channel_id}")
        if not self.preserves_order:
            errors.append(f"dataflow_channel_order_drift:{self.channel_id}")
        if not self.deadlock_checked:
            errors.append(f"dataflow_channel_deadlock_unchecked:{self.channel_id}")
        if not self.overflow_checked:
            errors.append(f"dataflow_channel_overflow_unchecked:{self.channel_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class FPGAResourceProfile:
    resource_id: str
    kind: FPGAResourceKind
    target_id: str
    descriptor: str
    owning_space: KernelSpace = KernelSpace.VIRTUAL_KRONE_SPACE
    virtualized: bool = True
    direct_user_access: bool = False

    def validate(self, target_id: str) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.resource_id:
            errors.append("fpga_resource_id_missing")
        if self.target_id != target_id:
            errors.append(f"fpga_resource_target_mismatch:{self.resource_id}")
        if not self.descriptor:
            errors.append(f"fpga_resource_descriptor_missing:{self.resource_id}")
        if self.owning_space == KernelSpace.VIRTUAL_USER_SPACE:
            errors.append(f"fpga_resource_user_owned:{self.resource_id}")
        if not self.virtualized:
            errors.append(f"fpga_resource_not_virtualized:{self.resource_id}")
        if self.direct_user_access:
            errors.append(f"fpga_resource_direct_user_access:{self.resource_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class FPGATargetProfile:
    target_id: str
    family: FPGATargetFamily
    architecture_tags: tuple[str, ...]
    resources: tuple[FPGAResourceProfile, ...]
    scheduler_interface: str
    hls_flow: str
    virtualized: bool = True
    physical_instantiation_attached: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.target_id:
            errors.append("fpga_target_id_missing")
        if not self.architecture_tags:
            errors.append(f"fpga_target_architecture_tags_missing:{self.target_id}")
        if not self.resources:
            errors.append(f"fpga_target_resources_missing:{self.target_id}")
        if not self.scheduler_interface:
            errors.append(f"fpga_target_scheduler_missing:{self.target_id}")
        if not self.hls_flow:
            errors.append(f"fpga_target_hls_flow_missing:{self.target_id}")
        if not self.virtualized:
            errors.append(f"fpga_target_not_virtualized:{self.target_id}")
        if self.physical_instantiation_attached:
            errors.append(f"fpga_target_physical_instantiation_forbidden:{self.target_id}")

        resource_ids = {resource.resource_id for resource in self.resources}
        if len(resource_ids) != len(self.resources):
            errors.append("duplicate_fpga_resource")
        for resource in self.resources:
            errors.extend(resource.validate(self.target_id))

        required = {
            FPGAResourceKind.PROCESSING_ELEMENT,
            FPGAResourceKind.FIFO_STREAM,
            FPGAResourceKind.HBM_MEMORY,
            FPGAResourceKind.NETWORK_ON_CHIP,
            FPGAResourceKind.DSP_TILE,
        }
        actual = {resource.kind for resource in self.resources}
        missing = sorted(required - actual, key=lambda item: item.value)
        if missing:
            labels = ",".join(item.value for item in missing)
            errors.append(f"fpga_target_required_resource_missing:{labels}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class CellularFlowMove:
    move_id: str
    kind: CellularMoveKind
    source_morphism_id: str
    target_morphism_id: str
    cellular_dimension: int
    strikk_witness: str
    preserves_dataflow_activation: bool = True
    preserves_backpressure: bool = True
    preserves_chiral_boundary: bool = True
    preserves_twisted_k_type: bool = True

    def validate(self, known_morphism_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.move_id:
            errors.append("cellular_flow_move_id_missing")
        if self.source_morphism_id not in known_morphism_ids:
            errors.append(f"cellular_flow_move_unknown_source:{self.move_id}")
        if self.target_morphism_id not in known_morphism_ids:
            errors.append(f"cellular_flow_move_unknown_target:{self.move_id}")
        if self.cellular_dimension < 0:
            errors.append(f"cellular_flow_move_negative_dimension:{self.move_id}")
        if not self.strikk_witness:
            errors.append(f"cellular_flow_move_strikk_missing:{self.move_id}")
        if not self.preserves_dataflow_activation:
            errors.append(f"cellular_flow_move_activation_drift:{self.move_id}")
        if not self.preserves_backpressure:
            errors.append(f"cellular_flow_move_backpressure_drift:{self.move_id}")
        if not self.preserves_chiral_boundary:
            errors.append(f"cellular_flow_move_chiral_drift:{self.move_id}")
        if not self.preserves_twisted_k_type:
            errors.append(f"cellular_flow_move_twisted_k_drift:{self.move_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class SigilAPIInterface:
    api_id: str
    protocols: tuple[str, ...]
    virtual_io_schema_id: str = VIRTUAL_IO_SCHEMA_ID
    coherent_sheaf_schema_id: str = COHERENT_SHEAF_SCHEMA_ID
    sigilitas_context: str = SIGILITAS_CONTEXT
    direct_hardware_calls: bool = False
    scheduler_submission_requires_krone: bool = True
    physical_resource_handles_exposed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.api_id:
            errors.append("sigil_api_id_missing")
        if not self.protocols:
            errors.append(f"sigil_api_protocols_missing:{self.api_id}")
        if self.virtual_io_schema_id != VIRTUAL_IO_SCHEMA_ID:
            errors.append(f"sigil_api_virtual_io_schema_mismatch:{self.api_id}")
        if self.coherent_sheaf_schema_id != COHERENT_SHEAF_SCHEMA_ID:
            errors.append(f"sigil_api_sheaf_schema_mismatch:{self.api_id}")
        if self.sigilitas_context != SIGILITAS_CONTEXT:
            errors.append(f"sigil_api_context_mismatch:{self.api_id}")
        if self.direct_hardware_calls:
            errors.append(f"sigil_api_direct_hardware_access_forbidden:{self.api_id}")
        if not self.scheduler_submission_requires_krone:
            errors.append(f"sigil_api_scheduler_krone_guard_missing:{self.api_id}")
        if self.physical_resource_handles_exposed:
            errors.append(f"sigil_api_physical_handles_exposed:{self.api_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class HPCLocalizedKernel:
    kernel_id: str
    dsl_forms: tuple[QuazrisDSLForm, ...]
    target: FPGATargetProfile
    quazris_types: tuple[QuazrisType, ...]
    morphisms: tuple[QuazrisMorphism, ...]
    channels: tuple[DataflowChannel, ...]
    cellular_moves: tuple[CellularFlowMove, ...]
    sigil_api: SigilAPIInterface
    plural_sheaf_sections: tuple[str, ...]
    pydantika_annotation_flow_ids: tuple[str, ...]
    kokompile_plan_id: str
    authorial_context: str = "JJBV_AUTHORED_SIGIL_ALGORITHMS"
    void_vortex_context: str = VOID_VORTEX_CONTEXT
    schema_id: str = SCHEMA_ID
    source_bound: bool = True
    fully_factorizable: bool = True
    conformal_architecture: bool = True
    pydantika_annotations_required: bool = True
    runtime_executed: bool = False
    hardware_synthesis_performed: bool = False
    scheduler_job_submitted: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.kernel_id:
            errors.append("hpc_localized_kernel_id_missing")
        if self.schema_id != SCHEMA_ID:
            errors.append("hpc_localized_kernel_schema_mismatch")
        if not self.source_bound:
            errors.append("hpc_localized_kernel_not_source_bound")
        if self.runtime_executed:
            errors.append("hpc_localized_kernel_runtime_execution_forbidden")
        if self.hardware_synthesis_performed:
            errors.append("hpc_localized_kernel_hardware_synthesis_forbidden")
        if self.scheduler_job_submitted:
            errors.append("hpc_localized_kernel_scheduler_submission_forbidden")
        if self.void_vortex_context != VOID_VORTEX_CONTEXT:
            errors.append("hpc_localized_kernel_void_context_mismatch")
        if not self.fully_factorizable:
            errors.append("hpc_localized_kernel_not_fully_factorizable")
        if not self.conformal_architecture:
            errors.append("hpc_localized_kernel_not_conformal")
        if not self.pydantika_annotations_required:
            errors.append("hpc_localized_kernel_pydantika_not_required")
        if not self.pydantika_annotation_flow_ids:
            errors.append("hpc_localized_kernel_pydantika_flows_missing")
        if not self.kokompile_plan_id:
            errors.append("hpc_localized_kernel_kokompile_plan_missing")
        required_forms = {
            QuazrisDSLForm.DATAFLOW,
            QuazrisDSLForm.DISCOPY_TYPED,
            QuazrisDSLForm.TWISTED_K_TYPED,
        }
        if not required_forms.issubset(set(self.dsl_forms)):
            errors.append("hpc_localized_kernel_dsl_forms_incomplete")
        if not self.plural_sheaf_sections:
            errors.append("hpc_localized_kernel_sheaf_sections_missing")

        errors.extend(self.target.validate())
        errors.extend(self.sigil_api.validate())

        type_ids = {item.type_id for item in self.quazris_types}
        if len(type_ids) != len(self.quazris_types):
            errors.append("duplicate_quazris_type")
        for item in self.quazris_types:
            errors.extend(item.validate())

        morphism_ids = {item.morphism_id for item in self.morphisms}
        if len(morphism_ids) != len(self.morphisms):
            errors.append("duplicate_quazris_morphism")
        for morphism in self.morphisms:
            errors.extend(morphism.validate(type_ids))

        channel_ids = {channel.channel_id for channel in self.channels}
        if len(channel_ids) != len(self.channels):
            errors.append("duplicate_dataflow_channel")
        for channel in self.channels:
            errors.extend(channel.validate(morphism_ids, type_ids))

        for move in self.cellular_moves:
            errors.extend(move.validate(morphism_ids))

        kinds = {morphism.kind for morphism in self.morphisms}
        required_kinds = {
            MorphismKind.PROCESSING_ELEMENT,
            MorphismKind.STREAM_CHANNEL,
            MorphismKind.MEMORY_MOVER,
            MorphismKind.NOC_ROUTE,
            MorphismKind.SHEAF_FLOW,
            MorphismKind.VOID_OUROBOROS,
        }
        missing_kinds = sorted(required_kinds - kinds, key=lambda item: item.value)
        if missing_kinds:
            labels = ",".join(item.value for item in missing_kinds)
            errors.append(f"hpc_localized_kernel_morphism_missing:{labels}")
        return tuple(errors)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["target"] = asdict(self.target)
        payload["quazris_types"] = [
            asdict(quazris_type) for quazris_type in self.quazris_types
        ]
        payload["morphisms"] = [
            asdict(morphism) for morphism in self.morphisms
        ]
        payload["channels"] = [asdict(channel) for channel in self.channels]
        payload["cellular_moves"] = [
            asdict(move) for move in self.cellular_moves
        ]
        payload["sigil_api"] = asdict(self.sigil_api)
        payload["kernel_sha256"] = stable_digest(payload)
        return payload


def stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return sha256(encoded).hexdigest()


def build_hpc_localized_quazris_kernel() -> HPCLocalizedKernel:
    """Build the canonical virtual HPC-localized SIGIL kernel candidate."""

    target_id = "target:amd-alveo-v80-versal-hbm-inspired"
    target = FPGATargetProfile(
        target_id,
        FPGATargetFamily.AMD_ALVEO_V80_INSPIRED,
        (
            "VERSAL_HBM_INSPIRED",
            "DATAFLOW_ARCHITECTURE",
            "HPC_LOCALIZED",
        ),
        (
            FPGAResourceProfile(
                "res:pe-array",
                FPGAResourceKind.PROCESSING_ELEMENT,
                target_id,
                "virtual processing element array",
            ),
            FPGAResourceProfile(
                "res:fifo-streams",
                FPGAResourceKind.FIFO_STREAM,
                target_id,
                "virtual FIFO and AXI-stream channels",
            ),
            FPGAResourceProfile(
                "res:hbm",
                FPGAResourceKind.HBM_MEMORY,
                target_id,
                "vendor-documented HBM memory profile",
            ),
            FPGAResourceProfile(
                "res:noc",
                FPGAResourceKind.NETWORK_ON_CHIP,
                target_id,
                "Versal-inspired network-on-chip route profile",
            ),
            FPGAResourceProfile(
                "res:dsp",
                FPGAResourceKind.DSP_TILE,
                target_id,
                "virtual DSP tile profile",
            ),
            FPGAResourceProfile(
                "res:hls",
                FPGAResourceKind.HLS_TOOLCHAIN,
                target_id,
                "Vivado/HLS-style lowering boundary",
            ),
            FPGAResourceProfile(
                "res:scheduler",
                FPGAResourceKind.SCHEDULER_QUEUE,
                target_id,
                "SLURM-like krone-guarded job boundary",
            ),
        ),
        "KRONE_GUARDED_SLURM_LIKE_QUEUE",
        "VIRTUAL_HLS_PLAN_ONLY",
    )
    quazris_types = (
        QuazrisType(
            "type:sigil-api-command",
            "SIGIL_API_REQUEST",
            "QUAZRIS_CONTROL_STREAM",
            "K::VOID_VORTEX_CONTROL",
            "Command",
            0,
        ),
        QuazrisType(
            "type:hbm-stream",
            "HBM_STREAM",
            "PLURAL_TYPED_DATAFLOW",
            "K::HBM_CARRIER",
            "HBMStream",
            1,
        ),
        QuazrisType(
            "type:pe-tile",
            "PROCESSING_ELEMENT_TILE",
            "DISCOPY_TYPED_MORPHISM",
            "K::PE_TILE",
            "PETile",
            2,
        ),
        QuazrisType(
            "type:coherent-sheaf-section",
            "PACA_ESTACA_SECTION",
            "COHERENT_SHEAF_PLURAL_FLOW",
            "K::SHEAF_SECTION",
            "SheafSection",
            2,
        ),
        QuazrisType(
            "type:void-vortex-proof",
            "VOID_OUROBOROS_OBLIGATION",
            "COMPOSITIONAL_CONTEXTUAL_LWE",
            "K::VOID_VORTEX_ALHAMBRA",
            "VoidProof",
            3,
            context_id=VOID_VORTEX_CONTEXT,
        ),
    )
    morphisms = (
        QuazrisMorphism(
            "mor:sigil-api-ingress",
            MorphismKind.SHEAF_FLOW,
            ("type:sigil-api-command",),
            ("type:coherent-sheaf-section",),
            "functor(SIGIL_API -> CoherentSheafSection)",
            "STRIKK::SIGIL_API_SHEAF_GATE",
        ),
        QuazrisMorphism(
            "mor:hbm-memory-move",
            MorphismKind.MEMORY_MOVER,
            ("type:coherent-sheaf-section",),
            ("type:hbm-stream",),
            "morphism(memory_move) preserves stream object",
            "STRIKK::HBM_MOVE_IS_VIRTUAL",
        ),
        QuazrisMorphism(
            "mor:noc-route",
            MorphismKind.NOC_ROUTE,
            ("type:hbm-stream",),
            ("type:pe-tile",),
            "noc_route : HBMStream -> PETile",
            "STRIKK::NOC_ROUTE_TYPED",
        ),
        QuazrisMorphism(
            "mor:pe-compute",
            MorphismKind.PROCESSING_ELEMENT,
            ("type:pe-tile",),
            ("type:coherent-sheaf-section",),
            "g . f with tensor-parallel PE composition",
            "STRIKK::DISCOPY_PE_MORPHISM",
        ),
        QuazrisMorphism(
            "mor:fifo-backpressure",
            MorphismKind.STREAM_CHANNEL,
            ("type:coherent-sheaf-section",),
            ("type:coherent-sheaf-section",),
            "fifo_channel preserves monoidal wire type",
            "STRIKK::BACKPRESSURE_HANDSHAKE",
        ),
        QuazrisMorphism(
            "mor:void-ouroboros-recur",
            MorphismKind.VOID_OUROBOROS,
            ("type:void-vortex-proof",),
            ("type:void-vortex-proof",),
            "trace(void_boundary) returns contextual obligation",
            "STRIKK::VOID_TYPED_OUROBOROS_FLOW",
        ),
    )
    channels = (
        DataflowChannel(
            "chan:hbm-to-noc",
            ChannelKind.HBM_STREAM,
            "mor:hbm-memory-move",
            "mor:noc-route",
            "type:hbm-stream",
            "BACKPRESSURE_REQUIRED",
            "DEPTH_POLICY_TOOL_PROVEN",
        ),
        DataflowChannel(
            "chan:noc-to-pe",
            ChannelKind.NOC_STREAM,
            "mor:noc-route",
            "mor:pe-compute",
            "type:pe-tile",
            "HANDSHAKE_READY_VALID",
            "DEPTH_POLICY_TOOL_PROVEN",
        ),
        DataflowChannel(
            "chan:pe-to-sheaf",
            ChannelKind.FIFO,
            "mor:pe-compute",
            "mor:fifo-backpressure",
            "type:coherent-sheaf-section",
            "BACKPRESSURE_REQUIRED",
            "DEPTH_POLICY_TOOL_PROVEN",
        ),
    )
    moves = (
        CellularFlowMove(
            "move:twisted-k-dataflow-fusion",
            CellularMoveKind.DATAFLOW_FUSION,
            "mor:noc-route",
            "mor:pe-compute",
            2,
            "STRIKK::TWISTED_K_DATAFLOW_FUSION",
        ),
        CellularFlowMove(
            "move:insert-backpressure",
            CellularMoveKind.BACKPRESSURE_INSERT,
            "mor:pe-compute",
            "mor:fifo-backpressure",
            2,
            "STRIKK::FIFO_BACKPRESSURE_CELL",
        ),
        CellularFlowMove(
            "move:void-vortex-return",
            CellularMoveKind.VOID_RECURSION,
            "mor:fifo-backpressure",
            "mor:void-ouroboros-recur",
            3,
            "STRIKK::VOID_VORTEX_ALHAMBRA_RETURN",
        ),
    )
    api = SigilAPIInterface(
        "api:sigil4cpython-hpc-localized",
        (
            "REST_LIFT",
            "IOS_LIFT",
            "HPC_SCHEDULER_LIFT",
            "UNIFORM_VIRTUAL_IO_STREAM",
        ),
    )
    return HPCLocalizedKernel(
        "SIGIL4CPYTHON_HPC_LOCALIZED_QUAZRIS_FPGA_KERNEL_V1",
        (
            QuazrisDSLForm.DATAFLOW,
            QuazrisDSLForm.DISCOPY_TYPED,
            QuazrisDSLForm.TWISTED_K_TYPED,
        ),
        target,
        quazris_types,
        morphisms,
        channels,
        moves,
        api,
        (
            "section:pydantika-coherent-sheaf",
            "section:virtual-rest-ios",
            "section:hpc-localized-quazris-fpga",
        ),
        (
            "ann:sigil4cpython:typed-kernel",
            "ann:sigil4cpython:paca-estaca",
            "ann:hpc-localized:quazris-dataflow",
        ),
        "kokompile:fully-factorizable-conformal-hpc-architecture",
    )


def compile_hpc_localized_quazris_kernel(
    kernel: HPCLocalizedKernel,
) -> dict[str, object]:
    """Validate an HPC-localized kernel and return an admission payload."""

    errors = kernel.validate()
    reject_markers = (
        "runtime_execution_forbidden",
        "hardware_synthesis_forbidden",
        "scheduler_submission_forbidden",
        "direct_hardware_access_forbidden",
        "direct_user_access",
        "fpga_resource_user_owned",
        "physical_instantiation_forbidden",
        "physical_handles_exposed",
    )
    if any(any(marker in error for marker in reject_markers) for error in errors):
        state = HPCLocalizedState.REJECT
    elif errors:
        state = HPCLocalizedState.HOLD_WITH_OBSTRUCTION
    else:
        state = HPCLocalizedState.ADMIT
    payload = kernel.to_dict()
    payload["uap_state"] = state.value
    payload["obstruction_ledger"] = list(errors)
    payload["runtime_executed"] = False
    payload["hardware_synthesis_performed"] = False
    payload["scheduler_job_submitted"] = False
    payload["resource_access_performed"] = False
    payload["human_review_required"] = True
    return payload


__all__ = [
    "COHERENT_SHEAF_SCHEMA_ID",
    "ChannelKind",
    "CellularFlowMove",
    "CellularMoveKind",
    "DataflowChannel",
    "FPGATargetFamily",
    "FPGATargetProfile",
    "FPGAResourceKind",
    "FPGAResourceProfile",
    "HPCLocalizedKernel",
    "HPCLocalizedState",
    "KernelSpace",
    "MorphismKind",
    "QuazrisDSLForm",
    "QuazrisMorphism",
    "QuazrisType",
    "SCHEMA_ID",
    "SIGILITAS_CONTEXT",
    "SigilAPIInterface",
    "VIRTUAL_IO_SCHEMA_ID",
    "VOID_VORTEX_CONTEXT",
    "build_hpc_localized_quazris_kernel",
    "compile_hpc_localized_quazris_kernel",
    "stable_digest",
]
