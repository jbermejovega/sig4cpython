import unittest
from dataclasses import replace

from sigil4cpython.localization_polyglot import (
    BindingAuthority,
    OpenMPICompliance,
    build_polyglot_localization_kernel,
    compile_polyglot_localization_kernel,
)


class Sigil4CPythonLocalizationPolyglotTests(unittest.TestCase):
    def test_default_polyglot_localization_kernel_is_admitted(self):
        kernel = build_polyglot_localization_kernel()
        payload = compile_polyglot_localization_kernel(kernel)
        self.assertEqual(payload["uap_state"], "ADMIT")
        self.assertFalse(payload["runtime_executed"])
        self.assertFalse(payload["external_imports_performed"])
        self.assertFalse(payload["hardware_or_scheduler_mutation"])
        self.assertIn("kernel_sha256", payload)

    def test_aperiodic_tile_periodic_drift_holds(self):
        kernel = build_polyglot_localization_kernel()
        bad_tile = replace(kernel.tiles[0], nonperiodic_witness=False)
        payload = compile_polyglot_localization_kernel(
            replace(kernel, tiles=(bad_tile,) + kernel.tiles[1:])
        )
        self.assertEqual(payload["uap_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertIn(
            "aperiodic_tile_periodic_drift:tile:dynamic-automorphism",
            payload["obstruction_ledger"],
        )

    def test_openmpi_scheduler_mutation_is_rejected(self):
        kernel = build_polyglot_localization_kernel()
        bad_openmpi = OpenMPICompliance(
            "openmpi:strikk-compliance",
            "bind:openmpi:compliance",
            "explicit_mpiexec_rank_witness_or_single_rank_fallback",
            scheduler_mutation=True,
        )
        payload = compile_polyglot_localization_kernel(
            replace(kernel, openmpi_compliance=bad_openmpi)
        )
        self.assertEqual(payload["uap_state"], "REJECT")
        self.assertIn(
            "openmpi_scheduler_mutation:openmpi:strikk-compliance",
            payload["obstruction_ledger"],
        )

    def test_homomorphic_displacement_requires_krone_authority(self):
        kernel = build_polyglot_localization_kernel()
        bad_policy = replace(
            kernel.homomorphic_policy,
            displacement_authority=BindingAuthority.VIRTUAL_ONLY,
        )
        payload = compile_polyglot_localization_kernel(
            replace(kernel, homomorphic_policy=bad_policy)
        )
        self.assertEqual(payload["uap_state"], "REJECT")
        self.assertIn(
            "homomorphic_policy_krone_authority_missing:"
            "policy:mahadev-homomorphic-encoding-krone-displacement",
            payload["obstruction_ledger"],
        )

    def test_linter_normalization_preserves_trace(self):
        kernel = build_polyglot_localization_kernel()
        bad_rule = replace(
            kernel.lexical_normalizations[0],
            preserve_input_trace=False,
        )
        payload = compile_polyglot_localization_kernel(
            replace(
                kernel,
                lexical_normalizations=(
                    bad_rule,
                )
                + kernel.lexical_normalizations[1:],
            )
        )
        self.assertEqual(payload["uap_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertIn(
            "lexical_trace_not_preserved:endofukntor",
            payload["obstruction_ledger"],
        )

    def test_missing_source_url_holds_with_obstruction(self):
        kernel = build_polyglot_localization_kernel()
        payload = compile_polyglot_localization_kernel(
            replace(kernel, source_urls=kernel.source_urls[:-1])
        )
        self.assertEqual(payload["uap_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertIn(
            "polyglot_localization_source_url_missing",
            payload["obstruction_ledger"],
        )


if __name__ == "__main__":
    unittest.main()
