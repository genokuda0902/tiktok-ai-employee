import unittest
from quality.cycle1631_qa import validate

BASE = dict(width=1080, height=1920, fps=24, duration=12, audio_present=True)
class GateTests(unittest.TestCase):
    def test_pass_when_everything_approved(self):
        self.assertEqual(validate(BASE, True, True, True, True), [])
    def test_audio_stream_not_speech(self):
        self.assertIn("japanese_narration_unverified", validate(BASE, False, True, True, True))
    def test_resolution_and_fps(self):
        self.assertEqual(validate(dict(BASE, width=720, fps=15), True, True, True, True), ["resolution", "frame_rate"])
    def test_no_audio(self):
        self.assertIn("missing_audio", validate(dict(BASE, audio_present=False), True, True, True, True))
if __name__ == "__main__": unittest.main()
