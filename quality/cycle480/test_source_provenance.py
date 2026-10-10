"""Unit tests for source provenance and fail-closed publication status."""
import unittest
from quality.cycle480.source_provenance import (
    extract_note, extract_notes, require_source_match, require_review_only, normalize,
)


class ProvenanceTests(unittest.TestCase):
    def test_source_values_retained(self):
        self.assertEqual(extract_note("資料更新／担当:佐藤／期限:火曜"), ["資料更新", "佐藤", "火曜"])

    def test_missing_fields_remain_unknown(self):
        self.assertEqual(extract_note("見積書を送る／担当:未記載"), ["見積書を送る", "要確認", "要確認"])

    def test_undefined_dates_are_unknown(self):
        self.assertEqual(extract_note("日程調整／期限:未定"), ["日程調整", "要確認", "要確認"])

    def test_whitespace_is_unknown(self):
        self.assertEqual(normalize("  "), "要確認")

    def test_empty_note_rejected(self):
        with self.assertRaises(ValueError):
            extract_note("")

    def test_invented_owner_rejected(self):
        with self.assertRaises(ValueError):
            require_source_match(["見積書を送る／担当:未記載"], [["見積書を送る", "田中", "要確認"]])

    def test_exact_rows_accepted(self):
        notes = ["資料更新／担当:佐藤／期限:火曜", "日程調整／期限:未記載"]
        self.assertTrue(require_source_match(notes, extract_notes(notes)))

    def test_generic_fields(self):
        self.assertEqual(extract_note("実績確認／数値:未記載", ("数値",)), ["実績確認", "要確認"])

    def test_review_only(self):
        self.assertTrue(require_review_only({"auto_post": False, "publication": "NOT_APPROVED", "human_review": "PENDING"}))

    def test_auto_post_rejected(self):
        with self.assertRaises(ValueError):
            require_review_only({"auto_post": True, "publication": "NOT_APPROVED", "human_review": "PENDING"})

    def test_premature_approval_rejected(self):
        with self.assertRaises(ValueError):
            require_review_only({"auto_post": False, "publication": "APPROVED", "human_review": "PENDING"})


if __name__ == "__main__":
    unittest.main()
