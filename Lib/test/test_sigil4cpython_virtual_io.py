import unittest
from dataclasses import replace

from sigil4cpython.virtual_io import (
    CellKind,
    IOCell,
    ResourceAuthority,
    VirtualIOProtocol,
    build_pacaiogame_virtual_rest_kernel,
    compile_virtual_io_kernel,
)


class Sigil4CPythonVirtualIOTests(unittest.TestCase):
    def test_default_virtual_rest_ios_kernel_is_admitted(self):
        kernel = build_pacaiogame_virtual_rest_kernel()
        payload = compile_virtual_io_kernel(kernel)
        self.assertEqual(payload["uap_state"], "ADMIT")
        self.assertFalse(payload["resource_access_performed"])
        self.assertFalse(payload["rest_call_performed"])
        self.assertFalse(payload["ios_call_performed"])
        self.assertIn("kernel_sha256", payload)

    def test_rest_ios_stream_drift_holds_with_obstruction(self):
        kernel = build_pacaiogame_virtual_rest_kernel()
        ports = tuple(
            replace(port, stream_type="DRIFTED_STREAM")
            if port.protocol == VirtualIOProtocol.IOS
            else port
            for port in kernel.ports
        )
        payload = compile_virtual_io_kernel(replace(kernel, ports=ports))
        self.assertEqual(payload["uap_state"], "HOLD_WITH_OBSTRUCTION")
        self.assertIn("rest_ios_stream_type_nonconformal", payload["obstruction_ledger"])

    def test_direct_resource_access_without_resource_cell_is_rejected(self):
        kernel = build_pacaiogame_virtual_rest_kernel()
        bad_cell = replace(kernel.cells[0], direct_resource_access=True)
        payload = compile_virtual_io_kernel(
            replace(kernel, cells=(bad_cell,) + kernel.cells[1:])
        )
        self.assertEqual(payload["uap_state"], "REJECT")
        self.assertIn(
            "direct_access_requires_resource_cell:cell:rest-lift",
            payload["obstruction_ledger"],
        )

    def test_attached_resource_cell_admits_physical_instantiation(self):
        kernel = build_pacaiogame_virtual_rest_kernel()
        resource_cell = IOCell(
            "cell:slurm-resource",
            CellKind.RESOURCE_CELL,
            "stream:uniform",
            "stream:uniform",
            ResourceAuthority.SCHEDULER_BOUND,
            "STRIKK::SLURM_RESOURCE_CELL",
            ("slurm:partition:debug",),
            True,
        )
        payload = compile_virtual_io_kernel(
            replace(
                kernel,
                cells=kernel.cells + (resource_cell,),
                physical_instantiation_attached=True,
            )
        )
        self.assertEqual(payload["uap_state"], "ADMIT")


if __name__ == "__main__":
    unittest.main()
