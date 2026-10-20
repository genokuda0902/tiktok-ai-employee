"""Offline tests for cycle728 shared scene08 design spec."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("scene08_spec", Path(__file__).with_name("scene08_spec.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class Scene08Tests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRES), 10)
        self.assertTrue(all(c.startswith("#") and len(c) == 7 for c in m.GENRES.values()))

    def test_safe_regions_and_no_overlap(self):
        self.assertTrue(m.validate())

    def test_speech_gate(self):
        self.assertEqual(m.caption_at(17.8), "")
        self.assertEqual(m.caption_at(18.0), "保存して、")
        self.assertEqual(m.caption_at(18.7), "あとで試そう。")
        self.assertEqual(m.caption_at(19.8), "")

    def test_three_action_steps(self):
        self.assertEqual(len(m.STEPS), 3)
        self.assertEqual(len(m.layout()["steps"]), 3)

    def test_monotonic_progress(self):
        xs = [m.smooth(i / 100) for i in range(101)]
        self.assertEqual(xs, sorted(xs))
        self.assertEqual((xs[0], xs[-1]), (0, 1))

    def test_duration_and_framerate(self):
        self.assertEqual(m.END_FRAME - m.START_FRAME, 74)
        self.assertEqual(m.FPS, 30)

if __name__ == "__main__":
    unittest.main()
