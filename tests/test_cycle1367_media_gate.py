import unittest
from quality.cycle1367_media_gate import publication_gate

class TestGate(unittest.TestCase):
    def test_aac_effect_is_not_narration(self):
        result=publication_gate({"video_codec":"h264","width":720,"height":1280,"audio_codec":"aac"})
        self.assertFalse(result["approved"])
        self.assertIn("japanese_narration_unverified",result["reasons"])
    def test_approved_only_with_explicit_evidence(self):
        result=publication_gate({"video_codec":"h264","width":1080,"height":1920,"audio_codec":"aac"},japanese_narration_verified=True,synchronized_captions_verified=True,rights_approved=True,employee_approved=True)
        self.assertTrue(result["approved"])
if __name__=="__main__": unittest.main()
