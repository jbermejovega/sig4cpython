import json
from pathlib import Path
import sys
import unittest

from pydantic import ValidationError

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parents[1]
sys.path.insert(0, str(TOOLS_DIR))

from localization_polyglot_models import (  # noqa: E402
    PolyglotLocalizationKernelModel,
    compile_pydantika_polyglot_localization_kernel,
)

# Add the experimental package only after Pydantika imports.  On GitHub
# Actions this checkout's Lib/ can otherwise shadow the runner stdlib.
sys.path.insert(0, str(ROOT / "Lib"))

from sigil4cpython.localization_polyglot import (  # noqa: E402
    build_polyglot_localization_kernel,
)


class PydantikaPolyglotLocalizationModelTests(unittest.TestCase):
    def payload(self):
        payload = build_polyglot_localization_kernel().to_dict()
        payload.pop("kernel_sha256")
        payload["pydantika_is_tooling_not_stdlib_dependency"] = True
        payload["human_review_required"] = True
        return json.loads(json.dumps(payload))

    def test_default_polyglot_localization_round_trips(self):
        certificate = compile_pydantika_polyglot_localization_kernel(
            self.payload()
        )
        self.assertEqual(len(certificate.payload_digest), 64)
        self.assertFalse(certificate.runtime_executed)
        self.assertFalse(certificate.external_imports_performed)
        self.assertFalse(certificate.hardware_or_scheduler_mutation)

    def test_extra_authority_is_rejected(self):
        payload = self.payload()
        payload["linux_kernel_driver"] = True
        with self.assertRaisesRegex(ValidationError, "extra_forbidden"):
            PolyglotLocalizationKernelModel.model_validate(payload)

    def test_missing_source_url_is_rejected(self):
        payload = self.payload()
        payload["source_urls"] = payload["source_urls"][:-1]
        with self.assertRaisesRegex(
            ValidationError,
            "polyglot_localization_source_url_missing",
        ):
            PolyglotLocalizationKernelModel.model_validate(payload)

    def test_openmpi_scheduler_mutation_is_rejected(self):
        payload = self.payload()
        payload["openmpi_compliance"]["scheduler_mutation"] = True
        with self.assertRaisesRegex(ValidationError, "literal_error"):
            PolyglotLocalizationKernelModel.model_validate(payload)

    def test_aperiodic_tile_annotation_is_required(self):
        payload = self.payload()
        payload["tiles"][0]["pydantika_annotation_id"] = "ann:missing"
        with self.assertRaisesRegex(
            ValidationError,
            "aperiodic_tile_unknown_annotation",
        ):
            PolyglotLocalizationKernelModel.model_validate(payload)

    def test_homomorphic_displacement_requires_krone(self):
        payload = self.payload()
        payload["homomorphic_policy"]["displacement_authority"] = "VIRTUAL_ONLY"
        with self.assertRaisesRegex(ValidationError, "literal_error"):
            PolyglotLocalizationKernelModel.model_validate(payload)


if __name__ == "__main__":
    unittest.main()
