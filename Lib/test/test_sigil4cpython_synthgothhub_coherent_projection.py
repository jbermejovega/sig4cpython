import unittest

from sigil4cpython.synthgothhub_coherent_projection import (
    EXPECTED_END_LINE,
    build_receipt,
    validate_projection_document,
    verify_fixed_point,
)

DOCUMENT = """projection SYNTHGOTHHUB_SIGIL4CPYTHON_PROJECTION_V1
author Jara Juana Bermejo-Vega / JJBV
source sigilbook#695@5f5d0f0b776d34077a22e897d8ec68cab6637d42
target jbermejovega/sigil4cpython
section SECTION_SIGIL4CPYTHON_PUBLIC
kernel SIGIL_PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK_KERNEL_V1
pi PI:SYNTHGOTHHUB:COHERENT_SHEAF:CYTHON:V1
invariant NO_IDENTITY_TRANSPORT
invariant NO_PLURAL_COLLAPSE
invariant TRACE_PRESERVED
invariant OBSTRUCTION_PRESERVED
end SYNTHGOTHHUB_SIGIL4CPYTHON_PROJECTION_V1"""


class ProjectionTests(unittest.TestCase):
    def test_projection_admits(self):
        self.assertEqual(validate_projection_document(DOCUMENT), ())
        receipt = build_receipt(DOCUMENT)
        self.assertTrue(verify_fixed_point(receipt))
        self.assertTrue(receipt.dependency_free_runtime)
        self.assertFalse(receipt.interpreter_semantics_changed)
        self.assertFalse(receipt.cython_stdlib_dependency_added)

    def test_missing_end_line_rejects(self):
        errors = validate_projection_document(DOCUMENT.rsplit("\n", 1)[0])
        self.assertIn("EXACT_END_LINE_MISSING", errors)

    def test_duplicate_end_line_rejects(self):
        errors = validate_projection_document(DOCUMENT + "\n" + EXPECTED_END_LINE)
        self.assertIn("END_LINE_NOT_UNIQUE", errors)

    def test_source_head_drift_rejects(self):
        errors = validate_projection_document(DOCUMENT.replace("5f5d0f0", "0000000"))
        self.assertTrue(any(item.startswith("MISSING_LINE:source") for item in errors))


if __name__ == "__main__":
    unittest.main()
