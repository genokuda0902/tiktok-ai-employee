"""stdlib tests for cycle816 audio pause alignment."""
import importlib.util
import pathlib
import unittest

MODULE = pathlib.Path(__file__).with_name("audio_pause_alignment.py")
spec = importlib.util.spec_from_file_location("audio_pause_alignment", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class AudioPauseTests(unittest.TestCase):
    def test_genre_count(self):
        self.assertEqual(len(mod.GENRE_ACCENTS), 10)
    def test_phrases(self):
        self.assertEqual(len(mod.PHRASES), 8)
        self.assertTrue(all(len(p) == 3 for p in mod.PHRASES))
    def test_detect_speech_onset(self):
        cuts, detected = mod.voice_guided_cuts(
            0, 3.3, [(0, .3), (1.3, 1.8), (2.9, 3.3)])
        self.assertTrue(detected)
        self.assertAlmostEqual(cuts[0], .3)
        self.assertTrue(all(a < b for a, b in zip(cuts, cuts[1:])))
    def test_pause_changes_equal_thirds(self):
        cuts, _ = mod.voice_guided_cuts(
            0, 3.3, [(0, .3), (1.3, 1.8), (2.9, 3.3)])
        self.assertGreater(abs(cuts[1] - 1.1), .1)
    def test_silence_fallback(self):
        cuts, detected = mod.voice_guided_cuts(0, 3, [(0, 3)])
        self.assertFalse(detected)
        self.assertEqual(len(cuts), 4)
    def test_no_publishing(self):
        code = MODULE.read_text(encoding="utf8")
        self.assertNotIn("api.tiktok.com", code)
        self.assertNotIn("requests.post(", code)

if __name__ == "__main__":
    unittest.main()
