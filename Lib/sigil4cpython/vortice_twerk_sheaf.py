"""Coherent sheaf projection for the Vórtice Taller Twerk source release.

Authored work: Jara Juana Bermejo Vega / JJBV.

The projection carries metadata and proof obligations from sigilbook into the
public experimental mirror. It does not alter CPython interpreter semantics,
copy Godot code, start a runtime, or write any upstream repository.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
from hashlib import sha256
import json

SCHEMA_ID = "SIGIL4CPYTHON_VORTICE_TWERK_COHERENT_SHEAF_V1"
AUTHOR = "Jara Juana Bermejo Vega / JJBV"
SOURCE_REPOSITORY = "jbermejovega/sigilbook"
SOURCE_BRANCH = "agent/sigilitas-vortice-taller-twerk-canonical-release-v1"
SOURCE_SHA = "f376c1fbbd66cb0abe120aae9afbe51b5560d4dd"


class ProjectionVerdict(str, Enum):
    ADMIT = "ADMIT_COHERENT_PROJECTION"
    HOLD = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT_INVALID_PROJECTION"


@dataclass(frozen=True, slots=True)
class SheafSection:
    section_id: str
    context: str
    payload_type: str
    provenance: tuple[str, ...]
    replay_trace: tuple[str, ...]
    identity: str

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not all((self.section_id, self.context, self.payload_type, self.identity)):
            errors.append("incomplete_section")
        if not self.provenance:
            errors.append(f"provenance_missing:{self.section_id}")
        if not self.replay_trace:
            errors.append(f"replay_missing:{self.section_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class RestrictionWitness:
    witness_id: str
    source_section: str
    target_section: str
    preserves_identity: bool = True
    preserves_plural_type: bool = True
    preserves_trace: bool = True
    identity_transport: bool = False

    def validate(self, known: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if self.source_section not in known or self.target_section not in known:
            errors.append(f"unknown_restriction_endpoint:{self.witness_id}")
        if self.source_section == self.target_section:
            errors.append(f"self_restriction_not_projection:{self.witness_id}")
        if not all((self.preserves_identity, self.preserves_plural_type, self.preserves_trace)):
            errors.append(f"restriction_invariant_failure:{self.witness_id}")
        if self.identity_transport:
            errors.append(f"restriction_identity_transport:{self.witness_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class CoherentProjection:
    schema_id: str
    author_owner: str
    source_repository: str
    source_branch: str
    source_sha: str
    target_repository: str
    sections: tuple[SheafSection, ...]
    restrictions: tuple[RestrictionWitness, ...]
    official_godot_engine: str
    godot_fork_reference: str
    godot_docs_reference: str
    portal_references: tuple[str, ...]
    source_bound: bool = True
    review_required: bool = True
    dependency_free: bool = True
    interpreter_semantics_changed: bool = False
    runtime_executed: bool = False
    upstream_write: bool = False
    pi_fixed: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.schema_id != SCHEMA_ID or self.author_owner != AUTHOR:
            errors.append("schema_or_author_mismatch")
        if self.source_repository != SOURCE_REPOSITORY:
            errors.append("unexpected_source_repository")
        if self.source_branch != SOURCE_BRANCH or self.source_sha != SOURCE_SHA:
            errors.append("source_pin_mismatch")
        if self.target_repository != "jbermejovega/sigil4cpython":
            errors.append("unexpected_target_repository")
        ids = [section.section_id for section in self.sections]
        if len(ids) != len(set(ids)):
            errors.append("section_ids_not_unique")
        identities = [section.identity for section in self.sections]
        if len(identities) != len(set(identities)):
            errors.append("section_identity_collapse")
        for section in self.sections:
            errors.extend(section.validate())
        known = set(ids)
        for restriction in self.restrictions:
            errors.extend(restriction.validate(known))
        if not all((self.source_bound, self.review_required, self.dependency_free, self.pi_fixed)):
            errors.append("coherent_projection_boundary_missing")
        if any((self.interpreter_semantics_changed, self.runtime_executed, self.upstream_write)):
            errors.append("forbidden_projection_effect")
        return tuple(errors)

    def digest(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return sha256(payload.encode()).hexdigest()


def build_projection() -> CoherentProjection:
    sections = (
        SheafSection("PACA_BASE", "SIGILITAS/VORTICE", "TALLER_TWERK", (SOURCE_SHA,), ("base", "typed"), "paca-base-object"),
        SheafSection("PACAIOGAMES", "SAFE_PLAY", "GAME_SURFACES", (SOURCE_SHA,), ("validate", "replay"), "pacaiogames-surface"),
        SheafSection("QUASARPI", "LOCALIZATION", "LOCALIZED_SUBMODEL", (SOURCE_SHA,), ("localize", "witness"), "quasarpi-localizer"),
        SheafSection("JARRASKHOREOPI", "CHOREOGRAPHY", "MOVEMENT_FIELD", (SOURCE_SHA,), ("compose", "pause", "return"), "jarraskhoreopi-engine"),
        SheafSection("QQUAPP_PORTAL", "CELLULAR_INTERFACE", "TWISTED_INJECTION", (SOURCE_SHA,), ("portal", "magic-jarras-twist"), "qquapp-portal"),
        SheafSection("SIGIL4GODOT", "SCENE_PLAN", "INERT_RENDER_WITNESS", (SOURCE_SHA,), ("compile", "preview"), "sigil4godot-plan"),
    )
    restrictions = tuple(
        RestrictionWitness(f"r{index}", sections[index].section_id, sections[index + 1].section_id)
        for index in range(len(sections) - 1)
    )
    return CoherentProjection(
        SCHEMA_ID,
        AUTHOR,
        SOURCE_REPOSITORY,
        SOURCE_BRANCH,
        SOURCE_SHA,
        "jbermejovega/sigil4cpython",
        sections,
        restrictions,
        "godotengine/godot@4e8c061c9b4a778102a085d9d10f64b3c6be0f87",
        "Zylann/godot@1ccfa7be094e11e1efe9a544c391fb0ce75b97e2",
        "godotengine/godot-docs@eb00dcad2c4628361af6de7e1356676ba006d5f4",
        (
            "brodcoli/Godot-Portal@1b4c05550e80f40bbe7a2f4356a000ab10df6e26",
            "io12/godot-portal-demo@0768670710a7c0e472a6ea7a225183c2edb9caf9",
            "Jhon-Crow/godot-topdown-MVP#732@220a106e2037936d45c59025f9f010d2d99ac006",
        ),
    )


def compile_projection(projection: CoherentProjection | None = None) -> dict[str, object]:
    model = projection or build_projection()
    errors = model.validate()
    return {
        "schema_id": model.schema_id,
        "author_owner": model.author_owner,
        "verdict": (ProjectionVerdict.ADMIT if not errors else ProjectionVerdict.REJECT).value,
        "errors": errors,
        "projection_sha256": model.digest(),
        "runtime_executed": False,
        "interpreter_semantics_changed": False,
    }


def with_identity_transport(projection: CoherentProjection) -> CoherentProjection:
    first = replace(projection.restrictions[0], identity_transport=True)
    return replace(projection, restrictions=(first, *projection.restrictions[1:]))


__all__ = [
    "AUTHOR", "SCHEMA_ID", "SOURCE_BRANCH", "SOURCE_REPOSITORY", "SOURCE_SHA",
    "CoherentProjection", "ProjectionVerdict", "RestrictionWitness", "SheafSection",
    "build_projection", "compile_projection", "with_identity_transport",
]
