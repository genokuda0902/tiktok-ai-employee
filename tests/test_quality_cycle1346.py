import unittest
from src.quality_cycle1346 import publication_gate

class GateTests(unittest.TestCase):
    def test_audio_tone_is_not_narration(self):
        self.assertFalse(publication_gate({"audio_codec":"aac", "narration_language":None})["posting_allowed"])
    def test_approval_required(self):
        data=dict(narration_language="ja", narration_verified=True, captions_synced=True, asset_rights_approved=True)
        self.assertFalse(publication_gate(data)["posting_allowed"])
        data["human_approved"]=True
        self.assertTrue(publication_gate(data)["posting_allowed"])
if __name__ == "__main__": unittest.main()
