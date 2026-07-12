#!/usr/bin/env python3
# SPDX-License-Identifier: PSF-2.0
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sigil4cpython_hpc import (  # noqa: E402
    CONTRACT_ID,
    KERNEL_ID,
    build_contract,
    repository_root,
    source_tree_state,
    verify_contract,
)


class Sigil4CPythonContractTests(unittest.TestCase):
    def test_contract_round_trip(self) -> None:
        document = build_contract()

        self.assertEqual(document["contract_id"], CONTRACT_ID)
        self.assertTrue(verify_contract(document))
        self.assertEqual(document["profile"]["pypl_profile"], "SIG4PYPL")
        self.assertEqual(document["jarramplas_boundary"]["kernel_id"], KERNEL_ID)
        self.assertFalse(document["jarramplas_boundary"]["identity_seed_transport"])
        self.assertFalse(document["jarramplas_boundary"]["plural_type_collapse"])

    def test_tampered_contract_is_rejected(self) -> None:
        document = build_contract()
        tampered = copy.deepcopy(document)
        tampered["profile"]["no_identity_transport"] = False

        self.assertFalse(verify_contract(tampered))

    def test_hpc_boundary_is_optional_and_non_mutating(self) -> None:
        document = build_contract()
        boundary = document["hpc_boundary"]

        self.assertTrue(boundary["single_rank_fallback"])
        self.assertTrue(boundary["openmpi_optional"])
        self.assertFalse(boundary["scheduler_mutation"])
        self.assertFalse(boundary["performance_claim_without_benchmark"])

    def test_expected_cpython_source_witnesses_are_present(self) -> None:
        state = source_tree_state(repository_root())

        self.assertTrue(state["complete"], state)
        self.assertIn("Python version", state["version_banner"])


if __name__ == "__main__":
    unittest.main()
