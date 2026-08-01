import unittest

from pydantic import ValidationError

from sigil4cpython.paca_estaca_open_pr_presheaf import build_reference_open_pr_presheaf
from Tools.sigil4cpython.paca_estaca_open_pr_presheaf_models import (
    PydantikaMergedOpenPrPresheaf,
    annotated_metadata_present,
    build_pydantika_reference,
    from_runtime,
)


class PydantikaPacaEstacaModelsTests(unittest.TestCase):
    def test_reference_round_trip(self) -> None:
        model = build_pydantika_reference()
        self.assertEqual(model.host_section_key, "jbermejovega/sigil4cpython#7")
        self.assertEqual(len(model.sections), 7)
        self.assertFalse(model.git_merge_requested)

    def test_annotated_metadata_is_present(self) -> None:
        self.assertTrue(annotated_metadata_present())

    def test_extra_fields_are_forbidden(self) -> None:
        payload = build_pydantika_reference().model_dump(mode="json")
        payload["unexpected"] = True
        with self.assertRaises(ValidationError):
            PydantikaMergedOpenPrPresheaf.model_validate(payload)

    def test_head_sha_is_strict(self) -> None:
        payload = build_pydantika_reference().model_dump(mode="json")
        payload["sections"][0]["head_sha"] = "bad"
        with self.assertRaises(ValidationError):
            PydantikaMergedOpenPrPresheaf.model_validate(payload)

    def test_certificate_is_deterministic(self) -> None:
        first = from_runtime(build_reference_open_pr_presheaf())
        second = from_runtime(build_reference_open_pr_presheaf())
        self.assertEqual(first.certificate(), second.certificate())


if __name__ == "__main__":
    unittest.main()
