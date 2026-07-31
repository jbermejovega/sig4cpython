import json
from pathlib import Path
import sys
import unittest

from pydantic import ValidationError

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parents[1]
sys.path.insert(0, str(TOOLS_DIR))

from hpc_localized_models import (  # noqa: E402
    HPCLocalizedKernelModel,
    compile_pydantika_hpc_localized_kernel,
)

# Add the experimental package only after Pydantika imports.  On GitHub
# Actions this checkout's Lib/ can otherwise shadow the runner stdlib.
sys.path.insert(0, str(ROOT / "Lib"))

from sigil4cpython.hpc_localized_kernel import (  # noqa: E402
    build_hpc_localized_quazris_kernel,
)


class PydantikaHPCLocalizedKernelModelTests(unittest.TestCase):
    def payload(self):
        payload = build_hpc_localized_quazris_kernel().to_dict()
        payload.pop("kernel_sha256")
        payload["pydantika_is_tooling_not_stdlib_dependency"] = True
        payload["virtual_plan_is_not_hardware_authority"] = True
        payload["human_review_required"] = True
        return json.loads(json.dumps(payload))

    def test_default_hpc_localized_kernel_round_trips(self):
        certificate = compile_pydantika_hpc_localized_kernel(self.payload())
        self.assertEqual(len(certificate.payload_digest), 64)
        self.assertFalse(certificate.runtime_executed)
        self.assertFalse(certificate.hardware_synthesis_performed)
        self.assertFalse(certificate.scheduler_job_submitted)

    def test_extra_authority_is_rejected(self):
        payload = self.payload()
        payload["physical_handle"] = "forbidden"
        with self.assertRaisesRegex(ValidationError, "extra_forbidden"):
            HPCLocalizedKernelModel.model_validate(payload)

    def test_missing_required_fpga_resource_is_rejected(self):
        payload = self.payload()
        payload["target"]["resources"] = [
            resource
            for resource in payload["target"]["resources"]
            if resource["kind"] != "HBM_MEMORY"
        ]
        with self.assertRaisesRegex(
            ValidationError,
            "fpga_target_required_resource_missing",
        ):
            HPCLocalizedKernelModel.model_validate(payload)

    def test_dataflow_activation_is_required(self):
        payload = self.payload()
        payload["morphisms"][0]["data_activated"] = False
        with self.assertRaisesRegex(ValidationError, "literal_error"):
            HPCLocalizedKernelModel.model_validate(payload)

    def test_kokompile_annotations_are_required(self):
        payload = self.payload()
        payload["pydantika_annotation_flow_ids"] = []
        with self.assertRaisesRegex(
            ValidationError,
            "too_short",
        ):
            HPCLocalizedKernelModel.model_validate(payload)


if __name__ == "__main__":
    unittest.main()
