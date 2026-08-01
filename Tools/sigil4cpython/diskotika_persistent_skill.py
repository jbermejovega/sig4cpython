"""DisCoPy validation for the persistent PACAIoGames skill compiler."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Mapping

from discopy.monoidal import Box, Ty


EXPECTED_DOMAIN = "SIGIL_AST_V1"
EXPECTED_CODOMAIN = "SIGIL_SEMANTICAL_KERNEL_V1"


@dataclass(frozen=True, slots=True)
class DiskotikaPersistentSkillCertificate:
    diagram_id: str
    domain: str
    codomain: str
    box_count: int
    diagram_sha256: str
    sequential_composition_verified: bool = True
    symmetry_inferred: bool = False
    trace_erased: bool = False
    runtime_executed: bool = False


def _stable_digest(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def validate_diskotika_persistent_skill(
    payload: dict[str, object],
) -> DiskotikaPersistentSkillCertificate:
    """Build and check the declared AST-to-semantics DisCoPy chain."""

    raw_diagram = payload.get("diskotika")
    if not isinstance(raw_diagram, dict):
        raise ValueError("diskotika_payload_missing")
    object_names = raw_diagram.get("object_types")
    morphisms = raw_diagram.get("morphisms")
    if not isinstance(object_names, (list, tuple)) or not object_names:
        raise ValueError("diskotika_objects_missing")
    if not isinstance(morphisms, (list, tuple)) or not morphisms:
        raise ValueError("diskotika_morphisms_missing")

    typed_objects = {str(name): Ty(str(name)) for name in object_names}
    diagram = None
    relation_trace: list[dict[str, str]] = []
    for raw_morphism in morphisms:
        if not isinstance(raw_morphism, dict):
            raise ValueError("diskotika_morphism_payload_invalid")
        morphism_id = str(raw_morphism.get("morphism_id", ""))
        source_name = str(raw_morphism.get("source_type", ""))
        target_name = str(raw_morphism.get("target_type", ""))
        relation_type = str(raw_morphism.get("relation_type", ""))
        if source_name not in typed_objects or target_name not in typed_objects:
            raise ValueError(f"diskotika_unknown_typed_object:{morphism_id}")
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
        raise ValueError("diskotika_diagram_empty")
    expected_domain = typed_objects.get(EXPECTED_DOMAIN)
    expected_codomain = typed_objects.get(EXPECTED_CODOMAIN)
    if diagram.dom != expected_domain:
        raise ValueError("diskotika_domain_mismatch")
    if diagram.cod != expected_codomain:
        raise ValueError("diskotika_codomain_mismatch")

    digest_payload = {
        "diagram_id": str(raw_diagram.get("diagram_id", "")),
        "domain": EXPECTED_DOMAIN,
        "codomain": EXPECTED_CODOMAIN,
        "relations": relation_trace,
    }
    return DiskotikaPersistentSkillCertificate(
        diagram_id=str(raw_diagram.get("diagram_id", "")),
        domain=EXPECTED_DOMAIN,
        codomain=EXPECTED_CODOMAIN,
        box_count=len(diagram.boxes),
        diagram_sha256=_stable_digest(digest_payload),
    )


def certificate_to_dict(
    certificate: DiskotikaPersistentSkillCertificate,
) -> dict[str, object]:
    return asdict(certificate)


__all__ = [
    "DiskotikaPersistentSkillCertificate",
    "certificate_to_dict",
    "validate_diskotika_persistent_skill",
]
