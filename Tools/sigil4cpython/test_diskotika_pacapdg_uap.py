import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "Lib"))

from sigil4cpython.pacapdg_uap_persistent_skill import (  # noqa: E402
    build_pacapdg_uap_persistent_skill_bundle,
    compile_pacapdg_uap_persistent_skill_bundle,
)
from diskotika_pacapdg_uap import (  # noqa: E402
    validate_diskotika_pacapdg_uap,
)


class DiskotikaPacapdgUapTests(unittest.TestCase):
    def setUp(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        self.payload = compile_pacapdg_uap_persistent_skill_bundle(bundle)

    def test_default_route_composes(self):
        certificate = validate_diskotika_pacapdg_uap(self.payload)
        self.assertTrue(certificate.sequential_composition_verified)
        self.assertTrue(certificate.pacapdg_typed)
        self.assertTrue(certificate.uap_typed)
        self.assertEqual(certificate.box_count, 6)
        self.assertEqual(certificate.domain, "PERSISTENT_PACA_SKILL_PACKET")
        self.assertEqual(certificate.codomain, "UAP_ADMISSION_WITNESS")
        self.assertFalse(certificate.trace_erased)
        self.assertFalse(certificate.identity_transported)
        self.assertFalse(certificate.runtime_executed)

    def test_noncomposable_route_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["diskotika_route"][1]["source_type"] = "BROKEN_SOURCE"
        with self.assertRaises(Exception):
            validate_diskotika_pacapdg_uap(payload)

    def test_wrong_domain_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["diskotika_route"][0]["source_type"] = "WRONG_DOMAIN"
        with self.assertRaisesRegex(
            ValueError,
            "diskotika_pacapdg_uap_domain_mismatch",
        ):
            validate_diskotika_pacapdg_uap(payload)

    def test_missing_stage_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["diskotika_route"].pop(2)
        with self.assertRaises(Exception):
            validate_diskotika_pacapdg_uap(payload)


if __name__ == "__main__":
    unittest.main()
