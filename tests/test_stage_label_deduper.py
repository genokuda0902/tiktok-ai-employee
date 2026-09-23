import unittest
from video_engine.stage_label_deduper import StageLabelCleanup, automatic_posting_allowed, requires_human_approval

class StageLabelCleanupTests(unittest.TestCase):
    def test_filter_is_narrow_and_deterministic(self):
        value = StageLabelCleanup().ffmpeg_filter()
        self.assertIn("w=220:h=34", value)

    def test_wrong_resolution_fails_closed(self):
        with self.assertRaises(ValueError):
            StageLabelCleanup().validate(720, 1280)

    def test_oversized_mask_fails_closed(self):
        with self.assertRaises(ValueError):
            StageLabelCleanup(width=300).validate(1080, 1920)

    def test_human_approval_and_no_auto_post(self):
        self.assertTrue(requires_human_approval())
        self.assertFalse(automatic_posting_allowed())

if __name__ == "__main__":
    unittest.main()
