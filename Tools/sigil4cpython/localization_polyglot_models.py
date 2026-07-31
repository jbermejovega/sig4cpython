"""Strict Pydantika models for SIGIL polyglot localization kernels."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


SCHEMA_ID = "SIGIL4CPYTHON_POLYGLOT_LOCALIZATION_PIPELINES_V1"
SIGIL_GRAPHICAL_CALCULUS = "SIGIL_GRAPHICAL_CALCULUS"
QUANTUM_QUIMBO_CONTEXT = "QUANTUM_QUIMBO_KERNEL_NOT_LINUX"
LINTER_CANON = "STRIKK_PLURAL_TYPED_SIGIL_LINTER_GLOBAL_FIELD_ENDOFUNCTOR_LIBRARY_V1"

SOURCE_URLS = {
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
}

REQUIRED_SURFACES = {
    "SIGIL4PY",
    "SIGIL4GODOT",
    "SIGIL4QUASARPI",
    "PACA_ALPACA",
    "PACA_ANTORCHA_PYTORCH",
    "MACAULAY2",
    "OPEN_MPI",
    "PACAIOGAMES",
    "QUANTUM_QUIMBO",
    "SIGIL4CPYTHON",
}


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


class LexicalNormalizationModel(StrictModel):
    input_term: str = Field(min_length=1, max_length=192)
    canonical_term: str = Field(min_length=1, max_length=192)
    preserve_input_trace: Literal[True] = True
    silent_erasure: Literal[False] = False


class SourceDictionaryEntryModel(StrictModel):
    entry_id: str = Field(min_length=1, max_length=192)
    source_kind: Literal[
        "ERROR_CORRECTION_ZOO_ASYMMETRIC",
        "ERROR_CORRECTION_ZOO_DYNAMIC",
        "ERROR_CORRECTION_ZOO_FLOQUET",
        "MAHADEV_QFHE_LWE",
        "VERIFIER_ON_A_LEASH",
        "FPGA_OPEN_SOURCE_STACK",
        "SIGIL_LINTER_ENDOFUNCTOR",
    ]
    source_url: str = Field(min_length=1, max_length=256)
    term: str = Field(min_length=1, max_length=256)
    canonical_type: str = Field(min_length=1, max_length=256)
    pydantika_annotation_id: str = Field(min_length=1, max_length=192)
    relation_type: str = Field(min_length=1, max_length=192)
    preserves_trace: Literal[True] = True


class PydantikaSchemaBindingModel(StrictModel):
    schema_id: str = Field(min_length=1, max_length=192)
    surface: Literal[
        "SIGIL4PY",
        "SIGIL4GODOT",
        "SIGIL4QUASARPI",
        "PACA_ALPACA",
        "PACA_ANTORCHA_PYTORCH",
        "MACAULAY2",
        "OPEN_MPI",
        "PACAIOGAMES",
        "QUANTUM_QUIMBO",
        "SIGIL4CPYTHON",
    ]
    python_type: str = Field(min_length=1, max_length=192)
    semantic_type: str = Field(min_length=1, max_length=192)
    annotation_ids: StringTuple = Field(min_length=1, max_length=64)
    localized: Literal[True] = True
    plural_typed: Literal[True] = True
    source_bound: Literal[True] = True


class AperiodicCellularTileModel(StrictModel):
    tile_id: str = Field(min_length=1, max_length=192)
    kind: Literal[
        "PENROSE",
        "WANG",
        "AMMANN_BEENKER",
        "DYNAMIC_AUTOMORPHISM",
        "FLOQUET_MEASUREMENT",
        "HYPERGRAPH_CELL",
    ]
    gliph_type: str = Field(min_length=1, max_length=192)
    adjacency_types: StringTuple = Field(min_length=1, max_length=64)
    substitution_rule: str = Field(min_length=1, max_length=256)
    pydantika_annotation_id: str = Field(min_length=1, max_length=192)
    nonperiodic_witness: Literal[True] = True
    localized: Literal[True] = True
    no_identity_transport: Literal[True] = True


class LocalizationRuleModel(StrictModel):
    algorithm_id: str = Field(min_length=1, max_length=192)
    tile_ids: StringTuple = Field(min_length=1, max_length=128)
    target_surfaces: StringTuple = Field(min_length=1, max_length=64)
    graphical_calculus: Literal[SIGIL_GRAPHICAL_CALCULUS] = (
        SIGIL_GRAPHICAL_CALCULUS
    )
    all_types_are_relations: Literal[True] = True
    all_relations_are_types: Literal[True] = True
    no_single_type_collapse: Literal[True] = True
    preserves_trace: Literal[True] = True
    preserves_locality: Literal[True] = True
    endofunctor_signature: str = Field(min_length=1, max_length=256)

    @model_validator(mode="after")
    def validate_signature(self) -> "LocalizationRuleModel":
        if "endofunctor" not in self.endofunctor_signature:
            raise ValueError("localization_rule_endofunctor_missing")
        return self


class PolyglotBindingModel(StrictModel):
    binding_id: str = Field(min_length=1, max_length=192)
    surface: str = Field(min_length=1, max_length=64)
    adapter_name: str = Field(min_length=1, max_length=192)
    language_or_runtime: str = Field(min_length=1, max_length=192)
    authority: Literal[
        "VIRTUAL_ONLY",
        "TOOLING_ONLY",
        "KRONE_ADMIN_REQUIRED",
        "SOURCE_DICTIONARY",
    ]
    pydantika_schema_id: str = Field(min_length=1, max_length=192)
    optional: bool = True
    imports_performed: Literal[False] = False
    runtime_executed: Literal[False] = False
    external_mutation_performed: Literal[False] = False


class OpenMPIComplianceModel(StrictModel):
    profile_id: str = Field(min_length=1, max_length=192)
    binding_id: str = Field(min_length=1, max_length=192)
    communicator_boundary: str = Field(min_length=1, max_length=256)
    mpi4py_optional: Literal[True] = True
    explicit_mpiexec_required: Literal[True] = True
    rank_witness_required_for_multi_rank: Literal[True] = True
    scheduler_mutation: Literal[False] = False
    performance_claim_without_benchmark: Literal[False] = False


class HomomorphicEncodingPolicyModel(StrictModel):
    policy_id: str = Field(min_length=1, max_length=192)
    source_kind: Literal["MAHADEV_QFHE_LWE"]
    encoding_family: str = Field(min_length=1, max_length=192)
    displacement_authority: Literal["KRONE_ADMIN_REQUIRED"]
    virtual_local_causality: Literal[True] = True
    compositional_contextual: Literal[True] = True
    krone_admin_required: Literal[True] = True
    cryptographic_security_claimed: Literal[False] = False
    quantum_execution_performed: Literal[False] = False


class UniversalAbstractPipelineModel(StrictModel):
    pipeline_id: str = Field(min_length=1, max_length=192)
    surface_ids: StringTuple = Field(min_length=1, max_length=64)
    dictionary_entry_ids: StringTuple = Field(min_length=1, max_length=128)
    pydantika_schema_ids: StringTuple = Field(min_length=1, max_length=128)
    harmonic_semantics: str = Field(min_length=1, max_length=256)
    universal_abstract_perception: Literal[True] = True
    compositional_contextual: Literal[True] = True
    no_plural_collapse: Literal[True] = True
    no_linux_kernel_claim: Literal[True] = True


LexicalTuple = Annotated[
    tuple[LexicalNormalizationModel, ...],
    BeforeValidator(_json_array_to_tuple),
]
DictionaryTuple = Annotated[
    tuple[SourceDictionaryEntryModel, ...],
    BeforeValidator(_json_array_to_tuple),
]
SchemaTuple = Annotated[
    tuple[PydantikaSchemaBindingModel, ...],
    BeforeValidator(_json_array_to_tuple),
]
TileTuple = Annotated[
    tuple[AperiodicCellularTileModel, ...],
    BeforeValidator(_json_array_to_tuple),
]
BindingTuple = Annotated[
    tuple[PolyglotBindingModel, ...],
    BeforeValidator(_json_array_to_tuple),
]
PipelineTuple = Annotated[
    tuple[UniversalAbstractPipelineModel, ...],
    BeforeValidator(_json_array_to_tuple),
]


class PolyglotLocalizationKernelModel(StrictModel):
    kernel_id: str = Field(min_length=1, max_length=192)
    lexical_normalizations: LexicalTuple = Field(min_length=1, max_length=64)
    dictionaries: DictionaryTuple = Field(min_length=1, max_length=256)
    schemas: SchemaTuple = Field(min_length=1, max_length=128)
    tiles: TileTuple = Field(min_length=1, max_length=128)
    localization_rule: LocalizationRuleModel
    bindings: BindingTuple = Field(min_length=1, max_length=128)
    openmpi_compliance: OpenMPIComplianceModel
    homomorphic_policy: HomomorphicEncodingPolicyModel
    pipelines: PipelineTuple = Field(min_length=1, max_length=64)
    source_urls: StringTuple = Field(min_length=1, max_length=256)
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    linter_canon: Literal[LINTER_CANON] = LINTER_CANON
    quantum_quimbo_context: Literal[QUANTUM_QUIMBO_CONTEXT] = (
        QUANTUM_QUIMBO_CONTEXT
    )
    source_bound: Literal[True] = True
    runtime_executed: Literal[False] = False
    external_imports_performed: Literal[False] = False
    hardware_or_scheduler_mutation: Literal[False] = False
    pydantika_is_tooling_not_stdlib_dependency: Literal[True] = True
    human_review_required: Literal[True] = True

    @model_validator(mode="after")
    def validate_kernel(self) -> "PolyglotLocalizationKernelModel":
        if not SOURCE_URLS.issubset(set(self.source_urls)):
            raise ValueError("polyglot_localization_source_url_missing")
        dictionary_ids = tuple(item.entry_id for item in self.dictionaries)
        if len(dictionary_ids) != len(set(dictionary_ids)):
            raise ValueError("duplicate_source_dictionary_entry")
        if any(item.source_url not in SOURCE_URLS for item in self.dictionaries):
            raise ValueError("source_dictionary_unknown_url")
        schema_ids = tuple(item.schema_id for item in self.schemas)
        if len(schema_ids) != len(set(schema_ids)):
            raise ValueError("duplicate_pydantika_schema")
        known_schema_ids = set(schema_ids)
        annotation_ids = {
            annotation_id
            for schema in self.schemas
            for annotation_id in schema.annotation_ids
        }
        tile_ids = tuple(tile.tile_id for tile in self.tiles)
        if len(tile_ids) != len(set(tile_ids)):
            raise ValueError("duplicate_aperiodic_tile")
        for tile in self.tiles:
            if tile.pydantika_annotation_id not in annotation_ids:
                raise ValueError("aperiodic_tile_unknown_annotation")
        if set(self.localization_rule.tile_ids) - set(tile_ids):
            raise ValueError("localization_rule_unknown_tile")
        surfaces = {schema.surface for schema in self.schemas}
        if surfaces != REQUIRED_SURFACES:
            raise ValueError("polyglot_localization_surface_missing")
        binding_ids = tuple(binding.binding_id for binding in self.bindings)
        if len(binding_ids) != len(set(binding_ids)):
            raise ValueError("duplicate_polyglot_binding")
        known_binding_ids = set(binding_ids)
        for binding in self.bindings:
            if binding.pydantika_schema_id not in known_schema_ids:
                raise ValueError("polyglot_binding_unknown_schema")
        if self.openmpi_compliance.binding_id not in known_binding_ids:
            raise ValueError("openmpi_unknown_binding")
        for pipeline in self.pipelines:
            if set(pipeline.dictionary_entry_ids) - set(dictionary_ids):
                raise ValueError("universal_pipeline_unknown_dictionary")
            if set(pipeline.pydantika_schema_ids) - known_schema_ids:
                raise ValueError("universal_pipeline_unknown_schema")
        return self

    def canonical_digest(self) -> str:
        encoded = json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


class PydantikaPolyglotLocalizationCertificate(StrictModel):
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    model_name: Literal["PolyglotLocalizationKernelModel"] = (
        "PolyglotLocalizationKernelModel"
    )
    payload_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    serialization_round_trip_verified: Literal[True] = True
    runtime_executed: Literal[False] = False
    external_imports_performed: Literal[False] = False
    hardware_or_scheduler_mutation: Literal[False] = False
    human_review_required: Literal[True] = True


def compile_pydantika_polyglot_localization_kernel(
    payload: dict[str, object],
) -> PydantikaPolyglotLocalizationCertificate:
    model = PolyglotLocalizationKernelModel.model_validate(payload)
    encoded = model.model_dump_json()
    reconstructed = PolyglotLocalizationKernelModel.model_validate_json(encoded)
    if reconstructed.model_dump(mode="json") != model.model_dump(mode="json"):
        raise ValueError("polyglot_localization_round_trip_failed")
    return PydantikaPolyglotLocalizationCertificate(
        payload_digest=model.canonical_digest()
    )


__all__ = [
    "PolyglotLocalizationKernelModel",
    "PydantikaPolyglotLocalizationCertificate",
    "SCHEMA_ID",
    "compile_pydantika_polyglot_localization_kernel",
]
