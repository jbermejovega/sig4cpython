from __future__ import annotations

from dataclasses import replace
import json
import unittest

from sigil4cpython.jaranian_total_colex_projection import (
    ChiralAxis,
    ColexLayer,
    PanelId,
    ProjectionState,
    SIGILBOOK_SOURCE_HEAD,
    SOURCE_BUNDLE_SHA256,
    build_reference_projection,
    compile_reference_projection_json,
)


class JaranianTotalColexProjectionTests(unittest.TestCase):
    def test_reference_projection_admits(self) -> None:
        projection = build_reference_projection()
        self.assertEqual(projection.validate(), ())
        self.assertIs(projection.state, ProjectionState.ADMIT_DEPENDENCY_FREE_PROJECTION)

    def test_exact_source_epoch_is_pinned(self) -> None:
        projection = build_reference_projection()
        self.assertEqual(projection.source.head_sha, SIGILBOOK_SOURCE_HEAD)
        self.assertEqual(projection.source.payload_sha256, SOURCE_BUNDLE_SHA256)
        self.assertFalse(projection.source.authority_transferred)

    def test_six_panels_and_four_layers(self) -> None:
        projection = build_reference_projection()
        self.assertEqual({item.panel_id for item in projection.panels}, set(PanelId))
        self.assertEqual({item.ordinal for item in projection.panels}, set(range(1, 7)))
        self.assertEqual(set(projection.layers), set(ColexLayer))

    def test_identity_is_explicit(self) -> None:
        projection = build_reference_projection()
        self.assertEqual(projection.identity_cell_id, "cell.identity")
        self.assertEqual(projection.identity_relation_id, "rel.identity")
        for context in projection.chiral_contexts:
            self.assertEqual(context.identity_cell_id, "cell.identity")
            self.assertIn("rel.identity", context.measurable_relation_ids)

    def test_three_contexts_remain_incomplete(self) -> None:
        projection = build_reference_projection()
        self.assertEqual({item.axis for item in projection.chiral_contexts}, set(ChiralAxis))
        for context in projection.chiral_contexts:
            self.assertTrue(context.held_relation_ids)
            self.assertFalse(context.all_relations_jointly_measurable)

    def test_held_claims_are_not_promoted(self) -> None:
        projection = build_reference_projection()
        self.assertEqual(
            {item.relation_id for item in projection.held_claims},
            {"rel.fm.reverse", "rel.hk.preservation", "rel.scutoid.intercalation"},
        )
        self.assertFalse(any(item.promoted for item in projection.held_claims))

    def test_dependency_and_cpython_boundaries(self) -> None:
        projection = build_reference_projection()
        self.assertTrue(projection.dependency_free)
        self.assertFalse(projection.pydantic_imported)
        self.assertFalse(projection.discopy_imported)
        self.assertFalse(projection.cpython_semantics_changed)
        self.assertFalse(projection.abi_changed)
        self.assertFalse(projection.stdlib_semantics_changed)
        self.assertFalse(projection.runtime_executed)

    def test_projection_digest_is_deterministic(self) -> None:
        first = build_reference_projection()
        second = build_reference_projection()
        self.assertEqual(first.projection_sha256, second.projection_sha256)

    def test_source_head_drift_rejects(self) -> None:
        projection = build_reference_projection()
        bad_source = replace(projection.source, head_sha="0" * 40)
        bad = replace(projection, source=bad_source)
        self.assertIn("source_head_drift", bad.validate())
        self.assertIs(bad.state, ProjectionState.REJECT)

    def test_single_context_global_completeness_rejects(self) -> None:
        projection = build_reference_projection()
        context = replace(
            projection.chiral_contexts[0],
            all_relations_jointly_measurable=True,
        )
        bad = replace(
            projection,
            chiral_contexts=(context,) + projection.chiral_contexts[1:],
        )
        self.assertIn("single_context_claims_global_completeness:X", bad.validate())

    def test_receipt_json_is_parseable(self) -> None:
        payload = json.loads(compile_reference_projection_json())
        self.assertEqual(payload["state"], "ADMIT_DEPENDENCY_FREE_PROJECTION")
        self.assertEqual(payload["panel_count"], 6)
        self.assertFalse(payload["runtime_executed"])
        self.assertFalse(payload["cpython_semantics_changed"])
        self.assertFalse(payload["final_kapsyla"])


if __name__ == "__main__":
    unittest.main()
