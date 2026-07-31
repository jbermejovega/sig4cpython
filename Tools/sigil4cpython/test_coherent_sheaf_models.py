import json
from pathlib import Path
import sys
import unittest

from pydantic import ValidationError

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parents[1]
sys.path.insert(0, str(TOOLS_DIR))
sys.path.insert(0, str(ROOT / "Lib"))

from coherent_sheaf_models import (
    PydantikaCoherentSheafModel,
    compile_pydantika_coherent_sheaf_model,
)
from sigil4cpython.coherent_sheaf import build_pydantika_coherent_sheaf


class PydantikaCoherentSheafModelTests(unittest.TestCase):
    def payload(self):
        payload = build_pydantika_coherent_sheaf().to_dict()
        payload.pop("sheaf_sha256")
        payload["pydantika_is_tooling_not_stdlib_dependency"] = True
        payload["human_review_required"] = True
        return json.loads(json.dumps(payload))

    def test_default_coherent_sheaf_round_trips(self):
        certificate = compile_pydantika_coherent_sheaf_model(self.payload())
        self.assertEqual(len(certificate.payload_digest), 64)
        self.assertFalse(certificate.runtime_executed)
        self.assertFalse(certificate.resource_access_performed)

    def test_extra_authority_is_rejected(self):
        payload = self.payload()
        payload["unknown_authority"] = True
        with self.assertRaisesRegex(ValidationError, "extra_forbidden"):
            PydantikaCoherentSheafModel.model_validate(payload)

    def test_missing_required_surface_is_rejected(self):
        payload = self.payload()
        payload["kernels"] = payload["kernels"][:-1]
        with self.assertRaisesRegex(
            ValidationError,
            "coherent_sheaf_required_surface_missing",
        ):
            PydantikaCoherentSheafModel.model_validate(payload)

    def test_void_ouroboros_phase_boundary_is_required(self):
        payload = self.payload()
        payload["ouroboros_flows"][0]["phases"] = ["ANNOTATE", "TRACE"]
        with self.assertRaisesRegex(
            ValidationError,
            "ouroboros_flow_phase_incomplete",
        ):
            PydantikaCoherentSheafModel.model_validate(payload)


if __name__ == "__main__":
    unittest.main()
