import json
from pathlib import Path
import sys
import unittest

from pydantic import ValidationError

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parents[1]
sys.path.insert(0, str(TOOLS_DIR))

from discopy_kqc_projection import build_discopy_projection_plan
from kqc_publication_models import (
    KQCPublicationSheafModel,
    compile_pydantika_publication_sheaf,
)


EXAMPLE = ROOT / "Misc" / "sigil4cpython" / "kqc_publication_sheaf_v1.json"


class PydantikaPublicationModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_source_bound_example_compiles_deterministically(self):
        certificate = compile_pydantika_publication_sheaf(self.payload)
        self.assertEqual(len(certificate.payload_digest), 64)
        self.assertTrue(certificate.serialization_round_trip_verified)
        self.assertFalse(certificate.source_files_copied)
        self.assertFalse(certificate.upstream_write_performed)
        self.assertFalse(certificate.runtime_executed)

    def test_unknown_semantic_authority_is_rejected(self):
        payload = dict(self.payload)
        payload["unknown_semantic_authority"] = True
        with self.assertRaisesRegex(ValidationError, "extra_forbidden"):
            KQCPublicationSheafModel.model_validate(payload)

    def test_upstream_hop_must_be_plan_only(self):
        payload = json.loads(json.dumps(self.payload))
        payload["publication_hops"][1]["authority"] = "WRITE_OWN_REPOSITORY"
        with self.assertRaisesRegex(ValidationError, "upstream_authority_must_be_plan_only"):
            KQCPublicationSheafModel.model_validate(payload)

    def test_cpython_bytecode_adaptive_jit_path_is_discopy_composable(self):
        plan = build_discopy_projection_plan(self.payload["kernels"][1:4])
        self.assertTrue(plan.composable)
        self.assertEqual(plan.obstruction_ledger, ())
        self.assertFalse(plan.backend_executed)
        self.assertFalse(plan.publication_performed)

    def test_mixed_compiler_branches_remain_noncomposable(self):
        plan = build_discopy_projection_plan(self.payload["kernels"])
        self.assertFalse(plan.composable)
        self.assertTrue(plan.obstruction_ledger)


if __name__ == "__main__":
    unittest.main()
