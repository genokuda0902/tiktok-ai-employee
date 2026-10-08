import unittest
import tempfile
import wave
from array import array
from pathlib import Path
from tools.quality.voice_scene_gate import scene_audio_gate

D = [1.5, 1.7, 1.8, 2, 2, 2, 2, 2]

class AudioGateTest(unittest.TestCase):
    def test_bad_scene_count(self):
        with self.assertRaises(ValueError):
            scene_audio_gate("missing.wav", [3] * 5)

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            scene_audio_gate("missing.wav", [2] * 7 + [-1])

    def test_signal_is_not_japanese_proof(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.wav"
            with wave.open(str(p), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(16000)
                w.writeframes((array("h", [1000]) * 240000).tobytes())
            r = scene_audio_gate(p, D)
            self.assertEqual(r["technical_audio"], "PASS")
            self.assertFalse(r["japanese_verified"])
            self.assertFalse(r["publication_approved"])
            with self.assertRaises(ValueError):
                scene_audio_gate(p, D, narration_claimed=True)
