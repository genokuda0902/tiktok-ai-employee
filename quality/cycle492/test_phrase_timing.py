import unittest
from quality.cycle492.phrase_timing import GENRES, timeline, publication_gate

class PhraseTimingTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
    def test_twelve_phrase_boundaries(self):
        all_segments = []
        for scene in range(6):
            all_segments.extend(timeline(["前半です。", "後半です。"], scene,
                                         speech_durations=[1.10, 1.25]))
        self.assertEqual(len(all_segments), 12)
        self.assertAlmostEqual(all_segments[-1].subtitle_end_s, 19.2)
        for p in all_segments:
            self.assertGreaterEqual(p.speech_start_s, p.subtitle_start_s)
            self.assertLessEqual(p.speech_end_s, p.subtitle_end_s)
    def test_overflow_fails(self):
        with self.assertRaises(ValueError):
            timeline(["A", "B"], 0, speech_durations=[1.55, 1.0])
    def test_mismatch_fails(self):
        with self.assertRaises(ValueError):
            timeline(["A", "B"], 0, speech_durations=[1.0])
    def test_no_native_voice_blocks_release(self):
        self.assertFalse(publication_gate(native_japanese_verified=False,
                         full_decode_pass=True, rights_approved=True, employee_approved=True))
    def test_employee_gate(self):
        self.assertFalse(publication_gate(native_japanese_verified=True,
                         full_decode_pass=True, rights_approved=True, employee_approved=False))
    def test_all_gates_only(self):
        self.assertTrue(publication_gate(native_japanese_verified=True,
                        full_decode_pass=True, rights_approved=True, employee_approved=True))

if __name__ == "__main__":
    unittest.main()
