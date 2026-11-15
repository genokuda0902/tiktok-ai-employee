import unittest
from quality.cycle1486.audio_gate import validate

class TestAudioGate(unittest.TestCase):
    def test_silent_rejected(self):
        self.assertFalse(validate(dict(video_present=True,audio_present=False,japanese_narration_verified=False,caption_sync_verified=False,human_approved=False)))
    def test_audio_track_alone_rejected(self):
        self.assertFalse(validate(dict(video_present=True,audio_present=True,japanese_narration_verified=False,caption_sync_verified=False,human_approved=False)))
    def test_all_verified(self):
        self.assertTrue(validate(dict(video_present=True,audio_present=True,japanese_narration_verified=True,caption_sync_verified=True,human_approved=True)))

if __name__ == "__main__": unittest.main()
