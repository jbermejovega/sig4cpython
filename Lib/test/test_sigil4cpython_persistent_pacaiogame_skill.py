import unittest
from dataclasses import replace

from sigil4cpython.persistent_pacaiogame_skill import (
    CANONICAL_AST_ID,
    CANONICAL_SEMANTICAL_KERNEL_ID,
    CANONICAL_SYNTACTICAL_KERNEL_ID,
    ValidatorKind,
    ValidatorStatus,
    build_persistent_pacaiogame_skill_compiler,
    compile_persistent_pacaiogame_skill_compiler,
)


class PersistentPacaIoGameSkillCompilerTests(unittest.TestCase):
    def test_default_compiler_emits_three_canonical_artifacts(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        payload = compile_persistent_pacaiogame_skill_compiler(compiler)

        self.assertEqual(payload["compile_state"], "ADMIT_PLAN_ONLY")
        self.assertTrue(payload["hosted_validation_required"])
        self.assertEqual(
            {item["artifact_id"] for item in payload["canonical_artifacts"]},
            {
                CANONICAL_AST_ID,
                CANONICAL_SYNTACTICAL_KERNEL_ID,
                CANONICAL_SEMANTICAL_KERNEL_ID,
            },
        )
        self.assertFalse(payload["runtime_executed"])
        self.assertFalse(payload["deployment_executed"])
        self.assertFalse(payload["git_merge_executed"])
        self.assertFalse(payload["branch_rewrite_executed"])
        self.assertFalse(payload["final_kapsyla"])

    def test_compilation_digest_is_deterministic(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        first = compile_persistent_pacaiogame_skill_compiler(compiler)
        second = compile_persistent_pacaiogame_skill_compiler(compiler)
        self.assertEqual(first["compiler_sha256"], second["compiler_sha256"])

    def test_arakne_physical_git_merge_is_rejected(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        unsafe = replace(
            compiler,
            arakne=replace(compiler.arakne, git_merge_executed=True),
        )
        payload = compile_persistent_pacaiogame_skill_compiler(unsafe)
        self.assertEqual(payload["compile_state"], "REJECT")
        self.assertIn(
            "arakne_git_merge_executed:"
            "arakne:source-bound-open-pr-semantic-fusion",
            payload["obstruction_ledger"],
        )

    def test_paca_antorcha_execution_is_rejected(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        unsafe = replace(
            compiler,
            paca_antorcha=replace(compiler.paca_antorcha, model_executed=True),
        )
        payload = compile_persistent_pacaiogame_skill_compiler(unsafe)
        self.assertEqual(payload["compile_state"], "REJECT")
        self.assertIn(
            "paca_antorcha_model_execution:"
            "paca-antorcha:persistent-skill-normalizer",
            payload["obstruction_ledger"],
        )

    def test_noncomposable_diskotika_chain_holds(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        second = replace(
            compiler.diskotika.morphisms[1],
            source_type=CANONICAL_AST_ID,
        )
        unsafe = replace(
            compiler,
            diskotika=replace(
                compiler.diskotika,
                morphisms=(compiler.diskotika.morphisms[0], second),
            ),
        )
        payload = compile_persistent_pacaiogame_skill_compiler(unsafe)
        self.assertEqual(payload["compile_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertTrue(
            any(
                item.startswith("diskotika_noncomposable_chain:")
                for item in payload["obstruction_ledger"]
            )
        )

    def test_failed_lean_witness_rejects(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        validators = tuple(
            replace(item, status=ValidatorStatus.FAIL)
            if item.validator == ValidatorKind.LENA_LEAN4
            else item
            for item in compiler.validators
        )
        payload = compile_persistent_pacaiogame_skill_compiler(
            replace(compiler, validators=validators)
        )
        self.assertEqual(payload["compile_state"], "REJECT")
        self.assertIn(
            "validator_failed:LENA_LEAN4",
            payload["obstruction_ledger"],
        )

    def test_annotation_plural_collapse_is_rejected(self):
        compiler = build_persistent_pacaiogame_skill_compiler()
        bad_annotation = replace(compiler.annotations[0], plural_typed=False)
        payload = compile_persistent_pacaiogame_skill_compiler(
            replace(compiler, annotations=(bad_annotation,))
        )
        self.assertEqual(payload["compile_state"], "REJECT")
        self.assertIn(
            "annotated_type_plural_collapse:"
            "annotation:persistent-pacaiogame-sigil4godot",
            payload["obstruction_ledger"],
        )


if __name__ == "__main__":
    unittest.main()
