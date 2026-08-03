"""DisCoPy validator for the PACAPDG/UAP persistent skill route."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Mapping

from discopy.monoidal import Box, Ty


EXPECTED_DOMAIN = "PERSISTENT_PACA_SKILL_PACKET"
EXPECTED_CODOMAIN = "UAP_ADMISSION_WITNESS"
EXPECTED_BOX_COUNT = 6


@dataclass(frozen=True, slots=True)
class DiskotikaPacapdgUapCertificate:
    route_id: str
    domain: str
    codomain: str
    box_count: int
    diagram_sha256: str
    pacapdg_typed: bool = True
    uap_typed: bool = True
    sequential_composition_verified: bool = True
    symmetry_inferred: bool = False
    trace_erased: bool = False
    identity_transported: bool = False
    runtime_executed: bool = False


def _stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def validate_diskotika_pacapdg_uap(
    payload: Mapping[str, object],
) -> DiskotikaPacapdgUapCertificate:
    """Build and validate the declared PACAPDG-to-UAP composition chain."""

    raw_route = payload.get("diskotika_route")
    if not isinstance(raw_route, (list, tuple)) or not raw_route:
        raise ValueError("diskotika_pacapdg_uap_route_missing")

    object_names: set[str] = set()
    for raw_morphism in raw_route:
        if not isinstance(raw_morphism, Mapping):
            raise ValueError("diskotika_pacapdg_uap_morphism_invalid")
        object_names.add(str(raw_morphism.get("source_type", "")))
        object_names.add(str(raw_morphism.get("target_type", "")))
    if "" in object_names:
        raise ValueError("diskotika_pacapdg_uap_object_missing")

    typed_objects = {name: Ty(name) for name in object_names}
    diagram = None
    relation_trace: list[dict[str, str]] = []
    for raw_morphism in raw_route:
        morphism_id = str(raw_morphism.get("morphism_id", ""))
        source_name = str(raw_morphism.get("source_type", ""))
        target_name = str(raw_morphism.get("target_type", ""))
        relation_type = str(raw_morphism.get("relation_type", ""))
        if not morphism_id or not relation_type:
            raise ValueError("diskotika_pacapdg_uap_relation_missing")
        box = Box(
            morphism_id,
            typed_objects[source_name],
            typed_objects[target_name],
            data={"relation_type": relation_type},
        )
        diagram = box if diagram is None else diagram >> box
        relation_trace.append(
            {
                "morphism_id": morphism_id,
                "source_type": source_name,
                "target_type": target_name,
                "relation_type": relation_type,
            }
        )

    if diagram is None:
        raise ValueError("diskotika_pacapdg_uap_diagram_empty")
    if diagram.dom != typed_objects.get(EXPECTED_DOMAIN):
        raise ValueError("diskotika_pacapdg_uap_domain_mismatch")
    if diagram.cod != typed_objects.get(EXPECTED_CODOMAIN):
        raise ValueError("diskotika_pacapdg_uap_codomain_mismatch")
    if len(diagram.boxes) != EXPECTED_BOX_COUNT:
        raise ValueError("diskotika_pacapdg_uap_box_count_mismatch")

    digest_payload = {
        "route_id": "diskotika:pacapdg-uap-persistent-skill",
        "domain": EXPECTED_DOMAIN,
        "codomain": EXPECTED_CODOMAIN,
        "relations": relation_trace,
    }
    return DiskotikaPacapdgUapCertificate(
        route_id="diskotika:pacapdg-uap-persistent-skill",
        domain=EXPECTED_DOMAIN,
        codomain=EXPECTED_CODOMAIN,
        box_count=len(diagram.boxes),
        diagram_sha256=_stable_digest(digest_payload),
    )


def certificate_to_dict(
    certificate: DiskotikaPacapdgUapCertificate,
) -> dict[str, object]:
    return asdict(certificate)


__all__ = [
    "DiskotikaPacapdgUapCertificate",
    "certificate_to_dict",
    "validate_diskotika_pacapdg_uap",
]
