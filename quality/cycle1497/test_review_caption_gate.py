import unittest
from review_caption_gate import gate

class GateTests(unittest.TestCase):
    def test_silent(self):
        result = gate({"streams":[{"codec_type":"video","width":720,"height":1280}]})
        self.assertFalse(result["audio_present"])
        self.assertFalse(result["publication_approved"])

    def test_audio_is_not_language_proof(self):
        result = gate({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]})
        self.assertTrue(result["audio_present"])
        self.assertFalse(result["japanese_narration_verified"])

    def test_small_frame_fails(self):
        result = gate({"streams":[{"codec_type":"video","width":540,"height":960}]})
        self.assertFalse(result["vertical_720_min"])

if __name__ == "__main__":
    unittest.main()
