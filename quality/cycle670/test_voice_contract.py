import unittest
from voice_contract import GENRES, BEATS, validate, srt, review_gate

class QualityContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            self.assertTrue(validate(genre))
    def test_complete_japanese_srt(self):
        self.assertEqual(srt().count(" --> "), 9)
        self.assertIn("00:00:20,000", srt())
        self.assertIn("六百五十", srt())
    def test_fail_closed_on_missing_or_overlong_voice(self):
        with self.assertRaises(ValueError):
            validate(GENRES[0], actual_voice_durations=[3.0] * len(BEATS))
        with self.assertRaises(ValueError):
            validate(GENRES[0], actual_voice_durations=[1.0])
    def test_publication_gate(self):
        self.assertEqual(review_gate()["publication"], "NOT_APPROVED")
        self.assertFalse(review_gate()["voice_caption_sync_verified"])
        self.assertFalse(review_gate(narration_present=True)["voice_caption_sync_verified"])
    def test_discontinuous_timeline_rejected(self):
        with self.assertRaises(ValueError):
            validate(GENRES[0], beats=((0,2,"a"),(3,20,"b")))
if __name__ == "__main__":
    unittest.main()
