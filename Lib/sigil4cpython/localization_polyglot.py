"""Polyglot localization contracts for SIGIL4CPython.

This module models a source-bound SIGIL localization algorithm based on
aperiodic cellular tilings and plural typed dictionaries.  It records guarded
bindings for sigil4py, sigil4godot, sigil4quasarpi, PACA Antorcha/PyTorch,
Macaulay2, OpenMPI, and PACA Alpaca semantic layers without importing those
systems, executing kernels, launching MPI, or changing CPython semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping


SCHEMA_ID = "SIGIL4CPYTHON_POLYGLOT_LOCALIZATION_PIPELINES_V1"
SIGIL_GRAPHICAL_CALCULUS = "SIGIL_GRAPHICAL_CALCULUS"
QUANTUM_QUIMBO_CONTEXT = "QUANTUM_QUIMBO_KERNEL_NOT_LINUX"
LINTER_CANON = "STRIKK_PLURAL_TYPED_SIGIL_LINTER_GLOBAL_FIELD_ENDOFUNCTOR_LIBRARY_V1"

SOURCE_URLS = (
    "https://errorcorrectionzoo.org/list/list_asymmetric",
    "https://errorcorrectionzoo.org/list/dynamic_gen",
    "https://errorcorrectionzoo.org/c/floquet",
    "https://arxiv.org/abs/1708.02130",
    "https://arxiv.org/pdf/1708.02130",
    "https://arxiv.org/abs/1708.07359",
    "https://arxiv.org/pdf/1708.07359",
    "https://github.com/Xilinx/SLASH",
    "https://github.com/Xilinx/AVED",
    "https://github.com/zama-ai/hpu_fpga",
    "https://github.com/clash-lang/clash-compiler",
    "https://github.com/clash-lang/clash-cores",
    "https://github.com/stanford-ppl/spatial",
    "https://github.com/jwiegley/categorical",
    "https://github.com/mattecapu/categorical-systems-theory",
    "https://github.com/ACT4E/ACT4E",
    "https://github.com/madnight/awesome-category-theory",
    "https://github.com/os-fpga/open-source-fpga-resource",
    "https://github.com/jbermejovega/sigil4cpython",
)


class LocalizationState(str, Enum):
    ADMIT = "ADMIT"
    HOLD_WITH_OBSTRUCTION = "HOLD_WITH_OBSTRUCTION"
    REJECT = "REJECT"


class PolyglotSurface(str, Enum):
    SIGIL4PY = "SIGIL4PY"
    SIGIL4GODOT = "SIGIL4GODOT"
    SIGIL4QUASARPI = "SIGIL4QUASARPI"
    PACA_ALPACA = "PACA_ALPACA"
    PACA_ANTORCHA_PYTORCH = "PACA_ANTORCHA_PYTORCH"
    MACAULAY2 = "MACAULAY2"
    OPEN_MPI = "OPEN_MPI"
    PACAIOGAMES = "PACAIOGAMES"
    QUANTUM_QUIMBO = "QUANTUM_QUIMBO"
    SIGIL4CPYTHON = "SIGIL4CPYTHON"


class BindingAuthority(str, Enum):
    VIRTUAL_ONLY = "VIRTUAL_ONLY"
    TOOLING_ONLY = "TOOLING_ONLY"
    KRONE_ADMIN_REQUIRED = "KRONE_ADMIN_REQUIRED"
    SOURCE_DICTIONARY = "SOURCE_DICTIONARY"


class AperiodicTileKind(str, Enum):
    PENROSE = "PENROSE"
    WANG = "WANG"
    AMMANN_BEENKER = "AMMANN_BEENKER"
    DYNAMIC_AUTOMORPHISM = "DYNAMIC_AUTOMORPHISM"
    FLOQUET_MEASUREMENT = "FLOQUET_MEASUREMENT"
    HYPERGRAPH_CELL = "HYPERGRAPH_CELL"


class SourceVocabularyKind(str, Enum):
    ERROR_CORRECTION_ZOO_ASYMMETRIC = "ERROR_CORRECTION_ZOO_ASYMMETRIC"
    ERROR_CORRECTION_ZOO_DYNAMIC = "ERROR_CORRECTION_ZOO_DYNAMIC"
    ERROR_CORRECTION_ZOO_FLOQUET = "ERROR_CORRECTION_ZOO_FLOQUET"
    MAHADEV_QFHE_LWE = "MAHADEV_QFHE_LWE"
    VERIFIER_ON_A_LEASH = "VERIFIER_ON_A_LEASH"
    FPGA_OPEN_SOURCE_STACK = "FPGA_OPEN_SOURCE_STACK"
    SIGIL_LINTER_ENDOFUNCTOR = "SIGIL_LINTER_ENDOFUNCTOR"


@dataclass(frozen=True, slots=True)
class LexicalNormalization:
    input_term: str
    canonical_term: str
    preserve_input_trace: bool = True
    silent_erasure: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.input_term or not self.canonical_term:
            errors.append("lexical_normalization_term_missing")
        if not self.preserve_input_trace:
            errors.append(f"lexical_trace_not_preserved:{self.input_term}")
        if self.silent_erasure:
            errors.append(f"lexical_silent_erasure_forbidden:{self.input_term}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class SourceDictionaryEntry:
    entry_id: str
    source_kind: SourceVocabularyKind
    source_url: str
    term: str
    canonical_type: str
    pydantika_annotation_id: str
    relation_type: str
    preserves_trace: bool = True

    def validate(self, known_urls: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.entry_id:
            errors.append("source_dictionary_entry_id_missing")
        if self.source_url not in known_urls:
            errors.append(f"source_dictionary_unknown_url:{self.entry_id}")
        if not self.term or not self.canonical_type:
            errors.append(f"source_dictionary_term_missing:{self.entry_id}")
        if not self.pydantika_annotation_id:
            errors.append(f"source_dictionary_annotation_missing:{self.entry_id}")
        if not self.relation_type:
            errors.append(f"source_dictionary_relation_missing:{self.entry_id}")
        if not self.preserves_trace:
            errors.append(f"source_dictionary_trace_drift:{self.entry_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PydantikaSchemaBinding:
    schema_id: str
    surface: PolyglotSurface
    python_type: str
    semantic_type: str
    annotation_ids: tuple[str, ...]
    localized: bool = True
    plural_typed: bool = True
    source_bound: bool = True

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.schema_id:
            errors.append("pydantika_schema_id_missing")
        if not self.python_type or not self.semantic_type:
            errors.append(f"pydantika_schema_type_missing:{self.schema_id}")
        if not self.annotation_ids:
            errors.append(f"pydantika_schema_annotations_missing:{self.schema_id}")
        if not self.localized:
            errors.append(f"pydantika_schema_not_localized:{self.schema_id}")
        if not self.plural_typed:
            errors.append(f"pydantika_schema_not_plural_typed:{self.schema_id}")
        if not self.source_bound:
            errors.append(f"pydantika_schema_not_source_bound:{self.schema_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class AperiodicCellularTile:
    tile_id: str
    kind: AperiodicTileKind
    gliph_type: str
    adjacency_types: tuple[str, ...]
    substitution_rule: str
    pydantika_annotation_id: str
    nonperiodic_witness: bool = True
    localized: bool = True
    no_identity_transport: bool = True

    def validate(self, known_annotations: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.tile_id:
            errors.append("aperiodic_tile_id_missing")
        if not self.gliph_type:
            errors.append(f"aperiodic_tile_gliph_missing:{self.tile_id}")
        if not self.adjacency_types:
            errors.append(f"aperiodic_tile_adjacency_missing:{self.tile_id}")
        if not self.substitution_rule:
            errors.append(f"aperiodic_tile_substitution_missing:{self.tile_id}")
        if self.pydantika_annotation_id not in known_annotations:
            errors.append(f"aperiodic_tile_unknown_annotation:{self.tile_id}")
        if not self.nonperiodic_witness:
            errors.append(f"aperiodic_tile_periodic_drift:{self.tile_id}")
        if not self.localized:
            errors.append(f"aperiodic_tile_not_localized:{self.tile_id}")
        if not self.no_identity_transport:
            errors.append(f"aperiodic_tile_identity_transport:{self.tile_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PolyglotBinding:
    binding_id: str
    surface: PolyglotSurface
    adapter_name: str
    language_or_runtime: str
    authority: BindingAuthority
    pydantika_schema_id: str
    optional: bool = True
    imports_performed: bool = False
    runtime_executed: bool = False
    external_mutation_performed: bool = False

    def validate(self, known_schema_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.binding_id:
            errors.append("polyglot_binding_id_missing")
        if not self.adapter_name or not self.language_or_runtime:
            errors.append(f"polyglot_binding_adapter_missing:{self.binding_id}")
        if self.authority == BindingAuthority.SOURCE_DICTIONARY and not self.optional:
            errors.append(f"source_dictionary_binding_must_be_optional:{self.binding_id}")
        if self.pydantika_schema_id not in known_schema_ids:
            errors.append(f"polyglot_binding_unknown_schema:{self.binding_id}")
        if self.imports_performed:
            errors.append(f"polyglot_binding_import_forbidden:{self.binding_id}")
        if self.runtime_executed:
            errors.append(f"polyglot_binding_runtime_execution_forbidden:{self.binding_id}")
        if self.external_mutation_performed:
            errors.append(f"polyglot_binding_external_mutation:{self.binding_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class OpenMPICompliance:
    profile_id: str
    binding_id: str
    communicator_boundary: str
    mpi4py_optional: bool = True
    explicit_mpiexec_required: bool = True
    rank_witness_required_for_multi_rank: bool = True
    scheduler_mutation: bool = False
    performance_claim_without_benchmark: bool = False

    def validate(self, known_binding_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.profile_id:
            errors.append("openmpi_profile_id_missing")
        if self.binding_id not in known_binding_ids:
            errors.append(f"openmpi_unknown_binding:{self.profile_id}")
        if not self.communicator_boundary:
            errors.append(f"openmpi_communicator_boundary_missing:{self.profile_id}")
        if not self.mpi4py_optional:
            errors.append(f"openmpi_mpi4py_not_optional:{self.profile_id}")
        if not self.explicit_mpiexec_required:
            errors.append(f"openmpi_mpiexec_guard_missing:{self.profile_id}")
        if not self.rank_witness_required_for_multi_rank:
            errors.append(f"openmpi_rank_witness_missing:{self.profile_id}")
        if self.scheduler_mutation:
            errors.append(f"openmpi_scheduler_mutation:{self.profile_id}")
        if self.performance_claim_without_benchmark:
            errors.append(f"openmpi_unbenchmarked_performance_claim:{self.profile_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class HomomorphicEncodingPolicy:
    policy_id: str
    source_kind: SourceVocabularyKind
    encoding_family: str
    displacement_authority: BindingAuthority
    virtual_local_causality: bool = True
    compositional_contextual: bool = True
    krone_admin_required: bool = True
    cryptographic_security_claimed: bool = False
    quantum_execution_performed: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.policy_id:
            errors.append("homomorphic_policy_id_missing")
        if self.source_kind != SourceVocabularyKind.MAHADEV_QFHE_LWE:
            errors.append(f"homomorphic_policy_wrong_source:{self.policy_id}")
        if not self.encoding_family:
            errors.append(f"homomorphic_policy_family_missing:{self.policy_id}")
        if self.displacement_authority != BindingAuthority.KRONE_ADMIN_REQUIRED:
            errors.append(f"homomorphic_policy_krone_authority_missing:{self.policy_id}")
        if not self.virtual_local_causality:
            errors.append(f"homomorphic_policy_local_causality_missing:{self.policy_id}")
        if not self.compositional_contextual:
            errors.append(f"homomorphic_policy_contextuality_missing:{self.policy_id}")
        if not self.krone_admin_required:
            errors.append(f"homomorphic_policy_admin_guard_missing:{self.policy_id}")
        if self.cryptographic_security_claimed:
            errors.append(f"homomorphic_policy_security_claim_forbidden:{self.policy_id}")
        if self.quantum_execution_performed:
            errors.append(f"homomorphic_policy_quantum_execution_forbidden:{self.policy_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class UniversalAbstractPipeline:
    pipeline_id: str
    surface_ids: tuple[PolyglotSurface, ...]
    dictionary_entry_ids: tuple[str, ...]
    pydantika_schema_ids: tuple[str, ...]
    harmonic_semantics: str
    universal_abstract_perception: bool = True
    compositional_contextual: bool = True
    no_plural_collapse: bool = True
    no_linux_kernel_claim: bool = True

    def validate(
        self,
        known_dictionary_ids: set[str],
        known_schema_ids: set[str],
    ) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.pipeline_id:
            errors.append("universal_pipeline_id_missing")
        if not self.surface_ids:
            errors.append(f"universal_pipeline_surfaces_missing:{self.pipeline_id}")
        if set(self.dictionary_entry_ids) - known_dictionary_ids:
            errors.append(f"universal_pipeline_unknown_dictionary:{self.pipeline_id}")
        if set(self.pydantika_schema_ids) - known_schema_ids:
            errors.append(f"universal_pipeline_unknown_schema:{self.pipeline_id}")
        if not self.harmonic_semantics:
            errors.append(f"universal_pipeline_harmonics_missing:{self.pipeline_id}")
        if not self.universal_abstract_perception:
            errors.append(f"universal_pipeline_perception_missing:{self.pipeline_id}")
        if not self.compositional_contextual:
            errors.append(f"universal_pipeline_contextuality_missing:{self.pipeline_id}")
        if not self.no_plural_collapse:
            errors.append(f"universal_pipeline_plural_collapse:{self.pipeline_id}")
        if not self.no_linux_kernel_claim:
            errors.append(f"universal_pipeline_linux_kernel_claim:{self.pipeline_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class LocalizationRule:
    algorithm_id: str
    tile_ids: tuple[str, ...]
    target_surfaces: tuple[PolyglotSurface, ...]
    graphical_calculus: str = SIGIL_GRAPHICAL_CALCULUS
    all_types_are_relations: bool = True
    all_relations_are_types: bool = True
    no_single_type_collapse: bool = True
    preserves_trace: bool = True
    preserves_locality: bool = True
    endofunctor_signature: str = (
        "endofunctor L : SIGIL_LOCALIZATION_LIBRARY -> "
        "SIGIL_LOCALIZATION_LIBRARY"
    )

    def validate(self, known_tile_ids: set[str]) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.algorithm_id:
            errors.append("localization_rule_id_missing")
        if not self.tile_ids or set(self.tile_ids) - known_tile_ids:
            errors.append(f"localization_rule_unknown_tile:{self.algorithm_id}")
        if not self.target_surfaces:
            errors.append(f"localization_rule_surfaces_missing:{self.algorithm_id}")
        if self.graphical_calculus != SIGIL_GRAPHICAL_CALCULUS:
            errors.append(f"localization_rule_calculus_mismatch:{self.algorithm_id}")
        if not self.all_types_are_relations:
            errors.append(f"localization_rule_types_not_relations:{self.algorithm_id}")
        if not self.all_relations_are_types:
            errors.append(f"localization_rule_relations_not_types:{self.algorithm_id}")
        if not self.no_single_type_collapse:
            errors.append(f"localization_rule_single_type_collapse:{self.algorithm_id}")
        if not self.preserves_trace:
            errors.append(f"localization_rule_trace_drift:{self.algorithm_id}")
        if not self.preserves_locality:
            errors.append(f"localization_rule_locality_drift:{self.algorithm_id}")
        if "endofunctor" not in self.endofunctor_signature:
            errors.append(f"localization_rule_endofunctor_missing:{self.algorithm_id}")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class PolyglotLocalizationKernel:
    kernel_id: str
    lexical_normalizations: tuple[LexicalNormalization, ...]
    dictionaries: tuple[SourceDictionaryEntry, ...]
    schemas: tuple[PydantikaSchemaBinding, ...]
    tiles: tuple[AperiodicCellularTile, ...]
    localization_rule: LocalizationRule
    bindings: tuple[PolyglotBinding, ...]
    openmpi_compliance: OpenMPICompliance
    homomorphic_policy: HomomorphicEncodingPolicy
    pipelines: tuple[UniversalAbstractPipeline, ...]
    source_urls: tuple[str, ...] = SOURCE_URLS
    schema_id: str = SCHEMA_ID
    linter_canon: str = LINTER_CANON
    quantum_quimbo_context: str = QUANTUM_QUIMBO_CONTEXT
    source_bound: bool = True
    runtime_executed: bool = False
    external_imports_performed: bool = False
    hardware_or_scheduler_mutation: bool = False

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.kernel_id:
            errors.append("polyglot_localization_kernel_id_missing")
        if self.schema_id != SCHEMA_ID:
            errors.append("polyglot_localization_schema_mismatch")
        if self.linter_canon != LINTER_CANON:
            errors.append("polyglot_localization_linter_canon_mismatch")
        if self.quantum_quimbo_context != QUANTUM_QUIMBO_CONTEXT:
            errors.append("polyglot_localization_quimbo_context_mismatch")
        if not self.source_bound:
            errors.append("polyglot_localization_not_source_bound")
        if self.runtime_executed:
            errors.append("polyglot_localization_runtime_execution_forbidden")
        if self.external_imports_performed:
            errors.append("polyglot_localization_external_import_forbidden")
        if self.hardware_or_scheduler_mutation:
            errors.append("polyglot_localization_hardware_mutation_forbidden")

        known_urls = set(self.source_urls)
        if not set(SOURCE_URLS).issubset(known_urls):
            errors.append("polyglot_localization_source_url_missing")
        if not self.lexical_normalizations:
            errors.append("polyglot_localization_lexical_rules_missing")
        for item in self.lexical_normalizations:
            errors.extend(item.validate())

        dictionary_ids = {item.entry_id for item in self.dictionaries}
        if len(dictionary_ids) != len(self.dictionaries):
            errors.append("duplicate_source_dictionary_entry")
        for item in self.dictionaries:
            errors.extend(item.validate(known_urls))

        schema_ids = {item.schema_id for item in self.schemas}
        if len(schema_ids) != len(self.schemas):
            errors.append("duplicate_pydantika_schema")
        annotation_ids = {
            annotation_id
            for schema in self.schemas
            for annotation_id in schema.annotation_ids
        }
        for schema in self.schemas:
            errors.extend(schema.validate())

        tile_ids = {tile.tile_id for tile in self.tiles}
        if len(tile_ids) != len(self.tiles):
            errors.append("duplicate_aperiodic_tile")
        for tile in self.tiles:
            errors.extend(tile.validate(annotation_ids))
        errors.extend(self.localization_rule.validate(tile_ids))

        binding_ids = {binding.binding_id for binding in self.bindings}
        if len(binding_ids) != len(self.bindings):
            errors.append("duplicate_polyglot_binding")
        for binding in self.bindings:
            errors.extend(binding.validate(schema_ids))
        errors.extend(self.openmpi_compliance.validate(binding_ids))
        errors.extend(self.homomorphic_policy.validate())
        for pipeline in self.pipelines:
            errors.extend(pipeline.validate(dictionary_ids, schema_ids))

        required_surfaces = set(PolyglotSurface)
        actual_surfaces = {schema.surface for schema in self.schemas}
        missing_surfaces = sorted(
            required_surfaces - actual_surfaces,
            key=lambda item: item.value,
        )
        if missing_surfaces:
            labels = ",".join(item.value for item in missing_surfaces)
            errors.append(f"polyglot_localization_surface_missing:{labels}")
        return tuple(errors)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["lexical_normalizations"] = [
            asdict(item) for item in self.lexical_normalizations
        ]
        payload["dictionaries"] = [asdict(item) for item in self.dictionaries]
        payload["schemas"] = [asdict(item) for item in self.schemas]
        payload["tiles"] = [asdict(tile) for tile in self.tiles]
        payload["localization_rule"] = asdict(self.localization_rule)
        payload["bindings"] = [asdict(binding) for binding in self.bindings]
        payload["openmpi_compliance"] = asdict(self.openmpi_compliance)
        payload["homomorphic_policy"] = asdict(self.homomorphic_policy)
        payload["pipelines"] = [asdict(pipeline) for pipeline in self.pipelines]
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


def _schema(surface: PolyglotSurface, semantic_type: str) -> PydantikaSchemaBinding:
    key = surface.value.lower().replace("_", "-")
    return PydantikaSchemaBinding(
        f"schema:{key}",
        surface,
        "PydantikaAnnotatedType",
        semantic_type,
        (
            f"ann:{key}:localized",
            f"ann:{key}:plural-relation-type",
        ),
    )


def build_polyglot_localization_kernel() -> PolyglotLocalizationKernel:
    """Build the canonical source-bound polyglot localization kernel."""

    schemas = (
        _schema(PolyglotSurface.SIGIL4PY, "SIGIL4PY_INTERMEDIATE_LAYER"),
        _schema(PolyglotSurface.SIGIL4GODOT, "SIGIL4GODOT_PACAIOGAMES"),
        _schema(PolyglotSurface.SIGIL4QUASARPI, "SIGIL4QUASARPI_EDGE_LAYER"),
        _schema(PolyglotSurface.PACA_ALPACA, "ALGEBRAIC_GEOMETRIC_SEMANTIC_LLM"),
        _schema(PolyglotSurface.PACA_ANTORCHA_PYTORCH, "PACA_ANTORCHA_TENSOR"),
        _schema(PolyglotSurface.MACAULAY2, "MACAULAY2_AG_BINDING"),
        _schema(PolyglotSurface.OPEN_MPI, "STRIKK_OPENMPI_COMPLIANCE"),
        _schema(PolyglotSurface.PACAIOGAMES, "PACAIOGAMES_TYPED_STREAM"),
        _schema(PolyglotSurface.QUANTUM_QUIMBO, QUANTUM_QUIMBO_CONTEXT),
        _schema(PolyglotSurface.SIGIL4CPYTHON, "SIGIL4CPYTHON_LOCALIZATION"),
    )
    dictionary = (
        SourceDictionaryEntry(
            "dict:eczoo:asymmetric",
            SourceVocabularyKind.ERROR_CORRECTION_ZOO_ASYMMETRIC,
            "https://errorcorrectionzoo.org/list/list_asymmetric",
            "asymmetric quantum codes",
            "ASYMMETRIC_NOISE_BIASED_CODE_FAMILY",
            "ann:quantum-quimbo:plural-relation-type",
            "noise_bias_relation",
        ),
        SourceDictionaryEntry(
            "dict:eczoo:dynamic",
            SourceVocabularyKind.ERROR_CORRECTION_ZOO_DYNAMIC,
            "https://errorcorrectionzoo.org/list/dynamic_gen",
            "dynamically generated quantum codes",
            "APERIODIC_MEASUREMENT_SEQUENCE_CODE",
            "ann:sigil4godot:plural-relation-type",
            "dynamic_automorphism_relation",
        ),
        SourceDictionaryEntry(
            "dict:eczoo:floquet",
            SourceVocabularyKind.ERROR_CORRECTION_ZOO_FLOQUET,
            "https://errorcorrectionzoo.org/c/floquet",
            "periodic Floquet code",
            "DYNAMICAL_PERIODIC_MEASUREMENT_CODE",
            "ann:pacaiogames:plural-relation-type",
            "floquet_measurement_relation",
        ),
        SourceDictionaryEntry(
            "dict:mahadev:qfhe",
            SourceVocabularyKind.MAHADEV_QFHE_LWE,
            "https://arxiv.org/abs/1708.02130",
            "classical homomorphic encryption for quantum circuits",
            "KRONE_GUARDED_HOMOMORPHIC_ENCODING",
            "ann:paca-alpaca:plural-relation-type",
            "lwe_blind_delegation_relation",
        ),
        SourceDictionaryEntry(
            "dict:leash:rigidity",
            SourceVocabularyKind.VERIFIER_ON_A_LEASH,
            "https://arxiv.org/abs/1708.07359",
            "classical verifier delegated quantum computation",
            "TWO_PROVER_RIGIDITY_WITNESS",
            "ann:paca-alpaca:localized",
            "delegated_verification_relation",
        ),
        SourceDictionaryEntry(
            "dict:linter:endofunctor",
            SourceVocabularyKind.SIGIL_LINTER_ENDOFUNCTOR,
            "https://github.com/jbermejovega/sigil4cpython",
            "endofukntor",
            "endofunctor",
            "ann:sigil4cpython:localized",
            "lexical_trace_relation",
        ),
    )
    tiles = (
        AperiodicCellularTile(
            "tile:dynamic-automorphism",
            AperiodicTileKind.DYNAMIC_AUTOMORPHISM,
            "QUNO_TYPED_GLIPH",
            ("noise_bias_relation", "dynamic_automorphism_relation"),
            "aperiodic_measurement_sequence_localization",
            "ann:sigil4godot:plural-relation-type",
        ),
        AperiodicCellularTile(
            "tile:floquet-measurement",
            AperiodicTileKind.FLOQUET_MEASUREMENT,
            "PACAIOGAMES_MEASUREMENT_GLIPH",
            ("floquet_measurement_relation", "lwe_blind_delegation_relation"),
            "periodic_measurement_cell_guarded_as_relation",
            "ann:pacaiogames:plural-relation-type",
        ),
        AperiodicCellularTile(
            "tile:ag-semantic",
            AperiodicTileKind.PENROSE,
            "ALGEBRAIC_GEOMETRIC_SEMANTIC_GLIPH",
            ("delegated_verification_relation", "lexical_trace_relation"),
            "nonperiodic_semantic_patchwork_localization",
            "ann:paca-alpaca:plural-relation-type",
        ),
    )
    bindings = (
        PolyglotBinding(
            "bind:sigil4py:intermediate",
            PolyglotSurface.SIGIL4PY,
            "sigil4py.intermediate",
            "Python",
            BindingAuthority.VIRTUAL_ONLY,
            "schema:sigil4py",
        ),
        PolyglotBinding(
            "bind:sigil4godot:pacaiogames",
            PolyglotSurface.SIGIL4GODOT,
            "sigil4godot.pacaiogames",
            "Godot/GDScript",
            BindingAuthority.VIRTUAL_ONLY,
            "schema:sigil4godot",
        ),
        PolyglotBinding(
            "bind:sigil4quasarpi:edge",
            PolyglotSurface.SIGIL4QUASARPI,
            "sigil4quasarpi.edge",
            "Python",
            BindingAuthority.VIRTUAL_ONLY,
            "schema:sigil4quasarpi",
        ),
        PolyglotBinding(
            "bind:paca-antorcha:pytorch",
            PolyglotSurface.PACA_ANTORCHA_PYTORCH,
            "paca.antorcha.torch",
            "PyTorch",
            BindingAuthority.TOOLING_ONLY,
            "schema:paca-antorcha-pytorch",
        ),
        PolyglotBinding(
            "bind:macaulay2:ag",
            PolyglotSurface.MACAULAY2,
            "macaulay2.ag",
            "Macaulay2",
            BindingAuthority.TOOLING_ONLY,
            "schema:macaulay2",
        ),
        PolyglotBinding(
            "bind:openmpi:compliance",
            PolyglotSurface.OPEN_MPI,
            "mpi4py.openmpi",
            "OpenMPI",
            BindingAuthority.KRONE_ADMIN_REQUIRED,
            "schema:open-mpi",
        ),
        PolyglotBinding(
            "bind:paca-alpaca:semantic-llm",
            PolyglotSurface.PACA_ALPACA,
            "paca.alpaca.semantic",
            "LLM-semantic-plan",
            BindingAuthority.SOURCE_DICTIONARY,
            "schema:paca-alpaca",
        ),
    )
    pipelines = (
        UniversalAbstractPipeline(
            "pipeline:universal-abstract-harmonic-semantics",
            tuple(schema.surface for schema in schemas),
            tuple(item.entry_id for item in dictionary),
            tuple(schema.schema_id for schema in schemas),
            "COMPOSITIONAL_CONTEXTUAL_TYPED_HARMONIC_GENERATIVE_SEMANTICS",
        ),
    )
    return PolyglotLocalizationKernel(
        "SIGIL4CPYTHON_POLYGLOT_LOCALIZATION_PIPELINES_V1",
        (
            LexicalNormalization("endofukntor", "endofunctor"),
            LexicalNormalization("quzris", "quazris"),
        ),
        dictionary,
        schemas,
        tiles,
        LocalizationRule(
            "algorithm:cellular-aperiodic-sigil-localization",
            tuple(tile.tile_id for tile in tiles),
            tuple(schema.surface for schema in schemas),
        ),
        bindings,
        OpenMPICompliance(
            "openmpi:strikk-compliance",
            "bind:openmpi:compliance",
            "explicit_mpiexec_rank_witness_or_single_rank_fallback",
        ),
        HomomorphicEncodingPolicy(
            "policy:mahadev-homomorphic-encoding-krone-displacement",
            SourceVocabularyKind.MAHADEV_QFHE_LWE,
            "QUO_QUANTUM_HOMOMORPHIC_ENCODING",
            BindingAuthority.KRONE_ADMIN_REQUIRED,
        ),
        pipelines,
    )


def compile_polyglot_localization_kernel(
    kernel: PolyglotLocalizationKernel,
) -> dict[str, object]:
    """Validate a localization kernel and return an admission payload."""

    errors = kernel.validate()
    reject_markers = (
        "runtime_execution_forbidden",
        "external_import_forbidden",
        "hardware_mutation_forbidden",
        "import_forbidden",
        "external_mutation",
        "scheduler_mutation",
        "krone_authority_missing",
        "security_claim_forbidden",
        "quantum_execution_forbidden",
        "linux_kernel_claim",
    )
    if any(any(marker in error for marker in reject_markers) for error in errors):
        state = LocalizationState.REJECT
    elif errors:
        state = LocalizationState.HOLD_WITH_OBSTRUCTION
    else:
        state = LocalizationState.ADMIT
    payload = kernel.to_dict()
    payload["uap_state"] = state.value
    payload["obstruction_ledger"] = list(errors)
    payload["runtime_executed"] = False
    payload["external_imports_performed"] = False
    payload["hardware_or_scheduler_mutation"] = False
    payload["human_review_required"] = True
    return payload


__all__ = [
    "AperiodicCellularTile",
    "AperiodicTileKind",
    "BindingAuthority",
    "LINTER_CANON",
    "LexicalNormalization",
    "LocalizationRule",
    "LocalizationState",
    "OpenMPICompliance",
    "PydantikaSchemaBinding",
    "PolyglotBinding",
    "PolyglotLocalizationKernel",
    "PolyglotSurface",
    "QUANTUM_QUIMBO_CONTEXT",
    "SCHEMA_ID",
    "SIGIL_GRAPHICAL_CALCULUS",
    "SOURCE_URLS",
    "SourceDictionaryEntry",
    "SourceVocabularyKind",
    "UniversalAbstractPipeline",
    "build_polyglot_localization_kernel",
    "compile_polyglot_localization_kernel",
    "stable_digest",
]
