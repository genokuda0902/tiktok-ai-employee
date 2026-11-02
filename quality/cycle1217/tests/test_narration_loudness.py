import importlib.util
import tempfile
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'narration_loudness.py'
spec = importlib.util.spec_from_file_location('narration_loudness', P)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class LoudnessTests(unittest.TestCase):
    def test_genre_count(self):
        self.assertEqual(len(mod.GENRES), 10)
        self.assertEqual(len(set(mod.GENRES)), 10)

    def test_genre_names(self):
        self.assertIn('ai', mod.GENRES)
        self.assertIn('career', mod.GENRES)
        self.assertIn('travel', mod.GENRES)

    def test_target_values(self):
        self.assertEqual(mod.TARGET_I, -16)
        self.assertEqual(mod.TARGET_TP, -1.5)

    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            mod.master('/not-a-file.mp4', '/tmp/none.mp4')

    def test_invalid_genre(self):
        with self.assertRaises(ValueError):
            mod.master('/not-a-file.mp4', '/tmp/none.mp4', genre='unknown')

    def test_same_path(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'a.mp4'
            p.write_bytes(b'bad')
            with self.assertRaises(ValueError):
                mod.master(p, p)

    def test_ffmpeg_failure(self):
        with self.assertRaises(RuntimeError):
            mod.run(['ffmpeg', '-no_such_option'])

    def test_measure_invalid_input(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'a.mp4'
            p.write_bytes(b'bad')
            with self.assertRaises(RuntimeError):
                mod.loudness_measure(p)


if __name__ == '__main__':
    unittest.main()
