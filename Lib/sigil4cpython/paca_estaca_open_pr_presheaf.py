"""Dependency-free coherent presheaf over a selected open-PR ledger.

The module projects source-bound review sections from ``sigilbook`` and
``sigil4cpython`` into one finite PACA Estaca / Universal Abstracta metadata
kernel.  A Pydantika merge is a deterministic join of typed metadata and
witnesses.  It is never a Git merge, identity transport, runtime deployment,
or authority transfer.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping


SCHEMA_ID = "SIGIL4CPYTHON_PACA_ESTACA_OPEN_PR_PRESHEAF_V1"
HOST_SECTION_KEY = "jbermejovega/sigil4cpython#7"

REQUIRED_FACETS = frozenset(
    {
        "PACA_ESTACA_TYPED",
        "UNIVERSAL_ABSTRAKTA_TYPED",
        "COHERENT_PRESHEAF_TYPED",
        "PYDANTIKA_TYPED",
        "SIGIL4CPYTHON_TYPED",
        "OPEN_PR_LEDGER_TYPED",
        "STRIKK_TYPED",
        "PACAPDG_TYPED",
        "UAP_TYPED",
        "SAFE_REPLAY_TYPED",
        "PACAPANDOC_TYPED",
        "PACA_FEDI_TYPED",
        "PACA_MOOG_TYPED",
        "KOKOMPI_TYPED",
    }
)


class KernelDecision(str, Enum):
    ADMIT = "ADMIT_STRUCTURAL_PRESHEAF_KERNEL"
    HOLD = "HOLD_WITH_OPEN_PR_OR_REVIEW_OBSTRUCTION"
    REJECT = "REJECT_RULEZERO_OR_LEDGER_VIOLATION"


class PullState(str, Enum):
    OPEN = "OPEN"
    CLOSED_MERGED = "CLOSED_MERGED"
    CLOSED_UNMERGED = "CLOSED_UNMERGED"


class Mergeability(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"


class SectionRole(str, Enum):
    HOST_SIGIL4CPYTHON_KERNEL = "HOST_SIGIL4CPYTHON_KERNEL"
    CPYTHON_PACA_ESTACA_PROJECTION = "CPYTHON_PACA_ESTACA_PROJECTION"
    PYDANTIKA_COHERENT_SOURCE = "PYDANTIKA_COHERENT_SOURCE"
    UNIVERSAL_ABSTRAKTA_CELLULAR_SOURCE = "UNIVERSAL_ABSTRAKTA_CELLULAR_SOURCE"
    OPEN_PR_LEDGER_SOURCE = "OPEN_PR_LEDGER_SOURCE"
    PACA_ESTACA_CANONICAL_SOURCE = "PACA_ESTACA_CANONICAL_SOURCE"
    UNIVERSAL_ABSTRACTA_MEDIA_SOURCE = "UNIVERSAL_ABSTRACTA_MEDIA_SOURCE"


class RelationKind(str, Enum):
    PROJECTS_TO = "PROJECTS_TO"
    REFINES = "REFINES"
    PROVIDES_LEDGER = "PROVIDES_LEDGER"
    PROVIDES_CELLULAR_PIPELINE = "PROVIDES_CELLULAR_PIPELINE"
    PROVIDES_CANONICAL_PACA_ESTACA = "PROVIDES_CANONICAL_PACA_ESTACA"
    SHARES_TYPED_BOUNDARY = "SHARES_TYPED_BOUNDARY"


def _canonical(payload: object) -> str:
    def default(item: object) -> object:
        if isinstance(item, Enum):
            return item.value
        raise TypeError(type(item).__name__)

    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=default,
    )


def stable_digest(payload: object) -> str:
    return sha256(_canonical(payload).encode("utf-8")).hexdigest()


def _is_hex(value: str, length: int) -> bool:
    return len(value) == length and all(character in "0123456789abcdef" for character in value)


@dataclass(frozen=True, slots=True)
class OpenPullSection:
    repository: str
    pull_request: int
    head_sha: str
    state: PullState
    mergeability: Mergeability
    draft: bool
    role: SectionRole
    facets: tuple[str, ...]
    context_id: str
    pi_digest: str
    trace_digest: str
    source_bound: bool = True
    identity_fixed: bool = True
    no_type_collapse: bool = True
    runtime_authority: bool = False
    merge_authority: bool = False

    @property
    def key(self) -> str:
        return f"{self.repository}#{self.pull_request}"

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if "/" not in self.repository:
            errors.append(f"repository_name_invalid:{self.key}")
        if self.pull_request <= 0:
            errors.append(f"pull_request_number_invalid:{self.key}")
        if not _is_hex(self.head_sha, 40):
            errors.append(f"head_sha_invalid:{self.key}")
        if not self.facets:
            errors.append(f"section_facets_missing:{self.key}")
        if len(self.facets) != len(set(self.facets)):
            errors.append(f"section_facets_duplicated:{self.key}")
        if not self.context_id:
            errors.append(f"section_context_missing:{self.key}")
        if not _is_hex(self.pi_digest, 64):
            errors.append(f"section_pi_digest_invalid:{self.key}")
        if not _is_hex(self.trace_digest, 64):
            errors.append(f"section_trace_digest_invalid:{self.key}")
        if not self.source_bound:
            errors.append(f"section_not_source_bound:{self.key}")
        if not self.identity_fixed:
            errors.append(f"section_identity_transport:{self.key}")
        if not self.no_type_collapse:
            errors.append(f"section_type_collapse:{self.key}")
        if self.runtime_authority:
            errors.append(f"section_runtime_authority_forbidden:{self.key}")
        if self.merge_authority:
            errors.append(f"section_merge_authority_forbidden:{self.key}")
        if self.state == PullState.CLOSED_MERGED and self.draft:
            errors.append(f"merged_section_cannot_be_draft:{self.key}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PresheafRestriction:
    restriction_id: str
    source_key: str
    target_key: str
    kind: RelationKind
    shared_facets: tuple[str, ...]
    witness_digest: str
    context_id: str
    commutes: bool = True
    scheduler_authority: bool = False
    content_imported: bool = False
    identity_transport: bool = False
    obstruction_ids: tuple[str, ...] = ()

    def validate(
        self,
        sections: Mapping[str, OpenPullSection],
    ) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.restriction_id:
            errors.append("restriction_id_missing")
        if self.source_key == self.target_key:
            errors.append(f"restriction_self_loop:{self.restriction_id}")
        if self.source_key not in sections or self.target_key not in sections:
            errors.append(f"restriction_unknown_endpoint:{self.restriction_id}")
            return tuple(errors)
        if not self.shared_facets:
            errors.append(f"restriction_shared_facets_missing:{self.restriction_id}")
        if len(self.shared_facets) != len(set(self.shared_facets)):
            errors.append(f"restriction_shared_facets_duplicated:{self.restriction_id}")
        source_facets = set(sections[self.source_key].facets)
        target_facets = set(sections[self.target_key].facets)
        if not set(self.shared_facets).issubset(source_facets & target_facets):
            errors.append(f"restriction_shared_facet_mismatch:{self.restriction_id}")
        if not _is_hex(self.witness_digest, 64):
            errors.append(f"restriction_witness_invalid:{self.restriction_id}")
        if not self.context_id:
            errors.append(f"restriction_context_missing:{self.restriction_id}")
        if self.scheduler_authority:
            errors.append(f"restriction_scheduler_authority_forbidden:{self.restriction_id}")
        if self.content_imported:
            errors.append(f"restriction_content_import_forbidden:{self.restriction_id}")
        if self.identity_transport:
            errors.append(f"restriction_identity_transport:{self.restriction_id}")
        if self.commutes and self.obstruction_ids:
            errors.append(f"commuting_restriction_has_obstruction:{self.restriction_id}")
        if not self.commutes and not self.obstruction_ids:
            errors.append(f"noncommuting_restriction_missing_obstruction:{self.restriction_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class TripleCoherence:
    witness_id: str
    section_keys: tuple[str, str, str]
    restriction_ids: tuple[str, str, str]
    witness_digest: str
    commutes: bool = True
    obstruction_ids: tuple[str, ...] = ()

    def validate(
        self,
        section_keys: set[str],
        restriction_ids: set[str],
    ) -> tuple[str, ...]:
        errors: list[str] = []
        if len(set(self.section_keys)) != 3:
            errors.append(f"triple_sections_not_distinct:{self.witness_id}")
        if len(set(self.restriction_ids)) != 3:
            errors.append(f"triple_restrictions_not_distinct:{self.witness_id}")
        if not set(self.section_keys).issubset(section_keys):
            errors.append(f"triple_unknown_section:{self.witness_id}")
        if not set(self.restriction_ids).issubset(restriction_ids):
            errors.append(f"triple_unknown_restriction:{self.witness_id}")
        if not _is_hex(self.witness_digest, 64):
            errors.append(f"triple_witness_invalid:{self.witness_id}")
        if self.commutes and self.obstruction_ids:
            errors.append(f"commuting_triple_has_obstruction:{self.witness_id}")
        if not self.commutes and not self.obstruction_ids:
            errors.append(f"noncommuting_triple_missing_obstruction:{self.witness_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PydantikaOpenPrLedger:
    ledger_id: str
    host_section_key: str
    sections: tuple[OpenPullSection, ...]
    restrictions: tuple[PresheafRestriction, ...]
    triples: tuple[TripleCoherence, ...]
    selected_scope: str
    full_repository_history_claimed: bool = False
    git_merge_requested: bool = False
    github_actions_invoked: bool = False
    append_only: bool = True
    human_review_required: bool = True
    global_section_claimed: bool = False
    mathematical_sheaf_proved: bool = False
    final_kapsyla: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.ledger_id:
            errors.append("ledger_id_missing")
        if not self.selected_scope:
            errors.append("ledger_selected_scope_missing")
        if self.full_repository_history_claimed:
            errors.append("full_repository_history_claim_forbidden")
        if self.git_merge_requested:
            errors.append("git_merge_request_forbidden")
        if self.github_actions_invoked:
            errors.append("github_actions_invocation_forbidden")
        if not self.append_only:
            errors.append("ledger_must_be_append_only")
        if not self.human_review_required:
            errors.append("human_review_cannot_be_disabled")
        if self.global_section_claimed:
            errors.append("global_section_claim_forbidden")
        if self.mathematical_sheaf_proved:
            errors.append("mathematical_sheaf_claim_forbidden")
        if self.final_kapsyla:
            errors.append("final_kapsyla_forbidden")

        by_key = {section.key: section for section in self.sections}
        if len(by_key) != len(self.sections):
            errors.append("duplicate_pull_section")
        if self.host_section_key not in by_key:
            errors.append("host_section_missing")
        if self.host_section_key != HOST_SECTION_KEY:
            errors.append("unexpected_host_section")

        all_pi = {section.pi_digest for section in self.sections}
        if len(all_pi) != 1:
            errors.append("pi_sector_drift")
        all_facets: set[str] = set()
        for section in self.sections:
            errors.extend(section.validate())
            all_facets.update(section.facets)
        missing_facets = sorted(REQUIRED_FACETS - all_facets)
        if missing_facets:
            errors.append("required_paca_estaca_facets_missing:" + ",".join(missing_facets))

        restriction_ids = {item.restriction_id for item in self.restrictions}
        if len(restriction_ids) != len(self.restrictions):
            errors.append("duplicate_restriction")
        for item in self.restrictions:
            errors.extend(item.validate(by_key))
        for item in self.triples:
            errors.extend(item.validate(set(by_key), restriction_ids))

        incoming_to_host = {
            item.source_key
            for item in self.restrictions
            if item.target_key == self.host_section_key and item.commutes
        }
        required_sources = {
            "jbermejovega/sigil4cpython#6",
            "jbermejovega/sigilbook#649",
            "jbermejovega/sigilbook#668",
            "jbermejovega/sigilbook#621",
            "jbermejovega/sigilbook#622",
            "jbermejovega/sigilbook#576",
        }
        missing_sources = sorted(required_sources - incoming_to_host)
        if missing_sources:
            errors.append("host_source_restrictions_missing:" + ",".join(missing_sources))
        return tuple(errors)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["schema_id"] = SCHEMA_ID
        payload["required_facets"] = sorted(REQUIRED_FACETS)
        payload["ledger_digest"] = stable_digest(payload)
        return payload


def _facet_digest(label: str) -> str:
    return stable_digest({"label": label, "schema_id": SCHEMA_ID})


def _section(
    repository: str,
    pull_request: int,
    head_sha: str,
    *,
    mergeability: Mergeability,
    draft: bool,
    role: SectionRole,
    facets: tuple[str, ...],
    pi_digest: str,
) -> OpenPullSection:
    key = f"{repository}#{pull_request}"
    return OpenPullSection(
        repository=repository,
        pull_request=pull_request,
        head_sha=head_sha,
        state=PullState.OPEN,
        mergeability=mergeability,
        draft=draft,
        role=role,
        facets=facets,
        context_id=f"context:{key}",
        pi_digest=pi_digest,
        trace_digest=_facet_digest(f"trace:{key}:{head_sha}"),
    )


def _restriction(
    restriction_id: str,
    source_key: str,
    target_key: str,
    kind: RelationKind,
    shared_facets: tuple[str, ...],
) -> PresheafRestriction:
    return PresheafRestriction(
        restriction_id=restriction_id,
        source_key=source_key,
        target_key=target_key,
        kind=kind,
        shared_facets=shared_facets,
        witness_digest=_facet_digest(f"restriction:{restriction_id}"),
        context_id="TOTAL_PACA_ESTACA_UNIVERSAL_ABSTRAKTA_CONTEXT",
    )


def build_reference_open_pr_presheaf() -> PydantikaOpenPrLedger:
    """Build the verified selected-source ledger for the active CPython kernel."""

    pi_digest = _facet_digest("PI:PACA_ESTACA:UNIVERSAL_ABSTRAKTA")
    sections = (
        _section(
            "jbermejovega/sigil4cpython",
            7,
            "54efbe9fd41c58aae68401d99b40ec48c2d3084e",
            mergeability=Mergeability.TRUE,
            draft=False,
            role=SectionRole.HOST_SIGIL4CPYTHON_KERNEL,
            facets=(
                "SIGIL4CPYTHON_TYPED",
                "COHERENT_PRESHEAF_TYPED",
                "PYDANTIKA_TYPED",
                "PACA_ESTACA_TYPED",
                "UNIVERSAL_ABSTRAKTA_TYPED",
                "OPEN_PR_LEDGER_TYPED",
                "STRIKK_TYPED",
                "SAFE_REPLAY_TYPED",
            ),
            pi_digest=pi_digest,
        ),
        _section(
            "jbermejovega/sigil4cpython",
            6,
            "f46124461838d94fc5835b340cf08aac8233e7dc",
            mergeability=Mergeability.TRUE,
            draft=True,
            role=SectionRole.CPYTHON_PACA_ESTACA_PROJECTION,
            facets=(
                "SIGIL4CPYTHON_TYPED",
                "COHERENT_PRESHEAF_TYPED",
                "PYDANTIKA_TYPED",
                "PACA_ESTACA_TYPED",
                "UNIVERSAL_ABSTRAKTA_TYPED",
                "SAFE_REPLAY_TYPED",
            ),
            pi_digest=pi_digest,
        ),
        _section(
            "jbermejovega/sigilbook",
            649,
            "040117f2620b517182b7eb7d551d27b05ac0216d",
            mergeability=Mergeability.TRUE,
            draft=True,
            role=SectionRole.PYDANTIKA_COHERENT_SOURCE,
            facets=(
                "COHERENT_PRESHEAF_TYPED",
                "PYDANTIKA_TYPED",
                "PACA_ESTACA_TYPED",
                "UNIVERSAL_ABSTRAKTA_TYPED",
                "PACAPDG_TYPED",
                "UAP_TYPED",
                "SAFE_REPLAY_TYPED",
            ),
            pi_digest=pi_digest,
        ),
        _section(
            "jbermejovega/sigilbook",
            668,
            "7ed6a43b02309c929909b4447266c96d0d92e9c9",
            mergeability=Mergeability.TRUE,
            draft=True,
            role=SectionRole.UNIVERSAL_ABSTRAKTA_CELLULAR_SOURCE,
            facets=(
                "UNIVERSAL_ABSTRAKTA_TYPED",
                "PYDANTIKA_TYPED",
                "KOKOMPI_TYPED",
                "STRIKK_TYPED",
                "PACAPDG_TYPED",
                "UAP_TYPED",
                "SAFE_REPLAY_TYPED",
            ),
            pi_digest=pi_digest,
        ),
        _section(
            "jbermejovega/sigilbook",
            621,
            "8c9db5c8116ceeca56aa5fd92d52b8fbbe86047e",
            mergeability=Mergeability.FALSE,
            draft=True,
            role=SectionRole.OPEN_PR_LEDGER_SOURCE,
            facets=(
                "OPEN_PR_LEDGER_TYPED",
                "PYDANTIKA_TYPED",
                "COHERENT_PRESHEAF_TYPED",
                "PACAPDG_TYPED",
                "UAP_TYPED",
                "SAFE_REPLAY_TYPED",
            ),
            pi_digest=pi_digest,
        ),
        _section(
            "jbermejovega/sigilbook",
            622,
            "ec4235cde55ad7130a34881d0c998baf8b3d1a14",
            mergeability=Mergeability.TRUE,
            draft=False,
            role=SectionRole.PACA_ESTACA_CANONICAL_SOURCE,
            facets=(
                "PACA_ESTACA_TYPED",
                "PYDANTIKA_TYPED",
                "KOKOMPI_TYPED",
                "STRIKK_TYPED",
                "PACAPDG_TYPED",
                "UAP_TYPED",
                "SAFE_REPLAY_TYPED",
            ),
            pi_digest=pi_digest,
        ),
        _section(
            "jbermejovega/sigilbook",
            576,
            "8ab7fcbdade65cb2ce801eb21c5efc647822ce31",
            mergeability=Mergeability.TRUE,
            draft=True,
            role=SectionRole.UNIVERSAL_ABSTRACTA_MEDIA_SOURCE,
            facets=(
                "UNIVERSAL_ABSTRAKTA_TYPED",
                "COHERENT_PRESHEAF_TYPED",
                "PYDANTIKA_TYPED",
                "PACAPANDOC_TYPED",
                "PACA_FEDI_TYPED",
                "PACA_MOOG_TYPED",
                "PACAPDG_TYPED",
                "UAP_TYPED",
                "SAFE_REPLAY_TYPED",
            ),
            pi_digest=pi_digest,
        ),
    )

    restrictions = (
        _restriction(
            "r:649:6",
            "jbermejovega/sigilbook#649",
            "jbermejovega/sigil4cpython#6",
            RelationKind.PROJECTS_TO,
            ("COHERENT_PRESHEAF_TYPED", "PYDANTIKA_TYPED", "PACA_ESTACA_TYPED"),
        ),
        _restriction(
            "r:6:7",
            "jbermejovega/sigil4cpython#6",
            HOST_SECTION_KEY,
            RelationKind.REFINES,
            ("SIGIL4CPYTHON_TYPED", "COHERENT_PRESHEAF_TYPED", "PACA_ESTACA_TYPED"),
        ),
        _restriction(
            "r:649:7",
            "jbermejovega/sigilbook#649",
            HOST_SECTION_KEY,
            RelationKind.PROJECTS_TO,
            ("COHERENT_PRESHEAF_TYPED", "PYDANTIKA_TYPED", "PACA_ESTACA_TYPED"),
        ),
        _restriction(
            "r:668:7",
            "jbermejovega/sigilbook#668",
            HOST_SECTION_KEY,
            RelationKind.PROVIDES_CELLULAR_PIPELINE,
            ("UNIVERSAL_ABSTRAKTA_TYPED", "PYDANTIKA_TYPED", "STRIKK_TYPED"),
        ),
        _restriction(
            "r:621:7",
            "jbermejovega/sigilbook#621",
            HOST_SECTION_KEY,
            RelationKind.PROVIDES_LEDGER,
            ("OPEN_PR_LEDGER_TYPED", "PYDANTIKA_TYPED", "COHERENT_PRESHEAF_TYPED"),
        ),
        _restriction(
            "r:622:7",
            "jbermejovega/sigilbook#622",
            HOST_SECTION_KEY,
            RelationKind.PROVIDES_CANONICAL_PACA_ESTACA,
            ("PACA_ESTACA_TYPED", "PYDANTIKA_TYPED", "STRIKK_TYPED"),
        ),
        _restriction(
            "r:576:7",
            "jbermejovega/sigilbook#576",
            HOST_SECTION_KEY,
            RelationKind.PROJECTS_TO,
            ("UNIVERSAL_ABSTRAKTA_TYPED", "COHERENT_PRESHEAF_TYPED", "PYDANTIKA_TYPED"),
        ),
        _restriction(
            "r:576:668",
            "jbermejovega/sigilbook#576",
            "jbermejovega/sigilbook#668",
            RelationKind.SHARES_TYPED_BOUNDARY,
            ("UNIVERSAL_ABSTRAKTA_TYPED", "PYDANTIKA_TYPED", "PACAPDG_TYPED", "UAP_TYPED"),
        ),
        _restriction(
            "r:668:576",
            "jbermejovega/sigilbook#668",
            "jbermejovega/sigilbook#576",
            RelationKind.SHARES_TYPED_BOUNDARY,
            ("UNIVERSAL_ABSTRAKTA_TYPED", "PYDANTIKA_TYPED", "PACAPDG_TYPED", "UAP_TYPED"),
        ),
    )
    triples = (
        TripleCoherence(
            "t:649:6:7",
            (
                "jbermejovega/sigilbook#649",
                "jbermejovega/sigil4cpython#6",
                HOST_SECTION_KEY,
            ),
            ("r:649:6", "r:6:7", "r:649:7"),
            _facet_digest("triple:649:6:7"),
        ),
        TripleCoherence(
            "t:576:668:7",
            (
                "jbermejovega/sigilbook#576",
                "jbermejovega/sigilbook#668",
                HOST_SECTION_KEY,
            ),
            ("r:576:668", "r:668:7", "r:576:7"),
            _facet_digest("triple:576:668:7"),
        ),
    )
    return PydantikaOpenPrLedger(
        ledger_id=SCHEMA_ID,
        host_section_key=HOST_SECTION_KEY,
        sections=sections,
        restrictions=restrictions,
        triples=triples,
        selected_scope=(
            "source-bound open PRs defining SIGIL4CPython coherent presheaf, "
            "PACA Estaca, Universal Abstrakta, and Pydantika ledger projection"
        ),
    )


def compile_reference_open_pr_presheaf(
    ledger: PydantikaOpenPrLedger,
) -> dict[str, object]:
    errors = ledger.validate()
    fatal_markers = (
        "identity_transport",
        "type_collapse",
        "runtime_authority_forbidden",
        "merge_authority_forbidden",
        "git_merge_request_forbidden",
        "github_actions_invocation_forbidden",
        "pi_sector_drift",
        "shared_facet_mismatch",
        "scheduler_authority_forbidden",
        "content_import_forbidden",
    )
    if any(any(marker in error for marker in fatal_markers) for error in errors):
        decision = KernelDecision.REJECT
    elif errors:
        decision = KernelDecision.HOLD
    elif any(
        section.state == PullState.OPEN
        or section.draft
        or section.mergeability != Mergeability.TRUE
        for section in ledger.sections
    ):
        decision = KernelDecision.HOLD
    else:
        decision = KernelDecision.ADMIT

    payload = ledger.to_dict()
    payload.update(
        {
            "decision": decision.value,
            "obstruction_ledger": list(errors),
            "selected_open_pr_count": sum(
                section.state == PullState.OPEN for section in ledger.sections
            ),
            "git_merge_executed": False,
            "github_actions_invoked": False,
            "runtime_executed": False,
            "interpreter_semantics_changed": False,
            "native_extension_loaded": False,
            "global_section_claimed": False,
            "final_kapsyla": False,
        }
    )
    payload["compile_digest"] = stable_digest(payload)
    return payload


__all__ = [
    "HOST_SECTION_KEY",
    "KernelDecision",
    "Mergeability",
    "OpenPullSection",
    "PullState",
    "PydantikaOpenPrLedger",
    "RelationKind",
    "REQUIRED_FACETS",
    "SCHEMA_ID",
    "SectionRole",
    "PresheafRestriction",
    "TripleCoherence",
    "build_reference_open_pr_presheaf",
    "compile_reference_open_pr_presheaf",
    "stable_digest",
]
