import unittest
from dataclasses import replace

from sigil4cpython.pacapdg_uap_persistent_skill import (
    CANDIDATE_AST_ID,
    CANDIDATE_SEMANTICAL_KERNEL_ID,
    CANDIDATE_SYNTACTICAL_KERNEL_ID,
    REQUIRED_FACETS,
    UapCompileState,
    ValidatorStatus,
    build_pacapdg_uap_persistent_skill_bundle,
    compile_pacapdg_uap_persistent_skill_bundle,
)


class PacapdgUapPersistentSkillTests(unittest.TestCase):
    def test_default_bundle_emits_three_v2_candidates(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        payload = compile_pacapdg_uap_persistent_skill_bundle(bundle)

        self.assertEqual(payload["compile_state"], "ADMIT_PLAN_ONLY")
        self.assertEqual(
            payload["promotion_state"],
            "CANDIDATE_CANONICAL_NOT_PROMOTED",
        )
        self.assertTrue(payload["hosted_validation_required"])
        self.assertEqual(
            {item["artifact_id"] for item in payload["candidate_artifacts"]},
            {
                CANDIDATE_AST_ID,
                CANDIDATE_SYNTACTICAL_KERNEL_ID,
                CANDIDATE_SEMANTICAL_KERNEL_ID,
            },
        )
        self.assertTrue(set(REQUIRED_FACETS).issubset(payload["contract"]["facets"]))
        self.assertFalse(payload["runtime_executed"])
        self.assertFalse(payload["deployment_executed"])
        self.assertFalse(payload["git_merge_executed"])
        self.assertFalse(payload["branch_rewrite_executed"])
        self.assertFalse(payload["uap_execution_authorized"])
        self.assertFalse(payload["candidate_promoted"])
        self.assertFalse(payload["final_kapsyla"])

    def test_bundle_digest_is_deterministic(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        first = compile_pacapdg_uap_persistent_skill_bundle(bundle)
        second = compile_pacapdg_uap_persistent_skill_bundle(bundle)
        self.assertEqual(first["bundle_sha256"], second["bundle_sha256"])

    def test_missing_pacapdg_facet_is_rejected(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        facets = tuple(
            item for item in bundle.contract.facets if item != "PACAPDG_TYPED"
        )
        unsafe = replace(bundle, contract=replace(bundle.contract, facets=facets))
        payload = compile_pacapdg_uap_persistent_skill_bundle(unsafe)
        self.assertEqual(payload["compile_state"], UapCompileState.REJECT.value)
        self.assertTrue(
            any(
                item.startswith("pacapdg_uap_facets_missing:")
                for item in payload["obstruction_ledger"]
            )
        )

    def test_uap_execution_authority_is_rejected(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        unsafe = replace(
            bundle,
            contract=replace(bundle.contract, execution_authority=True),
        )
        payload = compile_pacapdg_uap_persistent_skill_bundle(unsafe)
        self.assertEqual(payload["compile_state"], UapCompileState.REJECT.value)
        self.assertIn(
            "pacapdg_uap_execution_authority",
            payload["obstruction_ledger"],
        )

    def test_candidate_premature_promotion_is_rejected(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        promoted_ast = replace(bundle.candidate_artifacts[0], promoted=True)
        unsafe = replace(
            bundle,
            candidate_artifacts=(promoted_ast,) + bundle.candidate_artifacts[1:],
        )
        payload = compile_pacapdg_uap_persistent_skill_bundle(unsafe)
        self.assertEqual(payload["compile_state"], UapCompileState.REJECT.value)
        self.assertIn(
            f"uap_candidate_premature_promotion:{CANDIDATE_AST_ID}",
            payload["obstruction_ledger"],
        )

    def test_noncanonical_stage_order_holds(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        reversed_order = tuple(reversed(bundle.contract.stage_order))
        unsafe = replace(
            bundle,
            contract=replace(bundle.contract, stage_order=reversed_order),
        )
        payload = compile_pacapdg_uap_persistent_skill_bundle(unsafe)
        self.assertEqual(
            payload["compile_state"],
            UapCompileState.HOLD_WITH_OBSTRUCTION.value,
        )
        self.assertIn(
            "pacapdg_uap_stage_order_mismatch",
            payload["obstruction_ledger"],
        )

    def test_failed_lean_validator_rejects(self):
        bundle = build_pacapdg_uap_persistent_skill_bundle()
        validators = tuple(
            replace(item, status=ValidatorStatus.FAIL)
            if item.validator_kind == "LENA_LEAN4"
            else item
            for item in bundle.validators
        )
        payload = compile_pacapdg_uap_persistent_skill_bundle(
            replace(bundle, validators=validators)
        )
        self.assertEqual(payload["compile_state"], UapCompileState.REJECT.value)
        self.assertIn(
            "uap_validator_failed:LENA_LEAN4",
            payload["obstruction_ledger"],
        )


if __name__ == "__main__":
    unittest.main()
