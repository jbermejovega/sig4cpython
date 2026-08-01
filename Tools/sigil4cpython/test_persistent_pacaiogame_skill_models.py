import sys
import unittest
from copy import deepcopy
from pathlib import Path

from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "Lib"))

from sigil4cpython.persistent_pacaiogame_skill import (  # noqa: E402
    build_persistent_pacaiogame_skill_compiler,
    compile_persistent_pacaiogame_skill_compiler,
)
from persistent_pacaiogame_skill_models import (  # noqa: E402
    PersistentPacaSkillCompilerPayloadModel,
    compile_pydantika_persistent_skill,
)


class PydantikaPersistentPacaSkillTests(unittest.TestCase):
    def setUp(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        self.payload = compile_persistent_pacaiogame_skill_compiler(compiler)

    def test_default_payload_round_trips(self):
        certificate = compile_pydantika_persistent_skill(self.payload)
        self.assertTrue(certificate.compiler_digest_verified)
        self.assertTrue(certificate.serialization_round_trip_verified)
        self.assertEqual(certificate.canonical_artifact_count, 3)
        self.assertEqual(len(certificate.artifact_digests), 3)

    def test_compiler_digest_tampering_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["compile_state"] = "HOLD_WITH_OBSTRUCTION"
        with self.assertRaisesRegex(ValueError, "compiler_digest_mismatch"):
            compile_pydantika_persistent_skill(payload)

    def test_extra_field_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["unexpected_authority"] = True
        unsigned = dict(payload)
        unsigned.pop("compiler_sha256")
        from persistent_pacaiogame_skill_models import _stable_digest

        payload["compiler_sha256"] = _stable_digest(unsigned)
        with self.assertRaisesRegex(ValidationError, "extra_forbidden"):
            PersistentPacaSkillCompilerPayloadModel.model_validate(payload)

    def test_physical_arakne_merge_is_rejected_by_model(self):
        payload = deepcopy(self.payload)
        payload["arakne"]["git_merge_executed"] = True
        unsigned = dict(payload)
        unsigned.pop("compiler_sha256")
        from persistent_pacaiogame_skill_models import _stable_digest

        payload["compiler_sha256"] = _stable_digest(unsigned)
        with self.assertRaisesRegex(
            ValidationError,
            "arakne_git_merge_boundary_broken",
        ):
            PersistentPacaSkillCompilerPayloadModel.model_validate(payload)

    def test_missing_validator_is_rejected(self):
        payload = deepcopy(self.payload)
        payload["validator_states"].pop("LENA_LEAN4")
        unsigned = dict(payload)
        unsigned.pop("compiler_sha256")
        from persistent_pacaiogame_skill_models import _stable_digest

        payload["compiler_sha256"] = _stable_digest(unsigned)
        with self.assertRaisesRegex(
            ValidationError,
            "persistent_validator_family_incomplete",
        ):
            PersistentPacaSkillCompilerPayloadModel.model_validate(payload)


if __name__ == "__main__":
    unittest.main()
