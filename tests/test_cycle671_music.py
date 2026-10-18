"""Tests for offline soundtrack: deterministic, bounded, genre-configured, voice-ducked."""
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "quality" / "cycle671"))
from original_music import GENRE_PRESETS, render_music, duck_music

class TestCycle671Music(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_PRESETS), 10)
        for genre in GENRE_PRESETS:
            audio = render_music(duration=0.8, sr=8000, genre=genre)
            self.assertEqual(len(audio), 6400)
            self.assertLessEqual(float(np.max(np.abs(audio))), 0.03)
            self.assertGreater(float(np.std(audio)), 0.0001)

    def test_reproducibility(self):
        self.assertTrue(np.array_equal(render_music(1, 8000),
                                       render_music(1, 8000)))

    def test_ducking_during_voice(self):
        music = np.full(8000, 0.01, dtype=np.float32)
        voice = np.concatenate([np.zeros(4000), np.full(4000, 0.2)]).astype(np.float32)
        out, stats = duck_music(music, voice, sr=8000)
        self.assertLess(float(np.mean(out[6000:])),
                        float(np.mean(out[1000:3000])) * 0.5)
        self.assertLess(stats["min_gain"], stats["max_gain"])

    def test_invalid_genre(self):
        with self.assertRaises(ValueError):
            render_music(1, 8000, genre="unknown")

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            duck_music(np.zeros(3), np.zeros(2))

if __name__ == "__main__":
    unittest.main()
