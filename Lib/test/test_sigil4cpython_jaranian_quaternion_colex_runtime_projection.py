from __future__ import annotations

from dataclasses import replace
import json
import unittest

from sigil4cpython.jaranian_quaternion_colex_runtime_projection import (
    RuntimeProjectionState,
    SIGILBOOK_RUNTIME_HEAD,
    build_reference_runtime_projection,
    compile_reference_runtime_projection_json,
)


class JaranianQuaternionColexRuntimeProjectionTests(unittest.TestCase):
    def test_reference_projection_admits(self) -> None:
        projection = build_reference_runtime_projection()
        self.assertEqual(projection.validate(), ())
        self.assertIs(projection.state, RuntimeProjectionState.ADMIT_SOURCE_RUNTIME_PROJECTION)

    def test_runtime_source_epoch_is_exact(self) -> None:
        projection = build_reference_runtime_projection()
        self.assertEqual(projection.source_head_sha, SIGILBOOK_RUNTIME_HEAD)
        self.assertEqual(projection.source_file_count if hasattr(projection, 'source_file_count') else len(projection.source_files), 3)

    def test_identity_is_distinct_from_stabilizer_polytope(self) -> None:
        projection = build_reference_runtime_projection()
        self.assertNotEqual(projection.identity_anchor_id, projection.stabilizer_polytope_id)

    def test_quaternion_equation_inventory(self) -> None:
        projection = build_reference_runtime_projection()
        self.assertEqual(len(projection.equations), 11)
        self.assertIn("XYZ_NEG_ONE", {item.equation_id for item in projection.equations})
        self.assertTrue(all(item.source_checked for item in projection.equations))
        self.assertFalse(any(item.runtime_observed for item in projection.equations))

    def test_contexts_preserve_geometry_and_hold_axes(self) -> None:
        projection = build_reference_runtime_projection()
        self.assertEqual({item.axis for item in projection.contexts}, {"GLOBAL", "X", "Y", "Z"})
        for context in projection.contexts:
            self.assertTrue(context.identity_visible)
            self.assertTrue(context.stabilizer_visible)
            self.assertTrue(context.chirality_layers_visible)
            self.assertFalse(context.all_relations_jointly_measurable)
        self.assertTrue(all(item.held_axes for item in projection.contexts if item.axis != "GLOBAL"))

    def test_antipode_and_normalization_contract(self) -> None:
        projection = build_reference_runtime_projection()
        self.assertEqual(projection.opposite_phase_operation, "QUATERNION_ANTIPODE")
        self.assertTrue(projection.composite_states_normalized)
        self.assertEqual(projection.phase_projection_radius, "sqrt(3)")
        self.assertFalse(projection.parity_layers_are_pauli_contexts)

    def test_dependency_and_execution_boundary(self) -> None:
        projection = build_reference_runtime_projection()
        self.assertTrue(projection.dependency_free)
        self.assertFalse(projection.cpython_semantics_changed)
        self.assertFalse(projection.abi_changed)
        self.assertFalse(projection.godot_started)
        self.assertFalse(projection.scene_instantiated)
        self.assertFalse(projection.physical_measurement_executed)
        self.assertFalse(projection.runtime_executed)
        self.assertFalse(projection.final_kapsyla)

    def test_projection_digest_is_deterministic(self) -> None:
        first = build_reference_runtime_projection()
        second = build_reference_runtime_projection()
        self.assertEqual(first.projection_sha256, second.projection_sha256)

    def test_identity_collapse_rejects(self) -> None:
        projection = build_reference_runtime_projection()
        bad = replace(projection, identity_anchor_id=projection.stabilizer_polytope_id)
        self.assertIn("identity_silently_collapsed_into_stabilizer_polytope", bad.validate())
        self.assertIs(bad.state, RuntimeProjectionState.REJECT)

    def test_parity_context_collapse_rejects(self) -> None:
        projection = build_reference_runtime_projection()
        bad = replace(projection, parity_layers_are_pauli_contexts=True)
        self.assertIn("parity_context_collapse", bad.validate())

    def test_receipt_json_is_parseable(self) -> None:
        payload = json.loads(compile_reference_runtime_projection_json())
        self.assertEqual(payload["state"], "ADMIT_SOURCE_RUNTIME_PROJECTION")
        self.assertEqual(payload["source_file_count"], 3)
        self.assertEqual(payload["equation_count"], 11)
        self.assertEqual(payload["context_count"], 4)
        self.assertTrue(payload["identity_anchor_distinct"])
        self.assertFalse(payload["runtime_executed"])
        self.assertFalse(payload["final_kapsyla"])


if __name__ == "__main__":
    unittest.main()
