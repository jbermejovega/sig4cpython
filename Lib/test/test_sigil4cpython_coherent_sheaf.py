import unittest
from dataclasses import replace

from sigil4cpython.coherent_sheaf import (
    AgentSpace,
    IrreducibleResource,
    ReleaseScale,
    build_pydantika_coherent_sheaf,
    compile_pydantika_coherent_sheaf,
)


class Sigil4CPythonCoherentSheafTests(unittest.TestCase):
    def test_default_coherent_sheaf_is_admitted(self):
        sheaf = build_pydantika_coherent_sheaf()
        payload = compile_pydantika_coherent_sheaf(sheaf)
        self.assertEqual(payload["uap_state"], "ADMIT")
        self.assertFalse(payload["runtime_executed"])
        self.assertFalse(payload["resource_access_performed"])
        self.assertIn("sheaf_sha256", payload)

    def test_every_kernel_keeps_user_and_krone_spaces(self):
        sheaf = build_pydantika_coherent_sheaf()
        bad_kernel = replace(
            sheaf.kernels[0],
            agents=tuple(
                agent
                for agent in sheaf.kernels[0].agents
                if agent.space != AgentSpace.VIRTUAL_KRONE_SPACE
            ),
        )
        payload = compile_pydantika_coherent_sheaf(
            replace(sheaf, kernels=(bad_kernel,) + sheaf.kernels[1:])
        )
        self.assertEqual(payload["uap_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertIn(
            "kernel_krone_space_agent_missing:sigilbook",
            payload["obstruction_ledger"],
        )

    def test_direct_user_resource_access_is_rejected(self):
        sheaf = build_pydantika_coherent_sheaf()
        bad_resource = IrreducibleResource(
            "res:user-owned",
            "sigilbook",
            "DEVICE",
            AgentSpace.VIRTUAL_USER_SPACE,
            ReleaseScale.MICROCANONICAL,
            "context:sigilbook",
            direct_user_access=True,
        )
        bad_kernel = replace(
            sheaf.kernels[0],
            resources=(bad_resource,),
        )
        payload = compile_pydantika_coherent_sheaf(
            replace(sheaf, kernels=(bad_kernel,) + sheaf.kernels[1:])
        )
        self.assertEqual(payload["uap_state"], "REJECT")
        self.assertIn(
            "direct_user_resource_access_forbidden:res:user-owned",
            payload["obstruction_ledger"],
        )

    def test_gluing_without_shared_annotation_holds(self):
        sheaf = build_pydantika_coherent_sheaf()
        bad_gluing = replace(sheaf.gluings[0], shared_annotation_ids=())
        payload = compile_pydantika_coherent_sheaf(
            replace(sheaf, gluings=(bad_gluing,) + sheaf.gluings[1:])
        )
        self.assertEqual(payload["uap_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertIn(
            "sheaf_gluing_shared_annotation_missing:glue:sigilbook:sigil4py",
            payload["obstruction_ledger"],
        )


if __name__ == "__main__":
    unittest.main()
