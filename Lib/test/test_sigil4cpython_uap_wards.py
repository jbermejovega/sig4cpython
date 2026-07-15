import unittest

from sigil4cpython.uap_wards import (
    UAPWard,
    build_pacadocencia_uap_kernel,
    kokompile_kernel,
    validate_kokompiled_kernel,
)


class Sigil4CPythonUAPWardsTests(unittest.TestCase):
    def test_default_kernel_validates(self):
        kernel = build_pacadocencia_uap_kernel()
        payload = validate_kokompiled_kernel(kernel)
        self.assertTrue(payload["accepted"])
        self.assertEqual(payload["kernel_id"], "SIGIL4CPYTHON_PACADOCENCIA_UAP_WARDS_V1")
        self.assertIn("kernel_sha256", payload)

    def test_unknown_hyperedge_vertex_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown vertices"):
            kokompile_kernel(
                "bad",
                ["known"],
                [["known", "missing"]],
                [UAPWard("trace", "invariant", "source")],
            )

    def test_obstruction_ward_requires_witness(self):
        kernel = kokompile_kernel(
            "blocked",
            ["trace"],
            [["trace"]],
            [UAPWard("blocked", "trace must remain", "source", status="obstruction")],
        )
        with self.assertRaisesRegex(ValueError, "obstructions_keep_witness"):
            validate_kokompiled_kernel(kernel)


if __name__ == "__main__":
    unittest.main()
