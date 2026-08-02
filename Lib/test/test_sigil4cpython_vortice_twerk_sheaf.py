from dataclasses import replace
import unittest

from sigil4cpython.vortice_twerk_sheaf import (
    ProjectionVerdict,
    build_projection,
    compile_projection,
    with_identity_transport,
)


class VorticeTwerkSheafTests(unittest.TestCase):
    def test_projection_is_admitted_and_dependency_free(self) -> None:
        projection = build_projection()
        compiled = compile_projection(projection)

        self.assertEqual(projection.validate(), ())
        self.assertEqual(compiled["verdict"], ProjectionVerdict.ADMIT.value)
        self.assertFalse(compiled["runtime_executed"])
        self.assertFalse(compiled["interpreter_semantics_changed"])
        self.assertEqual(len(compiled["projection_sha256"]), 64)

    def test_digest_is_deterministic(self) -> None:
        self.assertEqual(build_projection().digest(), build_projection().digest())

    def test_identity_transport_is_rejected(self) -> None:
        compiled = compile_projection(with_identity_transport(build_projection()))
        self.assertEqual(compiled["verdict"], ProjectionVerdict.REJECT.value)
        self.assertTrue(any("identity_transport" in error for error in compiled["errors"]))

    def test_interpreter_semantic_change_is_rejected(self) -> None:
        projection = replace(build_projection(), interpreter_semantics_changed=True)
        compiled = compile_projection(projection)
        self.assertEqual(compiled["verdict"], ProjectionVerdict.REJECT.value)
        self.assertIn("forbidden_projection_effect", compiled["errors"])


if __name__ == "__main__":
    unittest.main()
