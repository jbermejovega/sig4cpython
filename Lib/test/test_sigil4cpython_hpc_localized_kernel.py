import unittest
from dataclasses import replace

from sigil4cpython.hpc_localized_kernel import (
    FPGAResourceProfile,
    HPCLocalizedKernel,
    KernelSpace,
    build_hpc_localized_quazris_kernel,
    compile_hpc_localized_quazris_kernel,
)


class Sigil4CPythonHPCLocalizedKernelTests(unittest.TestCase):
    def test_default_hpc_localized_kernel_is_admitted(self):
        kernel = build_hpc_localized_quazris_kernel()
        payload = compile_hpc_localized_quazris_kernel(kernel)
        self.assertEqual(payload["uap_state"], "ADMIT")
        self.assertFalse(payload["runtime_executed"])
        self.assertFalse(payload["hardware_synthesis_performed"])
        self.assertFalse(payload["scheduler_job_submitted"])
        self.assertIn("kernel_sha256", payload)

    def test_hardware_synthesis_attempt_is_rejected(self):
        kernel = replace(
            build_hpc_localized_quazris_kernel(),
            hardware_synthesis_performed=True,
        )
        payload = compile_hpc_localized_quazris_kernel(kernel)
        self.assertEqual(payload["uap_state"], "REJECT")
        self.assertIn(
            "hpc_localized_kernel_hardware_synthesis_forbidden",
            payload["obstruction_ledger"],
        )

    def test_direct_api_hardware_call_is_rejected(self):
        kernel = build_hpc_localized_quazris_kernel()
        bad_api = replace(kernel.sigil_api, direct_hardware_calls=True)
        payload = compile_hpc_localized_quazris_kernel(
            replace(kernel, sigil_api=bad_api)
        )
        self.assertEqual(payload["uap_state"], "REJECT")
        self.assertIn(
            "sigil_api_direct_hardware_access_forbidden:"
            "api:sigil4cpython-hpc-localized",
            payload["obstruction_ledger"],
        )

    def test_morphism_without_dataflow_activation_holds(self):
        kernel = build_hpc_localized_quazris_kernel()
        bad_morphism = replace(kernel.morphisms[0], data_activated=False)
        payload = compile_hpc_localized_quazris_kernel(
            replace(kernel, morphisms=(bad_morphism,) + kernel.morphisms[1:])
        )
        self.assertEqual(payload["uap_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertIn(
            "quazris_morphism_not_dataflow:mor:sigil-api-ingress",
            payload["obstruction_ledger"],
        )

    def test_user_owned_fpga_resource_is_rejected(self):
        kernel = build_hpc_localized_quazris_kernel()
        bad_resource = FPGAResourceProfile(
            "res:user-fpga",
            kernel.target.resources[0].kind,
            kernel.target.target_id,
            "bad user owned resource",
            owning_space=KernelSpace.VIRTUAL_USER_SPACE,
            direct_user_access=True,
        )
        bad_target = replace(
            kernel.target,
            resources=(bad_resource,) + kernel.target.resources[1:],
        )
        payload = compile_hpc_localized_quazris_kernel(
            replace(kernel, target=bad_target)
        )
        self.assertEqual(payload["uap_state"], "REJECT")
        self.assertIn(
            "fpga_resource_direct_user_access:res:user-fpga",
            payload["obstruction_ledger"],
        )

    def test_kokompile_factorization_is_required(self):
        kernel: HPCLocalizedKernel = replace(
            build_hpc_localized_quazris_kernel(),
            fully_factorizable=False,
            conformal_architecture=False,
            pydantika_annotation_flow_ids=(),
            kokompile_plan_id="",
        )
        payload = compile_hpc_localized_quazris_kernel(kernel)
        self.assertEqual(payload["uap_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertIn(
            "hpc_localized_kernel_not_fully_factorizable",
            payload["obstruction_ledger"],
        )
        self.assertIn(
            "hpc_localized_kernel_not_conformal",
            payload["obstruction_ledger"],
        )
        self.assertIn(
            "hpc_localized_kernel_pydantika_flows_missing",
            payload["obstruction_ledger"],
        )
        self.assertIn(
            "hpc_localized_kernel_kokompile_plan_missing",
            payload["obstruction_ledger"],
        )


if __name__ == "__main__":
    unittest.main()
