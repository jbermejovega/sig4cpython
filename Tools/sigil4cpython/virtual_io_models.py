"""Strict Pydantika models for SIGIL4CPython virtual IO kernels."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


SCHEMA_ID = "SIGIL4CPYTHON_VIRTUAL_REST_IO_KERNELS_V1"


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


class VirtualIOPortModel(StrictModel):
    port_id: str = Field(min_length=1, max_length=192)
    protocol: Literal["REST", "IOS", "MCP", "HPC_SCHEDULER", "STREAM"]
    semantic_type: str = Field(min_length=1, max_length=192)
    stream_type: str = Field(default="UNIFORM_VIRTUAL_IO_STREAM", min_length=1, max_length=192)
    attached_to_resource: Literal[False] = False


class IOCellModel(StrictModel):
    cell_id: str = Field(min_length=1, max_length=192)
    kind: Literal[
        "VIRTUAL_IO",
        "REST_LIFT",
        "IOS_LIFT",
        "RESOURCE_CELL",
        "STRIKK_GUARD",
        "TWISTED_MOVE",
    ]
    source_port_id: str = Field(min_length=1, max_length=192)
    target_port_id: str = Field(min_length=1, max_length=192)
    authority: Literal[
        "VIRTUAL_ONLY",
        "CELLULAR_ATTACHED",
        "HARDWARE_BOUND",
        "SCHEDULER_BOUND",
    ]
    strikk_type: str = Field(min_length=1, max_length=192)
    resource_refs: StringTuple = Field(default=(), max_length=128)
    direct_resource_access: bool = False

    @model_validator(mode="after")
    def validate_resource_access(self) -> "IOCellModel":
        if self.authority == "VIRTUAL_ONLY" and self.resource_refs:
            raise ValueError("virtual_cell_has_resource_refs")
        if self.direct_resource_access:
            if self.kind != "RESOURCE_CELL":
                raise ValueError("direct_access_requires_resource_cell")
            if self.authority == "VIRTUAL_ONLY":
                raise ValueError("direct_access_requires_attached_authority")
            if not self.resource_refs:
                raise ValueError("direct_access_resource_refs_missing")
        return self


class CellularTwistedMoveModel(StrictModel):
    move_id: str = Field(min_length=1, max_length=192)
    source_cell_id: str = Field(min_length=1, max_length=192)
    target_cell_id: str = Field(min_length=1, max_length=192)
    cellular_dimension: int = Field(ge=0, le=32)
    preserves_stream_type: Literal[True] = True
    preserves_authority_boundary: Literal[True] = True
    strikk_witness: str = Field(min_length=1, max_length=192)


PortTuple = Annotated[tuple[VirtualIOPortModel, ...], BeforeValidator(_json_array_to_tuple)]
CellTuple = Annotated[tuple[IOCellModel, ...], BeforeValidator(_json_array_to_tuple)]
MoveTuple = Annotated[tuple[CellularTwistedMoveModel, ...], BeforeValidator(_json_array_to_tuple)]


class VirtualIOKernelModel(StrictModel):
    kernel_id: str = Field(min_length=1, max_length=192)
    ports: PortTuple = Field(min_length=1, max_length=4096)
    cells: CellTuple = Field(min_length=1, max_length=4096)
    twisted_moves: MoveTuple = Field(default=(), max_length=4096)
    claim_boundary: StringTuple = Field(min_length=1, max_length=4096)
    physical_instantiation_attached: bool = False
    restful_logic_lifted: Literal[True] = True
    ios_logic_lifted: Literal[True] = True
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    pydantika_is_tooling_not_stdlib_dependency: Literal[True] = True
    virtual_stream_is_not_hardware_authority: Literal[True] = True
    resource_access_performed: Literal[False] = False

    @model_validator(mode="after")
    def validate_kernel(self) -> "VirtualIOKernelModel":
        port_ids = tuple(port.port_id for port in self.ports)
        if len(port_ids) != len(set(port_ids)):
            raise ValueError("duplicate_virtual_io_port")
        cell_ids = tuple(cell.cell_id for cell in self.cells)
        if len(cell_ids) != len(set(cell_ids)):
            raise ValueError("duplicate_virtual_io_cell")
        known_ports = set(port_ids)
        if any(
            cell.source_port_id not in known_ports or cell.target_port_id not in known_ports
            for cell in self.cells
        ):
            raise ValueError("io_cell_unknown_port")
        known_cells = set(cell_ids)
        if any(
            move.source_cell_id not in known_cells or move.target_cell_id not in known_cells
            for move in self.twisted_moves
        ):
            raise ValueError("twisted_move_unknown_cell")
        rest_ios_ports = [port for port in self.ports if port.protocol in {"REST", "IOS"}]
        if len({port.stream_type for port in rest_ios_ports}) > 1:
            raise ValueError("rest_ios_stream_type_nonconformal")
        if len({port.semantic_type for port in rest_ios_ports}) > 1:
            raise ValueError("rest_ios_semantic_type_nonconformal")
        direct_cells = [cell for cell in self.cells if cell.direct_resource_access]
        if self.physical_instantiation_attached and not direct_cells:
            raise ValueError("physical_instantiation_without_resource_cell")
        if not self.physical_instantiation_attached and direct_cells:
            raise ValueError("resource_cell_attached_without_physical_instantiation")
        return self

    def canonical_digest(self) -> str:
        encoded = json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


class PydantikaVirtualIOCertificate(StrictModel):
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    model_name: Literal["VirtualIOKernelModel"] = "VirtualIOKernelModel"
    payload_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    serialization_round_trip_verified: Literal[True] = True
    resource_access_performed: Literal[False] = False
    rest_call_performed: Literal[False] = False
    ios_call_performed: Literal[False] = False
    human_review_required: Literal[True] = True


def compile_pydantika_virtual_io_kernel(payload: dict[str, object]) -> PydantikaVirtualIOCertificate:
    model = VirtualIOKernelModel.model_validate(payload)
    encoded = model.model_dump_json()
    reconstructed = VirtualIOKernelModel.model_validate_json(encoded)
    if reconstructed.model_dump(mode="json") != model.model_dump(mode="json"):
        raise ValueError("virtual_io_kernel_round_trip_failed")
    return PydantikaVirtualIOCertificate(payload_digest=model.canonical_digest())


__all__ = [
    "PydantikaVirtualIOCertificate",
    "SCHEMA_ID",
    "VirtualIOKernelModel",
    "compile_pydantika_virtual_io_kernel",
]
