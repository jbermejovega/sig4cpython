"""Strict Pydantika mirror for the PACA Estaca open-PR presheaf."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Annotated, Literal, get_args, get_origin, get_type_hints

from pydantic import BaseModel, ConfigDict, Field, model_validator

from sigil4cpython.paca_estaca_open_pr_presheaf import (
    REQUIRED_FACETS,
    SCHEMA_ID,
    PydantikaOpenPrLedger,
    build_reference_open_pr_presheaf,
)


Token = Annotated[str, Field(min_length=1, max_length=256)]
HeadSHA = Annotated[str, Field(pattern=r"^[0-9a-f]{40}$")]
Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
FacetFamily = Annotated[tuple[Token, ...], Field(min_length=1, max_length=64)]


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        allow_inf_nan=False,
        str_strip_whitespace=True,
    )


class PydantikaPullSection(StrictModel):
    repository: Token
    pull_request: int = Field(gt=0)
    head_sha: HeadSHA
    state: Literal["OPEN", "CLOSED_MERGED", "CLOSED_UNMERGED"]
    mergeability: Literal["TRUE", "FALSE", "UNKNOWN"]
    draft: bool
    role: Token
    facets: FacetFamily
    context_id: Token
    pi_digest: Digest
    trace_digest: Digest
    source_bound: Literal[True] = True
    identity_fixed: Literal[True] = True
    no_type_collapse: Literal[True] = True
    runtime_authority: Literal[False] = False
    merge_authority: Literal[False] = False

    @property
    def key(self) -> str:
        return f"{self.repository}#{self.pull_request}"

    @model_validator(mode="after")
    def facets_are_unique(self) -> "PydantikaPullSection":
        if len(self.facets) != len(set(self.facets)):
            raise ValueError("duplicate_plural_facet")
        return self


class PydantikaRestriction(StrictModel):
    restriction_id: Token
    source_key: Token
    target_key: Token
    kind: Token
    shared_facets: FacetFamily
    witness_digest: Digest
    context_id: Token
    commutes: bool
    scheduler_authority: Literal[False] = False
    content_imported: Literal[False] = False
    identity_transport: Literal[False] = False
    obstruction_ids: tuple[Token, ...] = ()


class PydantikaTriple(StrictModel):
    witness_id: Token
    section_keys: tuple[Token, Token, Token]
    restriction_ids: tuple[Token, Token, Token]
    witness_digest: Digest
    commutes: bool
    obstruction_ids: tuple[Token, ...] = ()


class PydantikaMergedOpenPrPresheaf(StrictModel):
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    ledger_id: Literal[SCHEMA_ID] = SCHEMA_ID
    host_section_key: Literal["jbermejovega/sigil4cpython#7"]
    sections: tuple[PydantikaPullSection, ...] = Field(min_length=7, max_length=64)
    restrictions: tuple[PydantikaRestriction, ...] = Field(min_length=6, max_length=128)
    triples: tuple[PydantikaTriple, ...] = Field(min_length=2, max_length=64)
    selected_scope: Token
    full_repository_history_claimed: Literal[False] = False
    git_merge_requested: Literal[False] = False
    github_actions_invoked: Literal[False] = False
    append_only: Literal[True] = True
    human_review_required: Literal[True] = True
    global_section_claimed: Literal[False] = False
    mathematical_sheaf_proved: Literal[False] = False
    final_kapsyla: Literal[False] = False

    @model_validator(mode="after")
    def validate_presheaf(self) -> "PydantikaMergedOpenPrPresheaf":
        section_map = {section.key: section for section in self.sections}
        if len(section_map) != len(self.sections):
            raise ValueError("duplicate_pull_section")
        if self.host_section_key not in section_map:
            raise ValueError("host_section_missing")
        if len({section.pi_digest for section in self.sections}) != 1:
            raise ValueError("pi_sector_drift")
        facets = {facet for section in self.sections for facet in section.facets}
        missing = sorted(REQUIRED_FACETS - facets)
        if missing:
            raise ValueError("required_facets_missing:" + ",".join(missing))

        restriction_map = {item.restriction_id: item for item in self.restrictions}
        if len(restriction_map) != len(self.restrictions):
            raise ValueError("duplicate_restriction")
        for item in self.restrictions:
            if item.source_key not in section_map or item.target_key not in section_map:
                raise ValueError("restriction_unknown_endpoint")
            shared = set(section_map[item.source_key].facets) & set(
                section_map[item.target_key].facets
            )
            if not set(item.shared_facets).issubset(shared):
                raise ValueError("restriction_shared_facet_mismatch")
            if item.commutes and item.obstruction_ids:
                raise ValueError("commuting_restriction_has_obstruction")
            if not item.commutes and not item.obstruction_ids:
                raise ValueError("noncommuting_restriction_missing_obstruction")

        for triple in self.triples:
            if len(set(triple.section_keys)) != 3:
                raise ValueError("triple_sections_not_distinct")
            if not set(triple.section_keys).issubset(section_map):
                raise ValueError("triple_unknown_section")
            if not set(triple.restriction_ids).issubset(restriction_map):
                raise ValueError("triple_unknown_restriction")
        return self

    def certificate(self) -> str:
        encoded = json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


def from_runtime(ledger: PydantikaOpenPrLedger) -> PydantikaMergedOpenPrPresheaf:
    payload = ledger.to_dict()
    payload.pop("required_facets", None)
    payload.pop("ledger_digest", None)
    return PydantikaMergedOpenPrPresheaf.model_validate(payload)


def build_pydantika_reference() -> PydantikaMergedOpenPrPresheaf:
    return from_runtime(build_reference_open_pr_presheaf())


def annotated_metadata_present() -> bool:
    hints = get_type_hints(PydantikaPullSection, include_extras=True)
    required = ("repository", "head_sha", "facets", "pi_digest", "trace_digest")
    return all(
        get_origin(hints[name]) is Annotated and bool(get_args(hints[name])[1:])
        for name in required
    )


__all__ = [
    "Digest",
    "FacetFamily",
    "HeadSHA",
    "PydantikaMergedOpenPrPresheaf",
    "PydantikaPullSection",
    "PydantikaRestriction",
    "PydantikaTriple",
    "Token",
    "annotated_metadata_present",
    "build_pydantika_reference",
    "from_runtime",
]
