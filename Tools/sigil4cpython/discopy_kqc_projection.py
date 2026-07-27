"""Optional DisCoPy projection for KQC publication-sheaf compiler paths.

The pure-data plan is always available.  Materialization imports DisCoPy only
when explicitly requested and never grants publication, execution, or semantic
authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Mapping


@dataclass(frozen=True, slots=True)
class DiscopyBoxPlan:
    box_id: str
    source_type: str
    target_type: str
    strategy: str
    context_id: str


@dataclass(frozen=True, slots=True)
class DiscopyProjectionPlan:
    plan_id: str
    boxes: tuple[DiscopyBoxPlan, ...]
    composable: bool
    obstruction_ledger: tuple[str, ...]
    backend_required: str = "discopy>=1.2.2,<2"
    backend_executed: bool = False
    publication_performed: bool = False
    identity_transport: bool = False

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["boxes"] = [asdict(box) for box in self.boxes]
        return payload

    def canonical_digest(self) -> str:
        encoded = json.dumps(
            self.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


def build_discopy_projection_plan(
    kernels: Iterable[Mapping[str, object]],
    *,
    plan_id: str = "SIGIL4CPYTHON_KQC_DISCOPY_PROJECTION_V1",
) -> DiscopyProjectionPlan:
    boxes = tuple(
        DiscopyBoxPlan(
            box_id=str(kernel["kernel_id"]),
            source_type=str(kernel["source_type"]),
            target_type=str(kernel["target_type"]),
            strategy=str(kernel["strategy"]),
            context_id=str(kernel["context_id"]),
        )
        for kernel in kernels
    )
    obstructions: list[str] = []
    for left, right in zip(boxes, boxes[1:]):
        if left.target_type != right.source_type:
            obstructions.append(
                f"noncomposable_box_boundary:{left.box_id}->{right.box_id}"
            )
    return DiscopyProjectionPlan(
        plan_id=plan_id,
        boxes=boxes,
        composable=not obstructions,
        obstruction_ledger=tuple(obstructions),
    )


def materialize_discopy_diagram(plan: DiscopyProjectionPlan) -> dict[str, object]:
    """Materialize a sequential monoidal diagram when DisCoPy is available.

    The returned dictionary is a witness only.  It does not execute a compiler or
    publish a patch.
    """

    if not plan.composable:
        return {
            "state": "HOLD_WITH_OBSTRUCTION",
            "obstruction_ledger": list(plan.obstruction_ledger),
            "backend_executed": False,
        }
    try:
        from discopy.monoidal import Box, Id, Ty
    except ImportError:
        return {
            "state": "HOLD_BACKEND_UNAVAILABLE",
            "required_backend": plan.backend_required,
            "backend_executed": False,
        }

    if not plan.boxes:
        return {
            "state": "HOLD_WITH_OBSTRUCTION",
            "obstruction_ledger": ["empty_discopy_plan"],
            "backend_executed": False,
        }

    first = plan.boxes[0]
    diagram = Id(Ty(first.source_type))
    for item in plan.boxes:
        diagram = diagram >> Box(
            item.box_id,
            Ty(item.source_type),
            Ty(item.target_type),
        )
    return {
        "state": "ADMIT_DIAGRAM_WITNESS",
        "diagram_repr": repr(diagram),
        "plan_digest": plan.canonical_digest(),
        "backend_executed": True,
        "compiler_executed": False,
        "publication_performed": False,
    }


__all__ = [
    "DiscopyBoxPlan",
    "DiscopyProjectionPlan",
    "build_discopy_projection_plan",
    "materialize_discopy_diagram",
]
