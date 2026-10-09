import unittest
from dataclasses import replace
from video_engine.quality_cycle450.cinematic_bookends import (
    BookendPlan, CYCLE450, validate, frames, qa_gates
)

class TestCinematicBookends(unittest.TestCase):
    def test_valid_plan(self): self.assertTrue(validate(CYCLE450))
    def test_exact_frames(self): self.assertEqual(frames(CYCLE450),{"hook":75,"middle":450,"outro":75,"total":600})
    def test_japanese_voice_missing_is_not_hidden(self): self.assertIn("JAPANESE_NARRATION_MISSING",qa_gates(CYCLE450))
    def test_never_approved(self): self.assertIn("PUBLICATION_NOT_APPROVED",qa_gates(CYCLE450))
    def test_no_claim_of_missed_sales(self):
        with self.assertRaises(ValueError):validate(replace(CYCLE450,hook_claim="2件の売上を失った"))
    def test_reject_unsupported_asset_rights(self):
        with self.assertRaises(ValueError):validate(replace(CYCLE450,assets_rights="UNKNOWN"))
    def test_reject_publication(self):
        with self.assertRaises(ValueError):validate(replace(CYCLE450,publication_status="APPROVED"))
    def test_reject_wrong_canvas(self):
        with self.assertRaises(ValueError):validate(replace(CYCLE450,width=720))
    def test_reject_non_finite_time(self):
        with self.assertRaises(ValueError):validate(replace(CYCLE450,duration=float("nan")))
    def test_reject_empty_cta(self):
        with self.assertRaises(ValueError):validate(replace(CYCLE450,call_to_action=""))
    def test_reject_bad_counts(self):
        with self.assertRaises(ValueError):validate(replace(CYCLE450,target_count=9))
    def test_genre_neutral_counts(self):
        p=BookendPlan(source_count=12,target_count=3,hook_claim="12件の記録、未対応は3件。",call_to_action="保存")
        self.assertTrue(validate(p))
if __name__=="__main__":unittest.main()
