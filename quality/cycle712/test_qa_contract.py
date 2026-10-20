import unittest
from qa_contract import GENRES, VALUES, Approval, publishable, verify_story, caption_safe, make_srt

class Cycle712Tests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(set(GENRES)), 10)
    def test_math(self):
        self.assertTrue(verify_story())
        self.assertEqual(sum(VALUES), 650000)
    def test_caption(self):
        self.assertTrue(caption_safe(1340,1515))
        self.assertIn("00:00:21,000", make_srt())
    def test_voice_gate(self):
        self.assertFalse(publishable(Approval(assets_approved=True,privacy_checked=True)))
