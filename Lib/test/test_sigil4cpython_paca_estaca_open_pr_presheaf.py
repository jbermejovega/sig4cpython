from dataclasses import replace
import unittest

from sigil4cpython.paca_estaca_open_pr_presheaf import (
    HOST_SECTION_KEY,
    KernelDecision,
    PresheafRestriction,
    REQUIRED_FACETS,
    build_reference_open_pr_presheaf,
    compile_reference_open_pr_presheaf,
    stable_digest,
)


class PacaEstacaOpenPrPresheafTests(unittest.TestCase):
    def test_reference_compiles_to_hold(self) -> None:
        ledger = build_reference_open_pr_presheaf()
        payload = compile_reference_open_pr_presheaf(ledger)
        self.assertEqual(payload["decision"], KernelDecision.HOLD.value)
        self.assertEqual(payload["selected_open_pr_count"], 7)
        self.assertFalse(payload["git_merge_executed"])
        self.assertFalse(payload["github_actions_invoked"])
        self.assertFalse(payload["interpreter_semantics_changed"])

    def test_full_paca_estaca_facet_cover(self) -> None:
        ledger = build_reference_open_pr_presheaf()
        facets = {facet for section in ledger.sections for facet in section.facets}
        self.assertTrue(REQUIRED_FACETS.issubset(facets))
        self.assertEqual(ledger.host_section_key, HOST_SECTION_KEY)

    def test_duplicate_pull_section_holds(self) -> None:
        ledger = build_reference_open_pr_presheaf()
        broken = replace(ledger, sections=ledger.sections + (ledger.sections[0],))
        self.assertIn("duplicate_pull_section", broken.validate())

    def test_identity_transport_rejects(self) -> None:
        ledger = build_reference_open_pr_presheaf()
        broken_section = replace(ledger.sections[0], identity_fixed=False)
        broken = replace(ledger, sections=(broken_section,) + ledger.sections[1:])
        payload = compile_reference_open_pr_presheaf(broken)
        self.assertEqual(payload["decision"], KernelDecision.REJECT.value)

    def test_cross_repository_scheduler_authority_rejects(self) -> None:
        ledger = build_reference_open_pr_presheaf()
        broken_restriction = replace(ledger.restrictions[0], scheduler_authority=True)
        broken = replace(
            ledger,
            restrictions=(broken_restriction,) + ledger.restrictions[1:],
        )
        payload = compile_reference_open_pr_presheaf(broken)
        self.assertEqual(payload["decision"], KernelDecision.REJECT.value)

    def test_shared_facet_mismatch_rejects(self) -> None:
        ledger = build_reference_open_pr_presheaf()
        source = ledger.restrictions[0]
        broken_restriction = PresheafRestriction(
            restriction_id=source.restriction_id,
            source_key=source.source_key,
            target_key=source.target_key,
            kind=source.kind,
            shared_facets=("NONEXISTENT_TYPED",),
            witness_digest=source.witness_digest,
            context_id=source.context_id,
        )
        broken = replace(
            ledger,
            restrictions=(broken_restriction,) + ledger.restrictions[1:],
        )
        payload = compile_reference_open_pr_presheaf(broken)
        self.assertEqual(payload["decision"], KernelDecision.REJECT.value)

    def test_digest_is_deterministic(self) -> None:
        first = compile_reference_open_pr_presheaf(build_reference_open_pr_presheaf())
        second = compile_reference_open_pr_presheaf(build_reference_open_pr_presheaf())
        self.assertEqual(first["compile_digest"], second["compile_digest"])
        self.assertEqual(stable_digest(first), stable_digest(second))


if __name__ == "__main__":
    unittest.main()
