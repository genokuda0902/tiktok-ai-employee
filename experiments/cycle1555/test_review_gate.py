import unittest
from experiments.cycle1555.review_gate import review_gate

class ReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.metadata = {"streams": [
            {"codec_type": "video", "codec_name": "h264", "width": 720, "height": 1280},
            {"codec_type": "audio", "codec_name": "aac"}
        ]}
    def test_effects_not_speech(self):
        self.assertFalse(review_gate(self.metadata)["publishable"])
    def test_approval_required(self):
        self.assertFalse(review_gate(self.metadata, narration_verified=True, captions_aligned=True, rights_approved=True)["publishable"])
    def test_all_evidence(self):
        self.assertTrue(review_gate(self.metadata, narration_verified=True, captions_aligned=True, rights_approved=True, employee_approved=True)["publishable"])

if __name__ == "__main__":
    unittest.main()
