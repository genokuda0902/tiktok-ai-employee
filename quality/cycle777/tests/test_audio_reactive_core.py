"""Cycle777 synthetic CI tests; no user media required."""
import importlib.util
import pathlib
import unittest

CORE = pathlib.Path(__file__).resolve().parents[1] / "audio_reactive_core.py"
spec = importlib.util.spec_from_file_location("audio_reactive_core", CORE)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

class TestCycle777(unittest.TestCase):
    def test_audio_envelope(self):
        audio = [0.0]*1600 + [0.5]*1600 + [0.0]*1600
        rms = core.rms_windows(audio, 1600, 10)
        env = core.smooth_envelope(rms)
        self.assertEqual(len(rms), 30)
        self.assertGreater(max(env), 0.8)
        self.assertEqual(env[0], 0.0)
        self.assertGreater(max(env), env[-1])

    def test_bar_response(self):
        low = core.waveform_bars(0)
        high = core.waveform_bars(1)
        self.assertEqual(len(low), 12)
        self.assertTrue(all(b>a for a,b in zip(low,high)))

    def test_progress(self):
        self.assertEqual(core.cue_progress(1,1,2),0)
        self.assertAlmostEqual(core.cue_progress(1.5,1,2),0.5)
        self.assertEqual(core.cue_progress(2,1,2),1)
        with self.assertRaises(ValueError):
            core.cue_progress(1,2,2)

    def test_layout_and_genre_color(self):
        self.assertTrue(core.panel_within_safe_area())
        self.assertEqual(core.parse_accent("#52EBD0"),(82,235,208))
        with self.assertRaises(ValueError):
            core.parse_accent("red")

if __name__=="__main__":
    unittest.main()
