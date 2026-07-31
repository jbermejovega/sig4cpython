"""Focused tests for the SIGIL4CPython universal presheaf kernel."""

from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from sigil4cpython.universal_presheaf_pipeline import (  # noqa: E402
    GLOBAL_SECTION_ID,
    PipelinePhase,
    PipelineStage,
    PresheafState,
    SectionKind,
    build_universal_presheaf_kernel,
    compile_universal_presheaf_kernel,
)


class UniversalPresheafPipelineTests(unittest.TestCase):
    def test_default_kernel_is_structurally_valid(self) -> None:
        kernel = build_universal_presheaf_kernel()
        self.assertEqual(kernel.validate(), ())
        self.assertEqual(len(kernel.epochs), 4)
        self.assertEqual({item.kind for item in kernel.sections}, set(SectionKind))

    def test_compile_holds_open_epochs_without_merging(self) -> None:
        state, payload = compile_universal_presheaf_kernel()
        self.assertEqual(state, PresheafState.HOLD_WITH_OBSTRUCTION)
        self.assertFalse(payload["git_merge_executed"])
        self.assertFalse(payload["main_mutated"])
        self.assertFalse(payload["runtime_executed"])

    def test_every_local_section_has_global_restriction(self) -> None:
        kernel = build_universal_presheaf_kernel()
        local_ids = {item.section_id for item in kernel.sections if item.local}
        restricted = {item.target_section_id for item in kernel.restrictions}
        self.assertEqual(local_ids, restricted)
        self.assertTrue(all(item.source_section_id == GLOBAL_SECTION_ID for item in kernel.restrictions))

    def test_ledger_merge_preserves_open_pr_identity_and_order(self) -> None:
        kernel = build_universal_presheaf_kernel()
        epoch_ids = tuple(item.epoch_id for item in kernel.epochs)
        self.assertEqual(kernel.ledger_merge.input_epoch_ids, epoch_ids)
        self.assertEqual(kernel.ledger_merge.output_epoch_ids, epoch_ids)
        self.assertFalse(kernel.ledger_merge.git_merge_executed)
        self.assertFalse(kernel.ledger_merge.authority_expansion)

    def test_duplicate_epoch_identity_rejected(self) -> None:
        kernel = build_universal_presheaf_kernel()
        duplicate = replace(kernel.epochs[1], epoch_id=kernel.epochs[0].epoch_id)
        broken = replace(kernel, epochs=(kernel.epochs[0], duplicate, *kernel.epochs[2:]))
        self.assertIn("duplicate_pr_epoch_identity", broken.validate())

    def test_missing_restriction_rejected(self) -> None:
        kernel = build_universal_presheaf_kernel()
        broken = replace(kernel, restrictions=kernel.restrictions[:-1])
        self.assertIn("presheaf_restriction_family_incomplete", broken.validate())

    def test_pipeline_cycle_rejected(self) -> None:
        kernel = build_universal_presheaf_kernel()
        stages = list(kernel.stages)
        stages[0] = PipelineStage(
            stage_id=stages[0].stage_id,
            phase=PipelinePhase.INGEST_LEDGER,
            dependency_ids=(stages[-1].stage_id,),
            input_types=stages[0].input_types,
            output_types=stages[0].output_types,
        )
        broken = replace(kernel, stages=tuple(stages))
        self.assertIn("pipeline_scheduler_cycle", broken.validate())

    def test_open_pr_cannot_absorb_authority(self) -> None:
        kernel = build_universal_presheaf_kernel()
        epoch = replace(kernel.epochs[0], authority_absorbed=True)
        broken = replace(kernel, epochs=(epoch, *kernel.epochs[1:]))
        self.assertTrue(any("pr_epoch_authority_absorption" in item for item in broken.validate()))

    def test_digest_is_deterministic(self) -> None:
        first = build_universal_presheaf_kernel().to_dict()["kernel_sha256"]
        second = build_universal_presheaf_kernel().to_dict()["kernel_sha256"]
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)


if __name__ == "__main__":
    unittest.main()
