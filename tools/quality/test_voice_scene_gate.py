import unittest
from tools.quality.voice_scene_gate import scene_audio_gate

class AudioGateTest(unittest.TestCase):
    def test_bad_scene_count(self):
        with self.assertRaises(ValueError):
            scene_audio_gate('missing.wav', [3] * 5)

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            scene_audio_gate('missing.wav', [2] * 7 + [-1])
