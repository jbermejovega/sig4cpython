import json
from pathlib import Path
import sys
import unittest

from pydantic import ValidationError

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parents[1]
sys.path.insert(0, str(TOOLS_DIR))
sys.path.insert(0, str(ROOT / "Lib"))

from sigil4cpython.virtual_io import build_pacaiogame_virtual_rest_kernel
from virtual_io_models import VirtualIOKernelModel, compile_pydantika_virtual_io_kernel


class PydantikaVirtualIOModelTests(unittest.TestCase):
    def payload(self):
        payload = build_pacaiogame_virtual_rest_kernel().to_dict()
        payload.pop("kernel_sha256")
        payload["pydantika_is_tooling_not_stdlib_dependency"] = True
        payload["virtual_stream_is_not_hardware_authority"] = True
        payload["resource_access_performed"] = False
        return payload

    def test_default_virtual_io_kernel_round_trips(self):
        certificate = compile_pydantika_virtual_io_kernel(self.payload())
        self.assertEqual(len(certificate.payload_digest), 64)
        self.assertFalse(certificate.resource_access_performed)
        self.assertFalse(certificate.rest_call_performed)
        self.assertFalse(certificate.ios_call_performed)

    def test_extra_semantic_authority_is_rejected(self):
        payload = self.payload()
        payload["unknown_authority"] = True
        with self.assertRaisesRegex(ValidationError, "extra_forbidden"):
            VirtualIOKernelModel.model_validate(payload)

    def test_rest_ios_semantic_drift_is_rejected(self):
        payload = json.loads(json.dumps(self.payload()))
        payload["ports"][1]["semantic_type"] = "DRIFTED_IOS_CONTROL"
        with self.assertRaisesRegex(ValidationError, "rest_ios_semantic_type_nonconformal"):
            VirtualIOKernelModel.model_validate(payload)

    def test_resource_cell_requires_physical_instantiation_flag(self):
        payload = self.payload()
        payload["cells"].append(
            {
                "cell_id": "cell:device",
                "kind": "RESOURCE_CELL",
                "source_port_id": "stream:uniform",
                "target_port_id": "stream:uniform",
                "authority": "HARDWARE_BOUND",
                "strikk_type": "STRIKK::DEVICE_RESOURCE_CELL",
                "resource_refs": ("device:loopback",),
                "direct_resource_access": True,
            }
        )
        with self.assertRaisesRegex(
            ValidationError,
            "resource_cell_attached_without_physical_instantiation",
        ):
            VirtualIOKernelModel.model_validate(payload)


if __name__ == "__main__":
    unittest.main()
