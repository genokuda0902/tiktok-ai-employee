import unittest
from quality.cycle1272_caption_coverage import check_scene_captions, publication_ready

SRT = "1\n00:00:00,000 --> 00:00:03,000\n導入\n\n2\n00:00:03,000 --> 00:00:06,000\n結論\n"

class ReviewTests(unittest.TestCase):
    def test_complete_coverage(self):
        self.assertTrue(check_scene_captions(SRT, 6000))
    def test_gap_fails(self):
        self.assertFalse(check_scene_captions(SRT.replace("00:00:03,000 -->", "00:00:04,000 -->"), 6000))
    def test_silent_video_never_approved(self):
        self.assertFalse(publication_ready(caption_coverage=True, japanese_narration_verified=False, speech_sync_verified=False, assets_approved=True, employee_approved=True))
    def test_no_employee_approval_fails(self):
        self.assertFalse(publication_ready(caption_coverage=True, japanese_narration_verified=True, speech_sync_verified=True, assets_approved=True, employee_approved=False))

if __name__ == "__main__":
    unittest.main()
