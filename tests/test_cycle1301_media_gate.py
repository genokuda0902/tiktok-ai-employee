import unittest
from quality.cycle1301_media_gate import publication_gate

class TestMediaGate(unittest.TestCase):
    def test_tone_is_not_narration(self):
        meta={"width":1080,"height":1920,"duration":15,"audio_streams":1}
        self.assertIn("japanese_narration",publication_gate(meta))
    def test_approved_full_media_passes(self):
        meta={"width":1080,"height":1920,"duration":15,"audio_streams":1}
        self.assertEqual([],publication_gate(meta,narration_verified=True,captions_synced=True,assets_approved=True,employee_approved=True))
    def test_missing_audio_and_resolution_fail(self):
        meta={"width":720,"height":1280,"duration":12,"audio_streams":0}
        self.assertIn("audio_stream",publication_gate(meta))
        self.assertIn("resolution",publication_gate(meta))
if __name__=="__main__":unittest.main()
