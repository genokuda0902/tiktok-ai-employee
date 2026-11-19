import unittest
from experiments.cycle1556.caption_timeline import STEPS, build_srt, srt_timestamp
class CaptionTest(unittest.TestCase):
    def test_four_captions(self):
        self.assertEqual(build_srt().count("-->"), 4)
    def test_last_ends_at_12s(self):
        self.assertIn("00:00:12,000", build_srt())
    def test_all_step_text_present(self):
        for title, detail in STEPS:
            self.assertIn(title, build_srt())
            self.assertIn(detail, build_srt())
    def test_time(self):
        self.assertEqual(srt_timestamp(63), "00:01:03,000")
if __name__ == "__main__": unittest.main()
