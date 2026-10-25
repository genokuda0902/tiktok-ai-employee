"""No private media needed: safety tests for 10-genre pacing compositor."""
import unittest
from cycle839.pacing import GENRES, CUT_FRAMES, SCENE_FRAMES, cuts_for_silences, kept_ranges

GAPS = [(2.809875, 3.705625), (5.855396, 6.704687),
        (8.867312, 9.723333), (12.177, 13.008979),
        (15.447521, 16.309708), (18.791187, 19.659625),
        (21.782312, 22.664333)]

class SafePacingTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)
    def test_cut_within_silence(self):
        boundary = 0
        for (a, b), (s, e), n in zip(cuts_for_silences(GAPS), GAPS, SCENE_FRAMES):
            boundary += n
            self.assertEqual(b-a, CUT_FRAMES)
            self.assertLess(b, boundary)
            self.assertGreater(a/30, s+0.05)
            self.assertLess(b/30, e-0.05)
    def test_frame_count(self):
        keep = kept_ranges(cuts_for_silences(GAPS))
        self.assertEqual(len(keep), 8)
        self.assertEqual(sum(b-a for a,b in keep), 691)
        self.assertEqual(keep[0][0], 0)
        self.assertEqual(keep[-1][1], 775)
    def test_missing_silence_fails_closed(self):
        with self.assertRaises(ValueError):
            cuts_for_silences(GAPS[1:])
    def test_short_gap_fails_closed(self):
        with self.assertRaises(ValueError):
            cuts_for_silences([(2.8,3.0)]+GAPS[1:])
    def test_duplicate_gap_fails_closed(self):
        with self.assertRaises(ValueError):
            cuts_for_silences(GAPS+[GAPS[0]])
    def test_overlap_fails_closed(self):
        with self.assertRaises(ValueError):
            kept_ranges([(10,22),(20,32)])
    def test_last_scene_preserved(self):
        self.assertEqual(kept_ranges(cuts_for_silences(GAPS))[-1][1], sum(SCENE_FRAMES))

if __name__ == '__main__':
    unittest.main()
