import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from voice_meter import (GENRE_COLORS, POLICY, FRAMES, METER_SIZE,
                         envelope, make_meter)

class VoiceMeterTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_COLORS), 10)
        self.assertEqual(len(set(GENRE_COLORS.values())), 10)
    def test_silent_meter_is_small(self):
        self.assertEqual(max(envelope([0] * 20)), 0)
    def test_speech_increases_meter(self):
        levels = envelope([0] * 8 + [0.20] * 12)
        self.assertGreater(levels[-1], levels[7] + 0.5)
    def test_release_after_speech(self):
        levels = envelope([0.2] * 10 + [0] * 20)
        self.assertLess(levels[-1], levels[9] / 10)
    def test_all_genres_render(self):
        for name in GENRE_COLORS:
            with self.subTest(genre=name):
                self.assertEqual(make_meter(0.5, 20, name).size, METER_SIZE)
    def test_frame_dependent_visuals(self):
        self.assertNotEqual(make_meter(0.8, 0).tobytes(), make_meter(0.8, 9).tobytes())
    def test_audio_level_dependent_visuals(self):
        self.assertNotEqual(make_meter(0, 0).tobytes(), make_meter(1, 0).tobytes())
    def test_invalid_genre_rejected(self):
        with self.assertRaises(ValueError):
            make_meter(0.5, 0, 'unapproved')
    def test_invalid_level_rejected(self):
        with self.assertRaises(ValueError):
            make_meter(1.1, 0)
    def test_review_only_and_length(self):
        self.assertIn('PUBLICATION_NOT_APPROVED', POLICY)
        self.assertEqual(FRAMES, 691)

if __name__ == '__main__':
    unittest.main()
