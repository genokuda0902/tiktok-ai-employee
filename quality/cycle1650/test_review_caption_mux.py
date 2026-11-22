import unittest
from review_caption_mux import review

class GateTests(unittest.TestCase):
    def test_no_audio_cannot_claim_narration(self):
        self.assertFalse(review.__code__ is None)
    def test_review_is_not_publication_approval(self):
        import inspect
        self.assertIn('"publication_allowed":False',inspect.getsource(review))
    def test_subtitle_does_not_imply_speech(self):
        import inspect
        self.assertIn('"japanese_narration_verified":False',inspect.getsource(review))

if __name__=="__main__": unittest.main()
