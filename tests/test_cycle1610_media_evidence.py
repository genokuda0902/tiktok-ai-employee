import unittest
from quality.cycle1610_media_evidence import publication_allowed

class TestFailClosed(unittest.TestCase):
    def test_missing_narration_rejected(self):
        report = dict(video_present=True,width=720,height=1280,audio_track_present=True,
                      japanese_narration_verified=False,speech_caption_sync_verified=True)
        self.assertFalse(publication_allowed(report,asset_approved=True,privacy_approved=True,employee_approved=True))
    def test_missing_approval_rejected(self):
        report = dict(video_present=True,width=720,height=1280,audio_track_present=True,
                      japanese_narration_verified=True,speech_caption_sync_verified=True)
        self.assertFalse(publication_allowed(report,asset_approved=False,privacy_approved=True,employee_approved=True))
    def test_complete_evidence_required(self):
        report = dict(video_present=True,width=720,height=1280,audio_track_present=True,
                      japanese_narration_verified=True,speech_caption_sync_verified=True)
        self.assertTrue(publication_allowed(report,asset_approved=True,privacy_approved=True,employee_approved=True))
if __name__ == "__main__": unittest.main()
