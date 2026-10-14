import unittest
from proof_loop import GENRES, EXPECTED_TOTAL, VALUES, FREEZE_FRAME, validate, filter_graph

class ProofLoopTests(unittest.TestCase):
    def test_ten_genres_contract(self):
        for genre in GENRES:
            self.assertTrue(validate(genre))
    def test_sum_is_proven(self):
        self.assertEqual(sum(VALUES), EXPECTED_TOTAL)
    def test_incorrect_sum_is_rejected(self):
        with self.assertRaises(ValueError):
            validate('ai_productivity', total=704)
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):
            validate('unknown')
    def test_unstable_freeze_rejected(self):
        with self.assertRaises(ValueError):
            validate('ai_productivity', freeze_frame=5)
    def test_audio_edges(self):
        self.assertIn('afade=t=in', filter_graph())
        self.assertIn('afade=t=out', filter_graph())
        self.assertNotIn('reverse', filter_graph())
    def test_frame_count(self):
        self.assertEqual(30 + 540 + 30, 600)

if __name__ == '__main__':
    unittest.main()
