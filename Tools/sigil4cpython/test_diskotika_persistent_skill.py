import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "Lib"))

from sigil4cpython.persistent_pacaiogame_skill import (  # noqa: E402
    build_persistent_pacaiogame_skill_compiler,
    compile_persistent_pacaiogame_skill_compiler,
)
from diskotika_persistent_skill import (  # noqa: E402
    validate_diskotika_persistent_skill,
)


class DiskotikaPersistentSkillTests(unittest.TestCase):
    def setUp(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        self.payload = compile_persistent_pacaiogame_skill_compiler(compiler)

    def test_declared_chain_is_sequentially_composable(self):
        certificate = validate_diskotika_persistent_skill(self.payload)
        self.assertTrue(certificate.sequential_composition_verified)
        self.assertEqual(certificate.domain, "SIGIL_AST_V1")
        self.assertEqual(certificate.codomain, "SIGIL_SEMANTICAL_KERNEL_V1")
        self.assertEqual(certificate.box_count, 2)
        self.assertFalse(certificate.symmetry_inferred)
        self.assertFalse(certificate.trace_erased)
        self.assertFalse(certificate.runtime_executed)

    def test_broken_chain_is_rejected_by_discopy(self):
        payload = deepcopy(self.payload)
        payload["diskotika"]["morphisms"][1]["source_type"] = "SIGIL_AST_V1"
        with self.assertRaises(Exception):
            validate_diskotika_persistent_skill(payload)


if __name__ == "__main__":
    unittest.main()
