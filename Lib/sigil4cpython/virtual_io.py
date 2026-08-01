"""Virtual REST/IOS stream contracts for SIGIL4CPython.

This module models REST endpoints and IOS handles as the same virtual IO stream
until a typed resource cell attaches concrete authority.  It is metadata only:
it does not open sockets, submit scheduler jobs, touch devices, or change
CPython interpreter semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Iterable, Mapping


SCHEMA_ID = "SIGIL4CPYTHON_VIRTUAL_REST_IO_KERNELS_V1"


class VirtualIOState(str, Enum):
    ADMIT = "ADMIT"
    HOLD_WITH_OBSTRUCTION = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT"


class VirtualIOProtocol(str, Enum):
    REST = "REST"
    IOS = "IOS"
    MCP = "MCP"
    HPC_SCHEDULER = "HPC_SCHEDULER"
    STREAM = "STREAM"


class ResourceAuthority(str, Enum):
    VIRTUAL_ONLY = "VIRTUAL_ONLY"
    CELLULAR_ATTACHED = "CELLULAR_ATTACHED"
    HARDWARE_BOUND = "HARDWARE_BOUND"
    SCHEDULER_BOUND = "SCHEDULER_BOUND"


class CellKind(str, Enum):
    VIRTUAL_IO = "VIRTUAL_IO"
    REST_LIFT = "REST_LIFT"
    IOS_LIFT = "IOS_LIFT"
    RESOURCE_CELL = "RESOURCE_CELL"
    STRIKK_GUARD = "STRIKK_GUARD"
    TWISTED_MOVE = "TWISTED_MOVE"


@dataclass(frozen=True, slots=True)
class VirtualIOPort:
    port_id: str
    protocol: VirtualIOProtocol
    semantic_type: str
    stream_type: str = "UNIFORM_VIRTUAL_IO_STREAM"
    attached_to_resource: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.port_id:
            errors.append("virtual_io_port_id_missing")
        if not self.semantic_type:
            errors.append(f"virtual_io_semantic_type_missing:{self.port_id}")
        if not self.stream_type:
            errors.append(f"virtual_io_stream_type_missing:{self.port_id}")
        if self.attached_to_resource and self.protocol in {
            VirtualIOProtocol.REST,
            VirtualIOProtocol.IOS,
        }:
            errors.append(f"resource_attachment_belongs_on_cell:{self.port_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class IOCell:
    cell_id: str
    kind: CellKind
    source_port_id: str
    target_port_id: str
    authority: ResourceAuthority
    strikk_type: str
    resource_refs: tuple[str, ...] = ()
    direct_resource_access: bool = False

    def validate(self, port_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.cell_id:
            errors.append("io_cell_id_missing")
        if self.source_port_id not in port_ids or self.target_port_id not in port_ids:
            errors.append(f"io_cell_unknown_port:{self.cell_id}")
        if not self.strikk_type:
            errors.append(f"io_cell_strikk_type_missing:{self.cell_id}")
        if self.authority == ResourceAuthority.VIRTUAL_ONLY and self.resource_refs:
            errors.append(f"virtual_cell_has_resource_refs:{self.cell_id}")
        if self.direct_resource_access:
            if self.kind != CellKind.RESOURCE_CELL:
                errors.append(f"direct_access_requires_resource_cell:{self.cell_id}")
            if self.authority == ResourceAuthority.VIRTUAL_ONLY:
                errors.append(f"direct_access_requires_attached_authority:{self.cell_id}")
            if not self.resource_refs:
                errors.append(f"direct_access_resource_refs_missing:{self.cell_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class CellularTwistedMove:
    move_id: str
    source_cell_id: str
    target_cell_id: str
    cellular_dimension: int
    preserves_stream_type: bool
    preserves_authority_boundary: bool
    strikk_witness: str

    def validate(self, cell_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.move_id:
            errors.append("twisted_move_id_missing")
        if self.source_cell_id not in cell_ids or self.target_cell_id not in cell_ids:
            errors.append(f"twisted_move_unknown_cell:{self.move_id}")
        if self.cellular_dimension < 0:
            errors.append(f"twisted_move_negative_dimension:{self.move_id}")
        if not self.preserves_stream_type:
            errors.append(f"twisted_move_stream_type_drift:{self.move_id}")
        if not self.preserves_authority_boundary:
            errors.append(f"twisted_move_authority_boundary_drift:{self.move_id}")
        if not self.strikk_witness:
            errors.append(f"twisted_move_strikk_witness_missing:{self.move_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class VirtualIOKernel:
    kernel_id: str
    ports: tuple[VirtualIOPort, ...]
    cells: tuple[IOCell, ...]
    twisted_moves: tuple[CellularTwistedMove, ...]
    claim_boundary: tuple[str, ...]
    physical_instantiation_attached: bool = False
    restful_logic_lifted: bool = True
    ios_logic_lifted: bool = True
    schema_id: str = SCHEMA_ID

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.kernel_id:
            errors.append("virtual_io_kernel_id_missing")
        if self.schema_id != SCHEMA_ID:
            errors.append("virtual_io_schema_id_mismatch")
        if not self.ports:
            errors.append("virtual_io_ports_missing")
        if not self.cells:
            errors.append("virtual_io_cells_missing")
        if not self.claim_boundary:
            errors.append("virtual_io_claim_boundary_missing")
        if not (self.restful_logic_lifted and self.ios_logic_lifted):
            errors.append("rest_ios_lift_incomplete")

        port_ids = {port.port_id for port in self.ports}
        if len(port_ids) != len(self.ports):
            errors.append("duplicate_virtual_io_port")
        for port in self.ports:
            errors.extend(port.validate())

        cell_ids = {cell.cell_id for cell in self.cells}
        if len(cell_ids) != len(self.cells):
            errors.append("duplicate_virtual_io_cell")
        for cell in self.cells:
            errors.extend(cell.validate(port_ids))

        for move in self.twisted_moves:
            errors.extend(move.validate(cell_ids))

        rest_ios_ports = [
            port
            for port in self.ports
            if port.protocol in {VirtualIOProtocol.REST, VirtualIOProtocol.IOS}
        ]
        stream_types = {port.stream_type for port in rest_ios_ports}
        semantic_types = {port.semantic_type for port in rest_ios_ports}
        if len(stream_types) > 1:
            errors.append("rest_ios_stream_type_nonconformal")
        if len(semantic_types) > 1:
            errors.append("rest_ios_semantic_type_nonconformal")

        direct_cells = [cell for cell in self.cells if cell.direct_resource_access]
        if self.physical_instantiation_attached and not direct_cells:
            errors.append("physical_instantiation_without_resource_cell")
        if not self.physical_instantiation_attached and direct_cells:
            errors.append("resource_cell_attached_without_physical_instantiation")
        return tuple(errors)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["ports"] = [asdict(port) for port in self.ports]
        payload["cells"] = [asdict(cell) for cell in self.cells]
        payload["twisted_moves"] = [asdict(move) for move in self.twisted_moves]
        payload["kernel_sha256"] = stable_digest(payload)
        return payload


def _normalize_tokens(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(value).strip() for value in values if str(value).strip()}))


def stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def build_pacaiogame_virtual_rest_kernel() -> VirtualIOKernel:
    """Build the canonical virtual REST/IOS kernel for PACAIoGames."""

    ports = (
        VirtualIOPort("rest:control", VirtualIOProtocol.REST, "PACAIOS_CONTROL"),
        VirtualIOPort("ios:control", VirtualIOProtocol.IOS, "PACAIOS_CONTROL"),
        VirtualIOPort("stream:uniform", VirtualIOProtocol.STREAM, "PACAIOS_CONTROL"),
    )
    cells = (
        IOCell(
            "cell:rest-lift",
            CellKind.REST_LIFT,
            "rest:control",
            "stream:uniform",
            ResourceAuthority.VIRTUAL_ONLY,
            "STRIKK::RESTFUL_LOGIC_LIFT",
        ),
        IOCell(
            "cell:ios-lift",
            CellKind.IOS_LIFT,
            "ios:control",
            "stream:uniform",
            ResourceAuthority.VIRTUAL_ONLY,
            "STRIKK::IOS_LOGIC_LIFT",
        ),
        IOCell(
            "cell:guard",
            CellKind.STRIKK_GUARD,
            "stream:uniform",
            "stream:uniform",
            ResourceAuthority.VIRTUAL_ONLY,
            "STRIKK::RESOURCE_AUTHORITY_GUARD",
        ),
    )
    moves = (
        CellularTwistedMove(
            "move:rest-ios-conformal",
            "cell:rest-lift",
            "cell:ios-lift",
            2,
            True,
            True,
            "witness:uniform-virtual-io-stream",
        ),
    )
    return VirtualIOKernel(
        "SIGIL4CPYTHON_PACAIOS_VIRTUAL_REST_IO_KERNEL_V1",
        ports,
        cells,
        moves,
        _normalize_tokens(
            (
                "virtual_stream_not_hardware_authority",
                "rest_endpoint_not_resource_access",
                "ios_handle_not_resource_access",
                "resource_access_requires_cellular_attachment",
                "strikk_type_required_for_resource_cells",
            )
        ),
    )


def compile_virtual_io_kernel(kernel: VirtualIOKernel) -> dict[str, object]:
    """Validate a virtual IO kernel and return a canonical admission payload."""

    errors = kernel.validate()
    direct_errors = tuple(error for error in errors if error.startswith("direct_access_"))
    if direct_errors:
        state = VirtualIOState.REJECT
    elif errors:
        state = VirtualIOState.HOLD_WITH_OBSTRUCTION
    else:
        state = VirtualIOState.ADMIT
    payload = kernel.to_dict()
    payload["uap_state"] = state.value
    payload["obstruction_ledger"] = list(errors)
    payload["resource_access_performed"] = False
    payload["rest_call_performed"] = False
    payload["ios_call_performed"] = False
    return payload


__all__ = [
    "CellKind",
    "CellularTwistedMove",
    "IOCell",
    "ResourceAuthority",
    "SCHEMA_ID",
    "VirtualIOKernel",
    "VirtualIOPort",
    "VirtualIOProtocol",
    "VirtualIOState",
    "build_pacaiogame_virtual_rest_kernel",
    "compile_virtual_io_kernel",
    "stable_digest",
]
