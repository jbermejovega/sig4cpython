import sys
import unittest
from copy import deepcopy
from pathlib import Path

from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "Lib"))

from sigil4cpython.pacapdg_uap_persistent_skill import (  # noqa: E402
    build_pacapdg_uap_persistent_skill_bundle,
    compile_pacapdg_uap_persistent_skill_bundle,
)
from pacapdg_uap_persistent_skill_models import (  # noqa: E402
    PacapdgUapPersistentSkillPayloadModel,
    _stable_digest,
    compile_pydantika_pacapdg_uap,
)


class PydantikaPacapdgUapTests(unittest.TestCase):
    def setUp(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        self.payload = compile_pacapdg_uap_persistent_skill_bundle(bundle)

    def _resign(self, payload):
        unsigned = dict(payload)
        unsigned.pop("bundle_sha256", None)
        payload["bundle_sha256"] = _stable_digest(unsigned)

    def test_default_payload_round_trips(self):
        certificate = compile_pydantika_pacapdg_uap(self.payload)
        self.assertTrue(certificate.pydantika_round_trip_verified)
        self.assertTrue(certificate.pacapdg_typed)
        self.assertTrue(certificate.uap_typed)
        self.assertEqual(certificate.artifact_count, 3)
        self.assertEqual(len(certificate.artifact_digests), 3)
        self.assertFalse(certificate.candidate_promoted)

    def test_bundle_digest_tampering_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["compile_state"] = "HOLD_WITH_OBSTRUCTION"
        with self.assertRaisesRegex(
            ValueError,
            "pacapdg_uap_bundle_digest_mismatch",
        ):
            compile_pydantika_pacapdg_uap(payload)

    def test_extra_field_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["undeclared_runtime_authority"] = True
        self._resign(payload)
        with self.assertRaisesRegex(ValidationError, "extra_forbidden"):
            PacapdgUapPersistentSkillPayloadModel.model_validate(payload)

    def test_missing_pacapdg_facet_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["contract"]["facets"] = tuple(
            item
            for item in payload["contract"]["facets"]
            if item != "PACAPDG_TYPED"
        )
        self._resign(payload)
        with self.assertRaisesRegex(
            ValidationError,
            "pacapdg_uap_required_facets_missing",
        ):
            PacapdgUapPersistentSkillPayloadModel.model_validate(payload)

    def test_candidate_promotion_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["candidate_artifacts"][0]["promoted"] = True
        self._resign(payload)
        with self.assertRaisesRegex(ValidationError, "literal_error"):
            PacapdgUapPersistentSkillPayloadModel.model_validate(payload)

    def test_noncomposable_route_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["diskotika_route"][1]["source_type"] = "BROKEN_SOURCE"
        self._resign(payload)
        with self.assertRaisesRegex(
            ValidationError,
            "pacapdg_uap_noncomposable_route",
        ):
            PacapdgUapPersistentSkillPayloadModel.model_validate(payload)


if __name__ == "__main__":
    unittest.main()
