"""Tooling tests for Pydantika universal-presheaf models."""

from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[1]
sys.path.append(str(ROOT / "Lib"))
sys.path.append(str(TOOLS))

from universal_presheaf_models import (  # noqa: E402
    UniversalPresheafModel,
    compile_universal_presheaf_models,
)


class UniversalPresheafModelTests(unittest.TestCase):
    def test_compilation_certificate(self) -> None:
        model, certificate = compile_universal_presheaf_models()
        self.assertEqual(certificate.state, "HOLD_WITH_OBSTRUCTION")
        self.assertEqual(certificate.epoch_count, 4)
        self.assertEqual(certificate.section_count, 8)
        self.assertFalse(certificate.git_merge_executed)
        self.assertEqual(len(certificate.payload_digest), 64)
        self.assertEqual(model.rulezero, "PIORNALEGO_ES_CANON")

    def test_round_trip(self) -> None:
        model, _ = compile_universal_presheaf_models()
        rebuilt = UniversalPresheafModel.model_validate_json(model.model_dump_json())
        self.assertEqual(model, rebuilt)

    def test_open_epochs_remain_distinct(self) -> None:
        model, _ = compile_universal_presheaf_models()
        ids = tuple(item.epoch_id for item in model.epochs)
        self.assertEqual(ids, model.ledger_merge.output_epoch_ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_paca_estaca_section_exists(self) -> None:
        model, _ = compile_universal_presheaf_models()
        kinds = {item.kind for item in model.sections}
        self.assertIn("PACA_ESTACA", kinds)
        self.assertIn("UNIVERSAL_ABSTRAKTA_PIPELINE", kinds)
        self.assertIn("QUNO_NORMA_ADJOINT_EPOCHS", kinds)

    def test_no_execution_or_authority_expansion(self) -> None:
        model, certificate = compile_universal_presheaf_models()
        self.assertFalse(model.runtime_executed)
        self.assertFalse(model.repository_mutated)
        self.assertFalse(model.ledger_merge.authority_expansion)
        self.assertFalse(certificate.final_kapsyla)


if __name__ == "__main__":
    unittest.main()
