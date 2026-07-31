from __future__ import annotations

import unittest

from sigil4cpython.pydantika_coherent_projection import (
    SOURCE_SHA,
    ProjectionVerdict,
    build_pydantika_coherent_projection,
    compile_pydantika_coherent_projection,
    with_identity_transport,
)


class PydantikaCoherentProjectionTests(unittest.TestCase):
    def test_projection_is_admitted(self) -> None:
        model = build_pydantika_coherent_projection()
        report = compile_pydantika_coherent_projection(model)

        self.assertEqual(
            report["verdict"],
            ProjectionVerdict.ADMIT.value,
        )
        self.assertEqual(report["source_sha"], SOURCE_SHA)
        self.assertEqual(len(model.sections), 7)
        self.assertEqual(model.ouroboros.void_type, "VOID")

    def test_projection_is_dependency_free_and_inert(self) -> None:
        model = build_pydantika_coherent_projection()

        self.assertTrue(model.dependency_free)
        self.assertFalse(model.interpreter_semantics_changed)
        self.assertFalse(model.runtime_executed)
        self.assertFalse(model.upstream_write)

    def test_identity_transport_is_rejected(self) -> None:
        model = with_identity_transport(
            build_pydantika_coherent_projection()
        )
        report = compile_pydantika_coherent_projection(model)

        self.assertEqual(
            report["verdict"],
            ProjectionVerdict.REJECT.value,
        )
        self.assertIn(
            "identity_transport:SIGILBOOK_KERNEL",
            report["errors"],
        )

    def test_ouroboros_projection_is_bounded(self) -> None:
        model = build_pydantika_coherent_projection()

        self.assertEqual(model.ouroboros.finite_budget, 42)
        self.assertTrue(
            model.ouroboros.recur_requires_decreasing_residue
        )
        self.assertTrue(model.ouroboros.error_history_append_only)
        self.assertFalse(model.ouroboros.budget_reset_allowed)


if __name__ == "__main__":
    unittest.main()
