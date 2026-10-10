"""Regression tests for genre-neutral grounded-field quality gate."""
import unittest
from scene_gate import UNKNOWN, parse_notes, check_grounded

class GroundingTests(unittest.TestCase):
    def test_preserves_explicit(self):
        self.assertEqual(parse_notes(["資料更新／担当:佐藤／期限:火曜"]), [("資料更新","佐藤","火曜")])
    def test_missing_owner(self):
        self.assertEqual(parse_notes(["資料更新／期限:火曜"])[0][1],UNKNOWN)
    def test_missing_deadline(self):
        self.assertEqual(parse_notes(["資料更新／担当:佐藤"])[0][2],UNKNOWN)
    def test_missing_both(self):
        self.assertEqual(parse_notes(["資料更新"]),[("資料更新",UNKNOWN,UNKNOWN)])
    def test_unstated(self):
        self.assertEqual(parse_notes(["資料更新／担当:未記載／期限:未記載"])[0][1:],(UNKNOWN,UNKNOWN))
    def test_blank(self):
        self.assertEqual(parse_notes(["資料更新／担当:／期限:"])[0][1:],(UNKNOWN,UNKNOWN))
    def test_invention_rejected(self):
        with self.assertRaises(ValueError): check_grounded(["資料更新"],[("資料更新","Aさん","水曜")])
    def test_real_preserved(self):
        check_grounded(["資料更新／担当:佐藤／期限:火曜"],[("資料更新","佐藤","火曜")])
    def test_duplicate_field_rejected(self):
        with self.assertRaises(ValueError):parse_notes(["資料更新／期限:火曜／期限:水曜"])
    def test_unknown_field_rejected(self):
        with self.assertRaises(ValueError):parse_notes(["資料更新／売上:300"])
    def test_blank_note_rejected(self):
        with self.assertRaises(ValueError):parse_notes([""])
    def test_missing_task_rejected(self):
        with self.assertRaises(ValueError):parse_notes(["／担当:佐藤"])
if __name__=="__main__":unittest.main()
